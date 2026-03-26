# UX 리디자인 스펙

> 작성: ux-designer | 대상: `docs/index.html`
> 원칙: 기존 HTML 구조 유지, 외부 라이브러리 없음, CSS/Vanilla JS, 성능 우선

---

## 1. 현재 상태 분석

### 문제점 요약

| 영역 | 현재 상태 | 문제점 |
|------|----------|--------|
| **네비게이션** | 단색 `#1e293b` 사이드바, `border-left` active 표시 | 깊이감 없음, 스크롤 진행률 없음, 활성 상태 시각적 피드백 미흡 |
| **비주얼 디자인** | `linear-gradient(145deg)` 카드, 단순 border | Glass morphism 없음, 카드 간 계층 구분 약함, 섹션 분리가 1px border로만 처리 |
| **인터랙션** | `fade-in` (translateY 20px) 단일 애니메이션, 탭/아코디언 기본 전환 | 방향별 애니메이션 없음, stagger 없음, 숫자 카운트업 없음, 라이트박스 없음 |
| **백그라운드** | `heroPulse` (scale/rotate) 단일 radial-gradient | 히어로 외 섹션은 배경 효과 전무, mesh/particle 없음, 시각적 풍부함 부족 |

### 개선 영역별 상세 분석

**네비게이션 (sidebar, lines 73-121)**
- `.sidebar`는 `background: var(--bg-secondary)`로 완전 불투명 — glass 효과 부재
- `.toc-link.active`는 `border-left-color + background rgba(0.08)` — glow 없음
- 스크롤 진행률 인디케이터 HTML/CSS 모두 없음
- 섹션 카운터 배지 없음

**비주얼 디자인 (cards, sections)**
- `.highlight-card`, `.data-card`는 동일한 `var(--gradient-card)` — 차별화 없음
- 호버 효과는 `translateY(-2px) + box-shadow` — 미약한 피드백
- `.section` divider가 `border-bottom: 1px solid var(--border-default)` — 단조로움
- heading에 장식 요소 없음

**인터랙션 (JS, lines 1597-1673)**
- `IntersectionObserver` 1개로 `.fade-in` 클래스만 처리
- 탭 전환에 슬라이딩 인디케이터 없음 (border-bottom만 사용)
- 이미지(`.report-image`)에 클릭 이벤트 없음
- 숫자 데이터에 카운트업 애니메이션 없음

**백그라운드 (hero, lines 168-187)**
- `heroPulse`만 존재 (radial-gradient 2개, scale 1→1.05)
- 고정 배경 mesh 없음
- floating orb 없음
- 섹션별 배경색 변화 없음

---

## 2. 네비게이션 리디자인

### 2-1. Glass Morphism 사이드바

**Before:** 불투명 `#1e293b` 배경, 단순 `border-right`
**After:** 반투명 glass 배경, blur, 깊은 shadow

```css
/* === NAVIGATION: Glass Sidebar === */
.sidebar {
  /* 기존 var(--bg-secondary) 대체 */
  background: rgba(15, 23, 42, 0.85);
  backdrop-filter: blur(20px) saturate(180%);
  -webkit-backdrop-filter: blur(20px) saturate(180%);
  border-right: 1px solid rgba(148, 163, 184, 0.1);
  box-shadow: 4px 0 24px rgba(0, 0, 0, 0.2);
}
```

### 2-2. 스크롤 진행률 바

**추가할 HTML 요소:**
```html
<div class="scroll-progress" id="scrollProgress"></div>
```
> body 최상단(첫 번째 자식)으로 삽입

**CSS:**
```css
/* === NAVIGATION: Scroll Progress === */
.scroll-progress {
  position: fixed;
  top: 0;
  left: 0;
  width: 0%;
  height: 3px;
  background: linear-gradient(90deg, var(--accent-blue), var(--accent-purple), var(--accent-emerald));
  z-index: 1000;
  transition: width 0.1s linear;
  will-change: width;
  pointer-events: none;
}
```

**JS:**
```javascript
/* === Scroll Progress Bar === */
const scrollProgressBar = document.getElementById('scrollProgress');
window.addEventListener('scroll', function() {
  const scrollTop = document.documentElement.scrollTop;
  const scrollHeight = document.documentElement.scrollHeight - window.innerHeight;
  const progress = scrollHeight > 0 ? (scrollTop / scrollHeight) * 100 : 0;
  scrollProgressBar.style.width = progress + '%';
}, { passive: true });
```

### 2-3. Active Glow 효과

**Before:** `color: var(--accent-blue); border-left-color: var(--accent-blue); background: rgba(59,130,246,0.08)`
**After:** gradient background, inset glow shadow, smoother transition

