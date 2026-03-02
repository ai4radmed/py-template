# 명세서: `scripts/setup/setup_log_dir.py`

## 역할
- `.env` 의 `LOG_PATH` 설정을 해석해 로그 디렉터리를 생성하고, (비 Windows 환경에서) 소유자와 권한을 적절히 설정하는 초기화 스크립트이다.

## Public API / 동작 (요약)
- `resolve_log_path_from_env(log_path: str | None, project_name: str, os_name: str) -> str | None`  
  - `LOG_PATH` 문자열에서 `{PROJECT_NAME}`, `$HOME`(또는 Windows에서 `%USERPROFILE%`) 를 치환해 실제 경로 문자열을 만든다.
  - 입력이 비어 있거나 공백뿐이면 `None` 을 반환한다.
- `main() -> int`  
  - 프로젝트 루트의 `.env` 를 로드하고, `LOG_PATH` 를 해석한 뒤:
    - 경로가 이미 존재하는 파일이면 에러 후 종료,
    - 없으면 디렉터리를 생성하고, 비 Windows 환경에서는 `SUDO_USER` 또는 현재 사용자로 소유권과 `755` 권한을 설정한다.

## 핵심 규칙
- `.env` 또는 `LOG_PATH` 가 없으면 디렉터리를 만들지 않고, 명확한 메시지를 출력한 뒤 실패 코드로 종료한다.
- 실제 로그 디렉터리 생성·권한 설정은 이 스크립트의 책임이고, `common.logger` 는 디렉터리를 생성하지 않고 존재·권한만 검사한다.
- 개발 환경(dev)에서는 기본적으로 **사용자 쓰기 가능한 경로**(예: `$HOME/logs/{PROJECT_NAME}`)를 `LOG_PATH` 로 사용하고, 프로덕션(prod)에서는 `/var/log/{PROJECT_NAME}` 와 같이 별도 디렉터리를 인프라/배포 단계에서 미리 만들고, `.env` 또는 환경 변수로 `LOG_PATH` 값을 덮어쓰는 전략을 따른다.
