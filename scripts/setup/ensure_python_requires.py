"""
기능:
  - pyproject.toml의 requires-python 값을 읽어 uv로 Python 런타임 설치

변경이력 (기능과 1:1 매칭, 최신순):
  - 2026-02-28: get_requires_python 추출 함수 분리 (단위 테스트·GS/ISMS-P 대응)
  - 2026-02-28: ensure_python_requires.py로 파일명 변경
  - 2025-10-27: 크로스 플랫폼 호환성 개선 (BenKorea)
"""

import subprocess
import tomllib
from pathlib import Path


def get_requires_python(pyproject_path: Path) -> str | None:
    """
    pyproject.toml에서 requires-python 값을 추출.
    [project].requires-python 또는 [tool.uv].python 순으로 확인.
    """
    if not pyproject_path.exists():
        return None
    try:
        data = tomllib.loads(pyproject_path.read_text(encoding="utf-8"))
    except Exception:
        return None
    return data.get("project", {}).get("requires-python") or data.get("tool", {}).get("uv", {}).get("python")


def main() -> int:
    """pyproject.toml의 requires-python을 읽어 uv로 Python 버전을 설치. 성공 0, 실패 1."""
    project_root = Path(__file__).resolve().parents[2]
    pyproject = project_root / "pyproject.toml"

    requires_python = get_requires_python(pyproject)
    if not requires_python:
        print("[ensure-python-requires] requires-python 설정을 찾을 수 없습니다.")
        return 1

    try:
        subprocess.run(
            ["uv", "python", "install", str(requires_python)],
            check=True,
            cwd=project_root,
        )
        print(f"[ensure-python-requires] uv python install {requires_python} 완료")
        return 0
    except (subprocess.CalledProcessError, FileNotFoundError) as e:
        print(f"[ensure-python-requires] 실패 - uv python install {requires_python} 를 수동으로 실행하세요. 에러: {e}")
        return 1


if __name__ == "__main__":
    exit(main())
