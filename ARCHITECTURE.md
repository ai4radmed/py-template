# py-template 아키텍처 개요

이 문서는 나와 다른 개발자들의 이해를 돕기 위한 아키텍처 설명서입니다.
왜 이런 구조와 스크립트를 선택했는지, 유지보수 관점에서 이해하는 데 초점을 둡니다.

## 1. 기술 스택과 도구

- **Python 버전**: 3.12+
- **의존성·가상환경 관리**: [uv](https://github.com/astral-sh/uv)
  - `pyproject.toml` + `uv.lock` 기반
  - 일반적인 흐름: `uv venv .venv` → `uv sync` → `uv run ...`
- **코드 품질**: [ruff](https://docs.astral.sh/ruff/) (lint + format), [mypy](https://mypy-lang.org/) (정적 타입 검사)
- **커밋 전 검사**: [pre-commit](https://pre-commit.com/) — ruff + mypy 자동 실행
- **테스트**: [pytest](https://docs.pytest.org/) + [pytest-html](https://pypi.org/project/pytest-html/) + [pytest-cov](https://pypi.org/project/pytest-cov/) + [allure-pytest](https://pypi.org/project/allure-pytest/)
- **CI/CD**: GitHub Actions (멀티 OS 매트릭스, 산출물 Artifacts 업로드)

## 2. 코드 구조와 패키지 (Level 3 구현 뼈대)

### 2.1 패키징 설정
- `pyproject.toml` 에서 `src` 레이아웃을 사용합니다.
  ```toml
  [tool.setuptools]
  package-dir = {"" = "src"}

  [tool.setuptools.packages.find]
  where = ["src"]
  ```
  - 루트 패키지는 항상 `src/` 아래에서만 검색됩니다.

### 2.2 공용 유틸 패키지: `src/common/`
- **역할**: 애플리케이션 전역에서 재사용되는 순수 Python 유틸리티 모듈 모음.
- **구성 파일 (→ 1:1 명세서 매핑)**
  - `src/common/logger.py` ↔ `.spec/src/common/logger.md`  
    - `.env` + `config/logging.yml` 기반 로깅 초기화, 프로젝트 공용 로거, 감사 로그(`audit_log`) 제공.
  - `src/common/load_config.py` ↔ `.spec/src/common/load_config.md`  
    - YAML 파일 로드 + `${VAR}` 환경 변수 치환 후 `dict` 반환.
  - `src/common/expand_vars.py` ↔ `.spec/src/common/expand_vars.md`  
    - 문자열/딕셔너리/리스트 안의 `${VAR}` 패턴을 재귀적으로 치환.
  - `src/common/__init__.py` ↔ `.spec/src/common/__init__.md`  
    - `common` 네임스페이스 정의, 임포트 시 부수 효과 없음.

### 2.3 어댑터 패키지: `src/adapters/`
- **역할**: 외부 시스템(데이터베이스, 파일, 암호화 등) 연동 모듈 모음.
- **구성 파일 (→ 1:1 명세서 매핑)**
  - `src/adapters/__init__.py` ↔ `.spec/src/adapters/__init__.md`  
    - `adapters` 네임스페이스 정의, 자체 부수 효과 없음.
  - `src/adapters/database.py` ↔ `.spec/src/adapters/database.md`  
    - `.env` 기반 PostgreSQL 커넥션/쿼리/배치 실행 헬퍼. extra `py-template[db]` 필요.
  - `src/adapters/excel_io.py` ↔ `.spec/src/adapters/excel_io.md`  
    - 디렉터리 단위 엑셀 읽기/쓰기 유틸. extra `py-template[excel]` 필요.
  - `src/adapters/get_cipher.py` ↔ `.spec/src/adapters/get_cipher.md`  
    - FF3 Format-Preserving Encryption Cipher 생성. extra `py-template[cipher]` 필요.

### 2.4 의존성 그룹
- **핵심(core)**: `python-dotenv`, `pyyaml`
- **선택적**:
  - `db`: `psycopg2`
  - `excel`: `pandas`, `openpyxl`
  - `cipher`: `ff3`
- **개발(dev)**: `pytest`, `pytest-html`, `pytest-cov`, `allure-pytest`, `ruff`, `mypy`, `pre-commit`

## 3. 설정과 로깅

- **환경 변수**
  - `.env.example` → `.env` 복사 후 수정.
  - `python-dotenv`를 사용하여 애플리케이션 시작 시 자동 로드하는 패턴을 사용합니다.

- **로깅**
  - `config/logging.yml` 기반 설정.
  - `.env`의 `PROJECT_NAME`, `LOG_PATH`, `LOG_LEVEL` 등에 따라 동작이 달라집니다.
  - 콘솔/파일 분리, 서비스 로그와 audit 로그 분리, JSON 포맷 등의 정책을 포함합니다.
  - 환경변수 확장은 `common.expand_vars` 모듈에 위임 (중복 제거).

- **보안 및 규제 준수 로깅 (Audit Log)** 
  - 본 프로젝트는 개인정보 보호법 및 안전성 확보조치 기준에 따라 엄격한 감사 로그 정책을 적용합니다.
  - 로그 파일 관리 및 법적 필수 기재 항목(JSON 스키마), 마스킹 등에 대한 철학은 `documents/LOGGING_POLICY.md` 문서를 기준 삼아 반드시 준수하십시오.

## 4. setup 스크립트와 Makefile의 역할 (Level 3 유틸 + Level 2 명세서)

`scripts/setup/`와 `Makefile`은 **개발 편의를 위한 자동화 스크립트 모음**이며, 각 스크립트는 별도 명세서(`.spec/scripts/...`)로 정의됩니다.

### 4.1 setup 스크립트 (코드 ↔ 명세서 매핑)
- `scripts/setup/setup_env.py` ↔ `.spec/scripts/setup/setup_env.md`  
  - `.env.example` 을 `.env` 로 복사하고, `PROJECT_NAME`/`PROJECT_ROOT`/OS 별 기본 `LOG_PATH` 를 자동 치환하는 편의 스크립트.
  - 표준 패턴(수동 복사) 위에 올라가는 **선택적** 도구.
- `scripts/setup/setup_log_dir.py` ↔ `.spec/scripts/setup/setup_log_dir.md`  
  - `.env` 의 `LOG_PATH` 를 해석해 로그 디렉터리를 생성하고, (비 Windows) 소유자/권한을 설정.
  - `common.logger` 는 디렉터리를 생성하지 않고, 이 스크립트에 생성 책임을 위임.

### 4.2 Makefile 주요 타깃
- `env` — `.env` 생성/초기화 (`scripts/setup/setup_env.py` 활용 가능)
- `logs` — 로그 디렉터리 생성 (`scripts/setup/setup_log_dir.py`)
- `setup` — env + logs 일괄 실행
- `test` — pytest 실행
- `lint` — ruff check 실행
- `format` — ruff format 실행
- `typecheck` — mypy 실행
- `report` — GS 인증 산출물 생성 (HTML 리포트, 커버리지, Allure, JUnit)
- `update` — 템플릿 업데이트

## 5. 개발자용 권장 워크플로우

1. 리포지토리 클론
2. 프로젝트 루트에서 (사전 조건: 시스템에 `pyproject.toml` 의 `requires-python` 에 맞는 Python 버전이 설치되어 있어야 합니다. 필요하다면 `uv python install <버전>` 으로 먼저 설치하십시오):
   - `uv sync --group dev --extra all`
     - `.venv` 가 없다면 자동으로 생성되고, 의존성까지 한 번에 설치됩니다.
2-1. (IDE에서 가상환경 활성화 - 권장)
   - AntiGravity, Cursor IDE 등에서 Python 확장(예: VS Code Python Extension)을 설치합니다.
   - 명령 팔레트에서 `Python: Select Interpreter` 를 실행하고, 현재 프로젝트의 `.venv` 인터프리터를 선택합니다.
   - 이후 IDE에서 **새 터미널을 생성**하면 선택한 가상환경이 자동으로 반영된 셸이 열립니다.
3. `.env` 생성:
   - `.env.example`를 복사하거나, 필요 시 `make env` 사용
4. 로그 디렉터리 생성:
   - `make logs` (또는 직접 디렉터리 생성)
5. 코드 작성 시:
   - 공용 유틸/도메인 독립 모듈은 `src/common/` 아래에 추가
   - 외부 시스템 연동 모듈은 `src/adapters/` 아래에 추가
   - 임포트는 `common.xxx` 또는 `adapters.xxx` 형태로 패키지 기준으로 작성
6. 코드 품질:
   - `make lint` — 린트 검사
   - `make format` — 자동 포매팅
   - `make typecheck` — 타입 검사
   - `make test` — 테스트 실행
   - `make report` — GS 인증 산출물 생성

## 6. 테스트 구조 및 GS 인증 대응 (코드 ↔ Spec ↔ 요구사항)

### 6.1 테스트 디렉터리 구조
- `tests/unit/` — 개별 함수/클래스 단위 테스트 (빠른 실행)
- `tests/integration/` — 모듈 간 연동 테스트 (DB, 파일 등 외부 자원)
- `tests/e2e/` — 종단 간 테스트 (실제 사용자 시나리오)

### 6.2 테스트 레벨 명세서 매핑
- `tests/conftest.py` ↔ `.spec/tests/conftest.md`  
  - pytest 전역에서 `gs_req`, `isms` 마커를 등록.
- `tests/unit/test_expand_vars.py` ↔ `.spec/tests/unit/test_expand_vars.md`  
  - `common.expand_vars.expand_vars` 의 문자열/컬렉션/복합 구조/기타 타입 처리와 불변성을 검증.
- `tests/unit/test_excel_io.py` ↔ `.spec/tests/unit/test_excel_io.md`  
  - `adapters.excel_io.read_excels` 가 디렉터리 내 엑셀 파일을 정확히 읽어들이는지 검증.
- `tests/unit/test_setup_log_dir.py` ↔ `.spec/tests/unit/test_setup_log_dir.md`  
  - `resolve_log_path_from_env` 의 `{PROJECT_NAME}`/`$HOME`/`%USERPROFILE%` 치환 규칙을 검증.

### 6.3 GS/ISMS-P 마커와 산출물
- **GS/ISMS-P 마커**
  - `@pytest.mark.gs_req("GS-07")`, `@pytest.mark.gs_req("GS-29")`, `@pytest.mark.gs_req("GS-31")` 등으로 테스트와 체크리스트 항목을 매핑.
  - `@pytest.mark.isms("ISMS-2.7-46")`, `@pytest.mark.isms("ISMS-2.7-47")`, `@pytest.mark.isms("ISMS-2.8-54")` 등으로 ISMS-P 요구사항과 연계.
- **산출물 생성** (`make report`)
  - `reports/test_report.html` — pytest-html 테스트 결과 보고서
  - `reports/coverage/` — 라인 단위 코드 커버리지 (HTML)
  - `reports/junit.xml` — JUnit XML (CI 연동)
  - `reports/allure-results/` — Allure 대시보드 데이터

- **CI/CD** (`.github/workflows/ci.yml`)
  - lint → typecheck → 멀티 OS 테스트 → 산출물 Artifacts 업로드
  - GS 인증 "호환성/이식성" 증명을 위해 ubuntu + windows 매트릭스 실행

## 7. AI 에이전트와의 협업 가이드 (AI-Native Spec-Driven Development)

본 프로젝트는 AI의 역량을 극대화하기 위해 **AI-Native Spec-Driven Development (AI 네이티브 명세 주도 개발)** 방법론을 채택하고 있습니다. AI 에이전트(Cursor, Windsurf 등)는 본 지침을 최우선으로 준수해야 합니다.

### 7.1. 기본 원칙
- **uv 기반 Python 워크플로우**: 가상환경과 의존성 관리는 `pyproject.toml` + `uv.lock`을 기준으로 하며, `uv run`, `uv sync`를 사용합니다.
- **src 레이아웃**: 애플리케이션 코드는 `src/` 아래에 두며, `sys.path`나 `.pth`를 수정하는 방식은 지양합니다. 공용 로직은 `src/common`을, 외부 시스템 연동은 `src/adapters`를 활용합니다.
- **로깅·보안·테스트**:
  - 로깅/개인정보/감사 정책은 **`documents/LOGGING_POLICY.md`**를 최우선으로 따릅니다.
  - 테스트는 `pytest` 기반, 코드 품질은 `ruff` 및 `mypy`를 기본으로 간주합니다. 존재하는 `Makefile` 타깃(`make test`, `make lint` 등)을 존중합니다.
- **단일 진실 공급원(SSOT)**: 새로운 보안/컴플라이언스 정책 제안 시, 원본 마크다운을 `documents/`에 작성하고 프롬프트 규칙 파일(`.cursor/rules/*.mdc`)에서 이를 참조하게 합니다.

### 7.2. 명세의 계층 구조 (Specification Hierarchy)
AI는 다음 **파일 기반 3단계 명세 구조**를 이해하고 코드를 작성/검증합니다.

- **Level 1: 프로젝트 맵 (`ARCHITECTURE.md`)**  
  - (본 문서) 전체 시스템의 디렉터리 구조, 도메인별 책임, 코드 ↔ Spec 매핑, 핵심 규칙을 제공하는 상위 설계 문서.

- **Level 2: 개별 파일 명세서 (`.spec/` 폴더)**  
  - 각 구현 파일과 1:1 로 매핑되는 짧은 명세서.
  - 예시:
    - `src/common/logger.py` ↔ `.spec/src/common/logger.md`
    - `src/adapters/database.py` ↔ `.spec/src/adapters/database.md`
    - `scripts/setup/setup_log_dir.py` ↔ `.spec/scripts/setup/setup_log_dir.md`
    - `tests/unit/test_expand_vars.py` ↔ `.spec/tests/unit/test_expand_vars.md`
  - 각 명세서는 **역할 + Public API 요약 + 핵심 규칙 3~5줄** 만을 포함하여, AI 가 구현·수정 시 헷갈리지 않을 최소 정보를 제공한다.

- **Level 3: 구현체 (`src/`, `scripts/`, `tests/` 폴더)**  
  - Level 2 명세서를 바탕으로 작성된 실제 Python 코드와 테스트.
  - 코드는 항상 대응하는 명세서를 기준으로 변경해야 하며, 명세와 코드가 불일치하면 명세서를 우선 갱신한 뒤 코드를 수정한다.

### 7.3. 핵심 워크플로우 (Plan - Manifest - Execute - Verify)
1. **Plan**: 구현 기능 정의 후, AI에게 타겟 파일 목록과 명세(Spec) 초안을 요청
2. **Manifest**: 출력된 명세를 `.spec/` 디렉터리에 버전 관리 대상으로 저장
3. **Execute**: AI(에이전트)에게 특정 `.spec` 파일을 읽고 `src/` 하위에 코드를 구현하도록 명령
4. **Verify**: `make lint`, `make test` 등의 스크립트를 통한 명세 준수 강제 검증

### 7.5. AI 코드 생성 스타일 및 테스트 규칙
- **언어/주석 스타일**:  
  - 본 프로젝트의 기본 언어는 한국어입니다.  
  - 모듈/함수의 docstring, 주석, 사용자 메시지는 가능한 한 한국어로 작성합니다(외부 라이브러리 이름·공식 용어 등은 예외).
- **구현 + 테스트 동시 생성**:  
  - AI가 새 Level 3 파일(예: `src/...`, `scripts/...`)을 생성하거나 큰 기능을 추가할 때는, **항상 해당 기능을 검증하는 테스트 파일/테스트 케이스를 함께 생성**해야 합니다.  
  - 가능하면 테스트에도 대응하는 명세서(`.spec/tests/...`) 을 함께 추가합니다.

### 7.4. 대규모 확장을 위한 AI 아키텍처 원칙
1. **기능 단위 통합 테스트 명세화 (Test-Driven E2E Specs)**: 단위 파일 외에 사용자 시나리오 단위 검증 명세(`specs/features/`)를 작성해 AI가 종단 간(E2E) 테스트 코드를 자동 생성하게 유도.
2. **CI/CD "AI Agentic Reviewer"**: PR 단계에 검열용 분리 AI 에이전트를 도입하여 구현 코드와 기존 `.spec`의 일치 여부를 상호 검증하는 파이프라인 지향.
3. **컴포넌트 단위 패키지화 (Monorepo)**: 거대한 `src/` 대신, 도메인별 독립적인 패키지(예: `core`, `database`)로 분리하여 환각과 의존성 혼선을 방지.
4. **옵저버빌리티(Observability) 및 자가 치유(Self-Healing)**: 모든 명세는 에러 로그, Trace ID 등을 강제하여, 프로덕션 버그 발생 시 에이전트가 단일 `.spec`과 추적 로그로 원인을 파악해 수정한 뒤 Verify로 돌아가는 닫힌 루프(Self-Healing Loop)를 구성.
