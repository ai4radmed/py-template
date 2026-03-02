# 명세서: `tests/unit/test_excel_io.py`

## 역할
- `adapters.excel_io.read_excels` 함수가 디렉터리 내 엑셀 파일을 올바르게 읽어 `dict[str, DataFrame]` 을 반환하는지 검증한다.

## 테스트 범위 (요약)
- 임시 디렉터리에 `.xlsx` 와 `.xls` 파일을 생성하고, `read_excels` 호출 결과에 두 파일명이 모두 포함되는지 확인한다.
- 반환된 각 `DataFrame` 이 원본과 동일한지 `pd.testing.assert_frame_equal` 로 비교한다.

## 핵심 규칙
- GS/ISMS-P 마커를 사용해 기능 정확성과 시험 가능 구조를 증적한다.
