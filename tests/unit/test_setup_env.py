"""
변경이력:
  - 2026-03-02: .env.example 기반 setup_env 메인 동작 단위 테스트 추가 (AI)
"""

import os
import sys
from pathlib import Path

# scripts/setup 모듈 로드
_project_root = Path(__file__).resolve().parents[2]
_setup_dir = _project_root / "scripts" / "setup"
if str(_setup_dir) not in sys.path:
    sys.path.insert(0, str(_setup_dir))

import setup_env as _mod  # noqa: E402


def _write_env_example(path: Path) -> None:
    """테스트용 .env.example 파일 생성."""
    path.write_text(
        "PROJECT_NAME=example\nPROJECT_ROOT=/tmp/example\nLOG_PATH=/tmp/logs\nOTHER_KEY=keep\n",
        encoding="utf-8",
    )


def test_setup_env_creates_env_with_replacements(tmp_path: Path) -> None:
    """.env.example 을 기반으로 .env 를 생성하고 주요 값들을 치환한다."""
    _write_env_example(tmp_path / ".env.example")

    cwd = Path.cwd()
    try:
        os.chdir(tmp_path)
        exit_code = _mod.main()
    finally:
        os.chdir(cwd)

    assert exit_code == 0

    env_path = tmp_path / ".env"
    assert env_path.is_file()

    content = env_path.read_text(encoding="utf-8").splitlines()
    config: dict[str, str] = {}
    for line in content:
        if "=" in line:
            key, value = line.split("=", 1)
            config[key] = value

    assert config["PROJECT_NAME"] == tmp_path.name
    # Linux/WSL 기준: 백슬래시가 없으므로 그대로 절대 경로가 기록된다.
    assert config["PROJECT_ROOT"] == str(tmp_path)
    # LOG_PATH 는 OS 별 기본 경로이지만, 최소한 {PROJECT_NAME} 플레이스홀더를 포함해야 한다.
    assert "{PROJECT_NAME}" in config["LOG_PATH"]
    # 기타 키는 유지된다.
    assert config["OTHER_KEY"] == "keep"


def test_setup_env_missing_example_returns_error(tmp_path: Path) -> None:
    """.env.example 이 없으면 에러 코드와 메시지만 남기고 .env 를 생성하지 않는다."""
    cwd = Path.cwd()
    try:
        os.chdir(tmp_path)
        exit_code = _mod.main()
    finally:
        os.chdir(cwd)

    assert exit_code == 1
    assert not (tmp_path / ".env").exists()
