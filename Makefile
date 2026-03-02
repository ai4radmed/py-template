.PHONY: env logs

# 이 Makefile은 .env 파일 생성 및 로그 디렉터리 설정을 위한 최소 단축 명령만 제공합니다.
# 자세한 워크플로우는 ARCHITECTURE.md의 "개발자용 권장 워크플로우" 절을 참고하세요.

env:
	uv run python scripts/setup/setup_env.py

logs:
	uv run python scripts/setup/setup_log_dir.py

