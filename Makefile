.PHONY: env logs setup backup restore update test lint format typecheck report

# === 환경 설정 ===
env:
	uv run python scripts/setup/setup_env.py

logs:
ifeq ($(OS),Windows_NT)
	uv run python scripts/setup/create_logs.py
else
	sudo `which python` scripts/setup/create_logs.py
endif
	@echo "[create_logs] Log path and file creation complete."

setup: env logs
	@echo "[setup] 환경 설정 완료."

# === 데이터 관리 ===
backup:
	uv run python scripts/setup/backup.py

restore:
	uv run python scripts/setup/restore_backup.py
	@echo "[restore] Backup restored."

# === 개발 도구 ===
test:
	uv run pytest

lint:
	uv run ruff check .

format:
	uv run ruff format .

typecheck:
	uv run mypy src/

# === GS 인증 산출물 생성 ===
report:
	uv run pytest \
		--html=reports/test_report.html --self-contained-html \
		--cov=src --cov-report=html:reports/coverage --cov-report=term-missing \
		--alluredir=reports/allure-results \
		--junitxml=reports/junit.xml \
		-v

# === 템플릿 업데이트 ===
update:
	uv run python scripts/setup/update.py
