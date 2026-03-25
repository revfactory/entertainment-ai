# 디자인 시스템 레퍼런스

## 목차
1. [색상 팔레트](#색상-팔레트)
2. [타이포그래피](#타이포그래피)
3. [레이아웃 그리드](#레이아웃-그리드)
4. [컴포넌트 패턴](#컴포넌트-패턴)
5. [애니메이션](#애니메이션)
6. [CDN 의존성](#cdn-의존성)

---

## 색상 팔레트

```css
:root {
  /* 배경 */
  --bg-primary: #0f172a;
  --bg-secondary: #1e293b;
  --bg-tertiary: #334155;
  --bg-card: #1e293b;
  --bg-card-hover: #263548;

  /* 텍스트 */
  --text-primary: #f8fafc;
  --text-secondary: #94a3b8;
  --text-muted: #64748b;

  /* 액센트 */
  --accent-blue: #3b82f6;
  --accent-blue-light: #60a5fa;
  --accent-emerald: #10b981;
  --accent-amber: #f59e0b;
  --accent-red: #ef4444;
  --accent-purple: #8b5cf6;

  /* 보더 */
  --border-default: #334155;
  --border-hover: #475569;

  /* 그라디언트 */
  --gradient-hero: linear-gradient(135deg, #0f172a 0%, #1e1b4b 50%, #0f172a 100%);
  --gradient-card: linear-gradient(145deg, #1e293b, #263548);
}
```

## 타이포그래피

```css
/* 폰트 로드 */
@import url('https://cdn.jsdelivr.net/gh/orioncactus/pretendard/dist/web/static/pretendard.min.css');
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
@import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500&display=swap');

body {
  font-family: 'Pretendard', 'Inter', -apple-system, sans-serif;
  font-size: 1rem;
  line-height: 1.75;
  color: var(--text-primary);
}

h1 { font-size: 2.5rem; font-weight: 700; letter-spacing: -0.02em; }
h2 { font-size: 1.875rem; font-weight: 600; letter-spacing: -0.01em; }
h3 { font-size: 1.25rem; font-weight: 600; }

code, .mono { font-family: 'JetBrains Mono', monospace; font-size: 0.875rem; }
```

## 레이아웃 그리드

```
데스크톱 (1200px+):
┌──────────┬──────────────────────────────┐
│ Sidebar  │ Main Content                 │
│ 260px    │ flex-1 (max-width: 900px)    │
│ fixed    │ padding: 3rem                │
└──────────┴──────────────────────────────┘

태블릿 (768px~1199px):
┌─────────────────────────────────────────┐
│ 햄버거 메뉴 (사이드바 토글)               │
├─────────────────────────────────────────┤
│ Main Content (padding: 2rem)            │
└─────────────────────────────────────────┘

모바일 (767px 이하):
┌─────────────────────────────────────────┐
│ 상단 네비 (드롭다운)                     │
├─────────────────────────────────────────┤
│ Main Content (padding: 1rem)            │
└─────────────────────────────────────────┘
```

## 컴포넌트 패턴

### 히어로 섹션
```html
<section class="hero">
  <div class="hero-badge">Confidential · CTO Report</div>
  <h1>엔터테인먼트 산업 AI 활용 현황 및 전략 보고서</h1>
  <p class="hero-subtitle">2026년 3월 25일 · Version 2.0</p>
  <div class="hero-highlights">
    <div class="highlight-card">핵심 메시지 1</div>
    <div class="highlight-card">핵심 메시지 2</div>
    <div class="highlight-card">핵심 메시지 3</div>
  </div>
</section>
```

### 데이터 카드
```html
<div class="data-card">
  <div class="data-card-header">
    <span class="data-card-icon">📊</span>
    <h3>글로벌 시장 규모</h3>
  </div>
  <div class="data-card-value">994.8억$</div>
  <div class="data-card-label">2030년 전망 (CAGR 24.2%)</div>
  <div class="data-card-source">출처: Grand View Research</div>
</div>
```

### 리스크 배지
```html
<span class="risk-badge risk-high">HIGH</span>
<span class="risk-badge risk-medium">MEDIUM</span>
<span class="risk-badge risk-low">LOW</span>
```

### 테이블
```css
.report-table {
  width: 100%;
  border-collapse: separate;
  border-spacing: 0;
  border-radius: 0.75rem;
  overflow: hidden;
}
.report-table th {
  background: var(--bg-tertiary);
  padding: 0.75rem 1rem;
  text-align: left;
  font-weight: 600;
  font-size: 0.875rem;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  color: var(--text-secondary);
}
.report-table td {
  padding: 0.75rem 1rem;
  border-bottom: 1px solid var(--border-default);
}
.report-table tr:hover td {
  background: var(--bg-card-hover);
}
```

### 탭 전환 (분야별 동향)
```html
<div class="tabs">
  <button class="tab active" data-tab="film">영화/영상</button>
  <button class="tab" data-tab="music">음악</button>
  <button class="tab" data-tab="game">게임</button>
  <button class="tab" data-tab="broadcast">방송</button>
</div>
<div class="tab-content active" id="film">...</div>
<div class="tab-content" id="music">...</div>
```

### 사이드바 TOC
```html
<nav class="sidebar">
  <div class="sidebar-title">목차</div>
  <ul class="toc">
    <li><a href="#executive-summary" class="toc-link active">Executive Summary</a></li>
    <li><a href="#market" class="toc-link">시장 환경</a>
      <ul class="toc-sub">
        <li><a href="#market-size">글로벌 시장</a></li>
        <li><a href="#market-signal">전환 시그널</a></li>
      </ul>
    </li>
  </ul>
</nav>
```

## 애니메이션

```css
/* 스크롤 인 애니메이션 */
.fade-in {
  opacity: 0;
  transform: translateY(20px);
  transition: opacity 0.6s ease, transform 0.6s ease;
}
.fade-in.visible {
  opacity: 1;
  transform: translateY(0);
}

/* 카드 호버 */
.data-card {
  transition: transform 0.2s ease, box-shadow 0.2s ease;
}
.data-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.3);
}

/* TOC 활성 표시 */
.toc-link.active {
  color: var(--accent-blue);
  border-left: 2px solid var(--accent-blue);
  padding-left: 0.75rem;
}
```

## CDN 의존성

```html
<!-- Mermaid.js -->
<script src="https://cdn.jsdelivr.net/npm/mermaid@11/dist/mermaid.min.js"></script>
<script>
  mermaid.initialize({
    startOnLoad: true,
    theme: 'dark',
    themeVariables: {
      primaryColor: '#3b82f6',
      primaryTextColor: '#f8fafc',
      lineColor: '#64748b',
      sectionBkgColor: '#1e293b',
    }
  });
</script>

<!-- Lucide Icons (선택) -->
<script src="https://unpkg.com/lucide@latest"></script>
```