```css
/* === NAVIGATION: Active Glow === */
.toc-link {
  position: relative;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.5rem 1.5rem;
  color: var(--text-secondary);
  font-size: 0.875rem;
  border-left: 2px solid transparent;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  text-decoration: none;
}

.toc-link:hover {
  color: var(--text-primary);
  background: rgba(148, 163, 184, 0.06);
  padding-left: calc(1.5rem + 4px);
  text-decoration: none;
}

.toc-link.active {
  color: var(--accent-blue-light);
  border-left-color: var(--accent-blue);
  background: linear-gradient(90deg, rgba(59, 130, 246, 0.12), transparent);
  box-shadow: inset 3px 0 8px rgba(59, 130, 246, 0.2);
  font-weight: 500;
}
```

### 2-4. 섹션 카운터 배지

**추가할 HTML:** 각 `.toc-link`(메인 섹션만) 끝에 배지 span 추가
```html
<!-- 예시: 시장 환경 섹션 -->
<a href="#strategic-context" class="toc-link" data-section="strategic-context">
  <span class="toc-icon">📊</span> 시장 환경
  <span class="toc-badge">3</span>
</a>
```

**배지 개수 매핑:**
- Executive Summary: (배지 없음 — 하위 섹션 없음)
- 시장 환경: `3` (글로벌/지역별/전환 시그널)
- 기술 성숙도: `2` (기술별/Build vs Buy)
- 분야별 핵심 동향: `5` (영화/음악/게임/방송/한국)
- 리스크 & 기회: `2`
- 전략 권고: `4`
- 투자 로드맵: `2`
- Sora 교훈: `3`
- 부록/각주: (배지 없음)

**CSS:**
```css
/* === NAVIGATION: Section Badge === */
.toc-badge {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  min-width: 1.25rem;
  height: 1.25rem;
  padding: 0 0.35rem;
  border-radius: 0.625rem;
  background: rgba(59, 130, 246, 0.15);
  color: var(--accent-blue-light);
  font-size: 0.65rem;
  font-weight: 600;
  margin-left: auto;
  transition: all 0.3s ease;
}

.toc-link.active .toc-badge {
  background: rgba(59, 130, 246, 0.25);
  color: #fff;
}
```

---

## 3. 비주얼 디자인 업데이트

### 3-1. 새로운 CSS 변수

```css
/* === VISUAL: Extended CSS Variables === */
:root {
  /* 기존 변수 유지 + 추가 */
  --glass-bg: rgba(30, 41, 59, 0.6);
  --glass-border: rgba(148, 163, 184, 0.08);
  --glass-blur: blur(16px) saturate(180%);

  --gradient-border: linear-gradient(135deg, rgba(59, 130, 246, 0.3), rgba(139, 92, 246, 0.3), rgba(16, 185, 129, 0.3));
  --gradient-accent: linear-gradient(90deg, var(--accent-blue), var(--accent-purple));
  --gradient-divider: linear-gradient(90deg, transparent, rgba(59, 130, 246, 0.3), rgba(139, 92, 246, 0.3), transparent);

  --shadow-card: 0 4px 6px rgba(0, 0, 0, 0.1), 0 10px 40px rgba(0, 0, 0, 0.15);
  --shadow-card-hover: 0 8px 12px rgba(0, 0, 0, 0.15), 0 20px 60px rgba(0, 0, 0, 0.25);
  --shadow-glow-blue: 0 0 20px rgba(59, 130, 246, 0.15);

  --ease-smooth: cubic-bezier(0.4, 0, 0.2, 1);
  --ease-bounce: cubic-bezier(0.34, 1.56, 0.64, 1);
}
```

### 3-2. Glass Card (highlight-card 개선)

**Before:** `background: var(--gradient-card); border: 1px solid var(--border-default)`
**After:** Glass morphism + gradient border on hover + 깊은 shadow

```css
/* === VISUAL: Glass Highlight Card === */
.highlight-card {
  background: var(--glass-bg);
  backdrop-filter: blur(16px) saturate(180%);
  -webkit-backdrop-filter: blur(16px) saturate(180%);
  border: 1px solid var(--glass-border);
  border-radius: 1rem;
  padding: 1.5rem;
  text-align: left;
  position: relative;
  overflow: hidden;
  transition: all 0.4s var(--ease-smooth);
  box-shadow: var(--shadow-card), inset 0 1px 0 rgba(255, 255, 255, 0.05);
}

.highlight-card::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 2px;
  background: var(--gradient-accent);
  opacity: 0;
  transition: opacity 0.3s ease;
}

.highlight-card:hover {
  transform: translateY(-6px);
  box-shadow: var(--shadow-card-hover), inset 0 1px 0 rgba(255, 255, 255, 0.08);
  border-color: rgba(59, 130, 246, 0.2);
}

.highlight-card:hover::before {
  opacity: 1;
}
```

