"""
명세서(`.spec/src/common/expand_vars.md`) 기반 환경변수 치환 유틸리티.

역할:
- 문자열, 딕셔너리, 리스트 등 설정 구조 안의 `${VAR}` 패턴을
  현재 프로세스의 os.environ 값으로 재귀적으로 치환한다.
"""

from __future__ import annotations

import os
from typing import Any


def expand_vars_str(value: str) -> str:
    """문자열 내 ${VAR} 패턴을 os.environ 값으로 확장한다."""
    if not isinstance(value, str):
        return value

    result = value
    for key, env_value in os.environ.items():
        result = result.replace(f"${{{key}}}", env_value)
    return result


def expand_vars(value: str | dict | list | Any) -> str | dict | list | Any:
    """
    재귀적으로 환경변수 확장을 수행한다.

    지원 입력:
    - str: expand_vars_str 로 치환
    - dict: 값에 대해 재귀 호출
    - list: 각 원소에 대해 재귀 호출
    - 기타 타입: 그대로 반환
    """
    if isinstance(value, str):
        return expand_vars_str(value)
    if isinstance(value, dict):
        return {key: expand_vars(val) for key, val in value.items()}
    if isinstance(value, list):
        return [expand_vars(item) for item in value]
    return value
