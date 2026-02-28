# Git 태그와 GitHub 릴리스 사용 가이드

GitHub에서 **Release** 탭에 보이는 버전은 **Git 태그(tag)**를 기준으로 합니다.  
태그를 만들고 푸시하면, GitHub에서 그 태그로 **Release**를 만들 수 있습니다.

---

## 1. 태그란?

- **커밋에 붙이는 이름** (예: `v1.0.0`). 특정 시점을 “이 버전”으로 고정할 때 씁니다.
- 한 번 푸시한 태그는 **바꾸지 않는 것**이 원칙입니다(릴리스 버전 불변).

---

## 2. 버전 번호 규칙 (권장)

**시맨틱 버저닝(Semantic Versioning)**을 많이 씁니다.

- `v1.0.0` — 메이저.마이너.패치
- **메이저**: 하위 호환 깨지는 변경
- **마이너**: 하위 호환 유지 기능 추가
- **패치**: 버그 수정 등

이 프로젝트 `pyproject.toml` 버전은 `0.1.0`이므로, 첫 태그는 예를 들어 `v0.1.0`으로 맞추면 됩니다.

---

## 3. 로컬에서 태그 만들기

### lightweight 태그 (이름만)

```bash
# 현재 HEAD에 태그
git tag v0.1.0

# 특정 커밋에 태그
git tag v0.1.0 <커밋해시>
```

### annotated 태그 (권장 — 메시지·날짜·서명 가능)

```bash
git tag -a v0.1.0 -m "Release 0.1.0: 초기 템플릿"
```

- GitHub Release와 함께 쓸 때는 **annotated**를 쓰면 버전 설명으로 활용하기 좋습니다.

### 태그 목록 보기

```bash
git tag -l
git tag -l "v0.*"
```

### 태그 삭제 (아직 푸시 안 했을 때만 권장)

```bash
git tag -d v0.1.0
```

---

## 4. GitHub로 태그 푸시하기

```bash
# 태그 하나 푸시
git push origin v0.1.0

# 로컬 태그 전부 푸시
git push origin --tags
```

- 푸시된 태그는 GitHub 저장소 **Code → 태그 목록**과 **Releases**에서 볼 수 있습니다.

---

## 5. GitHub에서 Release 만들기

1. GitHub 저장소 → **Releases** → **Create a new release**
2. **Choose a tag**에서 방금 푸시한 태그(예: `v0.1.0`) 선택
   - 아직 태그가 없으면 **+ Create new tag**로 새 태그를 만들 수도 있음(그러면 해당 커밋에 태그가 생김).
3. **Release title**: 예) `v0.1.0` 또는 `Release 0.1.0`
4. **Describe this release**: 변경 사항, 설치 방법 등 입력
5. **Publish release** 클릭

이후 해당 Release가 **Releases** 탭에 고정되고, “v0.1.0 시점의 코드”로 다운로드·참조할 수 있습니다.

---

## 6. 이 저장소에서 한 번에 해보기 (예시)

현재 `pyproject.toml` 버전이 `0.1.0`이라면:

```bash
# 1. 작업 디렉터리 깨끗한지 확인 후
git status

# 2. annotated 태그 생성
git tag -a v0.1.0 -m "Release 0.1.0: py-template 초기 버전"

# 3. 원격에 푸시
git push origin v0.1.0
```

그 다음 GitHub 웹에서 **Releases → Create a new release**로 들어가서 태그 `v0.1.0`을 선택하고 설명을 채운 뒤 Publish하면 됩니다.

---

## 7. 주의사항

- **이미 푸시한 태그**는 보통 수정/삭제하지 않습니다. 잘못 만들었으면 새 버전 번호(예: `v0.1.1`)로 다시 태그하는 것이 안전합니다.
- **pyproject.toml의 `version`**과 태그 버전(예: `v0.1.0`)을 맞춰 두면, “어떤 소스가 어떤 릴리스인지” 추적하기 쉽습니다.

---

## 8. 요약

| 하고 싶은 일 | 명령 |
|--------------|------|
| 현재 커밋에 버전 태그 붙이기 | `git tag -a v0.1.0 -m "Release 0.1.0"` |
| 태그를 GitHub에 올리기 | `git push origin v0.1.0` |
| GitHub에서 릴리스 노트 작성 | Releases → Create new release → 태그 선택 후 작성 |

이렇게 하면 GitHub에서 “release 버전 + 태그”를 보고 사용하는 방식과 동일하게 사용할 수 있습니다.