### 3-3. Glass Data Card

```css
/* === VISUAL: Glass Data Card === */
.data-card {
  background: var(--glass-bg);
  backdrop-filter: blur(16px) saturate(180%);
  -webkit-backdrop-filter: blur(16px) saturate(180%);
  border: 1px solid var(--glass-border);
  border-radius: 1rem;
  padding: 1.5rem;
  transition: all 0.4s var(--ease-smooth);
  box-shadow: var(--shadow-card), inset 0 1px 0 rgba(255, 255, 255, 0.05);
}

.data-card:hover {
  transform: translateY(-4px);
  box-shadow: var(--shadow-card-hover);
  border-color: rgba(59, 130, 246, 0.15);
}
```

### 3-4. Gradient Border Card (선택적 — 핵심 카드에 적용)

```css
/* === VISUAL: Gradient Border Card === */
.gradient-border-card {
  position: relative;
  background: var(--bg-secondary);
  border-radius: 1rem;
  padding: 2rem;
}

.gradient-border-card::before {
  content: '';
  position: absolute;
  inset: 0;
  border-radius: 1rem;
  padding: 1px;
  background: var(--gradient-border);
  -webkit-mask: linear-gradient(#fff 0 0) content-box, linear-gradient(#fff 0 0);
  -webkit-mask-composite: xor;
  mask-composite: exclude;
  pointer-events: none;
}
```

### 3-5. 섹션 Divider (그라디언트 구분선)

**Before:** `.section { border-bottom: 1px solid var(--border-default); }`
**After:** 그라디언트 구분선으로 교체

```css
/* === VISUAL: Section Divider === */
.section {
  padding: 4rem 0;
  border-bottom: none; /* 기존 border 제거 */
  position: relative;
}

.section::after {
  content: '';
  position: absolute;
  bottom: 0;
  left: 0;
  right: 0;
  height: 1px;
  background: var(--gradient-divider);
}

.section:last-child::after {
  display: none;
}
```

### 3-6. Heading 장식 (사이드 바)

```css
/* === VISUAL: Section Heading Decoration === */
.section-header h2,
.section > h2 {
  position: relative;
  padding-left: 1rem;
}

.section-header h2::before,
.section > h2::before {
  content: '';
  position: absolute;
  left: 0;
  top: 0.15em;
  bottom: 0.15em;
  width: 4px;
  border-radius: 2px;
  background: linear-gradient(180deg, var(--accent-blue), var(--accent-purple));
}
```

### 3-7. 테이블 행 호버 Glow

```css
/* === VISUAL: Table Row Hover === */
.report-table tr {
  transition: all 0.2s ease;
}

.report-table tbody tr:hover {
  background: rgba(59, 130, 246, 0.04) !important;
  box-shadow: inset 3px 0 0 var(--accent-blue);
}

.report-table tbody tr:hover td {
  background: transparent;
}
```

### 3-8. Risk Badge Pulse

```css
/* === VISUAL: Risk Badge Pulse === */
.risk-high, .risk-red {
  animation: riskPulse 2s ease-in-out infinite;
}

@keyframes riskPulse {
  0%, 100% { box-shadow: 0 0 0 0 rgba(239, 68, 68, 0.2); }
  50% { box-shadow: 0 0 0 4px rgba(239, 68, 68, 0); }
}
```

---

## 4. 인터랙티브 요소

### 4-1. 향상된 스크롤 트리거 애니메이션

기존 `.fade-in` 유지하면서 방향별 + stagger 애니메이션 추가.

