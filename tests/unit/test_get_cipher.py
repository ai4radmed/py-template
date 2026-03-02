"""
adapters.get_cipher.get_cipher 함수 테스트.
"""

from __future__ import annotations

import pytest

pytest.importorskip("ff3")

import adapters.get_cipher as _mod  # noqa: E402


def test_get_cipher_uses_alphanumeric_alphabet(monkeypatch: pytest.MonkeyPatch) -> None:
    """alphabet_type 기본값(alphanumeric)에서 FF3_ALPHANUMERIC 환경변수를 사용하는지 검증."""
    # 환경 변수 설정
    monkeypatch.setenv("FF3_KEY", "K" * 32)
    monkeypatch.setenv("FF3_TWEAK", "0" * 16)
    monkeypatch.setenv("FF3_ALPHANUMERIC", "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ")
    monkeypatch.setenv("FF3_NUMERIC", "0123456789")

    # FF3Cipher.withCustomAlphabet 를 더미로 교체해 호출 인자만 검증
    calls: list[tuple[str, str, str]] = []

    class DummyCipher:
        @classmethod
        def withCustomAlphabet(cls, key: str, tweak: str, alphabet: str):  # type: ignore[override]  # noqa: N802
            calls.append((key, tweak, alphabet))
            return "DUMMY_CIPHER"

    monkeypatch.setattr(_mod, "FF3Cipher", DummyCipher)

    cipher = _mod.get_cipher()  # 기본값: alphanumeric

    assert cipher == "DUMMY_CIPHER"
    assert len(calls) == 1
    key, tweak, alphabet = calls[0]
    assert key == "K" * 32
    assert tweak == "0" * 16
    assert alphabet == "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"


def test_get_cipher_uses_numeric_alphabet(monkeypatch: pytest.MonkeyPatch) -> None:
    """alphabet_type='numeric' 인 경우 FF3_NUMERIC 환경변수를 사용하는지 검증."""
    monkeypatch.setenv("FF3_KEY", "K" * 32)
    monkeypatch.setenv("FF3_TWEAK", "0" * 16)
    monkeypatch.setenv("FF3_ALPHANUMERIC", "ignored")
    monkeypatch.setenv("FF3_NUMERIC", "0123456789")

    calls: list[tuple[str, str, str]] = []

    class DummyCipher:
        @classmethod
        def withCustomAlphabet(cls, key: str, tweak: str, alphabet: str):  # type: ignore[override]  # noqa: N802
            calls.append((key, tweak, alphabet))
            return "NUMERIC_CIPHER"

    monkeypatch.setattr(_mod, "FF3Cipher", DummyCipher)

    cipher = _mod.get_cipher(alphabet_type="numeric")

    assert cipher == "NUMERIC_CIPHER"
    assert len(calls) == 1
    key, tweak, alphabet = calls[0]
    assert key == "K" * 32
    assert tweak == "0" * 16
    assert alphabet == "0123456789"


def test_get_cipher_missing_env_raises(monkeypatch: pytest.MonkeyPatch) -> None:
    """필수 환경변수 누락 시 RuntimeError 를 발생시키는지 검증."""
    for key in ["FF3_KEY", "FF3_TWEAK", "FF3_ALPHANUMERIC", "FF3_NUMERIC"]:
        monkeypatch.delenv(key, raising=False)

    # log_critical 이 실제 로거를 건드리지 않도록 더미로 패치
    logged: list[str] = []
    monkeypatch.setattr(_mod, "log_critical", lambda msg: logged.append(msg))

    with pytest.raises(RuntimeError) as exc_info:
        _mod.get_cipher()

    msg = str(exc_info.value)
    assert "필수 환경변수(FF3_KEY, FF3_TWEAK, FF3_ALPHANUMERIC, FF3_NUMERIC)가 누락되었습니다." in msg
    assert any("필수 환경변수" in m for m in logged)
