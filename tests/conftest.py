"""
pytest 공통 설정 및 GS 인증 커스텀 마커 등록.

GS 인증 마커 사용 예시:
    @pytest.mark.gs_req("REQ-SEC-001")
    @pytest.mark.gs_category("보안성")
    def test_password_encryption_strength():
        ...
"""
