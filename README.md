# py-template

Python 전용 프로젝트들을 위한 공용 템플릿으로 사용하고자 이 프로젝트를 만들었습니다.

## 포함된 기능

### 환경 및 구조
- **가상환경·패키지**: [uv](https://github.com/astral-sh/uv)를 사용하여 `pyproject.toml` + `uv.lock` 기반으로 관리. 일반적인 흐름은 `uv venv .venv` → `uv sync`.
- **임포트 경로**: `src/common`과 `src/adapters`를 정식 패키지로 선언하여 어디서든 `import common.logger`, `import adapters.database` 등과 같이 사용.
- **환경 변수**: `.env` 기반. `make env`로 `.env.example` → `.env` 생성. `python-dotenv` 로드.

### 코드 품질 및 테스트
- **린터·포매터**: [ruff](https://docs.astral.sh/ruff/) — `make lint`, `make format`
- **타입 검사**: [mypy](https://mypy-lang.org/) — `make typecheck`
- **커밋 전 검사**: [pre-commit](https://pre-commit.com/) — ruff + mypy 자동 실행
- **테스트**: [pytest](https://docs.pytest.org/) — `make test` (unit / integration / e2e 구분)
- **GS 인증 산출물**: `make report` — HTML 테스트 리포트, 커버리지 리포트, Allure 결과, JUnit XML 자동 생성
- **CI/CD**: GitHub Actions — lint, typecheck, 멀티 OS(ubuntu/windows) 테스트, 산출물 Artifacts 업로드

### 로깅
- **로깅 시스템**: `config/logging.yml` + `.env`(`PROJECT_NAME`, `LOG_PATH`, `LOG_LEVEL`) 기반.
- **로그 경로**: `{PROJECT_ROOT}/logs` 또는 `.env`의 `LOG_PATH`(예: `/var/log/{PROJECT_NAME}`).
- **기능**: 콘솔/파일(service·audit 분리), JSON 포맷, 환경변수 치환, audit 전용 파일·stdout 미출력 정책.

### 핵심 유틸 (`src/common/`)
- **YAML 설정**: `common.load_config` — YAML 로드 + `${VAR}` 환경변수 치환.
- **환경변수 치환**: `common.substitute` — 문자열/딕셔너리/리스트 재귀 치환.

### 외부 연동 어댑터 (`src/adapters/`)
- **DB 연동**: `adapters.database` — PostgreSQL(psycopg2), `.env` 기반 연결·쿼리 헬퍼. (`uv sync --extra db`)
- **엑셀 입출력**: `adapters.excel_io` — 폴더 단위 xls/xlsx 읽기·쓰기, pandas 기반. (`uv sync --extra excel`)
- **암호화**: `adapters.get_cipher` — FF3(Format Preserving Encryption), `.env` 키/트웨이크/알파벳. (`uv sync --extra cipher`)

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
   uv sync --group dev --extra all
   ```
2. **환경 변수 로드용 .env 준비**
   ```bash
   make env  # 또는 .env.example을 복사 후 수동 수정
   ```
3. **로그 디렉터리 생성** (필요 시)
   ```bash
   make logs
   ```

## 프로젝트 구조

| 경로 | 설명 |
|------|------|
| `src/common/` | 핵심 유틸리티 (logger, substitute, load_config) |
| `src/adapters/` | 외부 시스템 연동 (database, excel_io, get_cipher) |
| `scripts/setup/` | 환경 설정, 로그, 백업 등 자동화 스크립트 |
| `config/` | 로깅 설정 등 (`config/logging.yml`) |
| `tests/unit/` | 단위 테스트 |
| `tests/integration/` | 통합 테스트 (DB, 파일 등 외부 자원) |
| `tests/e2e/` | 종단 간 테스트 (사용자 시나리오) |
| `.github/workflows/` | CI/CD 파이프라인 (GitHub Actions) |

## Makefile 타깃

| 타깃 | 설명 |
|------|------|
| `env` | `.env` 기반 환경 변수 초기화 |
| `logs` | 로그 디렉터리 및 파일 생성 |
| `setup` | env + logs 일괄 실행 |
| `backup` | 설정/환경 백업 |
| `restore` | 백업 복원 |
| `test` | pytest 실행 |
| `lint` | ruff 린트 검사 |
| `format` | ruff 자동 포매팅 |
| `typecheck` | mypy 타입 검사 |
| `report` | GS 인증 산출물 생성 (HTML 리포트, 커버리지, Allure, JUnit) |
| `update` | 템플릿 업데이트 |

## GS 인증 테스트 마커

테스트 코드에 GS 인증 요구사항을 매핑할 수 있습니다:

```python
import pytest

@pytest.mark.gs_req("REQ-SEC-001")
@pytest.mark.gs_category("보안성")
def test_password_encryption_strength():
    ...
```

사용 가능한 마커:
- `@pytest.mark.gs_req("REQ-XXX-NNN")` — GS 인증 요구사항 ID
- `@pytest.mark.gs_category("카테고리")` — 평가 항목 (기능 적합성, 보안성, 신뢰성 등)
- `@pytest.mark.integration` — 통합 테스트
- `@pytest.mark.e2e` — 종단 간 테스트

산출물 생성:
```bash
make report    # reports/ 디렉터리에 전체 산출물 생성
```

생성되는 파일:
| 파일 | 설명 |
|------|------|
| `reports/test_report.html` | pytest-html 테스트 결과 보고서 |
| `reports/coverage/` | 라인 단위 코드 커버리지 (HTML) |
| `reports/junit.xml` | JUnit XML (CI 연동용) |
| `reports/allure-results/` | Allure 대시보드 데이터 |
