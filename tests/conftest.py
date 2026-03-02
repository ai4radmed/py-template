"""
pytest 공통 설정 및 GS/ISMS-P 커스텀 마커를 등록하는 모듈.

마커 사용 예시:
    @pytest.mark.gs_req("GS-24")
    @pytest.mark.isms("ISMS-2.8-54")
    def test_password_encryption_strength():
        ...
"""

from __future__ import annotations

import pytest


def pytest_configure(config: pytest.Config) -> None:
    """GS 및 ISMS-P 기준 연계를 위한 커스텀 마커 정의."""

    # GS: 항목 번호만 사용 (구분은 GS인증기준.md에서 항목으로 조회 가능)
    config.addinivalue_line(
        "markers",
        "gs_req(id): GS 체크리스트 항목 ID. 예: GS-24, GS-31",
    )

    # ISMS-P 관련 마커
    config.addinivalue_line(
        "markers",
        "isms(id): ISMS-P 체크리스트 항목 ID를 명시합니다. 예: ISMS-2.8-54",
    )

