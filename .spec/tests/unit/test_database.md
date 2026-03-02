# 명세서: `tests/unit/test_database.py`

## 역할
- `adapters.database` 모듈의 Public API(`get_db_connection`, `execute_query`, `execute_many`) 가
  `.env` 기반으로 PostgreSQL 연결을 생성하고, 단일/배치 쿼리 실행 시 예외·트랜잭션을 올바르게 처리하는지 검증한다.

## 테스트 범위 (요약)
- `get_db_connection`:
  - (DB를 실제로 연결하지 않는 모킹 기반 테스트) `psycopg2.connect` 를 모킹하여,
    - .env/환경변수에서 읽은 인자들이 그대로 전달되는지,
    - 연결 성공 시 디버그 로그가 호출되는지 확인한다.
  - `psycopg2.Error` 발생 시 에러 로그를 남기고 예외를 다시 던지는지 검증한다.
- `execute_query`:
  - `get_db_connection` 과 커서(`cursor`)를 모킹하여,
    - `fetch_one=True` 일 때 `cursor.fetchone()` 결과를 반환하는지,
    - `fetch_all=True` 일 때 `cursor.fetchall()` 결과를 반환하는지,
    - 둘 다 False 인 경우 `None` 을 반환하는지 확인한다.
  - 정상 경로에서 `commit()`, `close()` 가 호출되는지,
    - 예외(`psycopg2.Error`) 발생 시 `rollback()` 후 예외를 다시 던지는지 검증한다.
- `execute_many`:
  - `executemany` 호출 후 `rowcount` 값을 반환하는지 확인한다.
  - 예외 발생 시 `rollback()` 호출과 에러 로그 기록, 예외 재전파를 검증한다.

## 핵심 규칙
- 테스트는 실제 DB 접속 대신 `psycopg2.connect` 및 커서 객체를 모킹하여, 네트워크/DB 의존성 없이 로직과 트랜잭션 흐름만 검증한다.
- DB 접속 정보는 `.env` 또는 환경변수에서 읽으며, 테스트에서도 이 값을 명시적으로 설정해 인자 전달이 올바른지 확인한다.

