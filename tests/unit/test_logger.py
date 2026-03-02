"""
common.logger 모듈의 핵심 정책 함수 테스트.
"""

from __future__ import annotations

import os
from pathlib import Path

import pytest

from common.logger import _assert_audit_is_file_only, _get_log_level, _require_parent_exists_and_writable


def test_get_log_level_valid_and_invalid(monkeypatch: pytest.MonkeyPatch) -> None:
    """유효/무효 LOG_LEVEL 값에 대해 올바르게 처리한다."""
    monkeypatch.setenv("LOG_LEVEL", "DEBUG")
    assert _get_log_level() == "DEBUG"

    monkeypatch.setenv("LOG_LEVEL", "invalid-level")
    assert _get_log_level() == "INFO"

    monkeypatch.delenv("LOG_LEVEL", raising=False)
    assert _get_log_level() == "INFO"


def test_require_parent_exists_and_writable_ok(tmp_path: Path) -> None:
    """상위 디렉터리가 존재하고 쓰기 가능하면 예외 없이 통과한다."""
    log_dir = tmp_path / "logs"
    log_dir.mkdir(parents=True, exist_ok=True)
    log_file = log_dir / "app.log"

    # 존재하는 디렉터리에 대해 예외가 발생하지 않아야 한다.
    _require_parent_exists_and_writable(log_file, handler_name="service_file")


def test_require_parent_exists_and_writable_missing_parent(tmp_path: Path) -> None:
    """상위 디렉터리가 존재하지 않으면 FileNotFoundError 를 발생시킨다."""
    missing_parent = tmp_path / "no_such_dir" / "app.log"

    with pytest.raises(FileNotFoundError):
        _require_parent_exists_and_writable(missing_parent, handler_name="service_file")


def test_assert_audit_is_file_only_ok() -> None:
    """audit 로거가 파일 핸들러만 사용하고 propagate=False 인 경우 예외가 없다."""
    config = {
        "loggers": {
            "audit": {
                "level": "INFO",
                "handlers": ["audit_file"],
                "propagate": False,
            }
        }
    }

    # 정책을 준수하는 구성은 예외 없이 통과해야 한다.
    _assert_audit_is_file_only(config)


def test_assert_audit_is_file_only_rejects_console_handler() -> None:
    """audit 로거에 console 핸들러가 포함되면 RuntimeError 를 발생시킨다."""
    config = {
        "loggers": {
            "audit": {
                "level": "INFO",
                "handlers": ["audit_file", "console"],
                "propagate": False,
            }
        }
    }

    with pytest.raises(RuntimeError):
        _assert_audit_is_file_only(config)


def test_assert_audit_is_file_only_rejects_propagate_true() -> None:
    """audit 로거가 propagate=True 이면 RuntimeError 를 발생시킨다."""
    config = {
        "loggers": {
            "audit": {
                "level": "INFO",
                "handlers": ["audit_file"],
                "propagate": True,
            }
        }
    }

    with pytest.raises(RuntimeError):
        _assert_audit_is_file_only(config)

