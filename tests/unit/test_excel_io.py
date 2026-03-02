"""
adapters.excel_io.read_excels 함수 테스트.
"""

from __future__ import annotations

from pathlib import Path

import pytest

pytest.importorskip("pandas")

import pandas as pd  # noqa: E402

from adapters.excel_io import read_excels  # noqa: E402


@pytest.mark.gs_req("GS-07")  # 기능의 정확성
@pytest.mark.isms("ISMS-2.7-47")  # 보안 설계 및 구현(시험 가능 구조와 연계)
def test_read_excels(tmp_path: Path) -> None:
    """임시 디렉터리에 생성한 엑셀 파일들을 read_excels 가 올바르게 읽는지 검증."""
    # 임시 엑셀 파일 생성
    df1 = pd.DataFrame({"a": [1, 2], "b": [3, 4]})
    df2 = pd.DataFrame({"x": [10, 20], "y": [30, 40]})
    file1 = tmp_path / "test1.xlsx"
    file2 = tmp_path / "test2.xls"
    df1.to_excel(file1, index=False)
    df2.to_excel(file2, index=False)

    # 함수 실행
    result = read_excels(str(tmp_path))

    # 검증
    assert "test1.xlsx" in result
    assert "test2.xls" in result
    pd.testing.assert_frame_equal(result["test1.xlsx"], df1)
    pd.testing.assert_frame_equal(result["test2.xls"], df2)