**CSS:**
```css
/* === INTERACTIVE: Enhanced Scroll Animations === */

/* 기존 fade-in 개선 */
.fade-in {
  opacity: 0;
  transform: translateY(30px);
  transition: opacity 0.8s var(--ease-smooth),
              transform 0.8s var(--ease-smooth);
  will-change: transform, opacity;
}

.fade-in.visible {
  opacity: 1;
  transform: translateY(0);
  will-change: auto;
}

/* 방향별 reveal */
.reveal-left {
  opacity: 0;
  transform: translateX(-30px);
  transition: opacity 0.8s var(--ease-smooth),
              transform 0.8s var(--ease-smooth);
}

.reveal-right {
  opacity: 0;
  transform: translateX(30px);
  transition: opacity 0.8s var(--ease-smooth),
              transform 0.8s var(--ease-smooth);
}

.reveal-scale {
  opacity: 0;
  transform: scale(0.95);
  transition: opacity 0.8s var(--ease-smooth),
              transform 0.8s var(--ease-smooth);
}

.reveal-left.visible,
.reveal-right.visible,
.reveal-scale.visible {
  opacity: 1;
  transform: none;
}

/* Stagger children (grid/list 내부 요소에 적용) */
.stagger-children > * {
  opacity: 0;
  transform: translateY(20px);
  transition: opacity 0.6s ease, transform 0.6s ease;
}

.stagger-children.visible > *:nth-child(1) { transition-delay: 0.05s; }
.stagger-children.visible > *:nth-child(2) { transition-delay: 0.1s; }
.stagger-children.visible > *:nth-child(3) { transition-delay: 0.15s; }
.stagger-children.visible > *:nth-child(4) { transition-delay: 0.2s; }
.stagger-children.visible > *:nth-child(5) { transition-delay: 0.25s; }
.stagger-children.visible > *:nth-child(6) { transition-delay: 0.3s; }
.stagger-children.visible > *:nth-child(7) { transition-delay: 0.35s; }
.stagger-children.visible > *:nth-child(8) { transition-delay: 0.4s; }

.stagger-children.visible > * {
  opacity: 1;
  transform: translateY(0);
}
```

**JS (기존 fadeObserver 대체):**
```javascript
/* === Enhanced Scroll Animation Observer === */
const revealObserver = new IntersectionObserver(function(entries, obs) {
  entries.forEach(function(entry) {
    if (entry.isIntersecting) {
      entry.target.classList.add('visible');
      obs.unobserve(entry.target); // 성능: 한 번만 트리거
    }
  });
}, { threshold: 0.1, rootMargin: '0px 0px -50px 0px' });

document.querySelectorAll('.fade-in, .reveal-left, .reveal-right, .reveal-scale, .stagger-children')
  .forEach(function(el) { revealObserver.observe(el); });
```

**적용 가이드 (HTML class 추가 위치):**
- `.hero-highlights` → `stagger-children` 추가
- 각 `.data-card` 그리드 컨테이너 → `stagger-children` 추가
- `.table-wrapper` → `reveal-scale` 추가
- `.callout` → `reveal-left` 추가
- `.mermaid-wrapper` → `reveal-scale` 추가
- 기존 `.fade-in` 클래스 유지 (하위 호환)

### 4-2. 카운터 카운트업 애니메이션

**JS:**
```javascript
/* === Counter Count-Up Animation === */
function animateCounter(el) {
  const target = parseFloat(el.dataset.value);
  const suffix = el.dataset.suffix || '';
  const prefix = el.dataset.prefix || '';
  const duration = 2000;
  const start = performance.now();

  function update(now) {
    const elapsed = now - start;
    const progress = Math.min(elapsed / duration, 1);
    const eased = 1 - Math.pow(1 - progress, 3); // ease-out cubic
    const current = target * eased;

    el.textContent = prefix + (Number.isInteger(target)
      ? Math.round(current).toLocaleString()
      : current.toFixed(1)) + suffix;

    if (progress < 1) requestAnimationFrame(update);
  }

  requestAnimationFrame(update);
}

// IntersectionObserver로 뷰포트 진입 시 트리거
const counterObserver = new IntersectionObserver(function(entries, obs) {
  entries.forEach(function(entry) {
    if (entry.isIntersecting) {
      animateCounter(entry.target);
      obs.unobserve(entry.target);
    }
  });
}, { threshold: 0.5 });

document.querySelectorAll('[data-value]').forEach(function(el) {
  counterObserver.observe(el);
});
```

**적용 가이드:** 숫자 데이터 요소에 `data-value`, `data-suffix`, `data-prefix` 속성 추가
```html
<!-- 예시 -->
<span class="card-number" data-value="1840" data-suffix="억$">0</span>
<span class="card-number" data-value="28.6" data-suffix="%">0</span>
```

### 4-3. 이미지 라이트박스

**추가할 HTML (body 끝에):**
```html
<div class="lightbox-overlay" id="lightboxOverlay">
  <img src="" alt="" id="lightboxImage">
</div>
```

**CSS:**
```css
/* === INTERACTIVE: Image Lightbox === */
.report-image {
  cursor: zoom-in;
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.report-image:hover {
  transform: scale(1.02);
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.4);
}

.lightbox-overlay {
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.9);
  backdrop-filter: blur(8px);
  -webkit-backdrop-filter: blur(8px);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 2000;
  opacity: 0;
  pointer-events: none;
  transition: opacity 0.3s ease;
  cursor: zoom-out;
}

.lightbox-overlay.active {
  opacity: 1;
  pointer-events: all;
}

.lightbox-overlay img {
  max-width: 90vw;
  max-height: 90vh;
  border-radius: 0.75rem;
  box-shadow: 0 25px 80px rgba(0, 0, 0, 0.5);
  transform: scale(0.9);
  transition: transform 0.3s var(--ease-smooth);
}

.lightbox-overlay.active img {
  transform: scale(1);
}
```

