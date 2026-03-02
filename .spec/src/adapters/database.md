# 명세서: `src/adapters/database.py`

## 역할
- `.env` 기반 PostgreSQL 연결을 생성하고, 단일/배치 쿼리 실행을 위한 헬퍼를 제공한다.
- 연결/쿼리 오류를 로깅하고 트랜잭션을 안전하게 롤백한 뒤 예외를 상위로 전파한다.

## Public API (요약)
- `get_db_connection()`  
  - `DB_HOST`, `DB_NAME`, `DB_USER`, `DB_PASSWORD`, `DB_PORT` 환경 변수를 사용해 표준 PostgreSQL 커넥션을 생성한다.
- `execute_query(query: str, params=None, fetch_one=False, fetch_all=False)`  
  - 내부에서 `get_db_connection()` 을 호출해 단일 쿼리를 실행하고, 옵션에 따라 `fetchone`/`fetchall` 결과 또는 `None` 을 반환한다.
- `execute_many(query: str, data_list)`  
  - 동일 쿼리에 여러 데이터를 배치 실행하고, 영향받은 행 수(`rowcount`) 를 반환한다.

## 핵심 규칙
- 각 헬퍼는 호출이 끝나면 항상 커넥션과 커서를 닫아야 하며, 커넥션 풀링은 수행하지 않는다.
- `psycopg2.Error` 발생 시 적절히 로그를 남기고, 커넥션이 열려 있으면 롤백 후 예외를 다시 던진다.
- DB 접속 정보는 오직 환경 변수에서 읽으며, 하드코딩하지 않는다.
- **Mypy 정적 타입 준수**: `Any` 반환을 지양하고, `Any` 타입인 `rowcount` 등은 명시적으로 `int` 로 형변환하여 반환한다.
