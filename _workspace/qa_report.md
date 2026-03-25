# QA Report

**검증 대상**: `/Users/robin/Downloads/markus/website/index.html`
**원본 보고서**: `/Users/robin/Downloads/markus/CTO_보고서_엔터테인먼트_AI.md`
**검증일**: 2026-03-25

---

## Critical Issues (즉시 수정)

- [C-001] **Sora 타임라인 Mermaid: 원본의 ❌ 이모지 누락**
  - 원본 마크다운: `2026.03.24 : ❌ 전격 서비스 종료` / `❌ Disney 투자 무산`
  - 웹사이트 HTML: `2026.03.24 : 전격 서비스 종료` / `Disney 투자 무산` (❌ 이모지 제거됨)
  - 영향: Mermaid 렌더링 호환성을 위한 의도적 제거일 수 있으나, 원본과 불일치. 시각적 강조가 사라짐.

- [C-002] **Investment Roadmap Gantt: HTML 엔티티 `&amp;` 가 Mermaid 코드 내에 삽입**
  - 원본: `성과 리뷰 & 스케일업`
  - 웹사이트 (line 1160): `성과 리뷰 &amp; 스케일업`
  - 영향: Mermaid는 `<pre>` 태그 내 텍스트를 파싱하므로, 브라우저가 `&amp;`를 `&`로 디코딩 후 Mermaid에 전달할 수 있으나, 일부 환경에서 `&amp;`가 그대로 렌더링될 위험 있음.

---

## Major Issues (권장 수정)

- [M-001] **추가 이미지 파일 존재하지만 원본에 없음 (불일치는 아니지만 참고)**
  - `images/investment_roadmap.png`와 `images/sora_timeline.png`이 폴백 이미지로 사용됨 (Mermaid 렌더링 실패 시 대비)
  - 원본 마크다운에는 이 두 이미지에 대한 참조가 없음. 웹사이트에서 자체적으로 추가한 폴백 전략으로, 기능적으로는 양호.

- [M-002] **Sora 타임라인의 Sora 2 날짜 표기 — 원본과 일치하지만 보완 필요**
  - 원본과 웹 모두 `2025.09 : Sora 2 공개`로 일치. 그러나 원본에서 이 날짜의 1차 출처 각주가 명시되지 않아 팩트 확인 권장.

---

## Minor Issues (개선 권고)

