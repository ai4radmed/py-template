# AI-Native Spec-Driven 아키텍처 초안 프롬프트 (py-template 전용)

이 저장소(`py-template`)에 대한 `ARCHITECTURE.md` 초안을 생성할 때 Gemini Web 에이전트에게 전달할 프롬프트 예시입니다.

```text
당신은 소프트웨어 아키텍트이자 AI-Native Spec-Driven Development 전문가입니다.

목표:
- "py-template"라는 Python 템플릿 프로젝트에 대한 상위 레벨 아키텍처 초안을 작성해 주세요.
- 결과물은 이 레포 루트에 둘 `ARCHITECTURE.md` 1개 파일의 내용입니다.
- 이 문서는 이후 IDE 에이전트(Cursor, AntiGravity 등)가 `.spec/` 명세와 코드를 생성할 때 기준이 됩니다.

프로젝트 설명:
- 프로젝트 이름: py-template
- 주요 목적/도메인:
  - Python 전용 프로젝트들을 위한 공용 템플릿
  - AI-Native Spec-Driven Development 방식으로, 다른 서비스/앱이 이 템플릿을 포크/복제하여 사용
- 주요 사용자 유형:
  - 템플릿을 기반으로 신규 서비스를 만드는 백엔드 개발자 및 1인 개발자
  - GS/ISMS-P 등 규제·컴플라이언스 요구사항을 만족해야 하는 조직의 개발팀
- 규제/보안 요구사항:
  - GS 인증 기준(34개) 및 ISMS-P 인증 기준(102개) 중, 코드로 검증 가능한 항목을 pytest + 마커로 매핑
  - 법령(개인정보 보호법, 안전성 확보조치 기준)을 고려한 로깅·감사 로그·데이터 마스킹 정책
- 기술 스택:
  - Python 3.12+
  - 패키지/런타임 관리: uv (`pyproject.toml` + `uv.lock`)
  - 테스트: pytest (+ pytest-html, pytest-cov, allure-pytest)
  - 품질: ruff, mypy, pre-commit
  - 선택적 의존성: PostgreSQL(psycopg2), pandas/openpyxl, ff3 (extra 그룹)
- 배포/자동화 환경:
  - GitHub Actions 기반 CI (ubuntu + windows 매트릭스)
  - Makefile 타깃: env, logs, setup, test, lint, format, typecheck, report 등
- 기타 제약 사항:
  - 템플릿 특성상, 애플리케이션 도메인은 고정하지 않고 공통 인프라 레이어(logger, load_config, adapters 등)에 초점을 맞춤
  - `.spec/`를 통해 개별 파일 명세를 관리하고, 코드 변경은 항상 명세 갱신 → 코드 수정 순서를 따름

작성 규칙:
1. 출력은 한국어로 작성해 주세요.
2. 최종 결과물은 `ARCHITECTURE.md` 전체 내용이라고 가정하고, 다음 구조를 따라 주세요:
   - `## 1. 개요 (Overview)`
   - `## 2. 명세의 계층 구조 (Specification Hierarchy)` — Level 1/2/3 설명
   - `## 3. 코드 구조와 패키지`
     - 예: `src/common/`, `src/adapters/`, `scripts/setup/`, `config/`, `tests/`, `.spec/` 등을 표로 정리
   - `## 4. 설정, 보안, 로깅`
     - `.env`, `config/logging.yml`, `documents/LOGGING_POLICY.md` 간 관계와 로깅/감사 로그 정책 개요
   - `## 5. 테스트 전략`
     - unit/integration/e2e 디렉터리 구조, pytest 마커(gs_req, isms, integration, e2e, local_only), `documents/GS_ISMS_TEST_MATRIX.md`와의 매핑 개요
   - `## 6. AI 에이전트와의 협업 가이드`
     - AI-Native Spec-Driven Development를 이 템플릿에 어떻게 적용하는지(Plan → Manifest → Execute → Verify)
     - `.spec/src/common/logger.md`, `.spec/src/adapters/database.md`, `.spec/scripts/setup/setup_env.md`, `.spec/tests/...` 등 대표적인 Level 2 명세 예시 포함
3. 이미 어느 정도 구현이 존재하지만, 이 프롬프트에서는 “이 템플릿이 지향하는 이상적인 구조와 책임”을 기준으로 설명해 주세요.
4. `.spec/` 폴더에서 어떤 파일들에 대해 Level 2 명세서를 둘지, 대표적인 매핑 예시(3~10개)를 포함해 주세요.
5. 문서는 200줄 이내로 유지하고, 이후 IDE 에이전트가 수정·확장하기 쉽게 섹션 구조를 명확히 해 주세요.

위 요구사항을 모두 반영하여, 바로 사용할 수 있는 `ARCHITECTURE.md` 초안을 생성해 주세요.
```

