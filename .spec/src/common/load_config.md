# 명세서: `src/common/load_config.py`

## 역할
- YAML 설정 파일을 UTF-8로 읽고, 내용에 포함된 `${VAR}` 패턴을 환경 변수로 치환해 `dict` 로 반환한다.
- 필요 시 특정 섹션만 잘라서 돌려주며, 로딩/파싱 오류는 로깅 후 예외를 그대로 전파한다.

## Public API (요약)
- `load_config(yml_path: str = "config/deidentification.yml", section: str | None = None) -> dict`  
  - `yml_path` 위치의 YAML을 `yaml.safe_load` 로 읽은 뒤 `common.expand_vars.expand_vars` 로 전체 구조에 대해 환경 변수 치환을 수행한다.
  - `section` 이 주어지면 해당 최상위 키에 해당하는 서브 딕셔너리를, 없으면 전체 설정 딕셔너리를 반환한다.

## 핵심 규칙
- 파일이 없거나 YAML 파싱에 실패하면 `common.logger.log_error` 로 남기고 예외를 다시 던진다.
- 반환값은 항상 `dict` 이며, 존재하지 않는 섹션은 빈 딕셔너리로 취급한다.
- 이 함수는 설정 로드·치환 이상의 부수 효과(예: 전역 상태 변경)는 가지지 않는다.
