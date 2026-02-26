# py-template 아키텍처 개요

이 문서는 나와 다른 개발자들의 이해를 돕기 위한 아키텍처 설명서입니다.  
왜 이런 구조와 스크립트를 선택했는지, 유지보수 관점에서 이해하는 데 초점을 둡니다.

## 1. 기술 스택과 도구

- **Python 버전**: 3.12+
- **의존성·가상환경 관리**: [uv](https://github.com/astral-sh/uv)
  - `pyproject.toml` + `uv.lock` 기반
  - 일반적인 흐름: `uv venv .venv` → `uv sync` → `uv run ...`

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
    → “프로젝트의 루트 패키지 위치는 `src` 디렉터리 안이다”라는 의미입니다.
  - `packages.find.where = ["src"]`  
    → `setuptools`가 패키지를 찾을 때 **`src` 아래에서만** 검색하도록 지정합니다.
  - 따라서 `src` 아래에 `__init__.py`를 가진 폴더(예: `src/common`)는 자동으로 패키지(`common`)로 인식됩니다.

- `src/common/`
  - 정식 Python 패키지(`src/common/__init__.py`)로 선언되어 있습니다.
  - 어디서든 `import common.logger`, `from common.load_config import load_config` 처럼 사용할 수 있습니다.
  - 주요 모듈:
    - `common.logger` — 로깅 설정/헬퍼
    - `common.load_config` — YAML 설정 파일 로드 + 환경변수 치환
    - `common.substitute` — 문자열/컬렉션 내 환경변수 치환
    - `common.database` — PostgreSQL 연결 및 쿼리 유틸
    - `common.excel_io` — 엑셀 입출력 유틸
    - `common.get_cipher` — FF3 기반 암호화 유틸

- `main.py`
  - 진입점 예시 스크립트.
  - 실제 프로젝트에서는 보통 `python -m 패키지.모듈` 또는 `uv run python -m ...` 형태로 실행 진입점을 구성합니다.

## 3. 설정과 로깅

- **환경 변수**
  - `.env.example` → `.env` 복사 후 수정.
  - `python-dotenv`를 사용하여 애플리케이션 시작 시 자동 로드하는 패턴을 사용합니다.

- **로깅**
  - `config/logging.yml` 기반 설정.
  - `.env`의 `PROJECT_NAME`, `LOG_PATH`, `LOG_LEVEL` 등에 따라 동작이 달라집니다.
  - 콘솔/파일 분리, 서비스 로그와 audit 로그 분리, JSON 포맷 등의 정책을 포함합니다.

## 4. setup 스크립트와 Makefile의 역할

`scripts/setup/`와 `Makefile`은 **개발 편의를 위한 자동화 스크립트 모음**입니다.

- 주요 스크립트 (요지)
  - `scripts/setup/create_logs.py` — 로그 디렉터리 및 파일 생성
  - `scripts/setup/backup.py` / `restore_backup.py` — 설정/환경 백업 및 복원
  - 기타: `.env` 생성, syspath 확인 등

- `Makefile` 주요 타깃
  - `env` — `.env` 생성/초기화
  - `logs` — 로그 디렉터리 생성
  - `backup` / `restore` — 백업/복원
  - `syspath` / `check` / `setup` / `freeze` 등

### syspath 관련 타깃에 대한 주의

과거에는 `scripts/setup/setup_syspath.py`에서 `.pth` 파일을 생성하여  
`{PROJECT_ROOT}/src`를 `sys.path`에 직접 등록하는 방식으로 임포트를 처리했습니다.

현재는:

- `src/common`을 정식 패키지로 선언하여 **패키지 임포트(`common.*`)**를 사용하는 것이 기본 방식입니다.
- `syspath`/`check`/`setup` 타깃과 관련 스크립트는 **레거시 지원 또는 특수한 상황**에서만 필요할 수 있으며,  
  새로운 코드에서는 가급적 사용하지 않는 것을 권장합니다.

## 5. 개발자용 권장 워크플로우

1. 리포지토리 클론
2. 프로젝트 루트에서:
   - `uv venv .venv`
   - `source .venv/bin/activate`
   - `uv sync`
3. `.env` 생성:
   - `.env.example`를 복사하거나, 필요 시 `make env` 사용
4. 로그 디렉터리 생성:
   - `make logs` (또는 직접 디렉터리 생성)
5. 코드 작성 시:
   - 공용 유틸/도메인 독립 모듈은 `src/common/` 아래에 추가
   - 임포트는 항상 `common.xxx` 형태로 패키지 기준으로 작성

## 6. AI 에이전트와의 협업 시 참고

- AI 에이전트는 `.cursor/rules/py-template.mdc`에 정의된 규칙을 기반으로 동작합니다.
- 새로운 스크립트나 구조 변경을 제안할 때:
  - 먼저 이 `ARCHITECTURE.md`와 `README.md`를 읽고,
  - uv 기반 워크플로우와 `src/common` 패키지 구조를 해치지 않는 방향으로 설계하는 것을 원칙으로 합니다.

