# GS · ISMS-P 테스트 매트릭스 (초안)

본 문서는 `GS인증기준.md` 및 `ISMS-P인증기준.md`의 각 항목을 **자동 테스트/수동 테스트/운영·정책 문서**와 매핑하기 위한 매트릭스 초안이다.  
향후 기준별 세부 설계가 진행되면 이 표를 확장·보완한다.

---

## 1. 컬럼 정의

- **기준 ID**: 공식 기준 번호 또는 내부 ID (예: `GS-07`, `ISMS-2.7-47`).
- **구분**: `GS` 또는 `ISMS-P`.
- **공식 설명 요약**: `GS인증기준.md`, `ISMS-P인증기준.md`에서 발췌한 요약.
- **검증 유형**:
  - `A` = 자동 테스트 (`pytest`)
  - `B` = 수동 테스트 (시나리오/체크리스트)
  - `C` = 운영·정책 문서
- **자동 테스트 ID**: `pytest` 테스트 경로 (`파일경로::테스트이름`).
- **수동 테스트 ID/문서**: 수동 테스트 케이스 ID 또는 문서 경로.
- **운영/정책 문서**: 관련 운영 규정, 정책, 절차서 파일 경로 또는 ID.

---

## 2. 매핑 표 (샘플)

> 아래 예시는 현재 존재하는 자동 테스트(`tests/unit/...`)와 일부 GS/ISMS-P 항목을 연결한 것으로, 전체 기준의 일부만을 시범적으로 매핑한 것이다.

| 기준 ID       | 구분   | 공식 설명 요약                                        | 검증 유형 | 자동 테스트 ID                                                                                     | 수동 테스트 ID/문서 | 운영/정책 문서 |
|--------------|--------|--------------------------------------------------------|-----------|----------------------------------------------------------------------------------------------------|---------------------|----------------|
| GS-07        | GS     | 기능의 정확성: 연산 결과나 데이터 처리가 정확한가?    | A         | `tests/unit/test_excel_io.py::test_read_excels`                                                   | -                   | -              |
| GS-31        | GS     | 시험 가능성: 수정된 기능에 대해 자체 테스트가 가능한가?| A         | `tests/unit/test_expand_vars.py::TestExpandVars::test_expand_vars_complex_structure`            | -                   | -              |
| ISMS-2.7-47  | ISMS-P | 보안 설계 및 구현: 시큐어 코딩 적용 및 보안 기능 구현 | A         | `tests/unit/test_excel_io.py::test_read_excels`                                                   | -                   | -              |
| ISMS-2.7-46  | ISMS-P | 보안 요구사항 정의: 개발 초기 단계 보안 요구사항 명세 | A         | `tests/unit/test_expand_vars.py::TestExpandVars::test_expand_vars_complex_structure`            | -                   | -              |
| ISMS-2.8-54  | ISMS-P | 로그 및 접속기록 관리: 로그 생성, 보관 및 위·변조 방지 | A/C       | `tests/unit/test_setup_log_dir.py::test_resolve_log_path_project_name_replaced`                 | -                   | `documents/LOGGING_POLICY.md` |
| GS-29        | GS     | 분석성: 오류 발생 시 원인 파악을 위한 진단 로그 충분 제공 | A/C       | `tests/unit/test_setup_log_dir.py::test_resolve_log_path_project_name_replaced`                 | -                   | `documents/LOGGING_POLICY.md` |

---

## 3. 확장 지침

1. **새로운 테스트가 GS/ISMS-P 기준을 충족하는 경우**
   - 테스트 코드에 적절한 `@pytest.mark.gs_req(...)`, `@pytest.mark.isms(...)` 마커를 부여한다.
   - 이 매트릭스 표에 해당 기준 ID 행을 추가하거나, 기존 행의 **자동 테스트 ID** 컬럼에 테스트 경로를 추가한다.

2. **수동 테스트 또는 운영 문서가 기준을 충족하는 경우**
   - 수동 테스트 문서(`documents/TEST_CASES/*.md` 등)에 기준 ID를 명시한다.
   - 본 매트릭스의 **수동 테스트 ID/문서** 또는 **운영/정책 문서** 컬럼에 해당 경로/ID를 기록한다.

3. **여러 기준을 동시에 충족하는 테스트**
   - 하나의 테스트가 여러 기준 ID로 마킹될 수 있으며, 이 경우 각 기준 행의 **자동 테스트 ID** 컬럼에 동일한 테스트 경로를 중복 기재한다.

본 매트릭스는 GS 및 ISMS-P 심사 시, “각 기준 항목이 어떤 테스트/문서에 의해 입증되는지”를 한눈에 보여주는 핵심 자료로 활용된다.

