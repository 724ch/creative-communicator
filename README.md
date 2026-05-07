# Creative Communicator — Lineage Series

크리에이티브 커뮤니케이터의 인지 회로를 사상사로 거슬러 추적하는 9-Part 딥 리포트 시리즈의 인덱스 페이지 + 9개 리포트.

---

## 폴더 구조

```
creative-communicator/
├── index.html         ← 빌드 결과 (직접 편집 X)
├── index.md           ← 편집 대상 (수정하면 빌드해서 반영)
├── _template.html     ← HTML 골격·CSS (디자인 시스템 변경 시 편집)
├── build.py           ← index.md → index.html 빌드 스크립트
├── README.md          ← 이 문서
└── reports/
    ├── advertising-history-report-v2.html   (Part I)
    ├── copywriting-frameworks-report-v2.html (Part II)
    ├── brain-science-creative-report-v2.html (Part III)
    ├── perception-communication-report-v2.html (Part IV)
    ├── modern-epistemology-lineage-v2.html  (Part V)
    ├── reasoning-lineage-report-v2.html     (Part VI)
    ├── spacetime-schema-lineage-v2.html     (Part VII)
    ├── part8-bauhaus-design-history.html    (Part VIII)
    └── part9-typography-archetypes.html     (Part IX)
```

---

## 워크플로우

### 1. 인덱스 콘텐츠 수정

`index.md`를 옵시디언이나 임의의 에디터로 열어 수정한다.

### 2. 빌드 실행

터미널에서:

```bash
cd ~/Desktop/creative-communicator
python3 build.py
```

성공 시:
```
✓ Built index.html (26,898 bytes · 9 reports)
```

### 3. 브라우저 새로고침

`index.html`을 브라우저에서 열어두었다면 새로고침으로 바로 반영 확인.

---

## index.md 작성 규칙

### Frontmatter (메타)

상단 `---` 사이에 시리즈 메타 정보. 키:값 형식.

```yaml
---
title: 페이지 타이틀(브라우저 탭)
hero_kicker: 상단 라벨
hero_tagline: 영문 부제
meta_author: 정찬휘 · Chanhwi Jeong
footer_copy: © 2026 · ...
footer_version: INDEX · v1.0 · ...
---
```

### 섹션 구조

본문은 `# SECTION` 단위로 분리:

- `# HERO` — 첫 화면 (H1, Lead)
- `# ABOUT` — 시리즈 소개 + 2 카드
- `# PRINCIPLES` — 디자인 원칙 3 카드
- `# REPORTS` — 9 Part 카드 그리드 ★
- `# THREADS` — 5 메타 스레드
- `# COLOPHON` — 작업 방법론 6 row + commit-box
- `# FOOTER` — 푸터 3열

### 서브섹션 (`##`)

각 섹션 안에서 `##` 로 카드/구성 요소 분리. 예:

```markdown
# REPORTS

## H2
아홉 개의 <em>인지 부품</em>

## Lead
각 리포트는 단독으로 ...

## Part I
- color: yellow
- date: 2026-04-17
- file: reports/advertising-history-report-v2.html
- title: 광고사 & 카피 역사
- sub: Advertising · From Myth to Algorithm
- meta: 5 PHASES · 6 THREADS

신화·종교·산업혁명·매스미디어·디지털·AI까지 — 광고가 **인간을 학습해온 200년**의 사상사. ...
```

### 메타 키 형식

`- key: value` (대시 + 공백 + 키 + 콜론). 메타 라인 다음에 빈 줄을 두고 본문 시작.

### 마크다운 규칙

지원되는 인라인 문법:
- `**bold**` → `<strong>bold</strong>`
- `[text](url)` → 외부 링크 (자동 새 탭)
- `<em>...</em>`, `<br/>` 등 인라인 HTML 그대로 보존

빈 줄로 분리된 단락은 `<p>...</p>`로 자동 처리.

---

## 새 Part 추가하는 법

1. 새 리포트 HTML을 `reports/` 폴더에 복사
2. `index.md`의 `# REPORTS` 섹션 끝에 새 카드 블록 추가:

```markdown
## Part X
- color: teal      # yellow / pink / teal / purple / blue / green / red / accent / dark 중
- date: 2026-MM-DD
- file: reports/your-report-filename.html
- title: 리포트 제목
- sub: Subtitle in English
- meta: N PHASES · 6 THREADS
- star: true       # 최신 Part에만 (선택)

핵심 명제 한 단락. **bold**와 인라인 HTML 사용 가능.
```

3. `python3 build.py` 실행

---

## 컬러 코드 (border-top)

| 값 | 색 |
|----|-----|
| `yellow` | 머스타드 |
| `pink` | 다홍 |
| `teal` | 청록 |
| `purple` | 보라 |
| `blue` | 청 |
| `green` | 녹 |
| `red` | 적 |
| `accent` | 오렌지 (시리즈 메인) |
| `dark` | 검정 (강조용) |

---

## 디자인 시스템 변경

CSS 토큰·간격·폰트는 `_template.html` 의 `<style>` 블록에서 편집. 그 후 빌드.

`:root` 블록의 변수만 바꿔도 시리즈 전체 톤이 변경된다 (현재 라이트 BRAUN 톤).

---

## 정직한 한계

이 시리즈는 인간 큐레이션 + AI 리서치 협업으로 만들어졌다. 자세한 작업 방법론과 갱신 정책은 인덱스 페이지의 **05 · Colophon** 섹션에 명시.

---

## License

교육·학습·인용 자유. 상업 전재는 사전 협의. 자세한 내용은 인덱스 Colophon 참조.
