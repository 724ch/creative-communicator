# SVG Diagram Standard · Creative Communicator Series

**버전:** v1.0 · 2026-05-07
**도입 시점:** Part XII 신체화 인식 계보의 9개 schema를 ASCII → SVG 변환하면서 정립.
**적용 범위:** 모든 시리즈 리포트의 `SCHEMA · 머릿속 그림` 블록.

---

## 0. 도입 이유

기존 ASCII 도식의 문제:
- 모바일 가로폭에서 박스가 깨지거나 잘림
- 모노스페이스 폰트가 한글과 어울리지 않음
- 박스·선·화살표가 텍스트 글자라 색·두께 변형이 제한적

SVG로 가면:
- 반응형 (`width: 100%`, `viewBox` 비율 유지)
- 시리즈 색·폰트 시스템 그대로
- 박스 위계·강조가 명확
- 인쇄·공유에서도 깨끗

---

## 1. 외곽 컨테이너

기존 `.schema` 블록을 인라인 스타일로 SVG 모드 전환:

```html
<div class="schema" style="white-space: normal; padding: 32px; text-align: center;">
  <div style="font-family: 'JetBrains Mono', monospace; font-size: 11px; letter-spacing: 0.3em; color: var(--text); margin-bottom: 8px; text-transform: uppercase;">DIAGRAM TITLE</div>
  <div style="font-size: 13px; color: var(--text-dim); margin-bottom: 24px;">부제 (한글)</div>
  <svg viewBox="0 0 800 [높이]" xmlns="http://www.w3.org/2000/svg"
       style="width: 100%; height: auto; max-width: 800px;"
       font-family="'Noto Sans KR', sans-serif" fill="#1a1a1a">
    <!-- diagram contents -->
  </svg>
</div>
<div class="schema-cap">CAPTION · ENGLISH</div>
```

핵심 — `white-space: normal`로 부모의 `pre`를 무력화 + `text-align: center`로 SVG 가운데. 그 외 다른 `.schema` 속성(배경 `var(--bg-code)` · border) 그대로 작동.

---

## 2. 색상 팔레트 (시리즈 표준)

| 토큰 | HEX | 용도 |
|---|---|---|
| `#1a1a1a` | text | 본문·기본 stroke |
| `#4a4845` | text-soft | 부가 설명 |
| `#807e7a` | text-dim | 캡션·메타 라벨 |
| `#c4c2bd` | text-faint | 분리선 |
| `#d9601f` | accent | 핵심 강조 (시리즈 시그니처) |
| `#2e8a7c` | teal | 대비/평행 |
| `#7e5a98` | purple | 사상/분류 |
| `#4a72a8` | blue | 시간/흐름 |
| `#4a8e4a` | green | 결과/공명 |
| `#b8954a` | yellow | 고대/기원 |
| `#c25787` | pink | 살/감각 |
| `#c14638` | red | 위험/마비 |

**박스 채우기 4단계:**
- **강조 박스** — `rgba(217,96,31,0.10)` 채우기 + `#d9601f` 1.8px stroke
- **결론·인용 박스** — `rgba(217,96,31,0.06)` + 1.5px stroke
- **일반 박스** — `#fff` 채우기 + `#1a1a1a` 또는 컬러 1.5px stroke
- **약한 박스** — `#f8f6f1` 채우기 + `#807e7a` 1px stroke

**화살표·라인:**
- 메인 화살표: `#1a1a1a` 1.5px
- 컬러 화살표 (강조 흐름): 해당 컬러 1.5px
- 점선 (평행·대비): `stroke-dasharray="4,3"` 또는 `"2,3"`
- 약한 분리선: `#c4c2bd` 1px stroke-dasharray="2,3"

---

## 3. 폰트 시스템

```
Noto Sans KR        — 본문 한글 (기본)
JetBrains Mono      — 라벨·메타 (letter-spacing: 0.2~0.3em + uppercase)
Nanum Myeongjo      — 인용·시적 강조 (font-style: italic)
Playfair Display    — 외래어·라틴 강조 (font-style: italic)
```

**크기 가이드:**
- 박스 안 큰 제목: 15-17px / font-weight: 700
- 박스 안 부제: 12-13px / fill: #807e7a
- 메타 라벨: 11px / JetBrains Mono / letter-spacing: 0.2-0.3em / uppercase
- 본문 텍스트: 13-14px
- 결론 텍스트: 14-16px

---

## 4. 5가지 패턴 컴포넌트

### 4.1 분기 (BRANCH) — 1 → N
**예시:** 스피노자 두 속성 / 소크라테스 두 길

```
        [SOURCE]
            │
    ┌───────┴───────┐
    ↓               ↓
  [LEFT]        [RIGHT]
    │               │
    ↓               ↓
  결과 1          결과 2
```

핵심 — 분기점에서 가로로 한 줄 그은 후 두 갈래 ↓.

### 4.2 합치 (MERGE) — N → 1
**예시:** 메를로퐁티 살 (FLESH가 SUBJECT/OBJECT로 분기 후 V로 다시 모임)

