"""
명세서(`.spec/src/common/load_config.md`) 기반 YAML 설정 로더.

역할:
- YAML 설정 파일을 UTF-8 로 읽고, 내용에 포함된 ${VAR} 패턴을
  환경 변수(os.environ) 값으로 치환해 dict 로 반환한다.
"""

from __future__ import annotations

from typing import cast

import yaml

from common.expand_vars import expand_vars


def load_config(yml_path: str = "config/deidentification.yml", section: str | None = None) -> dict:
    """
    YAML 설정 파일을 로드하고 환경변수를 치환하여 반환한다.

    Args:
        yml_path: YAML 파일 경로 (기본값: config/deidentification.yml)
        section: 특정 섹션만 추출하고 싶을 때 사용하는 최상위 키 이름.

    Returns:
        환경변수가 치환된 설정 딕셔너리.
        section 이 지정되었으나 존재하지 않으면 빈 dict 를 반환한다.

    Raises:
        FileNotFoundError: 설정 파일이 존재하지 않을 때
        yaml.YAMLError: YAML 파싱 오류 발생 시
        예기치 못한 예외는 로깅 후 그대로 다시 발생시킨다.
    """
    from .logger import log_debug, log_error

    try:
        log_debug(f"[load_config] Loading config from: {yml_path}, section: {section}")

        # 1. 파일 열기 및 파싱
        with open(yml_path, encoding="utf-8") as f:
            yaml_config = yaml.safe_load(f)

        # 2. 환경변수 치환
        substituted_config = expand_vars(yaml_config)

        # 3. 섹션 추출 (지정된 경우)
        if section:
            result = substituted_config.get(section, {})
            log_debug(f"[load_config] Extracted section '{section}' with {len(result)} keys")
            return cast(dict, result)

        # 4. 전체 반환
        log_debug(f"[load_config] Returning full config with {len(substituted_config)} top-level keys")
        return cast(dict, substituted_config)

    except FileNotFoundError:
        log_error(f"[load_config] Config file not found: {yml_path}")
        raise
    except yaml.YAMLError as exc:
        log_error(f"[load_config] YAML parsing error in {yml_path}: {exc}")
        raise
    except Exception as exc:  # noqa: BLE001
        log_error(f"[load_config] Unexpected error loading {yml_path}: {exc}")
        raise
