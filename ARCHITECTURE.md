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

## 2. 코드 구조와 패키지

- `pyproject.toml`의 패키지 관련 설정
  - 빌드 백엔드로 `setuptools`를 사용하며, 다음 설정을 통해 `src` 하위 폴더들을 패키지로 인식시킵니다.

    ```toml
    [tool.setuptools]
    package-dir = {"" = "src"}

    [tool.setuptools.packages.find]
    where = ["src"]
    ```

  - `package-dir = {"" = "src"}`
    → "프로젝트의 루트 패키지 위치는 `src` 디렉터리 안이다"라는 의미입니다.
  - `packages.find.where = ["src"]`
    → `setuptools`가 패키지를 찾을 때 **`src` 아래에서만** 검색하도록 지정합니다.

- **`src/common/`** — 핵심 유틸리티 (외부 의존성 없음, 순수 Python + dotenv/pyyaml)
  - `common.logger` — 로깅 설정/헬퍼
  - `common.load_config` — YAML 설정 파일 로드 + 환경변수 치환
  - `common.substitute` — 문자열/컬렉션 내 환경변수 치환

- **`src/adapters/`** — 외부 시스템 연동 (선택적 의존성 필요)
  - `adapters.database` — PostgreSQL 연결 및 쿼리 유틸 (`pip install py-template[db]`)
  - `adapters.excel_io` — 엑셀 입출력 유틸 (`pip install py-template[excel]`)
  - `adapters.get_cipher` — FF3 기반 암호화 유틸 (`pip install py-template[cipher]`)

- **의존성 분리**
  - 핵심(core): `python-dotenv`, `pyyaml`
  - 선택적: `db` (psycopg2), `excel` (pandas, openpyxl), `cipher` (ff3)
  - 개발: `pytest`, `pytest-html`, `pytest-cov`, `allure-pytest`, `ruff`, `mypy`, `pre-commit` (`[dependency-groups] dev`)

## 3. 설정과 로깅

- **환경 변수**
  - `.env.example` → `.env` 복사 후 수정.
  - `python-dotenv`를 사용하여 애플리케이션 시작 시 자동 로드하는 패턴을 사용합니다.

- **로깅**
  - `config/logging.yml` 기반 설정.
  - `.env`의 `PROJECT_NAME`, `LOG_PATH`, `LOG_LEVEL` 등에 따라 동작이 달라집니다.
  - 콘솔/파일 분리, 서비스 로그와 audit 로그 분리, JSON 포맷 등의 정책을 포함합니다.
  - 환경변수 치환은 `common.substitute` 모듈에 위임 (중복 제거).

- **보안 및 규제 준수 로깅 (Audit Log)** 
  - 본 프로젝트는 개인정보 보호법 및 안전성 확보조치 기준에 따라 엄격한 감사 로그 정책을 적용합니다.
  - 로그 파일 관리 및 법적 필수 기재 항목(JSON 스키마), 마스킹 등에 대한 철학은 `documents/LOGGING_POLICY.md` 문서를 기준 삼아 반드시 준수하십시오.

## 4. setup 스크립트와 Makefile의 역할

`scripts/setup/`와 `Makefile`은 **개발 편의를 위한 자동화 스크립트 모음**입니다.

- 주요 스크립트
  - `scripts/setup/setup_env.py` — `.env` 생성/초기화
  - `scripts/setup/setup_pyenv.py` — pyenv 설정
  - `scripts/setup/create_logs.py` — 로그 디렉터리 및 파일 생성
  - `scripts/setup/backup.py` / `restore_backup.py` — 설정/환경 백업 및 복원
  - `scripts/setup/update.py` — 템플릿 업데이트 (src/ 전체 복사)

- `Makefile` 주요 타깃
  - `env` — `.env` 생성/초기화
  - `logs` — 로그 디렉터리 생성
  - `setup` — env + logs 일괄 실행
  - `backup` / `restore` — 백업/복원
  - `test` — pytest 실행
  - `lint` — ruff check 실행
  - `format` — ruff format 실행
  - `typecheck` — mypy 실행
  - `report` — GS 인증 산출물 생성 (HTML 리포트, 커버리지, Allure, JUnit)
  - `update` — 템플릿 업데이트

## 5. 개발자용 권장 워크플로우

1. 리포지토리 클론
2. 프로젝트 루트에서:
   - `uv venv .venv`
   - `source .venv/bin/activate`
   - `uv sync --group dev --extra all`
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

## 6. 테스트 구조 및 GS 인증 대응

- **테스트 디렉터리**
  - `tests/unit/` — 개별 함수/클래스 단위 테스트 (빠른 실행)
  - `tests/integration/` — 모듈 간 연동 테스트 (DB, 파일 등 외부 자원)
  - `tests/e2e/` — 종단 간 테스트 (실제 사용자 시나리오)

- **GS 인증 마커**: pytest custom marker로 테스트와 인증 요구사항을 매핑
  - `@pytest.mark.gs_req("REQ-XXX-NNN")` — 요구사항 ID
  - `@pytest.mark.gs_category("보안성")` — 평가 항목

- **산출물 생성** (`make report`)
  - `reports/test_report.html` — pytest-html 테스트 결과 보고서
  - `reports/coverage/` — 라인 단위 코드 커버리지 (HTML)
  - `reports/junit.xml` — JUnit XML (CI 연동)
  - `reports/allure-results/` — Allure 대시보드 데이터

- **CI/CD** (`.github/workflows/ci.yml`)
  - lint → typecheck → 멀티 OS 테스트 → 산출물 Artifacts 업로드
  - GS 인증 "호환성/이식성" 증명을 위해 ubuntu + windows 매트릭스 실행

## 7. AI 에이전트와의 협업 시 참고

- AI 에이전트는 `.cursor/rules/entry.mdc`를 포함한 설정된 규칙들을 기반으로 동작합니다.
- 새로운 스크립트나 구조 변경을 제안할 때:
  - 먼저 이 `ARCHITECTURE.md`와 `README.md`를 읽고,
  - uv 기반 워크플로우와 `src/common` + `src/adapters` 패키지 구조를 해치지 않는 방향으로 설계하는 것을 원칙으로 합니다.
- **[문서화 패턴] 새로운 정책(보안, 컴플라이언스 등)을 정의할 때:** AI와 개발자 간의 문서 이원화(동기화 지옥)를 막기 위해, 원본 마크다운(SSOT)은 `documents/` 아래에 작성하고 `.cursor/rules/*.mdc` 파일에서는 해당 원본을 링크(참조)하는 방식만을 사용하십시오.
