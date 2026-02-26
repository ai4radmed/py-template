## Python 환경 및 로그 자동화 Makefile

venv:
	python scripts/setup/setup_pyenv.py
	python scripts/setup/setup_venv.py
	@echo "[setup_venv] Python virtual environment created."

env:
	python scripts/setup/setup_env.py

logs:
ifeq ($(OS),Windows_NT)
	python scripts/setup/create_logs.py
else
	sudo `which python` scripts/setup/create_logs.py
endif
	@echo "[create_logs] Log path and file creation complete."

syspath:
	python scripts/setup/setup_syspath.py
	@echo "[setup_syspath] Python syspath setup complete."

setup: env logs syspath
	@echo "[setup] All setup tasks completed."

restore:
	python scripts/setup/restore_backup.py
	@echo "[restore] Backup restored."

check:
	python scripts/setup/check_syspath.py
	@echo "[check_syspath] syspath check complete."

backup:
	python scripts/setup/backup.py

freeze:
	pip freeze > requirements.txt

update:
	python scripts/setup/update.py
