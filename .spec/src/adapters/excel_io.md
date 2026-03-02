# 명세서: `src/adapters/excel_io.py`

## 역할
- 지정한 디렉터리에서 엑셀 파일을 일괄 읽어 `dict[str, DataFrame]` 으로 제공하고, 여러 `DataFrame` 을 디렉터리에 일괄 저장하는 유틸리티이다.

## Public API (요약)
- `read_excels(input_dir: str) -> dict[str, pd.DataFrame]`  
  - `input_dir` 하위의 `.xls`/`.xlsx` 파일을 재귀적으로 찾아 모두 읽고, 파일명(예: `"test1.xlsx"`)을 키로 하는 딕셔너리를 반환한다.
- `save_excels(output_dir: str, dataframes_dict: dict[str, pd.DataFrame], prefix: str | None = None) -> None`  
  - `{파일명: DataFrame}` 딕셔너리를 받아, 필요 시 접두사와 확장자 정규화를 적용해 지정 디렉터리에 엑셀 파일로 저장한다.

## 핵심 규칙
- `output_dir` 가 비어 있거나 `dataframes_dict` 가 비어 있으면 저장을 수행하지 않고 로그만 남긴다.
- 파일 저장 시 `.xls` 확장자는 `.xlsx` 로 변환하고, 확장자가 없으면 `.xlsx` 를 붙인다.
- 개별 파일 읽기/쓰기 에러는 로깅하지만, 나머지 파일 처리까지 최대한 계속 진행한다.
- **Python 3.12+ 표준 준수**: `typing.Dict` 대신 내장 `dict`을 사용하고, 임포트를 정렬한다.