**JS:**
```javascript
/* === Image Lightbox === */
const lightboxOverlay = document.getElementById('lightboxOverlay');
const lightboxImage = document.getElementById('lightboxImage');

document.querySelectorAll('.report-image').forEach(function(img) {
  img.addEventListener('click', function() {
    lightboxImage.src = this.src;
    lightboxImage.alt = this.alt;
    lightboxOverlay.classList.add('active');
    document.body.style.overflow = 'hidden';
  });
});

lightboxOverlay.addEventListener('click', function() {
  this.classList.remove('active');
  document.body.style.overflow = '';
});

document.addEventListener('keydown', function(e) {
  if (e.key === 'Escape' && lightboxOverlay.classList.contains('active')) {
    lightboxOverlay.classList.remove('active');
    document.body.style.overflow = '';
  }
});
```

### 4-4. 슬라이딩 탭 인디케이터

**CSS:**
```css
/* === INTERACTIVE: Sliding Tab Indicator === */
.tabs {
  position: relative;
  display: flex;
  gap: 0;
  background: rgba(30, 41, 59, 0.5);
  border-radius: 0.75rem;
  padding: 0.25rem;
  border: 1px solid rgba(148, 163, 184, 0.1);
  border-bottom: none;
  margin-bottom: 1.5rem;
  overflow-x: auto;
}

.tab-btn {
  position: relative;
  z-index: 1;
  padding: 0.6rem 1.2rem;
  border-radius: 0.5rem;
  border: none;
  background: transparent;
  color: var(--text-secondary);
  font-size: 0.875rem;
  font-weight: 500;
  cursor: pointer;
  transition: color 0.3s ease;
  white-space: nowrap;
  font-family: inherit;
  border-bottom: none;
}

.tab-btn:hover {
  color: var(--text-primary);
}

.tab-btn.active {
  color: var(--text-primary);
  border-bottom-color: transparent;
}

.tab-indicator {
  position: absolute;
  bottom: 0.25rem;
  height: calc(100% - 0.5rem);
  background: rgba(59, 130, 246, 0.15);
  border-radius: 0.5rem;
  transition: left 0.3s var(--ease-smooth),
              width 0.3s var(--ease-smooth);
  pointer-events: none;
}
```

**JS (기존 탭 JS 수정):**
```javascript
/* === Sliding Tab Indicator === */
document.querySelectorAll('.tabs').forEach(function(tabsContainer) {
  // 인디케이터 요소 동적 생성
  const indicator = document.createElement('div');
  indicator.className = 'tab-indicator';
  tabsContainer.style.position = 'relative';
  tabsContainer.appendChild(indicator);

  const buttons = tabsContainer.querySelectorAll('.tab-btn');
  const parent = tabsContainer.parentElement;

  function moveIndicator(activeBtn) {
    indicator.style.left = activeBtn.offsetLeft + 'px';
    indicator.style.width = activeBtn.offsetWidth + 'px';
  }

  // 초기 위치
  const initialActive = tabsContainer.querySelector('.tab-btn.active');
  if (initialActive) moveIndicator(initialActive);

  buttons.forEach(function(btn) {
    btn.addEventListener('click', function() {
      var tabId = this.getAttribute('data-tab');

      buttons.forEach(function(b) { b.classList.remove('active'); });
      parent.querySelectorAll('.tab-content').forEach(function(c) { c.classList.remove('active'); });

      this.classList.add('active');
      moveIndicator(this);
      var target = document.getElementById(tabId);
      if (target) target.classList.add('active');
    });
  });
});
```

### 4-5. 툴팁 (CSS only)

```css
/* === INTERACTIVE: Tooltip === */
[data-tooltip] {
  position: relative;
  cursor: help;
}

[data-tooltip]::after {
  content: attr(data-tooltip);
  position: absolute;
  bottom: calc(100% + 8px);
  left: 50%;
  transform: translateX(-50%) translateY(4px);
  padding: 0.5rem 0.75rem;
  background: rgba(15, 23, 42, 0.95);
  backdrop-filter: blur(8px);
  border: 1px solid rgba(148, 163, 184, 0.15);
  border-radius: 0.5rem;
  font-size: 0.8rem;
  color: var(--text-secondary);
  white-space: nowrap;
  opacity: 0;
  pointer-events: none;
  transition: opacity 0.2s ease, transform 0.2s ease;
  z-index: 500;
}

[data-tooltip]:hover::after {
  opacity: 1;
  transform: translateX(-50%) translateY(0);
}
```

