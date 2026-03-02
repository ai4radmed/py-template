# 명세서: `src/adapters/__init__.py`

## 역할
- 외부 시스템 연동 모듈들을 묶는 `adapters` 패키지 네임스페이스를 정의한다.
- 주요 하위 모듈은 데이터베이스(`database`), 엑셀 입출력(`excel_io`), FF3 암호화 유틸(`get_cipher`) 이다.

## 핵심 규칙
- 패키지 자체는 임포트 시 부수 효과를 가지지 않고, 설명용 도큐멘테이션 수준에 머문다.
- 각 어댑터 모듈은 선택적 의존성(extras)에 의존하므로, 사용 시 `py-template[db]`, `py-template[excel]`, `py-template[cipher]` 와 같이 필요한 extra 만 설치한다.
