#!/usr/bin/env python3
"""
ARCHITECTURE.md (AI Agentic Reviewer) 실현을 위한 AI 기반 코드 리뷰 스크립트.
"""

import os
import subprocess
import sys
from pathlib import Path

try:
    import google.generativeai as genai
except ImportError:
    print("[CRITICAL] 'google-generativeai' 패키지가 설치되지 않았습니다. 'uv sync'를 실행하세요.")
    sys.exit(1)

# 설정: 환경변수에서 Gemini API 키 로드
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")


def get_changed_files() -> list[str]:
    """git diff를 통해 변경된 .py 파일 목록을 가져온다."""
    try:
        # PR 환경(CI)이면 main과 비교, 로컬이면 HEAD와 비교
        target = os.getenv("GITHUB_BASE_REF", "HEAD")
        cmd = (
            ["git", "diff", "--name-only", f"origin/main...{target}"]
            if target != "HEAD"
            else ["git", "diff", "--name-only", "HEAD~1"]
        )

        # 커밋이 하나도 없거나 레포가 초기 상태인 경우 fallback
        try:
            output = subprocess.check_output(cmd, stderr=subprocess.STDOUT).decode("utf-8")
        except subprocess.CalledProcessError:
            output = subprocess.check_output(["git", "diff", "--name-only", "HEAD"], stderr=subprocess.STDOUT).decode(
                "utf-8"
            )

        return [f for f in output.splitlines() if f.endswith(".py") and os.path.exists(f)]
    except Exception as exc:
        print(f"[ERROR] 변경 파일 목록 추출 실패: {exc}")
        return []


def find_spec_for_file(file_path: str) -> Path | None:
    """변경된 파일의 .spec 파일을 대응시킨다."""
    p = Path(file_path)
    spec_path = Path(".spec") / p.with_suffix(".md")
    return spec_path if spec_path.is_file() else None


def review_file_with_ai(file_path: str, spec_path: Path) -> str:
    """AI를 호출하여 실제 코드와 명세서를 비교 리뷰한다."""
    if not GEMINI_API_KEY:
        return "[SKIP] GEMINI_API_KEY가 설정되지 않아 AI 리뷰를 건너뜁니다."

    genai.configure(api_key=GEMINI_API_KEY)
    model = genai.GenerativeModel("gemini-1.5-flash")

    code_content = Path(file_path).read_text(encoding="utf-8")
    spec_content = spec_path.read_text(encoding="utf-8")

    prompt = f"""
당신은 'AI Agentic Reviewer'입니다.
다음 프로젝트의 명세서(Level 2)와 구현된 코드(Level 3)를 비교하여 리뷰를 수행하세요.

[규칙]
1. 명세서에 정의된 '핵심 규칙'과 'Public API'를 코드가 정확히 준수하는지 확인하십시오.
2. 명세와 일치하지 않는 부분이 있다면 구체적인 코드 라인이나 로직을 지적하십시오.
3. 명세에는 없지만 보안상 취약하거나 가독성이 현격히 떨어지는 부분이 있다면 추가 피드백을 주십시오.
4. 결과는 Markdown 형식으로 작성하고, 'PASS' 또는 'FAIL' 여부를 명확히 명시하십시오.

---
[명세서: {spec_path}]
{spec_content}

---
[구현 코드: {file_path}]
{code_content}
"""
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as exc:
        return f"[ERROR] AI 호출 중 오류 발생 ({file_path}): {exc}"


def main():
    print("=== AI Agentic Reviewer 시작 ===")

    if not GEMINI_API_KEY:
        print("[WARNING] GEMINI_API_KEY 환경변수가 없습니다. 시뮬레이션 모드로 동작합니다.")

    changed_files = get_changed_files()
    if not changed_files:
        print("리뷰할 변경된 Python 파일이 없습니다.")
        return

    has_violation = False
    review_results = []

    for f in changed_files:
        spec = find_spec_for_file(f)
        if spec:
            print(f"리뷰 중: {f} (명세: {spec})")
            res = review_file_with_ai(f, spec)
            review_results.append((f, res))
            if "FAIL" in res:
                has_violation = True
        else:
            print(f"명세 없음(건너뜀): {f}")

    # 결과 요약 출력
    print("\n" + "=" * 50)
    print("AI 리뷰 요약 리포트")
    print("=" * 50)
    for f, report in review_results:
        print(f"\n### File: {f}")
        print(report)
        print("-" * 30)

    if has_violation:
        print("\n[FAIL] 명세 위반 사항이 발견되었습니다.")
        sys.exit(1)
    else:
        print("\n[PASS] 모든 명세 준수 확인.")
        sys.exit(0)


if __name__ == "__main__":
    main()
