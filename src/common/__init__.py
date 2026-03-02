"""
Common utilities package for the py-template project.

역할:
- common 네임스페이스를 정의하고, logger/load_config/expand_vars 등의
  공용 유틸리티 모듈을 묶는 진입점이다.

주의:
- 임포트 시 부수 효과(환경 변수 변경, 파일 IO, 로깅 초기화 등)를 일으키지 않는다.
"""

