# py-template AI Context

이 문서는 **AI 에이전트(Cursor, Antigravity 등)**가 이 프로젝트에서 작업을 시작하기 전에 읽어야 할 공통 가이드입니다.  
세부 정책은 별도 문서로 분리하고, 여기서는 핵심 원칙과 링크만 제공합니다.

## 1. 기본 철학

- **uv 기반 Python 프로젝트**
  - 가상환경과 의존성 관리는 `pyproject.toml` + `uv.lock` + `uv sync`를 기준으로 합니다.
  - 실행 예시는 `uv run python -m 패키지.모듈`, `uv run pytest` 와 같은 형태를 우선 사용합니다.

- **src 레이아웃 + 패키지 임포트**
  - 애플리케이션 코드는 `src/` 아래에 둡니다.
  - 공용 유틸리티는 `src/common/` 패키지로 제공되며, 어디에서든 `import common.logger` 처럼 패키지 임포트를 사용합니다.
  - `sys.path`를 직접 수정하거나 `.pth` 파일을 생성하는 방식을 새로 도입하지 마십시오.

## 2. 코드 구조와 의존성 (요약)

- **코드 구조**
  - `src/common/` — 핵심 유틸리티 (logger, expand_vars, load_config, database, excel_io, get_cipher 등)
  - `scripts/setup/` — 환경 설정, 로그 디렉터리 생성 등 스크립트
  - `config/logging.yml` — 로깅 설정
  - `tests/` — 단위 테스트 등

- **의존성 분리(지향점)**
  - 핵심(core): `python-dotenv`, `pyyaml` 등 최소 런타임 의존성
  - 선택적: DB(`psycopg2`), Excel(`pandas`, `openpyxl`), 암호화(ff3) 등 기능별 의존성
  - 개발: pytest, ruff, mypy, pre-commit 등

구체적인 구현 상태나 최신 구조는 항상 `README.md`와 `ARCHITECTURE.md`를 우선 확인하십시오.

## 3. 테스트와 품질 (요약)

- 가능한 한 다음 도구와 패턴을 사용합니다.
  - 테스트: `pytest` (`tests/unit/`, `tests/integration/`, `tests/e2e/` 구조를 지향)
  - 코드 품질: `ruff`(lint + format), `mypy`(타입 검사) 등의 도입을 전제로 코드를 제안합니다.
  - Make 타깃: `make test`, `make lint`, `make format`, `make typecheck` 등 (존재 여부는 실제 `Makefile`을 확인)

CI/CD, 테스트 리포트, GS 인증 마커 등은 필요 시에만 제안하며, 이미 존재하는 설정이 있다면 그 패턴을 따릅니다.

## 4. 로깅·보안·개인정보

- 로깅 및 감사 로그(Audit Log) 정책은 **별도 정책 문서**를 단일 진실 공급원(Single Source of Truth)으로 사용합니다.
- 로깅 관련 코드를 작성하거나 수정하기 전에는 다음 문서를 반드시 먼저 참조하십시오.

- 로깅/개인정보/감사 로그 정책:
  - `@documents/LOGGING_POLICY.md`

해당 문서에는 5W1H 스키마, audit 전용 함수(`common.logger.audit_log`), 마스킹 정책 등이 정의되어 있다고 가정하고, 이 규칙을 위반하지 않는 방향으로만 코드를 제안합니다.

## 5. 개발자용 문서와의 관계

- 개발자는 다음 문서를 우선 참조합니다.
  - 프로젝트 개요 및 빠른 시작: `README.md`
  - 아키텍처와 구조 설명: `ARCHITECTURE.md`
- AI 에이전트는 이 `ai-context.md`를 통해 위 문서의 존재를 알고, 필요할 때 내용을 읽어야 합니다.

