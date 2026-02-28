"""
변경이력 (최신순):
  - 2026-02-28: setup_log_dir.resolve_log_path_from_env 단위 테스트 (BenKorea)
"""

import os
import sys
from pathlib import Path

import pytest

# scripts/setup 로드
_project_root = Path(__file__).resolve().parents[2]
_setup_dir = _project_root / "scripts" / "setup"
if str(_setup_dir) not in sys.path:
    sys.path.insert(0, str(_setup_dir))

import setup_log_dir as _mod

resolve_log_path_from_env = _mod.resolve_log_path_from_env


@pytest.mark.gs_req("GS-29")  # 분석성: 진단 로그 충분 제공
@pytest.mark.isms("ISMS-2.8-54")  # 로그 및 접속기록 관리
def test_resolve_log_path_project_name_replaced() -> None:
    """{PROJECT_NAME}이 프로젝트명으로 치환된다. 로그 경로 설정은 로그 생성·보관의 전제."""
    assert resolve_log_path_from_env(
        "/var/log/{PROJECT_NAME}", "myapp", "Linux"
    ) == "/var/log/myapp"
    assert resolve_log_path_from_env(
        "/var/log/{PROJECT_NAME}/sub", "py-template", "Linux"
    ) == "/var/log/py-template/sub"


def test_resolve_log_path_empty_or_whitespace_returns_none() -> None:
    """빈 문자열 또는 공백만 있으면 None."""
    assert resolve_log_path_from_env("", "x", "Linux") is None
    assert resolve_log_path_from_env("   ", "x", "Linux") is None
    assert resolve_log_path_from_env(None, "x", "Linux") is None


def test_resolve_log_path_home_expanded_on_linux() -> None:
    """Linux에서 $HOME이 환경변수 값으로 치환된다."""
    os.environ["HOME"] = "/home/user"
    try:
        assert resolve_log_path_from_env(
            "$HOME/logs/myapp", "myapp", "Linux"
        ) == "/home/user/logs/myapp"
    finally:
        os.environ.pop("HOME", None)


def test_resolve_log_path_home_expanded_on_darwin() -> None:
    """Darwin에서 $HOME 치환."""
    os.environ["HOME"] = "/Users/me"
    try:
        assert resolve_log_path_from_env(
            "$HOME/Library/Logs/{PROJECT_NAME}", "myapp", "Darwin"
        ) == "/Users/me/Library/Logs/myapp"
    finally:
        os.environ.pop("HOME", None)


def test_resolve_log_path_windows_userprofile() -> None:
    """Windows에서 %USERPROFILE% 치환."""
    os.environ["USERPROFILE"] = "C:\\Users\\me"
    try:
        result = resolve_log_path_from_env(
            "%USERPROFILE%\\AppData\\Local\\{PROJECT_NAME}", "myapp", "Windows"
        )
        assert result == "C:\\Users\\me\\AppData\\Local\\myapp"
    finally:
        os.environ.pop("USERPROFILE", None)


def test_resolve_log_path_project_name_default() -> None:
    """project_name이 빈 문자열이면 default로 치환된다."""
    assert resolve_log_path_from_env(
        "/var/log/{PROJECT_NAME}", "", "Linux"
    ) == "/var/log/default"
