# 명세서: `src/common/logger.py`

## 역할
- `.env` + `config/logging.yml` 기반으로 로깅을 1회 초기화하고, 프로젝트 전역 로거와 개인정보보호용 감사 로그 헬퍼를 제공한다.
- 감사 로그는 정책 문서(`documents/LOGGING_POLICY.md`)에 따라 별도 파일에만 남도록 보장한다.

## Public API (요약)
- `setup_logging() -> None`  
  - 아직 로깅이 설정되지 않았다면 `config/logging.yml` 을 로드해 `logging.config.dictConfig` 로 한 번만 초기화한다.
- `get_logger(name: str | None = PROJECT_NAME) -> logging.Logger`  
  - 지정 이름(기본: `PROJECT_NAME`)의 로거를 반환하며, 루트에 핸들러가 없으면 자동으로 `setup_logging()` 을 호출한다.
- `audit_log(...) -> None`  
  - `audit` 로거로 구조화된 JSON 형태의 감사 로그를 기록한다(행위자, 대상, 사유, 컴플라이언스 정보 포함).
- `log_debug/info/warn/error/critical(msg: str) -> None`  
  - 기본 프로젝트 로거에 대한 간단한 래퍼로, 메시지를 해당 레벨로 기록한다.

## 핵심 규칙
- 환경 변수 `PROJECT_NAME`, `LOG_PATH`, `LOG_LEVEL` 을 사용하며, `LOG_LEVEL` 이 유효하지 않으면 `INFO` 로 폴백한다.
- 파일 기반 로거는 디렉터리를 자동 생성하지 않고, 상위 디렉터리 존재·쓰기 권한만 검사한다(생성은 `scripts/setup/setup_log_dir.py` 책임).
- `audit` 로거는 console 핸들러를 가질 수 없고(`handlers` 에 `console` 금지), `propagate` 가 `False` 여야 한다.
- `config/logging.yml` 이 없거나 파일 핸들러 설정이 잘못된 경우(경로/치환 실패 등)에는 예외를 발생시켜 조용히 무시하지 않는다.
