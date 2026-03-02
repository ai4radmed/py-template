# 명세서: `tests/unit/test_conftest.py`

## 역할
- `tests/conftest.py` 의 `pytest_configure` 함수가 GS/ISMS-P 커스텀 마커를 올바르게 등록하는지 검증하는 단위 테스트를 제공한다.

## Public API / 동작 (요약)
- `test_gs_req_marker_registered()`  
  - 더미 `config` 객체를 생성한 뒤 `pytest_configure` 를 호출하고, `"markers"` 섹션에  
    `"gs_req(id): GS 체크리스트 항목 ID. 예: GS-24, GS-31"` 문자열이 추가되었는지 확인한다.
- `test_isms_marker_registered()`  
  - 더미 `config` 객체를 생성한 뒤 `pytest_configure` 를 호출하고, `"markers"` 섹션에  
    `"isms(id): ISMS-P 체크리스트 항목 ID를 명시합니다. 예: ISMS-2.8-54"` 문자열이 추가되었는지 확인한다.

## 핵심 규칙
- 실제 pytest 실행 환경에 의존하지 않고, `pytest.Config` 를 흉내낸 최소한의 더미 객체로 동작을 검증한다.
- 마커 등록 외의 부수 효과(파일 IO, 네트워크 등)는 테스트 대상에 포함하지 않는다.

