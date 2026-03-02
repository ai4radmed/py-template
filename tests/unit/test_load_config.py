"""
YAML 설정 로더(load_config) 테스트.
"""

from __future__ import annotations

import os
from pathlib import Path

import pytest

from common.load_config import load_config


def test_load_config_full_config(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    """전체 YAML을 로드하고 ${VAR} 패턴이 환경변수로 치환되는지 검증."""
    yaml_content = """
app:
  name: "${APP_NAME}"
  port: "${PORT}"
"""
    cfg_path = tmp_path / "config.yml"
    cfg_path.write_text(yaml_content, encoding="utf-8")

    monkeypatch.setenv("APP_NAME", "py-template")
    monkeypatch.setenv("PORT", "8080")

    cfg = load_config(str(cfg_path))

    assert cfg["app"]["name"] == "py-template"
    assert cfg["app"]["port"] == "8080"


def test_load_config_section_only(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    """section 인자를 사용해 특정 섹션만 잘라서 가져오는지 검증."""
    yaml_content = """
app:
  name: "${APP_NAME}"
logging:
  level: "${LOG_LEVEL}"
"""
    cfg_path = tmp_path / "config.yml"
    cfg_path.write_text(yaml_content, encoding="utf-8")

    monkeypatch.setenv("APP_NAME", "py-template")
    monkeypatch.setenv("LOG_LEVEL", "DEBUG")

    app_cfg = load_config(str(cfg_path), section="app")
    logging_cfg = load_config(str(cfg_path), section="logging")
    missing_cfg = load_config(str(cfg_path), section="missing")

    assert app_cfg == {"name": "py-template"}
    assert logging_cfg == {"level": "DEBUG"}
    assert missing_cfg == {}


def test_load_config_missing_file_raises(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    """존재하지 않는 YAML 경로에 대해 FileNotFoundError 를 발생시키는지 검증."""
    missing_path = tmp_path / "no_such_file.yml"

    with pytest.raises(FileNotFoundError):
        load_config(str(missing_path))

