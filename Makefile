.PHONY: env logs setup test test-fast report report-audit lint format typecheck

# === 환경 설정 ===
env:
	uv run python scripts/setup/setup_env.py

logs:
	uv run python scripts/setup/setup_log_dir.py

setup: env logs
	@echo "[setup] 환경 및 로그 디렉터리 설정 완료."

# === 개발 도구 ===
lint:
	uv run ruff check .

format:
	uv run ruff format .

typecheck:
	uv run mypy src/

# === 테스트 및 리포트 ===
# 테스트만 실행 (리포트 없음). 로컬 전체 = local_only 포함.
test:
	uv run pytest -v

# CI와 동일한 테스트 세트 (local_only 제외). 리포트 없음.
test-fast:
	uv run pytest -m "not local_only" -v

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
