"""
명세서(`.spec/src/common/logger.md`) 기반 로깅 유틸리티.

역할:
- config/logging.yml + .env 기반 로깅 설정
- get_logger, audit_log 등 래퍼 제공
- 파일 핸들러 경로·권한 검증
- audit 로거 stdout 금지 (정책: documents/LOGGING_POLICY.md)
"""

from __future__ import annotations

import logging
import logging.config
import os
import re
import socket
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from dotenv import load_dotenv

from common.expand_vars import expand_vars_str

load_dotenv(override=True)

PROJECT_NAME = os.getenv("PROJECT_NAME", "py-template")
# CI 또는 로컬 초기 환경을 위해 기본값 보장
if "PROJECT_NAME" not in os.environ:
    os.environ["PROJECT_NAME"] = PROJECT_NAME
if "LOG_PATH" not in os.environ:
    os.environ["LOG_PATH"] = "logs"

VALID_LEVELS = {"CRITICAL", "ERROR", "WARNING", "INFO", "DEBUG"}


def _get_log_level() -> str:
    """ENV LOG_LEVEL을 대문자로 읽어 유효성 검사 후 반환."""
    level = os.getenv("LOG_LEVEL", "INFO").upper()
    return level if level in VALID_LEVELS else "INFO"


def _require_parent_exists_and_writable(path: Path, handler_name: str) -> None:
    """
    컴플라이언스: 디렉토리 자동 생성 금지.
    존재/쓰기권한이 없으면 명확한 예외를 발생시킨다.
    """
    parent = path.parent
    if not parent.exists():
        raise FileNotFoundError(
            f"[{handler_name}] 로그 디렉토리가 존재하지 않습니다: {parent}\n"
            "- Linux 예: /var/log/<project>, ~/logs\n"
            "- Windows 예: C:\\logs, %USERPROFILE%\\logs\n"
            "- .env의 LOG_PATH 설정을 확인하세요."
        )
    if not os.access(parent, os.W_OK):
        raise PermissionError(
            f"[{handler_name}] 로그 디렉토리에 쓰기 권한이 없습니다: {parent}\n"
            "- Unix: chmod/chown 검토, Windows: 보안 탭 권한 부여 필요\n"
            "- CI 환경이라면 실행 사용자(예: 서비스 계정) 권한을 확인하세요."
        )


def _ensure_project_logger(config: dict, level: str) -> None:
    """
    ${PROJECT_NAME} 로거가 YAML에 없더라도 안전하게 동작하도록 보장.
    - handlers는 비워 두고 propagate만 True로 둬 루트로 전달되게 함.
    """
    loggers = config.setdefault("loggers", {})
    if PROJECT_NAME not in loggers:
        loggers[PROJECT_NAME] = {"level": level, "propagate": True}


def _assert_audit_is_file_only(config: dict) -> None:
    """
    개인정보보호정책: audit 로거는 전용 파일에만 기록되어야 하며 stdout(console) 금지.
    정책 위반 구성 발견 시 예외를 발생시킨다.
    """
    audit = config.get("loggers", {}).get("audit")
    if not audit:
        return
    handlers = set(audit.get("handlers", []))
    if "console" in handlers:
        raise RuntimeError("개인정보보호정책 위반: 'audit' 로거에 console 핸들러를 사용할 수 없습니다.")
    # propagate가 True이면 루트 console로 전파될 수 있으므로 금지
    if audit.get("propagate", False):
        raise RuntimeError("개인정보보호정책 위반: 'audit' 로거는 propagate: false 여야 합니다.")


