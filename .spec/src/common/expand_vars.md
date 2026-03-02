# 명세서: `src/common/expand_vars.py`

## 역할
- 문자열, 딕셔너리, 리스트 등 설정 구조 안의 `${VAR}` 패턴을 현재 프로세스의 `os.environ` 값으로 재귀적으로 치환한다.
- 환경 변수 기반 설정을 단순하고 일관되게 적용하기 위한 공용 유틸리티이다.

## Public API (요약)
- `expand_vars_str(value: str) -> str`  
  - 단일 문자열에서 `${KEY}` 패턴을 `os.environ["KEY"]` 값으로 치환한다(없는 키는 그대로 둔다).
- `expand_vars(value: str | dict | list | Any) -> str | dict | list | Any`  
  - `str` 은 `expand_vars_str` 로, `dict`/`list` 는 재귀적으로 각 값에 대해 호출하고, 그 외 타입은 그대로 반환한다.

## 핵심 규칙
- 비문자열 타입(int, float, bool, None 등)은 변경하지 않고 그대로 반환한다.
- 딕셔너리/리스트 입력에 대해서는 새 객체를 만들어 반환하여 원본 데이터를 변경하지 않는다(불변성 보장).
- 치환 규칙은 단순한 문자열 `replace` 기반으로, 정의되지 않은 `${VAR}` 은 에러 없이 그대로 남겨 둔다.
