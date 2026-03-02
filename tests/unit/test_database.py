"""
adapters.database 모듈 테스트.
"""

from __future__ import annotations

from typing import Any

import pytest

pytest.importorskip("psycopg2")

import adapters.database as _db  # noqa: E402


class DummyCursor:
    def __init__(self, fetch_one_result: Any = None, fetch_all_result: Any = None, rowcount: int = 0) -> None:
        self.fetch_one_result = fetch_one_result
        self.fetch_all_result = fetch_all_result
        self.rowcount = rowcount
        self.executed = []
        self.closed = False

    def execute(self, query: str, params: Any | None = None) -> None:  # noqa: D401
        """쿼리 실행 기록."""
        self.executed.append(("execute", query, params))

    def executemany(self, query: str, data_list: list[Any]) -> None:  # noqa: D401
        """배치 쿼리 실행 기록."""
        self.executed.append(("executemany", query, data_list))

    def fetchone(self) -> Any:  # noqa: D401
        """사전 설정된 fetch_one_result 반환."""
        return self.fetch_one_result

    def fetchall(self) -> Any:  # noqa: D401
        """사전 설정된 fetch_all_result 반환."""
        return self.fetch_all_result

    def close(self) -> None:  # noqa: D401
        """커서 종료 플래그 설정."""
        self.closed = True


class DummyConnection:
    def __init__(self, cursor: DummyCursor) -> None:
        self._cursor = cursor
        self.committed = False
        self.rolled_back = False
        self.closed = False

    def cursor(self) -> DummyCursor:  # noqa: D401
        """더미 커서를 반환."""
        return self._cursor

    def commit(self) -> None:  # noqa: D401
        """커밋 플래그 설정."""
        self.committed = True

    def rollback(self) -> None:  # noqa: D401
        """롤백 플래그 설정."""
        self.rolled_back = True

    def close(self) -> None:  # noqa: D401
        """연결 종료 플래그 설정."""
        self.closed = True


class DummyPsycopg2:
    class Error(Exception):
        """psycopg2.Error 대체용 더미 예외."""

    def __init__(self, connection: DummyConnection | None = None, should_fail: bool = False) -> None:
        self._connection = connection
        self.should_fail = should_fail
        self.connect_args: tuple = ()
        self.connect_kwargs: dict[str, Any] = {}

    def connect(self, *args: Any, **kwargs: Any) -> DummyConnection:
        """psycopg2.connect 대체 구현."""
        self.connect_args = args
        self.connect_kwargs = kwargs
        if self.should_fail:
            raise DummyPsycopg2.Error("connection failed")
        assert self._connection is not None, "DummyConnection must be provided when should_fail=False"
        return self._connection


def test_get_db_connection_uses_env(monkeypatch: pytest.MonkeyPatch) -> None:
    """get_db_connection 이 환경변수 기반 인자를 사용해 연결을 생성하는지 검증."""
    cursor = DummyCursor()
    conn = DummyConnection(cursor)
    dummy_psycopg2 = DummyPsycopg2(connection=conn)

    monkeypatch.setenv("DB_HOST", "db.example.com")
    monkeypatch.setenv("DB_NAME", "mydb")
    monkeypatch.setenv("DB_USER", "user")
    monkeypatch.setenv("DB_PASSWORD", "secret")
    monkeypatch.setenv("DB_PORT", "15432")

    # adapters.database 모듈의 psycopg2 를 더미로 교체
    monkeypatch.setattr(_db, "psycopg2", dummy_psycopg2)

    # log_debug 가 호출되기만 하면 되므로 더미로 교체
    calls: list[str] = []
    monkeypatch.setattr(_db, "log_debug", lambda msg: calls.append(msg))

    result_conn = _db.get_db_connection()

    assert result_conn is conn
    # psycopg2.connect 에 전달된 인자를 확인
    assert dummy_psycopg2.connect_kwargs["host"] == "db.example.com"
    assert dummy_psycopg2.connect_kwargs["database"] == "mydb"
    assert dummy_psycopg2.connect_kwargs["user"] == "user"
    assert dummy_psycopg2.connect_kwargs["password"] == "secret"
    assert dummy_psycopg2.connect_kwargs["port"] == "15432"
    assert any("데이터베이스 연결 성공" in c for c in calls)


def test_execute_query_fetch_one_and_rollback_on_error(monkeypatch: pytest.MonkeyPatch) -> None:
    """execute_query 가 fetch_one 동작과 예외/롤백 흐름을 올바르게 처리하는지 검증."""
    # 정상 케이스: fetch_one
    cursor_ok = DummyCursor(fetch_one_result=("row",))
    conn_ok = DummyConnection(cursor_ok)
    dummy_psycopg2_ok = DummyPsycopg2(connection=conn_ok)
    monkeypatch.setattr(_db, "psycopg2", dummy_psycopg2_ok)

    result = _db.execute_query("SELECT 1", fetch_one=True)
    assert result == ("row",)
    assert conn_ok.committed is True
    assert conn_ok.closed is True
    assert cursor_ok.closed is True

    # 예외 케이스: 쿼리 실행 중 psycopg2.Error 발생 시 롤백
    class FailingCursor(DummyCursor):
        def execute(self, query: str, params: Any | None = None) -> None:  # noqa: D401
            raise DummyPsycopg2.Error("execute failed")

    cursor_fail = FailingCursor()
    conn_fail = DummyConnection(cursor_fail)
    dummy_psycopg2_fail = DummyPsycopg2(connection=conn_fail)
    monkeypatch.setattr(_db, "psycopg2", dummy_psycopg2_fail)

    error_logged: list[str] = []
    monkeypatch.setattr(_db, "log_error", lambda msg: error_logged.append(msg))

    with pytest.raises(DummyPsycopg2.Error):
        _db.execute_query("SELECT 1")

    assert conn_fail.rolled_back is True
    assert conn_fail.closed is True
    assert any("쿼리 실행 오류" in msg for msg in error_logged)


def test_execute_many_returns_rowcount_and_rollback_on_error(monkeypatch: pytest.MonkeyPatch) -> None:
    """execute_many 가 rowcount 를 반환하고, 예외 시 롤백하는지 검증."""
    # 정상 케이스
    cursor_ok = DummyCursor(rowcount=3)
    conn_ok = DummyConnection(cursor_ok)
    dummy_psycopg2_ok = DummyPsycopg2(connection=conn_ok)
    monkeypatch.setattr(_db, "psycopg2", dummy_psycopg2_ok)

    affected = _db.execute_many("INSERT INTO t VALUES (%s)", [("a",), ("b",), ("c",)])
    assert affected == 3
    assert conn_ok.committed is True
    assert conn_ok.closed is True

    # 예외 케이스
    class FailingCursor(DummyCursor):
        def executemany(self, query: str, data_list: list[Any]) -> None:  # noqa: D401
            raise DummyPsycopg2.Error("executemany failed")

    cursor_fail = FailingCursor()
    conn_fail = DummyConnection(cursor_fail)
    dummy_psycopg2_fail = DummyPsycopg2(connection=conn_fail)
    monkeypatch.setattr(_db, "psycopg2", dummy_psycopg2_fail)

    error_logged: list[str] = []
    monkeypatch.setattr(_db, "log_error", lambda msg: error_logged.append(msg))

    with pytest.raises(DummyPsycopg2.Error):
        _db.execute_many("INSERT INTO t VALUES (%s)", [("x",)])

    assert conn_fail.rolled_back is True
    assert conn_fail.closed is True
    assert any("배치 실행 오류" in msg for msg in error_logged)

