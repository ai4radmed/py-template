"""
변경이력:
  - 2026-02-28: test_substitute → test_expand_vars 리네임 (BenKorea)
  - 2025-11-26: 다양한 데이터 타입(str, dict, list, nested) 테스트 (BenKorea)
  - 2025-11-26: 엣지 케이스 및 에러 처리 검증 (BenKorea)
"""

import os

import pytest

from common.expand_vars import expand_vars


class TestExpandVars:
    """expand_vars 함수 테스트 클래스"""

    def setup_method(self):
        """각 테스트 전 환경변수 설정"""
        os.environ["TEST_VAR"] = "test_value"
        os.environ["PROJECT_NAME"] = "py-template"
        os.environ["LOG_PATH"] = "/var/log/app"
        os.environ["PORT"] = "8080"

    def teardown_method(self):
        """각 테스트 후 환경변수 정리"""
        for key in ["TEST_VAR", "PROJECT_NAME", "LOG_PATH", "PORT"]:
            os.environ.pop(key, None)

    # ========== 문자열 확장 테스트 ==========

    def test_expand_vars_simple_string(self):
        """단순 문자열 내 환경변수 확장"""
        result = expand_vars("Value is ${TEST_VAR}")
        assert result == "Value is test_value"

    def test_expand_vars_multiple_vars(self):
        """하나의 문자열에 여러 환경변수 확장"""
        result = expand_vars("${PROJECT_NAME} runs on port ${PORT}")
        assert result == "py-template runs on port 8080"

    def test_expand_vars_repeated_var(self):
        """동일 환경변수 반복 확장"""
        result = expand_vars("${TEST_VAR} and ${TEST_VAR}")
        assert result == "test_value and test_value"

    def test_expand_vars_no_vars(self):
        """환경변수 없는 문자열 그대로 반환"""
        result = expand_vars("plain string")
        assert result == "plain string"

    def test_expand_vars_undefined_var(self):
        """미정의 환경변수는 확장되지 않음"""
        result = expand_vars("${UNDEFINED_VAR}")
        assert result == "${UNDEFINED_VAR}"

    # ========== 딕셔너리 확장 테스트 ==========

    def test_expand_vars_dict(self):
        """딕셔너리 값 확장"""
        input_dict = {"name": "${PROJECT_NAME}", "port": "${PORT}", "static": "no_substitution"}
        result = expand_vars(input_dict)
        assert result == {"name": "py-template", "port": "8080", "static": "no_substitution"}

    def test_expand_vars_nested_dict(self):
        """중첩 딕셔너리 재귀 확장"""
        input_dict = {"app": {"name": "${PROJECT_NAME}", "logging": {"path": "${LOG_PATH}"}}}
        result = expand_vars(input_dict)
        assert result["app"]["name"] == "py-template"
        assert result["app"]["logging"]["path"] == "/var/log/app"

    # ========== 리스트 확장 테스트 ==========

    def test_expand_vars_list(self):
        """리스트 원소 확장"""
        input_list = ["${PROJECT_NAME}", "${PORT}", "static"]
        result = expand_vars(input_list)
        assert result == ["py-template", "8080", "static"]

    def test_expand_vars_nested_list(self):
        """중첩 리스트 재귀 확장"""
        input_list = ["${TEST_VAR}", ["${PROJECT_NAME}", "${PORT}"]]
        result = expand_vars(input_list)
        assert result == ["test_value", ["py-template", "8080"]]

    # ========== 복합 구조 테스트 ==========

    @pytest.mark.gs_req("GS-31")  # 시험 가능성
    @pytest.mark.isms("ISMS-2.7-46")  # 보안 요구사항 정의(환경 기반 설정 구조)
    def test_expand_vars_complex_structure(self):
        """딕셔너리 + 리스트 혼합 구조 확장"""
        input_data = {
            "project": "${PROJECT_NAME}",
            "servers": [{"host": "localhost", "port": "${PORT}"}, {"host": "prod", "port": "443"}],
            "paths": {"logs": ["${LOG_PATH}/app.log", "${LOG_PATH}/error.log"]},
        }
        result = expand_vars(input_data)

        assert result["project"] == "py-template"
        assert result["servers"][0]["port"] == "8080"
        assert result["servers"][1]["port"] == "443"
        assert result["paths"]["logs"][0] == "/var/log/app/app.log"
        assert result["paths"]["logs"][1] == "/var/log/app/error.log"

    # ========== 기타 타입 테스트 ==========

    def test_expand_vars_integer(self):
        """정수는 그대로 반환"""
        result = expand_vars(12345)
        assert result == 12345

    def test_expand_vars_float(self):
        """실수는 그대로 반환"""
        result = expand_vars(3.14)
        assert result == 3.14

    def test_expand_vars_boolean(self):
        """불린은 그대로 반환"""
        assert expand_vars(True) is True
        assert expand_vars(False) is False

    def test_expand_vars_none(self):
        """None은 그대로 반환"""
        result = expand_vars(None)
        assert result is None

    # ========== 엣지 케이스 테스트 ==========

    def test_expand_vars_empty_string(self):
        """빈 문자열 처리"""
        result = expand_vars("")
        assert result == ""

    def test_expand_vars_empty_dict(self):
        """빈 딕셔너리 처리"""
        result = expand_vars({})
        assert result == {}

    def test_expand_vars_empty_list(self):
        """빈 리스트 처리"""
        result = expand_vars([])
        assert result == []

    def test_expand_vars_with_special_chars(self):
        """특수문자 포함 환경변수명"""
        os.environ["TEST_VAR_123"] = "special_value"
        result = expand_vars("${TEST_VAR_123}")
        assert result == "special_value"
        os.environ.pop("TEST_VAR_123")

    def test_expand_vars_preserves_original(self):
        """원본 데이터 불변성 확인 (immutability)"""
        original = {"key": "${TEST_VAR}"}
        result = expand_vars(original)

        # 원본은 변경되지 않아야 함
        assert original["key"] == "${TEST_VAR}"
        assert result["key"] == "test_value"

