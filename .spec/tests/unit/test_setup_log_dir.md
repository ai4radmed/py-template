# 명세서: `tests/unit/test_setup_log_dir.py`

## 역할
- `scripts/setup/setup_log_dir.py` 의 `resolve_log_path_from_env` 함수가 OS/환경 변수/프로젝트명 조합에 따라 로그 경로를 올바르게 해석하는지 검증한다.

## 테스트 범위 (요약)
- `{PROJECT_NAME}` 치환, 빈 문자열/None 입력 시 `None` 반환 여부를 확인한다.
- Linux/Darwin 에서 `$HOME`, Windows 에서 `%USERPROFILE%` 가 올바르게 치환되는지 검증한다.
- `project_name` 이 비어 있을 때 `"default"` 로 치환되는지 확인한다.

## 핵심 규칙
- 각 테스트에서 필요한 환경 변수를 임시로 설정하고, 테스트 종료 후 원복한다.
- 로그 경로 설정이 올바르게 해석되는 것은 로그 생성·보관 정책(컴플라이언스)의 전제 조건임을 GS/ISMS-P 마커로 증적한다.
