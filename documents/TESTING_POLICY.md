# 테스트 및 컴플라이언스 정책 (Testing & Compliance Policy)

본 테스트 정책은 본 프로젝트의 **자동/수동 테스트**와 `GS인증기준.md`, `ISMS-P인증기준.md` 간의 **1:1 매핑**을 가능하게 하여, 테스트 결과가 그대로 **GS·ISMS-P 심사 제출용 증적**으로 활용될 수 있도록 하는 것을 목표로 한다.

---

## 1. 목적 및 우선순위

1. **[1순위] 규제 및 인증 기준 충족**
   - `GS인증기준.md`의 34개 항목과 `ISMS-P인증기준.md`의 102개 항목 중, **애플리케이션 및 코드로 직접 검증 가능한 항목**에 대해 테스트를 통해 증적을 확보한다.
2. **[2순위] 회귀 테스트 및 품질 확보**
   - 기능 변경 시 GS/ISMS-P 관련 테스트가 자동으로 재실행되어, 인증 관점의 퇴행(regression)이 조기에 탐지되도록 한다.
3. **[3순위] AI-Driven IDE 친화성**
   - `pytest` 커스텀 마커(`gs_req`, `isms`)와 명시적인 매핑 문서(`GS_ISMS_TEST_MATRIX.md`)를 통해, 개발자가 기준 번호를 외우지 않고도 **자동완성 기반으로 기준을 검색·연결**할 수 있게 한다.

---

## 2. 적용 범위

- **포함(테스트로 직접 검증)**:
  - GS 기준 중 기능 적합성, 성능 효율성, 호환성, 신뢰성, 보안성, 유지보수성, 이식성 등 **소프트웨어 동작으로 입증 가능한 항목**.
  - ISMS-P 기준 중 **인증·권한관리(2.4), 접근통제(2.5), 암호화 적용(2.6), 개발 보안(2.7), 시스템 및 서비스 운영관리 일부(2.8), 로그·사고 대응 일부(2.10)** 등.
- **제외(운영·관리체계 문서로 관리)**:
  - ISMS-P 제1장(관리체계 수립 및 운영), 인적/외부자/물리 보안, 교육·정책·보고·점검 등은 운영 규정, 절차서, 회의록, 교육 이수 기록 등 **별도 운영 문서**로 관리하며, 자동/수동 테스트의 직접 대상에서 제외한다.

---

## 3. 검증 방식 분류

각 기준 항목은 아래 세 가지 검증 방식 중 하나 이상에 매핑된다.

1. **자동 테스트 (Automated Test, 타입 A)**
   - `pytest` 기반 유닛/통합/E2E 테스트.
   - CI 파이프라인에서 항상 실행되며, 실패 시 기준 미충족 가능성을 의미한다.
2. **수동 테스트 (Manual Test, 타입 B)**
   - 운영 또는 QA에서 수행하는 시나리오 기반 테스트.
   - `documents/TEST_CASES/*.md` 등으로 정의하며, 수행 결과(스크린샷, 로그 캡처 등)를 증적으로 남긴다.
3. **운영/정책 문서 (Policy / Process Evidence, 타입 C)**
   - 보안 정책, 운영 매뉴얼, 백업·복구 절차, 교육 계획, 점검 보고서 등 **비코드 증적**으로만 충족되는 항목.
   - 예: 경영진 보고, 관리체계 점검, 인력 보안 교육 등.

`GS_ISMS_TEST_MATRIX.md` 파일에서 각 기준 항목에 대해 A/B/C 중 어떤 방식을 사용하는지 명시한다.

---

## 4. 테스트와 기준 매핑 방식

> **태그(마커)를 어떻게 실행·활용하는지**는 **`documents/TAG_USAGE_GUIDE.md`**에서 요약합니다.

### 4.1 pytest 마커 규칙

`tests/conftest.py`에는 다음과 같은 커스텀 마커가 정의되어 있다.

- `@pytest.mark.gs_req("GS-07")`
  - GS 체크리스트 항목 ID. 구분(카테고리)은 `documents/GS인증기준.md`에서 항목으로 조회.
- `@pytest.mark.isms("ISMS-2.8-54")`
  - ISMS-P 체크리스트 항목 ID를 명시.
- `@pytest.mark.local_only`
  - 로컬에서만 실행. CI에서는 `pytest -m "not local_only"`로 제외. GS/ISMS-P 심사용 전체 테스트·리포트는 로컬에서 `make report`로 수행 시 포함된다.

**원칙**:

- “이 테스트가 없으면 해당 GS/ISMS-P 항목을 설득력 있게 설명하기 어렵다” 수준의 테스트에만 기준 마커를 부여한다.
- 순수 기술 유닛 테스트(도우미 유틸 등)는 필요 시에만 기준과 연결하고, 기본적으로는 품질 확보용으로만 유지할 수 있다.

### 4.2 테스트 예시 (기존 테스트와의 통합)