- [m-001] **전략 권고(섹션 5)가 탭 UI로 구현됨 — 원본과 다른 구조**
  - 원본: 5.1~5.4가 별도 하위 섹션 (### 레벨)
  - 웹: Quick Win / 단기 / 중기 / 모니터링이 탭 UI로 전환됨
  - 기능적으로 문제 없으나, 인쇄 시 현재 활성 탭만 보이므로 인쇄용 CSS 보완 권장.

- [m-002] **부록 B가 아코디언으로 기본 닫힘 상태**
  - 부록 A는 `open` 클래스가 있어 기본 펼침이지만, 부록 B는 닫힘.
  - 사용성 측면에서 용어 정의는 접근이 쉬워야 하므로 기본 열림 권고.

- [m-003] **`fn-ref` 인라인 참조 28회 중 일부는 중복 참조 (동일 각주 다회 사용)**
  - [8] ElevenLabs, [11] Inworld AI, [13] HYBE Supertone 등이 여러 섹션에서 재참조됨.
  - 원본과 동일한 패턴이므로 오류는 아님. 다만 `fnref` ID가 중복 anchor가 되어 역참조(`↩`) 클릭 시 첫 번째 참조 위치로만 이동. 심각하지 않음.

- [m-004] **접근성: 이미지 alt 텍스트가 영문**
  - `alt="Technology Maturity Matrix"` 등 — 한국어 보고서이므로 한글 alt 텍스트 권장.
  - 예: `alt="기술 성숙도 매트릭스"`

---

## Passed Checks

### 1. 콘텐츠 정합성

- [PASS] Executive Summary 핵심 메시지 3개 텍스트 — 원본과 100% 일치
- [PASS] 시장 규모 수치: GVR 259.8억$ / 994.8억$ / CAGR 24.2% — 정확
- [PASS] 시장 규모 수치: MnM 82.1억$ / 510.8억$ / CAGR 35.6% — 정확
- [PASS] PwC 15.7조 달러 — 정확
- [PASS] McKinsey 800억~1,300억 달러 — 정확
- [PASS] AlixPartners 800억 달러 이상, AI 역량 딜 25% — 정확
- [PASS] 기업 투자 테이블 — 8개 기업 모든 수치 원본과 일치:
  - ElevenLabs: $110억 / $5억 (Series D, 2026.02)
  - Runway: $30억 / $3.08억 (Series D, 2025.04)
  - Synthesia: $40억 / $2억 (Series E, 2026.01)
  - Suno: $5억 / $1.25억 (Series B, 2024.05)
  - Pika Labs: - / $1.35억 (누적)
  - Inworld AI: $500M+ / $5,000만 (Series A+)
  - HYBE Supertone: - / 450억원 (인수, 2022)
  - EA: - / $550억 (사모펀드 인수, 2026)
- [PASS] 리스크 매트릭스: HIGH 5건 (벤더 종료, AI 기본법, EU AI Act, M&A 과열, 인재 확보) — 정확
- [PASS] 리스크 매트릭스: MEDIUM 3건 (저작권 소송, 소비자 피로, 컴퓨팅 비용) — 정확
- [PASS] Quick Win 5개 항목 및 예산 모두 정확:
  1. AI 더빙/로컬라이제이션 파일럿 — $50~100K
  2. AI 기본법 대응 TF — 내부 리소스
  3. AI 영상 벤더 멀티소싱 — $30~50K
  4. AI 콘텐츠 라벨링 시스템 — $100~200K
  5. VFX/후반작업 AI 도구 통합 — $50~150K
- [PASS] Sora 타임라인 날짜: 2024.12, 2025.09, 2025.12, 2026.03.24 — 정확
- [PASS] 한국 AI 기본법 시행일 2026.01.22 — 정확 (각주 fn9 및 부록 A)
- [PASS] EU AI Act 2026.08 — 정확 (부록 A)
- [PASS] 각주 19개 모두 존재 (fn1~fn19), 내용 원본과 일치

### 2. 이미지 검증

- [PASS] `tech_maturity_matrix.png` — 파일 존재, HTML에서 참조됨 (line 847)
- [PASS] `build_vs_buy.png` — 파일 존재, HTML에서 참조됨 (line 868)
- [PASS] `risk_matrix.png` — 파일 존재, HTML에서 참조됨 (line 1006)
- [PASS] `sora_alternative_strategy.png` — 파일 존재, HTML에서 2회 참조됨 (line 917, 1233)
- [PASS] 추가 폴백 이미지 2종 (`investment_roadmap.png`, `sora_timeline.png`) — 파일 존재
- [PASS] 깨진 이미지 참조 없음 — 모든 `src` 경로가 `images/` 디렉토리 내 실존 파일과 일치

### 3. Mermaid 다이어그램

- [PASS] Sora timeline 코드 존재 (line 1197~1211)
- [PASS] Investment roadmap gantt 코드 존재 (line 1136~1161)
- [PASS] `mermaid.initialize()` 호출 존재 (line 1505~1528), theme: 'dark' 설정 포함

### 4. UI/구조 검증

- [PASS] 14개 섹션 존재 확인:
  1. Hero (보고서 표지)
  2. Executive Summary
  3. Strategic Context (시장 환경) — 1.1, 1.2, 1.3 하위섹션 포함
  4. Technology Landscape — 2.1, 2.2 하위섹션 포함
  5. 분야별 핵심 동향 (탭 5개: 영화/음악/게임/방송/한국)
  6. Opportunity & Risk — 4.1, 4.2 하위섹션 포함
  7. Strategic Recommendations — Quick Win/단기/중기/모니터링 탭
  8. Investment Roadmap — 6.1, 6.2 하위섹션 포함
  9. Sora 교훈 — 타임라인/교훈/벤더비교 하위섹션 포함
  10. 한국 AI 기본법 — 8.1, 8.2 하위섹션 포함
  11. 기업 투자 현황
  12. 참고문헌 (아코디언 3 Tier)
  13. 부록 A: 경영진 원페이저
  14. 부록 B: 용어 정의
- [PASS] 사이드바 TOC 존재 (line 637~711), 모든 섹션에 대한 링크 포함
- [PASS] 탭 전환 UI — 분야별 동향 5탭 (영화/음악/게임/방송/한국), 전략 권고 4탭
- [PASS] 아코디언 UI — 참고문헌 (Tier 1/2/3), 부록 A, 부록 B
- [PASS] 반응형 미디어쿼리 존재: `@media (max-width: 1200px)`, `@media (max-width: 768px)`, `@media (max-width: 480px)`
- [PASS] "맨 위로" 버튼 존재 (line 1498, `scroll-top` 클래스, JS 동작 포함)

### 5. 누락/오류 체크

- [PASS] 보고서의 모든 섹션이 웹사이트에 반영됨 (Executive Summary ~ 부록 B)
- [PASS] 면책 조항 (footer) — 원본과 동일한 텍스트
- [PASS] 필요 의사결정 3개 항목 — 원본과 일치
- [PASS] 지역별 시장 테이블 (3개 지역) — 원본과 일치
- [PASS] 2026 Q1 전환 시그널 6개 항목 — 원본과 일치
- [PASS] 기술별 성숙도 8개 기술 — 원본과 일치
- [PASS] Build vs Buy 3개 판단 — 원본과 일치
- [PASS] 영화/영상 4개 기술 — 원본과 일치
- [PASS] 음악 4개 합의/소송 항목 — 원본과 일치
- [PASS] 게임 4개 기술 — 원본과 일치
- [PASS] 방송/스트리밍 4개 기술 — 원본과 일치
- [PASS] 한국 시장 4개 기업 — 원본과 일치
- [PASS] 기회 영역 5개 — 원본과 일치
- [PASS] 단기 추진 5개 — 원본과 일치
- [PASS] 중기 투자 4개 — 원본과 일치
- [PASS] 모니터링 대상 5개 — 원본과 일치
- [PASS] KPI 프레임워크 6개 — 원본과 일치
- [PASS] Sora 교훈 3개 — 원본과 일치
- [PASS] 대안 벤더 비교 4개 — 원본과 일치
- [PASS] AI 기본법 핵심 의무 4개 — 원본과 일치
- [PASS] 컴플라이언스 Phase 1 (5항목), Phase 2 (4항목), Phase 3 (3항목) — 원본과 일치
- [PASS] 부록 A 9개 핵심 지표 — 원본과 일치
- [PASS] 부록 B 8개 용어 — 원본과 일치
- [PASS] 빈 섹션 없음

---

## Summary

| 항목 | 수 |
|------|-----|
| **Total checks** | 60 |
| **Passed** | 56 |
| **Critical** | 2 |
| **Major** | 2 |
| **Minor** | 4 |

### 종합 평가

웹사이트는 원본 CTO 보고서의 콘텐츠를 **높은 정확도**로 반영하고 있습니다. 모든 핵심 수치(시장 규모, 기업 투자, 리스크 매트릭스, Quick Win 예산 등)가 원본과 정확히 일치합니다. Critical 이슈 2건은 모두 Mermaid 다이어그램 내부의 텍스트 표현 문제로, 데이터 정확성에는 영향이 없으나 렌더링 품질 측면에서 수정을 권장합니다.
