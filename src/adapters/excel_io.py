"""
명세서(`.spec/src/adapters/excel_io.md`) 기반 엑셀 입출력 유틸리티.

역할:
- 지정한 디렉터리에서 엑셀 파일을 일괄 읽어 dict[str, DataFrame] 으로 제공하고,
  여러 DataFrame 을 디렉터리에 일괄 저장하는 함수들을 제공한다.
"""

from __future__ import annotations

import inspect
import os
from pathlib import Path

import pandas as pd

from common.logger import log_debug, log_error, log_info


def read_excels(input_dir: str) -> dict[str, pd.DataFrame]:
    """
    input_dir 하위의 .xls/.xlsx 파일을 재귀적으로 읽어 딕셔너리로 반환한다.

    반환 형식:
        {파일명(str): pandas.DataFrame}
    """
    excel_files = Path(input_dir).rglob("*.xls*")
    dfs: dict[str, pd.DataFrame] = {}
    for file in excel_files:
        try:
            df = pd.read_excel(file)
            dfs[file.name] = df
            log_debug(f"[read_excels] from: {file.name} (shape={df.shape})")
        except Exception as exc:  # noqa: BLE001
            frame = inspect.currentframe()
            func_name = frame.f_code.co_name if frame else "unknown"
            log_error(f"[{func_name}] 엑셀 파일 읽기 오류: {file} - {exc}")
    return dfs


def save_excels(output_dir: str, dataframes_dict: dict[str, pd.DataFrame], prefix: str | None = None) -> None:
    """
    데이터프레임 딕셔너리를 지정된 디렉토리에 엑셀 파일로 저장하는 함수.

    Args:
        output_dir: 저장할 디렉토리 경로
        dataframes_dict: {파일명: DataFrame} 형태의 딕셔너리
        prefix: 파일명 앞에 붙일 접두사 (예: "deid_", "structured_")
    """
    # 유효성 검사
    if not output_dir or not isinstance(output_dir, str) or output_dir.strip() == "":
        log_error("[save_excels] output_dir가 설정되지 않았습니다.")
        return

    if not dataframes_dict:
        log_info("[save_excels] 저장할 데이터가 없습니다.")
        return

    # 출력 디렉토리 생성
    try:
        os.makedirs(output_dir, exist_ok=True)
        log_debug(f"[save_excels] 출력 디렉토리 준비: {output_dir}")
    except OSError as exc:  # noqa: BLE001
        log_error(f"[save_excels] 디렉토리 생성 실패: {output_dir} - {exc}")
        return

    # 각 파일 저장
    saved_count = 0
    failed_count = 0

    for original_filename, df in dataframes_dict.items():
        try:
            # 파일명 처리 (.xls → .xlsx 변환)
            base_filename = os.path.basename(original_filename)
            if base_filename.endswith(".xls"):
                base_filename = base_filename[:-4] + ".xlsx"
            elif not base_filename.endswith(".xlsx"):
                base_filename = base_filename + ".xlsx"

            # 접두사 추가
            name_parts = []
            if prefix:
                name_parts.append(prefix.rstrip("_"))

            # 파일명에서 확장자 분리
            name_without_ext = base_filename.replace(".xlsx", "")
            name_parts.append(name_without_ext)

            # 최종 파일명 생성
            final_filename = "_".join(name_parts) + ".xlsx"
            output_path = os.path.join(output_dir, final_filename)

            # 파일 저장
            df.to_excel(output_path, index=False)
            log_debug(f"[save_excels] 저장 완료: {output_path}")
            saved_count += 1

        except Exception as exc:  # noqa: BLE001
            log_error(f"[save_excels] 저장 실패: {original_filename} - {exc}")
            failed_count += 1

    # 결과 요약
    log_info(f"[save_excels] 저장 완료: {saved_count}개, 실패: {failed_count}개")
