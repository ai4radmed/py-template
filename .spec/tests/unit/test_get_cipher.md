# 명세서: `tests/unit/test_get_cipher.py`

## 역할
- `adapters.get_cipher.get_cipher` 함수가 `.env` 에서 FF3 관련 키들을 올바르게 읽어,
  `alphabet_type` 값에 따라 적절한 FF3Cipher 인스턴스를 생성하거나, 필수 값 누락 시 예외를 발생시키는지 검증한다.

## 테스트 범위 (요약)
- 정상 케이스:
  - `.env` 또는 환경변수에 `FF3_KEY`, `FF3_TWEAK`, `FF3_ALPHANUMERIC`, `FF3_NUMERIC` 를 설정한 뒤,
    - `alphabet_type="alphanumeric"` 일 때 `FF3Cipher.withCustomAlphabet(FF3_KEY, FF3_TWEAK, FF3_ALPHANUMERIC)` 이 호출되는지,
    - `alphabet_type="numeric"` 일 때 `FF3Cipher.withCustomAlphabet(FF3_KEY, FF3_TWEAK, FF3_NUMERIC)` 이 호출되는지 모킹 기반으로 검증한다.
- 예외 케이스:
  - 네 개의 FF3 관련 환경 변수 중 하나라도 누락되면 `RuntimeError` 가 발생하고,
    - 에러 메시지가 명세된 텍스트(필수 환경변수 누락 안내)를 포함하는지 확인한다.

## 핵심 규칙
- 테스트는 실제 FF3 암복호화를 수행하지 않고, `FF3Cipher.withCustomAlphabet` 을 모킹하여 호출 인자와 예외 발생 여부만 검증한다.
- 환경 변수는 테스트 내에서 설정/정리하여, 다른 테스트에 영향을 주지 않도록 한다.

