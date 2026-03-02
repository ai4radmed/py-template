"""
명세서(`.spec/scripts/setup/setup_log_dir.md`) 기반 로그 디렉터리 초기화 스크립트.

역할:
- .env 의 LOG_PATH 설정을 해석해 로그 디렉터리를 생성하고,
  비 Windows 환경에서는 소유자·그룹 및 권한(755)을 설정한다.
"""

from __future__ import annotations

import getpass
import os
import platform
import shutil
from pathlib import Path

from dotenv import load_dotenv


def resolve_log_path_from_env(log_path: str | None, project_name: str, os_name: str) -> str | None:
    """
    LOG_PATH 문자열에서 {PROJECT_NAME}, %USERPROFILE%, $HOME 치환 후 반환.

    - log_path 가 비어 있거나 공백뿐이면 None 반환.
    - Windows: %USERPROFILE% 를 환경변수 USERPROFILE 값으로 치환.
    - 그 외 OS: $HOME 을 환경변수 HOME 값으로 치환.
    """
    if not log_path or not log_path.strip():
        return None

    s = log_path.strip().replace("{PROJECT_NAME}", (project_name or "default").strip())
    if os_name == "Windows":
        s = s.replace("%USERPROFILE%", os.environ.get("USERPROFILE", ""))
    else:
        s = s.replace("$HOME", os.environ.get("HOME", ""))

    return s.strip() or None


def main() -> int:
    """로그 디렉터리 생성 및(선택) 소유권·권한 설정. 성공 0, 실패 1."""
    root = Path.cwd()
    env_file = root / ".env"
    if not env_file.is_file():
        print("[setup_log_dir] .env 파일이 없습니다. 먼저 .env를 복사하세요.")
        return 1

    load_dotenv(env_file)

    raw_log_path = os.getenv("LOG_PATH")
    project_name = os.getenv("PROJECT_NAME", "default")
    os_name = platform.system()
    print(f"[setup_log_dir] OS: {os_name}")

    log_path = resolve_log_path_from_env(raw_log_path, project_name, os_name)
    print(f"[setup_log_dir] log_path: {log_path}")
    if not log_path:
        print("[setup_log_dir] .env에 LOG_PATH가 정의되어 있지 않습니다.")
        return 1

    log_dir = Path(log_path)

    if log_dir.exists() and not log_dir.is_dir():
        print(f"[setup_log_dir] 오류: 경로가 이미 파일입니다. 디렉터리만 허용됩니다. {log_dir}")
        return 1

    if not log_dir.is_dir():
        log_dir.mkdir(parents=True, exist_ok=True)
        print(f"[setup_log_dir] 로그 디렉터리 생성: {log_dir}")
        if os_name != "Windows":
            try:
                user = os.getenv("SUDO_USER") or getpass.getuser()
                shutil.chown(str(log_dir), user=user, group=user)
                os.chmod(str(log_dir), 0o755)
                print(f"[setup_log_dir] 소유자 및 권한 변경: {user}:{user}, 755")
            except Exception as exc:  # noqa: BLE001
                print(f"[setup_log_dir] 소유자/권한 변경 실패: {exc}")
    else:
        print(f"[setup_log_dir] 이미 디렉터리 존재: {log_dir}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
