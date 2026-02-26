# py-template

Python 전용 프로젝트들을 위한 공용 템플릿으로 사용하고자 이 프로젝트를 만들었습니다.

## 포함된 기능

### 환경 및 구조
- **가상환경·패키지**: [uv](https://github.com/astral-sh/uv)를 사용하여 `pyproject.toml` + `uv.lock` 기반으로 관리. 일반적인 흐름은 `uv venv .venv` → `uv sync`.
- **임포트 경로**: `src/common`을 정식 패키지로 선언하여 어디서든 `import common.logger` 등과 같이 사용. 별도의 syspath 설정이 없어도 동작하며, 과거 `.pth` 기반 스크립트는 레거시 용도로만 사용.
- **환경 변수**: `.env` 기반. `make env`로 `.env.example` → `.env` 생성. `python-dotenv` 로드.

### 로깅
- **로깅 시스템**: `config/logging.yml` + `.env`(`PROJECT_NAME`, `LOG_PATH`, `LOG_LEVEL`) 기반.
- **로그 경로**: `{PROJECT_ROOT}/logs` 또는 `.env`의 `LOG_PATH`(예: `/var/log/{PROJECT_NAME}`).
- **기능**: 콘솔/파일(service·audit 분리), JSON 포맷, 환경변수 치환, audit 전용 파일·stdout 미출력 정책.

### 설정·유틸
- **YAML 설정**: `common.load_config` — YAML 로드 + `$VAR`/`${VAR}` 환경변수 치환.
- **환경변수 치환**: `common.substitute` — 문자열/딕셔너리/리스트 재귀 치환.
- **DB 연동**: `common.database` — PostgreSQL(psycopg2), `.env` 기반 연결·쿼리 헬퍼.
- **엑셀 입출력**: `common.excel_io` — 폴더 단위 xls/xlsx 읽기·쓰기, pandas 기반.
- **암호화**: `common.get_cipher` — FF3(Format Preserving Encryption), `.env` 키/트웨이크/알파벳.

### 테스트·개발
- **테스트**: `pytest`, `tests/unit/` 구조. `make` 외에 `pytest` 직접 실행 가능.
- **에디터**: `.vscode/settings.json` — 워크스페이스 기본 인터프리터 `.venv` 지정.

### 운영
- **백업·복원**: `scripts/setup/backup.py`, `restore_backup.py`. `make backup`, `make restore`.

## 요구사항

- Python 3.12+
- [uv](https://github.com/astral-sh/uv) (패키지/가상환경 관리)

## 빠른 시작

1. **가상환경 생성 및 의존성 설치(uv)**
   ```bash
   uv venv .venv
   source .venv/bin/activate   # Linux/macOS
   uv sync
   ```
2. **환경 변수 로드용 .env 준비**
   ```bash
   make env  # 또는 .env.example을 복사 후 수동 수정
   ```
3. **로그 디렉터리 생성** (필요 시)
   ```bash
   make logs
   ```

> 기존 `make venv`, `make syspath`, `make setup` 등은 과거 pip/requirements.txt + syspath(.pth) 기반 플로우를 위한 타깃으로,  
> uv 기반 신규 프로젝트에서는 사용하지 않는 것을 권장합니다.

## 프로젝트 구조

| 경로 | 설명 |
|------|------|
| `src/` | 파이썬 소스 및 공용 모듈 (예: `common` 패키지) |
| `scripts/setup/` | 가상환경, 로그, syspath 등 설정 스크립트 |
| `config/` | 로깅 설정 등 (`config/logging.yml`) |
| `logs/` | 로그 출력 디렉터리 (설정에 따라 생성) |

## Makefile 대상

- `venv` — 가상환경 생성
- `env` — `.env` 기반 환경 변수 로드
- `logs` — 로그 디렉터리 및 파일 생성
- `syspath` — `src`를 `sys.path`에 등록 (.pth)
- `setup` — env + logs + syspath 일괄 실행
- `check` — syspath 설정 확인
- `freeze` — `pip freeze`로 `requirements.txt` 갱신

---

## 제안: 누락 기술 정리 및 템플릿 확장

아래는 **이미 구현되어 있으나 README에 명시되지 않았던 것**을 반영한 항목과, **일반적인 파이썬 프로젝트 템플릿에서 추가하면 좋은 것**입니다.

### 이번에 문서에 반영한 구현 사항
- YAML 설정 로드·환경변수 치환(`load_config`, `substitute`)
- PostgreSQL 헬퍼(`database`), 엑셀 입출력(`excel_io`), FF3 암호화(`get_cipher`)
- 로깅 상세(콘솔/파일 분리, JSON, audit 정책)
- `.env`/`make env` 역할, 백업·복원 스크립트, VSCode 설정

### 추가하면 좋은 것 (우선순위 참고)

| 구분 | 항목 | 설명 |
|------|------|------|
| **빌드·의존성** | `pyproject.toml` | uv 사용 시 `[project]`, optional deps(dev/test) 정의. `requirements.txt`와 병행 또는 대체. |
| **코드 품질** | 린터·포매터 | [ruff](https://docs.astral.sh/ruff/)(lint+format) 또는 black+isort. `make lint`, `make format` 등. |
| **타입** | 정적 타입 검사 | [mypy](https://mypy-lang.org/) 또는 [pyright](https://microsoft.github.io/pyright/). 점진적 도입 가능. |
| **커밋 전 검사** | pre-commit | ruff/mypy/테스트 훅으로 커밋 전 자동 검사. |
| **CI** | GitHub Actions 등 | `pytest`, 린트, (선택) 타입 체크 자동 실행. |
| **문서** | LICENSE | MIT/Apache 등 라이선스 파일. 템플릿 재사용 시 권리 명시. |
| **실행 예시** | `make test` | `pytest`를 실행하는 타깃이 있으면 사용법이 명확해짐. |
| **선택** | Docker | `Dockerfile`·`docker-compose.yml` 예시로 배포/로컬 환경 통일. |
| **선택** | 보안 스캔 | `pip-audit` 또는 Dependabot으로 의존성 취약점 점검. |