### 4-6. 스크롤 투 탑 버튼 (Glass 개선)

**Before:** 불투명 `var(--accent-blue)` 배경
**After:** Glass morphism + border

```css
/* === INTERACTIVE: Scroll-to-Top (Glass) === */
.scroll-top {
  position: fixed;
  bottom: 2rem;
  right: 2rem;
  width: 3rem;
  height: 3rem;
  background: rgba(59, 130, 246, 0.2);
  backdrop-filter: blur(8px);
  -webkit-backdrop-filter: blur(8px);
  border: 1px solid rgba(59, 130, 246, 0.3);
  color: var(--accent-blue-light);
  border-radius: 50%;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  opacity: 0;
  transform: translateY(10px);
  visibility: hidden;
  transition: all 0.3s ease;
  z-index: 500;
  box-shadow: 0 4px 12px rgba(59, 130, 246, 0.2);
}

.scroll-top.visible {
  opacity: 1;
  visibility: visible;
  transform: translateY(0);
}

.scroll-top:hover {
  background: rgba(59, 130, 246, 0.35);
  transform: translateY(-2px);
  box-shadow: 0 8px 24px rgba(59, 130, 246, 0.3);
}

.scroll-top svg {
  width: 20px;
  height: 20px;
}
```

---

## 5. 백그라운드 애니메이션

### 5-1. CSS Gradient Mesh (고정 배경)

**추가할 HTML (body 첫 번째 자식):**
```html
<div class="bg-mesh" aria-hidden="true"></div>
```

**CSS:**
```css
/* === BACKGROUND: Gradient Mesh === */
.bg-mesh {
  position: fixed;
  inset: 0;
  z-index: -1;
  overflow: hidden;
  pointer-events: none;
}

.bg-mesh::before,
.bg-mesh::after {
  content: '';
  position: absolute;
  border-radius: 50%;
  filter: blur(100px);
  opacity: 0.4;
  will-change: transform;
}

.bg-mesh::before {
  width: 600px;
  height: 600px;
  background: radial-gradient(circle, rgba(59, 130, 246, 0.15), transparent 70%);
  top: -200px;
  right: -100px;
  animation: meshFloat1 20s ease-in-out infinite alternate;
}

.bg-mesh::after {
  width: 500px;
  height: 500px;
  background: radial-gradient(circle, rgba(139, 92, 246, 0.12), transparent 70%);
  bottom: -150px;
  left: -100px;
  animation: meshFloat2 25s ease-in-out infinite alternate;
}

@keyframes meshFloat1 {
  0% { transform: translate(0, 0) scale(1); }
  33% { transform: translate(50px, 80px) scale(1.1); }
  66% { transform: translate(-30px, 40px) scale(0.95); }
  100% { transform: translate(20px, -20px) scale(1.05); }
}

@keyframes meshFloat2 {
  0% { transform: translate(0, 0) scale(1); }
  50% { transform: translate(-60px, -40px) scale(1.15); }
  100% { transform: translate(40px, 60px) scale(0.9); }
}
```

### 5-2. 히어로 Floating Orbs

**추가할 HTML (`.hero-content` 앞, `.hero` 내부):**
```html
<div class="hero-orb hero-orb-1" aria-hidden="true"></div>
<div class="hero-orb hero-orb-2" aria-hidden="true"></div>
<div class="hero-orb hero-orb-3" aria-hidden="true"></div>
```

**CSS:**
```css
/* === BACKGROUND: Hero Floating Orbs === */
.hero-orb {
  position: absolute;
  border-radius: 50%;
  filter: blur(80px);
  pointer-events: none;
  will-change: transform;
}

.hero-orb-1 {
  width: 300px;
  height: 300px;
  background: rgba(59, 130, 246, 0.2);
  top: 10%;
  left: 15%;
  animation: orbFloat 15s ease-in-out infinite;
}

.hero-orb-2 {
  width: 250px;
  height: 250px;
  background: rgba(139, 92, 246, 0.15);
  top: 60%;
  right: 10%;
  animation: orbFloat 18s ease-in-out infinite reverse;
}

.hero-orb-3 {
  width: 200px;
  height: 200px;
  background: rgba(16, 185, 129, 0.1);
  bottom: 10%;
  left: 40%;
  animation: orbFloat 22s ease-in-out infinite 3s;
}

@keyframes orbFloat {
  0%, 100% { transform: translate(0, 0) scale(1); }
  25% { transform: translate(30px, -20px) scale(1.05); }
  50% { transform: translate(-20px, 30px) scale(0.95); }
  75% { transform: translate(15px, 15px) scale(1.02); }
}
```

