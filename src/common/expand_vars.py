"""
변경이력:
  - 2026-02-28: substitute → expand_vars 리네임 (BenKorea)
  - 2026-02-28: 모듈 expand_vars.py로 통일 (BenKorea)
  - 2025-11-25: 환경변수 치환(문자열/컬렉션 재귀) (BenKorea)
"""

import os
from typing import Any


def expand_vars_str(value: str) -> str:
    """문자열 내 ${VAR} 패턴을 os.environ 값으로 확장."""
    if not isinstance(value, str):
        return value
    for k, v in os.environ.items():
        value = value.replace(f"${{{k}}}", v)
    return value


def expand_vars(value: str | dict | list | Any) -> str | dict | list | Any:
    """
    재귀적으로 환경변수 확장을 수행.

    지원 입력: str, dict, list. 기타 타입은 그대로 반환.
    """
    if isinstance(value, str):
        return expand_vars_str(value)
    if isinstance(value, dict):
        return {key: expand_vars(val) for key, val in value.items()}
    if isinstance(value, list):
        return [expand_vars(v) for v in value]
    return value
