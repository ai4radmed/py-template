"""
명세서(`.spec/src/adapters/get_cipher.md`) 기반 FF3 Cipher 팩토리.

역할:
- FF3 기반 Format-Preserving Encryption 을 위한 FF3Cipher 인스턴스를 생성해 반환한다.
"""

from __future__ import annotations

import os

from dotenv import load_dotenv
from ff3 import FF3Cipher

from common.logger import log_critical, log_debug


def get_cipher(alphabet_type: str = "alphanumeric") -> FF3Cipher:
    """
    FF3Cipher 인스턴스를 생성해 반환한다.

    - alphabet_type 이 "numeric" 이면 FF3_NUMERIC 을,
      그 외에는 FF3_ALPHANUMERIC 을 사용한다.
    - FF3_KEY, FF3_TWEAK, FF3_ALPHANUMERIC, FF3_NUMERIC 중 하나라도 누락되면
      치명 로그를 남기고 RuntimeError 를 발생시킨다.
    """
    load_dotenv()
    key = os.getenv("FF3_KEY")
    tweak = os.getenv("FF3_TWEAK")
    alphabet = os.getenv("FF3_NUMERIC") if alphabet_type == "numeric" else os.getenv("FF3_ALPHANUMERIC")

    log_debug(f"[get_cipher] alphabet_type = {alphabet_type}")

    if not key or not tweak or not alphabet:
        msg = "필수 환경변수(FF3_KEY, FF3_TWEAK, FF3_ALPHANUMERIC, FF3_NUMERIC)가 누락되었습니다."
        log_critical(msg)
        raise RuntimeError(msg)

    return FF3Cipher.withCustomAlphabet(key, tweak, alphabet)

