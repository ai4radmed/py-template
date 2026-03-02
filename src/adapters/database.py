"""
명세서(`.spec/src/adapters/database.md`) 기반 PostgreSQL 데이터베이스 어댑터.

역할:
- .env 기반 PostgreSQL 연결을 생성하고, 단일/배치 쿼리 실행을 위한 헬퍼를 제공한다.
"""

from __future__ import annotations

import os

import psycopg2
from dotenv import load_dotenv

from common.logger import log_debug, log_error

load_dotenv()


def get_db_connection() -> psycopg2.extensions.connection:
    """표준 PostgreSQL 데이터베이스 연결을 반환한다."""
    try:
        conn = psycopg2.connect(
            host=os.getenv("DB_HOST", "localhost"),
            database=os.getenv("DB_NAME", "ai4ref"),
            user=os.getenv("DB_USER", "postgres"),
            password=os.getenv("DB_PASSWORD", "postgres"),
            port=os.getenv("DB_PORT", "5432"),
        )
        log_debug("데이터베이스 연결 성공")
        return conn
    except psycopg2.Error as exc:
        log_error(f"데이터베이스 연결 실패: {exc}")
        raise


def execute_query(
    query: str,
    params: object | None = None,
    fetch_one: bool = False,
    fetch_all: bool = False,
):
    """
    단일 SQL 쿼리를 실행하는 헬퍼.

    - fetch_one=True 이면 cursor.fetchone() 결과 반환
    - fetch_all=True 이면 cursor.fetchall() 결과 반환
    - 둘 다 False 이면 None 반환
    """
    conn = None
    try:
        conn = get_db_connection()
        cur = conn.cursor()

        cur.execute(query, params)

        result = None
        if fetch_one:
            result = cur.fetchone()
        elif fetch_all:
            result = cur.fetchall()

        conn.commit()
        cur.close()
        conn.close()

        return result

    except psycopg2.Error as exc:
        log_error(f"쿼리 실행 오류: {exc}")
        if conn is not None:
            conn.rollback()
            conn.close()
        raise


def execute_many(query: str, data_list: list[object]) -> int:
    """
    동일한 쿼리에 여러 데이터 레코드를 배치 실행하는 헬퍼.

    영향받은 행 수(rowcount)를 반환한다.
    """
    conn = None
    try:
        conn = get_db_connection()
        cur = conn.cursor()

        cur.executemany(query, data_list)

        conn.commit()
        affected_rows = cur.rowcount
        cur.close()
        conn.close()

        return affected_rows

    except psycopg2.Error as exc:
        log_error(f"배치 실행 오류: {exc}")
        if conn is not None:
            conn.rollback()
            conn.close()
        raise