### 5-3. Canvas Particle Network (선택적)

> 성능 부담이 있으므로 선택적으로 적용. 모바일에서는 파티클 수 감소, 탭 비활성 시 일시정지.

**추가할 HTML (`.hero` 내부, orb 뒤):**
```html
<canvas id="particleCanvas" style="position:absolute;inset:0;width:100%;height:100%;pointer-events:none;z-index:0;" aria-hidden="true"></canvas>
```

**JS:**
```javascript
/* === BACKGROUND: Canvas Particle Network (Optional) === */
(function() {
  const canvas = document.getElementById('particleCanvas');
  if (!canvas) return;

  // reduced-motion 체크
  if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) return;

  const ctx = canvas.getContext('2d');
  const isMobile = window.innerWidth < 768;
  const particleCount = isMobile ? 15 : 40;
  const maxDistance = 150;
  let particles = [];
  let animationId;

  function resize() {
    const rect = canvas.parentElement.getBoundingClientRect();
    canvas.width = rect.width;
    canvas.height = rect.height;
  }

  function init() {
    particles = [];
    for (let i = 0; i < particleCount; i++) {
      particles.push({
        x: Math.random() * canvas.width,
        y: Math.random() * canvas.height,
        vx: (Math.random() - 0.5) * 0.3,
        vy: (Math.random() - 0.5) * 0.3,
        radius: Math.random() * 2 + 1,
        opacity: Math.random() * 0.3 + 0.1
      });
    }
  }

  function animate() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);

    particles.forEach(function(p) {
      p.x += p.vx;
      p.y += p.vy;
      if (p.x < 0 || p.x > canvas.width) p.vx *= -1;
      if (p.y < 0 || p.y > canvas.height) p.vy *= -1;

      ctx.beginPath();
      ctx.arc(p.x, p.y, p.radius, 0, Math.PI * 2);
      ctx.fillStyle = 'rgba(59, 130, 246, ' + p.opacity + ')';
      ctx.fill();
    });

    // Draw connections
    for (let i = 0; i < particles.length; i++) {
      for (let j = i + 1; j < particles.length; j++) {
        const dx = particles[i].x - particles[j].x;
        const dy = particles[i].y - particles[j].y;
        const dist = Math.sqrt(dx * dx + dy * dy);
        if (dist < maxDistance) {
          const opacity = (1 - dist / maxDistance) * 0.15;
          ctx.beginPath();
          ctx.moveTo(particles[i].x, particles[i].y);
          ctx.lineTo(particles[j].x, particles[j].y);
          ctx.strokeStyle = 'rgba(59, 130, 246, ' + opacity + ')';
          ctx.lineWidth = 0.5;
          ctx.stroke();
        }
      }
    }

    animationId = requestAnimationFrame(animate);
  }

  resize();
  init();
  animate();

  window.addEventListener('resize', function() { resize(); init(); });

  // 탭 비활성 시 일시정지
  document.addEventListener('visibilitychange', function() {
    if (document.hidden) {
      cancelAnimationFrame(animationId);
    } else {
      animate();
    }
  });
})();
```

### 5-4. 성능 고려사항

```css
/* === PERFORMANCE: Reduce Motion === */
@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important;
  }

  .bg-mesh::before,
  .bg-mesh::after,
  .hero-orb {
    animation: none !important;
  }

  .fade-in,
  .reveal-left,
  .reveal-right,
  .reveal-scale {
    opacity: 1 !important;
    transform: none !important;
  }

  .stagger-children > * {
    opacity: 1 !important;
    transform: none !important;
  }
}

/* === PERFORMANCE: GPU Hints === */
.bg-mesh::before,
.bg-mesh::after,
.hero-orb,
.fade-in,
.reveal-left,
.reveal-right,
.reveal-scale,
.highlight-card,
.data-card {
  will-change: transform;
}

/* 애니메이션 완료 후 will-change 해제 */
.fade-in.visible,
.reveal-left.visible,
.reveal-right.visible,
.reveal-scale.visible {
  will-change: auto;
}
```

---

## 6. 디자인 토큰 업데이트

### 추가/변경할 CSS 변수 전체 목록

