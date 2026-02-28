# pytest 태그(마커) 활용 가이드

이 프로젝트의 **태그**는 pytest **마커(markers)**를 말합니다.  
테스트를 기준별로 묶어서 실행하거나, CI/로컬을 구분하거나, GS/ISMS-P 증적을 수집할 때 사용합니다.

---

## 1. 어떤 태그가 있는지

| 마커 | 의미 | 예시 |
|------|------|------|
| `gs_req("GS-NN")` | GS 인증 기준 항목 ID | `gs_req("GS-07")`, `gs_req("GS-31")` |
| `isms("ISMS-2.x-NN")` | ISMS-P 인증 기준 항목 ID | `isms("ISMS-2.7-47")`, `isms("ISMS-2.8-54")` |
| `local_only` | 로컬에서만 실행(CI 제외) | 환경/파일 의존 테스트 |
| `integration` | 통합 테스트(DB·파일 등) | (정의만 있음, 필요 시 사용) |
| `e2e` | 종단 간 테스트 | (정의만 있음, 필요 시 사용) |

정의 위치: `pyproject.toml` → `[tool.pytest.ini_options].markers`

---

## 2. 태그로 테스트 실행하기

### 일상적인 실행

```bash
# 전체 테스트 (local_only 포함) — 로컬에서만
make test
# 또는
uv run pytest -v

# CI와 동일 (local_only 제외) — 머지 전·PR 검증
make test-fast
# 또는
uv run pytest -m "not local_only" -v
```

### 특정 기준(GS/ISMS)만 실행

```bash
# GS-07에 해당하는 테스트만
uv run pytest -m "gs_req('GS-07')" -v

# ISMS 2.8-54에 해당하는 테스트만
uv run pytest -m "isms('ISMS-2.8-54')" -v

# GS-07 또는 GS-31
uv run pytest -m "gs_req('GS-07') or gs_req('GS-31')" -v

# GS와 ISMS 둘 다 붙은 테스트만 (AND)
uv run pytest -m "gs_req and isms" -v
```

> 마커에 인자(예: `GS-07`)가 있을 때는 `gs_req('GS-07')`처럼 **따옴표**를 씁니다.

### local_only만 / local_only 제외

```bash
# 로컬 전용 테스트만 실행 (예: pyproject 읽기 등)
uv run pytest -m "local_only" -v

# 로컬 전용 제외 (CI와 동일)
uv run pytest -m "not local_only" -v
```

### 조합 예시

```bash
# "GS 기준이면서 local_only가 아닌 테스트"만
uv run pytest -m "gs_req and not local_only" -v
```

---

## 3. 태그가 붙은 테스트 목록 보기

실행 없이 **어떤 테스트에 어떤 마커가 붙었는지**만 보고 싶을 때:

```bash
# 모든 마커와 테스트 목록
uv run pytest --markers

# 특정 마커가 붙은 테스트만 목록(실행 안 함)
uv run pytest -m "gs_req" --collect-only -q
uv run pytest -m "isms('ISMS-2.8-54')" --collect-only -q
```

---

## 4. 새 테스트에 태그 붙이기

- **GS/ISMS-P 증적**으로 쓸 테스트에만 `gs_req`, `isms`를 붙입니다.
- “이 테스트가 없으면 해당 기준을 설명하기 어렵다” 수준일 때만 붙이는 것을 권장합니다.

```python
@pytest.mark.gs_req("GS-07")   # 기능의 정확성
@pytest.mark.isms("ISMS-2.7-47")
def test_read_excels(tmp_path):
    ...
```

- 로컬 전용(CI 제외) 테스트는 `local_only`를 붙입니다.

```python
@pytest.mark.local_only
@pytest.mark.gs_req("GS-31")
def test_get_requires_python_from_project(tmp_path):
    ...
```

**규칙**: 테스트에 기준 마커를 붙였다면 `documents/GS_ISMS_TEST_MATRIX.md`에 해당 기준 행을 추가하거나, 기존 행의 “자동 테스트 ID” 컬럼에 이 테스트 경로를 추가합니다.

---

## 5. 언제 어떤 명령을 쓰면 좋은지

| 목적 | 추천 명령 |
|------|-----------|
| 로컬에서 전체 확인 | `make test` |
| PR/머지 전 검증(CI와 동일) | `make test-fast` |
| GS-07 관련만 빠르게 확인 | `uv run pytest -m "gs_req('GS-07')" -v` |
| 심사용 증적(리포트) 수집 | `make report` 또는 `make report-audit` |
| CI 파이프라인 | `uv run pytest -m "not local_only"` (+ 리포트 옵션) |

---

## 6. 참고 문서

- **마커 정의·정책**: `documents/TESTING_POLICY.md` §4
- **기준 ↔ 테스트 매핑**: `documents/GS_ISMS_TEST_MATRIX.md`
- **Makefile 타깃**: `make test`, `make test-fast`, `make report` — `TESTING_POLICY.md` §7
