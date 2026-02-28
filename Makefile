.PHONY: env logs setup ensure-python sync venv test test-fast report report-audit lint format typecheck check-venv

# 프로젝트 가상환경 사용 (활성화 여부와 무관하게 동일 동작)
VENV_PYTHON := $(CURDIR)/.venv/bin/python

# === 환경 설정 ===
# requires-python에 맞는 Python을 uv로 설치 (가상환경 생성 전 선행)
ensure-python:
	uv run python scripts/setup/ensure_python_requires.py

# 가상환경 생성 및 의존성 설치 (ensure-python 후 실행 권장)
sync:
	uv sync

# Python 설치 + 가상환경/의존성 한 번에 (클론 후 첫 설정 시)
venv: ensure-python sync
	@echo "[venv] Python 및 가상환경 준비 완료."

# .venv 존재 여부 확인 (logs 등 venv 필요한 타깃에서 사용)
check-venv:
ifeq ($(OS),Windows_NT)
	@test -f .venv/Scripts/python.exe || (echo "[make] 가상환경이 없습니다. 먼저 'make venv' 또는 'make sync'를 실행하세요."; exit 1)
else
	@test -f $(VENV_PYTHON) || (echo "[make] 가상환경이 없습니다. 먼저 'make venv' 또는 'make sync'를 실행하세요."; exit 1)
endif

env:
	uv run python scripts/setup/setup_env.py

logs: check-venv
ifeq ($(OS),Windows_NT)
	uv run python scripts/setup/setup_log_dir.py
else
	sudo -E $(VENV_PYTHON) scripts/setup/setup_log_dir.py
endif
	@echo "[setup_log_dir] 로그 디렉터리 설정 완료."

setup: env logs
	@echo "[setup] 환경 설정 완료."

# === 개발 도구 ===
# 테스트만 실행 (리포트 없음). 로컬 전체 = local_only 포함.
test:
	uv run pytest -v

# CI와 동일한 테스트 세트 (local_only 제외). 리포트 없음.
test-fast:
	uv run pytest -m "not local_only" -v

lint:
	uv run ruff check .

format:
	uv run ruff format .

typecheck:
	uv run mypy src/

# === 테스트 및 리포트 (업계표준: 실행과 리포트 생성 분리) ===
# 리포트 생성 = 테스트 실행 + 산출물(HTML, JUnit, Allure, coverage) 생성.
# report: 전체 테스트(local_only 포함) + 리포트 → GS/ISMS-P 심사용.
report:
	uv run pytest \
		--html=reports/test_report.html --self-contained-html \
		--cov=src --cov-report=html:reports/coverage --cov-report=term-missing \
		--alluredir=reports/allure-results \
		--junitxml=reports/junit.xml \
		-v

# report와 동일하되 별칭(심사용 전체 테스트+리포트임을 명시).
report-audit: report
	@echo "[report-audit] GS/ISMS-P 심사용 전체 테스트 및 리포트 생성 완료. reports/ 확인."