```css
:root {
  /* --- 기존 유지 --- */
  --bg-primary: #0f172a;
  --bg-secondary: #1e293b;
  --bg-tertiary: #334155;
  --bg-card: #1e293b;
  --bg-card-hover: #263548;
  --text-primary: #f8fafc;
  --text-secondary: #94a3b8;
  --text-muted: #64748b;
  --accent-blue: #3b82f6;
  --accent-blue-light: #60a5fa;
  --accent-emerald: #10b981;
  --accent-amber: #f59e0b;
  --accent-red: #ef4444;
  --accent-purple: #8b5cf6;
  --border-default: #334155;
  --border-hover: #475569;
  --gradient-hero: linear-gradient(135deg, #0f172a 0%, #1e1b4b 50%, #0f172a 100%);
  --gradient-card: linear-gradient(145deg, #1e293b, #263548);
  --sidebar-width: 280px;

  /* --- 신규 추가 --- */
  --glass-bg: rgba(30, 41, 59, 0.6);
  --glass-border: rgba(148, 163, 184, 0.08);
  --glass-blur: blur(16px) saturate(180%);

  --gradient-border: linear-gradient(135deg, rgba(59, 130, 246, 0.3), rgba(139, 92, 246, 0.3), rgba(16, 185, 129, 0.3));
  --gradient-accent: linear-gradient(90deg, var(--accent-blue), var(--accent-purple));
  --gradient-divider: linear-gradient(90deg, transparent, rgba(59, 130, 246, 0.3), rgba(139, 92, 246, 0.3), transparent);

  --shadow-card: 0 4px 6px rgba(0, 0, 0, 0.1), 0 10px 40px rgba(0, 0, 0, 0.15);
  --shadow-card-hover: 0 8px 12px rgba(0, 0, 0, 0.15), 0 20px 60px rgba(0, 0, 0, 0.25);
  --shadow-glow-blue: 0 0 20px rgba(59, 130, 246, 0.15);

  --ease-smooth: cubic-bezier(0.4, 0, 0.2, 1);
  --ease-bounce: cubic-bezier(0.34, 1.56, 0.64, 1);
}
```

---

## 7. 구현 체크리스트 (frontend-engineer용)

### HTML 변경사항
- [ ] `<body>` 첫 자식으로 `<div class="bg-mesh" aria-hidden="true"></div>` 추가
- [ ] `<body>` 첫 자식으로 `<div class="scroll-progress" id="scrollProgress"></div>` 추가
- [ ] `.hero` 내부에 orb 3개 + canvas 추가 (`.hero-content` 앞)
- [ ] `</body>` 앞에 lightbox overlay 추가
- [ ] `.toc-link`(메인 섹션)에 `.toc-badge` span 추가
- [ ] `.hero-highlights`에 `stagger-children` 클래스 추가
- [ ] 데이터 카드 그리드에 `stagger-children` 클래스 추가
- [ ] `.table-wrapper`에 `reveal-scale` 클래스 추가
- [ ] `.callout`에 `reveal-left` 클래스 추가
- [ ] 숫자 데이터 요소에 `data-value`/`data-suffix` 속성 추가

### CSS 변경사항
- [ ] `:root`에 새 CSS 변수 추가
- [ ] `.sidebar` glass morphism 적용
- [ ] `.scroll-progress` 스타일 추가
- [ ] `.toc-link` active glow 개선
- [ ] `.toc-badge` 스타일 추가
- [ ] `.highlight-card` glass card로 교체
- [ ] `.data-card` glass card로 교체
- [ ] `.section` divider를 gradient로 교체
- [ ] heading 장식 추가
- [ ] 테이블 행 호버 glow
- [ ] risk badge pulse
- [ ] 향상된 scroll 애니메이션 (방향별 + stagger)
- [ ] 이미지 라이트박스 CSS
- [ ] 탭 슬라이딩 인디케이터 CSS
- [ ] 툴팁 CSS
- [ ] scroll-to-top glass 개선
- [ ] bg-mesh CSS
- [ ] hero orb CSS
- [ ] reduce-motion 미디어쿼리
- [ ] will-change GPU 힌트

### JS 변경사항
- [ ] 스크롤 진행률 바 로직
- [ ] 향상된 IntersectionObserver (방향별 + stagger 지원)
- [ ] 카운터 카운트업 함수 + observer
- [ ] 이미지 라이트박스 이벤트
- [ ] 슬라이딩 탭 인디케이터 로직
- [ ] Canvas particle network (선택적)

---

> **참고:** 모든 CSS/JS 코드는 복사-붙여넣기 가능한 수준으로 작성되었으며, 기존 HTML 구조를 최대한 유지하는 전제로 설계되었습니다. 최소한의 HTML 추가(bg-mesh, scroll-progress, orbs, lightbox, badges)만 필요합니다.
