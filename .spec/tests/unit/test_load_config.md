# 명세서: `tests/unit/test_load_config.py`

## 역할
- `common.load_config.load_config` 함수가 YAML 설정 파일을 로드하고 `${VAR}` 패턴을 환경 변수 값으로 치환한 뒤, 전체 또는 특정 섹션을 올바르게 반환하는지 검증한다.

## 테스트 범위 (요약)
- 전체 설정 로드:
  - 임시 YAML 파일을 생성하고, `${VAR}` 패턴이 `os.environ` 에 설정된 값으로 치환되는지 확인한다.
- 섹션 단위 로드:
  - `section="app"`, `section="logging"` 등으로 호출 시 해당 최상위 키에 대한 딕셔너리만 반환되는지 검증한다.
  - 존재하지 않는 섹션 이름을 지정하면 빈 딕셔너리 `{}` 를 반환하는지 확인한다.
- 파일 부재 처리:
  - 존재하지 않는 YAML 경로에 대해 `FileNotFoundError` 를 발생시키는지 검증한다.

## 핵심 규칙
- 테스트는 `tmp_path` 를 사용해 실제 파일 시스템 상에 임시 YAML 파일을 생성하고, 절대 경로 기반 로드를 재현한다.
- 환경 변수는 `monkeypatch.setenv` 를 통해 테스트 함수 내에서만 설정하고, pytest 의 fixture 메커니즘을 통해 테스트 간 독립성을 유지한다.