좌우에서 사선이 가운데로 모임. 점선 사용해서 "한 직물" 같은 결과 박스로.

### 4.3 좌우 비교 (CONTRAST) — A | B
**예시:** 칸트 기존 vs 전환 / 후설 Körper vs Leib / 다마지오 데카르트 vs 다마지오

좌우 두 컬럼. 각각 같은 단계 흐름. 색상으로 차별화 (좌=회색/플레인, 우=액센트).

상단 라벨 두 개 + `<line>` 가로선으로 구분.

### 4.4 흐름 (FLOW) — 1 → 2 → 3 → ...
**예시:** 다마지오 정상인 vs 환자 4단계 / 4E Embedded 같은 단계

박스 → ↓ → 박스 → ↓ → 박스. 각 ↓는 1.5px stroke + 작은 화살촉.

수직 흐름 또는 수평 흐름 (들뢰즈 표상 모델: 세계 → 망막 → 뇌 → 표상).

### 4.5 카탈로그 (CATALOG) — 1, 2, 3, 4, 5
**예시:** 라코프 5 은유 / 메를로퐁티 신체 도식 3 사례

같은 폭 박스를 세로로 나열 + 각 박스 좌측에 번호 원 (`circle r=16`).

### 4.6 동심원 (NESTED) — 4E Cognition 결론
4겹 원 — `rgba(*,0.04~0.18)` 채우기로 안쪽일수록 진하게. 라벨은 위쪽에서 바깥→안.

---

## 5. 화살표 글리프

**스탠다드 위 → 아래 화살표:**
```svg
<path d="M [x] [y_top] L [x] [y_bottom]" stroke="#1a1a1a" stroke-width="1.5"/>
<path d="M [x] [y_bottom] L [x-5] [y_bottom-8] M [x] [y_bottom] L [x+5] [y_bottom-8]"
      stroke="#1a1a1a" stroke-width="1.5" fill="none"/>
```

**좌 ↔ 우 양방향 (점선):**
```svg
<path d="M [x1] [y] L [x2] [y]" stroke="#1a1a1a" stroke-width="1.5" stroke-dasharray="4,3"/>
<!-- 양쪽 화살촉 -->
<path d="M [x1] [y] L [x1+8] [y-4] M [x1] [y] L [x1+8] [y+4]" .../>
<path d="M [x2] [y] L [x2-8] [y-4] M [x2] [y] L [x2-8] [y+4]" .../>
```

---

## 6. 결론 박스 (필수 요소)

거의 모든 schema의 마지막에:
```svg
<rect x="60" y="[y]" width="680" height="80~120"
      fill="rgba(217,96,31,0.06)" stroke="#d9601f" stroke-width="1.5" rx="3"/>
<text x="400" y="[y+28]" text-anchor="middle"
      font-family="'JetBrains Mono', monospace" font-size="11" letter-spacing="3" fill="#d9601f">결론</text>
<text x="400" y="[y+58]" text-anchor="middle" font-size="14~16">결론 본문</text>
```

라벨은 `결론` / `의미` / `중요` / `DECISIVE PROPOSITION` 등.

---

## 7. ViewBox 가이드

- **너비:** 항상 800 (최대 가로 폭)
- **높이:** 도식 복잡도에 따라 400-1100. 한 화면(viewport)에 다 안 들어와도 됨 — 모바일에서 자연 스크롤.
- **여백:** 좌우 60-80px, 위아래 20-32px

---

## 8. 적용 진행 상황

- [x] **Part XII** 신체화 인식 계보 (9 schemas) — 2026-05-07 완료
- [ ] Part XIII 기억·시간·공간 (예상 6 schemas)
- [ ] Part XI 창작자의 9가지 동작
- [ ] Part X 수학적 사고의 7가지 동작
- [ ] Part IX 타이포그래피 아키타입
- [ ] Part VIII 디자인사 & 바우하우스
- [ ] Part VII 시간과 공간의 스키마
- [ ] Part VI 추론의 계보
- [ ] Part V 현대사상 인식론 계보
- [ ] Part XXI 무카이 〈디자인학〉
- [ ] (그 외 Part I~IV, XIV~XX는 schema 유무 검토 후 진행)

각 리포트 처리 후 이 체크리스트 갱신.

---

## 9. 새 리포트 작성 시 (Lineage 스킬 가이드)

`/lineage` 스킬로 새 리포트를 만들 때:

1. SCHEMA 블록은 **처음부터 SVG로** 작성. ASCII 단계 건너뛰기.
2. 위 5가지 패턴 중 적합한 것 골라 — viewBox 0 0 800 [높이], 컨테이너는 §1 그대로.
3. 색상은 §2 토큰 그대로, 컬러 클래스 매핑은 (분기/평행=teal·purple, 흐름=blue, 결과=green, 핵심=accent).
4. 결론 박스(§6) 필수.
5. 캡션 `<div class="schema-cap">` 유지.

이 표준은 시리즈 일관성의 한 부분이다 — 같은 타이포·같은 색·같은 박스 위계가 다른 리포트에서 만나면 시리즈가 한 작가의 작업처럼 보인다.
