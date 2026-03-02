# 명세서: `tests/unit/test_logger.py`

## 역할
- `common.logger` 모듈의 핵심 정책 함수들이 로깅 레벨, 로그 디렉터리 경로, audit 로거 정책을 올바르게 강제하는지 검증한다.

## 테스트 범위 (요약)
- `_get_log_level`:
  - 유효한 `LOG_LEVEL` 값에 대해서는 그대로 반환하고, 잘못된 값이나 미설정 시 `INFO` 로 폴백하는지 확인.
- `_require_parent_exists_and_writable`:
  - 상위 디렉터리가 존재하고 쓰기 가능하면 예외 없이 통과하는지,
  - 상위 디렉터리가 존재하지 않으면 `FileNotFoundError` 를 발생시키는지 확인.
- `_assert_audit_is_file_only`:
  - `audit` 로거가 console 핸들러를 포함하거나 `propagate=True` 인 경우 `RuntimeError` 를 발생시키는지,
  - 정책을 준수하는 구성에서는 예외가 발생하지 않는지 확인.

## 핵심 규칙
- 테스트는 실제 파일 시스템에 임시 디렉터리(`tmp_path`)를 사용하여 권한·경로 검증 로직을 재현한다.
- audit 로거 정책 위반 시 반드시 예외를 발생시켜 조용히 무시되지 않도록 보장한다.

