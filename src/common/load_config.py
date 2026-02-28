"""
변경경이력:
  - 2025-11-26 값에 포함된 ${VAR} 패턴을 환경변수값으로 치환 (BenKorea)
  - 2025-11-26 YAML 경로를 받아 dict로 로드 (BenKorea)
"""

from typing import cast

import yaml

from common.expand_vars import expand_vars
from common.logger import log_debug, log_error


def load_config(yml_path: str = "config/deidentification.yml", section: str | None = None) -> dict:
    """
    YAML 설정 파일을 로드하고 환경변수를 치환하여 반환

    Args:
        yml_path (str): YAML 파일 경로 (기본값: config/deidentification.yml)
        section (str, optional): 특정 섹션만 추출. None이면 전체 반환

    Returns:
        dict: 환경변수가 치환된 설정 딕셔너리

    Raises:
        FileNotFoundError: 설정 파일이 존재하지 않을 때
        yaml.YAMLError: YAML 파싱 오류 발생 시
    """
    try:
        log_debug(f"[load_config] Loading config from: {yml_path}, section: {section}")

        # 1. 파일 열기 및 파싱
        with open(yml_path, encoding="utf-8") as f:
            yaml_config = yaml.safe_load(f)

        # 2. 환경변수 치환
        substituted_config = expand_vars(yaml_config)

        # 3. 섹션 추출 (지정된 경우)
        if section:
            result = substituted_config.get(section, {})
            log_debug(f"[load_config] Extracted section '{section}' with {len(result)} keys")
            return cast(dict, result)

        # 4. 전체 반환
        log_debug(f"[load_config] Returning full config with {len(substituted_config)} top-level keys")
        return cast(dict, substituted_config)

    except FileNotFoundError:
        log_error(f"[load_config] Config file not found: {yml_path}")
        raise
    except yaml.YAMLError as e:
        log_error(f"[load_config] YAML parsing error in {yml_path}: {e}")
        raise
    except Exception as e:
        log_error(f"[load_config] Unexpected error loading {yml_path}: {e}")
        raise
