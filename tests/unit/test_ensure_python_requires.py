"""
변경이력:
  - 2026-02-28: 로컬 전용: CI에서는 -m "not local_only" 로 제외 (BenKorea)
  - 2026-02-28: GS-31 시험 가능성, ISMS-P 개발보안 증적 (BenKorea)
"""

import sys
from pathlib import Path

import pytest

# scripts/setup 모듈 로드 (pythonpath에 src만 있으므로 경로 추가)
_project_root = Path(__file__).resolve().parents[2]
_setup_dir = _project_root / "scripts" / "setup"
if str(_setup_dir) not in sys.path:
    sys.path.insert(0, str(_setup_dir))

import ensure_python_requires as _mod

get_requires_python = _mod.get_requires_python


@pytest.mark.local_only
@pytest.mark.gs_req("GS-31")
@pytest.mark.isms("ISMS-2.7-46")
def test_get_requires_python_from_project(tmp_path: Path) -> None:
    """[project] requires-python 값을 읽어 반환한다."""
    (tmp_path / "pyproject.toml").write_text(
        '[project]\nname = "x"\nrequires-python = ">=3.12.10"',
        encoding="utf-8",
    )
    assert get_requires_python(tmp_path / "pyproject.toml") == ">=3.12.10"


@pytest.mark.local_only
@pytest.mark.gs_req("GS-31")
@pytest.mark.isms("ISMS-2.7-46")
def test_get_requires_python_fallback_tool_uv(tmp_path: Path) -> None:
    """[project]에 없으면 [tool.uv].python 값을 반환한다."""
    (tmp_path / "pyproject.toml").write_text(
        '[tool.uv]\npython = "3.12"\n',
        encoding="utf-8",
    )
    assert get_requires_python(tmp_path / "pyproject.toml") == "3.12"
