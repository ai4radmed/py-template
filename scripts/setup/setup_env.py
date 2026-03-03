"""
명세서(`.spec/scripts/setup/setup_env.md`) 기반 .env 생성 편의 스크립트.

역할:
- 프로젝트 루트에서 `.env.example` 을 `.env` 로 복사하고,
  - PROJECT_NAME: 현재 폴더명
  - PROJECT_ROOT: 현재 루트 절대 경로
  - LOG_PATH: OS 별 기본 추천 경로
  로 자동 치환한다.
"""

from __future__ import annotations

import platform
import re
import shutil
from pathlib import Path


def main() -> int:
    """setup_env 스크립트 엔트리 포인트. 성공 시 0, 실패 시 1."""
    os_name = platform.system()
    print(f"[setup_env] 운영체제: {os_name}")

    root = Path.cwd()
    cur_dir_name = root.name
    src = root / ".env.example"
    dst = root / ".env"

    if not src.is_file():
        print(f"[setup_env] .env.example 파일이 없습니다. 경로: {src}")
        return 1

    shutil.copyfile(src, dst)

    content = dst.read_text(encoding="utf-8")

    # PROJECT_NAME = 현재 폴더명
    content = re.sub(
        r"^PROJECT_NAME=.*",
        lambda _: f"PROJECT_NAME={cur_dir_name}",
        content,
        flags=re.MULTILINE,
    )

    # PROJECT_ROOT = 현재 루트 절대 경로
    abs_path = str(root)
    content = re.sub(
        r"^PROJECT_ROOT=.*",
        lambda _: f"PROJECT_ROOT={abs_path}",
        content,
        flags=re.MULTILINE,
    )

    # OS 별 기본 LOG_PATH 추천값 설정 (dev 기본은 사용자 쓰기 가능한 경로)
    if os_name == "Linux":
        # 개발 환경 기본값: $HOME/logs/{PROJECT_NAME}
        log_path = "$HOME/logs/{PROJECT_NAME}"
    elif os_name == "Darwin":
        log_path = "$HOME/Library/Logs/{PROJECT_NAME}"
    elif os_name == "Windows":
        log_path = "%USERPROFILE%\\AppData\\Local\\{PROJECT_NAME}"
    else:
        log_path = "$HOME/logs/{PROJECT_NAME}"

    content = re.sub(
        r"^LOG_PATH=.*",
        lambda _: f"LOG_PATH={log_path}",
        content,
        flags=re.MULTILINE,
    )

    dst.write_text(content, encoding="utf-8")
    print("[setup_env] .env 파일이 생성되고, 경로 및 프로젝트명이 현재 폴더명으로 자동 치환되었습니다.")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
