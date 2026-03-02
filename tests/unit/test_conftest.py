"""
`tests.conftest.py` 의 `pytest_configure` 함수가
GS/ISMS-P 커스텀 마커를 올바르게 등록하는지 검증하는 단위 테스트.
"""

from __future__ import annotations

from dataclasses import dataclass, field

import conftest as conftest_module

EXPECTED_GS_MARKER = "gs_req(id): GS 체크리스트 항목 ID. 예: GS-24, GS-31"
EXPECTED_ISMS_MARKER = (
    "isms(id): ISMS-P 체크리스트 항목 ID를 명시합니다. 예: ISMS-2.8-54"
)


@dataclass
class DummyConfig:
    """pytest.Config 의 addinivalue_line 동작만 흉내 내는 더미 설정 객체."""

    values: list[tuple[str, str]] = field(default_factory=list)

    def addinivalue_line(self, name: str, line: str) -> None:
        self.values.append((name, line))

    def marker_lines(self) -> list[str]:
        """등록된 markers 섹션의 라인만 추출한다."""
        return [line for key, line in self.values if key == "markers"]


def test_gs_req_marker_registered() -> None:
    """gs_req 마커 정의가 markers 설정에 등록되는지 확인한다."""
    config = DummyConfig()

    # 실제 pytest 실행 환경 대신 더미 Config 로 호출
    conftest_module.pytest_configure(config)  # type: ignore[arg-type]

    markers = config.marker_lines()
    assert (
        EXPECTED_GS_MARKER in markers
    ), f"gs_req 마커 정의가 markers 설정에 없습니다: {markers!r}"


def test_isms_marker_registered() -> None:
    """isms 마커 정의가 markers 설정에 등록되는지 확인한다."""
    config = DummyConfig()

    conftest_module.pytest_configure(config)  # type: ignore[arg-type]

    markers = config.marker_lines()
    assert (
        EXPECTED_ISMS_MARKER in markers
    ), f"isms 마커 정의가 markers 설정에 없습니다: {markers!r}"