def _load_logging_config() -> dict:
    """
    config/logging.yml을 로드하여:
      - YAML 로드 및 ENV 치환은 common.load_config 사용(단일 책임)
      - LOG_LEVEL로 레벨 일괄 오버라이드
      - 파일 핸들러 filename 치환 및 경로/권한 검증
      - 프로젝트 로거 보장
      - audit stdout 금지 검증
    을 수행한 dictConfig용 딕셔너리를 반환.
    """
    from common.load_config import load_config

    yaml_path = Path(__file__).parent.parent.parent / "config" / "logging.yml"
    if not yaml_path.exists():
        raise FileNotFoundError(f"logging.yml 파일이 필요합니다: {yaml_path}")

    config = load_config(str(yaml_path))

    # 1) LOG_LEVEL 일괄 오버라이드
    level = _get_log_level()
    config.setdefault("root", {})["level"] = level
    for _, logger_cfg in config.get("loggers", {}).items():
        logger_cfg["level"] = level

    # 2) 프로젝트 로거 보장
    _ensure_project_logger(config, level)

    # 3) 파일 핸들러의 filename 처리(치환 후 경로/권한 검증)
    for handler_name, handler_cfg in config.get("handlers", {}).items():
        handler_class = handler_cfg.get("class", "")
        # FileHandler, RotatingFileHandler 등 파일 기반 핸들러 탐지
        if re.search(r"FileHandler$", handler_class):
            raw_filename = handler_cfg.get("filename", "")
            if not raw_filename:
                raise ValueError(f"[{handler_name}] filename이 지정되어 있지 않습니다.")
            expanded = os.path.expandvars(expand_vars_str(raw_filename))
            if expanded == raw_filename and ("${" in raw_filename or "$" in raw_filename):
                raise ValueError(
                    f"[{handler_name}] 환경변수 치환 실패: {raw_filename}\n- .env의 관련 변수를 확인하세요."
                )
            file_path = Path(expanded)
            _require_parent_exists_and_writable(file_path, handler_name)
            handler_cfg["filename"] = str(file_path)

    # 4) audit stdout 금지(정책 점검)
    _assert_audit_is_file_only(config)

    return dict(config)


_setup_in_progress = False


def setup_logging() -> None:
    """dictConfig로 로깅을 초기화."""
    global _setup_in_progress
    if _setup_in_progress:
        # 이미 설정 진행 중이면 재진입 방지 (circular import/recursion)
        return

    _setup_in_progress = True
    try:
        cfg = _load_logging_config()
        logging.config.dictConfig(cfg)
    finally:
        _setup_in_progress = False


def get_logger(name: str | None = PROJECT_NAME) -> logging.Logger:
    """
    지정된 이름의 로거 반환. 최초 호출 시 자동으로 setup_logging() 수행.
    기본값은 .env의 PROJECT_NAME.
    """
    root_logger = logging.getLogger()
    if not root_logger.hasHandlers() and not _setup_in_progress:
        setup_logging()
    return logging.getLogger(name or None)


def audit_log(
    action_type: str,
    actor_id: str,
    actor_ip: str | None = None,
    target_id: str | None = None,
    action_reason: str | None = None,
    detail: dict[str, Any] | None = None,
    compliance: str = "개인정보의 안전성 확보조치 기준 제8조",
) -> None:
    """
    개인정보보호 관련 감사 로그(Audit Log)를 JSON 형태로 기록합니다.
    'audit' 로거는 전용 파일(/audit.log 등)에만 기록되어야 하며 stdout은 금지되어 있습니다.

    단일 서버/로컬 환경이거나 식별할 클라이언트 IP가 없는 경우 actor_ip를 "127.0.0.1"
    또는 내부망 IP로 처리하여 넘길 수 있습니다.

    :param action_type: 수행 업무 구분 (예: READ, CREATE, DOWNLOAD 등)
    :param actor_id: 개인정보취급자(접속자)의 고유 식별자 (ID, 사번 등)
    :param actor_ip: 접속지 정보 (단말기 IP, 식별 불가 시 'unknown' 또는 'localhost/127.0.0.1')
    :param target_id: 처리한 정보주체의 식별자 (고객ID, 환자번호 등)
    :param action_reason: (특히 다운로드/출력 시) 엑세스 사유
    :param detail: 추가적인 로깅 메타데이터 딕셔너리
    :param compliance: 준수 법령 레퍼런스
    """
    audit_logger = get_logger("audit")

    # 법적 요구사항 (5W1H) 기반 구조화된 JSON 로그 조립
    log = {
        "log_type": "audit",
        "timestamp": datetime.now(UTC).isoformat(),
        "actor": {
            "user_id": actor_id,
            "ip_address": actor_ip or "unknown",
        },
        "action": {
            "type": action_type,
            "reason": action_reason,
        },
        "target": {
            "subject_id": target_id,
        },
        "system": {
            "compliance": compliance,
            "server_hostname": socket.gethostname(),  # Docker 컨테이너 ID 또는 호스트명
        },
    }

    # 추가 사용자 정의 필드 병합
    if detail:
        action_data = log.get("action")
        if isinstance(action_data, dict):
            action_data["detail"] = detail

    audit_logger.info(log)


# 편의 래퍼(일관 API)
def log_debug(msg: str) -> None:
    get_logger().debug(msg)


def log_info(msg: str) -> None:
    get_logger().info(msg)


def log_warn(msg: str) -> None:
    get_logger().warning(msg)


def log_error(msg: str) -> None:
    get_logger().error(msg)


def log_critical(msg: str) -> None:
    get_logger().critical(msg)

