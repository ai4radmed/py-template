# 명세서: `tests/conftest.py`

## 역할
- pytest 전역 설정에서 GS/ISMS-P 기준과 테스트를 연결하기 위한 커스텀 마커(`gs_req`, `isms`) 를 등록한다.

## Public API / 동작 (요약)
- `pytest_configure(config: pytest.Config) -> None`  
  - `config.addinivalue_line("markers", "gs_req(id): ...")` 와 `config.addinivalue_line("markers", "isms(id): ...")` 를 통해 두 마커를 pytest 에 선언한다.

## 핵심 규칙
- 마커 등록 외에 무거운 초기화(파일 IO, 네트워크 등)는 수행하지 않고, 테스트 실행 시 부작용을 최소화한다.
