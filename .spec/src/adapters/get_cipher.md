# 명세서: `src/adapters/get_cipher.py`

## 역할
- FF3 기반 Format-Preserving Encryption 을 위한 `FF3Cipher` 인스턴스를 생성해 반환하는 팩토리 함수 모듈이다.

## Public API (요약)
- `get_cipher(alphabet_type: str = "alphanumeric")`  
  - `.env` 에서 `FF3_KEY`, `FF3_TWEAK`, `FF3_ALPHANUMERIC`, `FF3_NUMERIC` 값을 읽고, `alphabet_type` 이 `"numeric"` 이면 숫자 알파벳, 그 외에는 영숫자 알파벳을 사용해 `FF3Cipher.withCustomAlphabet(...)` 인스턴스를 생성한다.

## 핵심 규칙
- 네 개의 FF3 관련 환경 변수 중 하나라도 누락되면 치명 로그를 남기고 `RuntimeError` 를 발생시킨다.
- 실제 암복호화는 호출자가 수행하며, 이 모듈은 키/알파벳을 캡슐화한 Cipher 인스턴스 생성에만 책임이 있다.