- `tests/unit/test_excel_io.py::test_read_excels`
  - `@pytest.mark.gs_req("GS-07")` / `@pytest.mark.gs_category("기능 적합성")`
  - `@pytest.mark.isms("ISMS-2.7-47")`
  - 의미: “엑셀 I/O 기능이 명세대로 동작하며, 시스템이 시험 가능한 구조로 설계되어 있다”는 것을 GS 기능 적합성 및 ISMS-P 개발 보안 기준의 증적 중 하나로 사용.

- `tests/unit/test_expand_vars.py::TestExpandVars::test_expand_vars_complex_structure`
  - `@pytest.mark.gs_req("GS-31")` / `@pytest.mark.gs_category("유지보수성")`
  - `@pytest.mark.isms("ISMS-2.7-46")`
  - 의미: “환경 기반 설정(expand_vars)을 통해 테스트 가능하고 유지보수하기 쉬운 구조를 확보했다”는 것을 GS 시험 가능성 및 ISMS-P 보안 요구사항 정의의 증적 중 하나로 사용.

---

## 5. GS/ISMS-P 매트릭스 문서 (`GS_ISMS_TEST_MATRIX.md`)

`GS_ISMS_TEST_MATRIX.md`는 다음 정보를 포함하는 단일 진실 공급원(Single Source of Truth)이다.

- 기준 ID (예: `GS-07`, `ISMS-2.8-54`)
- 기준 구분 (GS / ISMS-P)
- 공식 설명 요약
- 검증 유형 (A=자동, B=수동, C=운영/정책 문서)
- 자동 테스트 ID 목록 (예: `tests/unit/test_excel_io.py::test_read_excels`)
- 수동 테스트 ID 또는 문서 경로
- 운영/정책 문서 ID 또는 파일 경로

테스트 코드의 pytest 마커와 매트릭스의 기준 ID를 **동일한 문자열로 유지**하여, 양방향 탐색(기준 → 테스트, 테스트 → 기준)이 가능하도록 한다.

---

## 6. 제출용 산출물 구성

GS 및 ISMS-P 심사 시, 본 정책에 따라 다음 파일들이 제출용 핵심 산출물이 된다.

- `documents/LOGGING_POLICY.md`
- `documents/TESTING_POLICY.md`
- `documents/GS인증기준.md`
- `documents/ISMS-P인증기준.md`
- `documents/GS_ISMS_TEST_MATRIX.md`
- `tests/` 디렉터리 (자동 테스트 구현체)
- `documents/TEST_CASES/*.md` (필요 시 추가될 수동 테스트 정의)
- 관련 운영·정책 문서 (`documents/OPERATION_POLICIES/*.md` 등, 필요 시 확장)

이 구성을 통해, **기존 자동 테스트와 GS/ISMS-P 기준이 하나의 일관된 정책과 매트릭스로 연결**되며, 테스트 실행 결과가 곧 컴플라이언스 증적이 되는 구조를 지향한다.

---

## 7. 테스트 실행과 리포트 생성 (업계표준 분리)

**원칙**: “테스트 실행”과 “테스트 결과(리포트) 생성”은 개념적으로 분리하며, 필요에 따라 동일 실행에서 함께 수행하거나 별도 타깃/단계로 수행한다.

### 7.1 로컬 vs CI 구분

| 구분 | 테스트 범위 | 리포트 | 용도 |
|------|-------------|--------|------|
| **CI** | `pytest -m "not local_only"` | 동일 실행 시 생성 | PR/푸시 검증, 빠른 피드백 |
| **로컬 일상** | `make test` (전체) 또는 `make test-fast` (CI와 동일) | 없음 | 개발 중 회귀 확인 |
| **로컬 GS/ISMS-P 대응** | `make report` 또는 `make report-audit` (전체, local_only 포함) | 생성 | 심사 제출용 증적 수집 |

### 7.2 Makefile 타깃

- **`make test`**  
  테스트만 실행(리포트 없음). 전체 테스트(local_only 포함). 로컬에서 빠르게 확인할 때 사용.
- **`make test-fast`**  
  CI와 동일한 테스트 세트(local_only 제외). 리포트 없음. 머지 전 로컬 검증용.
- **`make report`**  
  **테스트 실행 + 리포트 생성**을 한 번에 수행. 전체 테스트(local_only 포함)를 실행하고, `reports/` 아래에 HTML·JUnit·Allure·coverage 산출물을 생성. **GS/ISMS-P 심사용 증적**으로 사용.
- **`make report-audit`**  
  `make report`와 동일. “심사용 전체 테스트·리포트”임을 명시한 별칭.

### 7.3 정리

- **테스트 실행**: `make test` / `make test-fast` 또는 `uv run pytest [옵션]` — 결과는 터미널에만 출력.
- **리포트 생성**: 테스트를 다시 실행하면서 `--html`, `--junitxml`, `--alluredir`, `--cov-report` 등으로 산출물을 만드는 단계. 로컬에서는 **`make report`(또는 `make report-audit`) 한 번**으로 “전체 테스트 + 심사용 리포트”를 수행한다.
- CI에서는 “테스트 실행”과 “리포트 생성”을 **같은 job에서 한 번에** 수행하되, `local_only` 테스트는 제외하여 시간을 제한한다. 로컬에서 심사용 증적이 필요할 때만 **전체(local_only 포함) + 리포트**를 `make report`로 수행하면 된다.

