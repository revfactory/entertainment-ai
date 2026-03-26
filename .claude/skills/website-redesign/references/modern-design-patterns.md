# 모던 웹 디자인 패턴 레퍼런스 (2025-2026)

## 목차
1. [네비게이션 패턴](#1-네비게이션-패턴)
2. [Glass Morphism & 깊이감](#2-glass-morphism--깊이감)
3. [인터랙티브 요소](#3-인터랙티브-요소)
4. [백그라운드 애니메이션](#4-백그라운드-애니메이션)
5. [마이크로 인터랙션](#5-마이크로-인터랙션)
6. [모던 카드 & 컨테이너](#6-모던-카드--컨테이너)
7. [성능 최적화](#7-성능-최적화)

---

## 1. 네비게이션 패턴

### 1-1. Floating Glass Navigation (사이드바)

기존의 단색 사이드바를 반투명 glass 효과로 교체한다.

```css
.sidebar {
  background: rgba(15, 23, 42, 0.85);
  backdrop-filter: blur(20px) saturate(180%);
  -webkit-backdrop-filter: blur(20px) saturate(180%);
  border-right: 1px solid rgba(148, 163, 184, 0.1);
  box-shadow: 4px 0 24px rgba(0, 0, 0, 0.2);
}
```

### 1-2. 스크롤 진행률 인디케이터

페이지 상단에 읽기 진행률을 표시하는 얇은 바.

```css
.scroll-progress {
  position: fixed;
  top: 0;
  left: 0;
  width: 0%;
  height: 3px;
  background: linear-gradient(90deg, var(--accent-blue), var(--accent-purple), var(--accent-emerald));
  z-index: 1000;
  transition: width 0.1s linear;
}
```

```javascript
window.addEventListener('scroll', () => {
  const scrollTop = document.documentElement.scrollTop;
  const scrollHeight = document.documentElement.scrollHeight - window.innerHeight;
  const progress = (scrollTop / scrollHeight) * 100;
  document.querySelector('.scroll-progress').style.width = progress + '%';
});
```

### 1-3. Active Section Glow 효과

활성 TOC 링크에 subtle glow 추가.

```css
.toc-link.active {
  color: var(--accent-blue-light);
  border-left-color: var(--accent-blue);
  background: linear-gradient(90deg, rgba(59, 130, 246, 0.12), transparent);
  box-shadow: inset 3px 0 8px rgba(59, 130, 246, 0.2);
  font-weight: 500;
}

.toc-link {
  position: relative;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.toc-link:hover {
  color: var(--text-primary);
  background: rgba(148, 163, 184, 0.06);
  padding-left: calc(1.5rem + 4px);
}
```

### 1-4. 사이드바 섹션 카운터 배지

각 섹션 옆에 읽기 상태 또는 하위 항목 수를 표시하는 작은 배지.

```css
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
}
```

---

## 2. Glass Morphism & 깊이감

### 2-1. Glass Card

```css
.glass-card {
  background: rgba(30, 41, 59, 0.6);
  backdrop-filter: blur(16px) saturate(180%);
  -webkit-backdrop-filter: blur(16px) saturate(180%);
  border: 1px solid rgba(148, 163, 184, 0.08);
  border-radius: 1rem;
  box-shadow:
    0 4px 6px rgba(0, 0, 0, 0.1),
    0 10px 40px rgba(0, 0, 0, 0.15),
    inset 0 1px 0 rgba(255, 255, 255, 0.05);
  transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
}

.glass-card:hover {
  transform: translateY(-4px);
  box-shadow:
    0 8px 12px rgba(0, 0, 0, 0.15),
    0 20px 60px rgba(0, 0, 0, 0.25),
    inset 0 1px 0 rgba(255, 255, 255, 0.08);
  border-color: rgba(59, 130, 246, 0.2);
}
```

### 2-2. 섹션 Divider (그라디언트 구분선)

```css
.section-divider {
  height: 1px;
  background: linear-gradient(90deg, transparent, rgba(59, 130, 246, 0.3), rgba(139, 92, 246, 0.3), transparent);
  margin: 0;
  border: none;
}
```

### 2-3. 섹션 Heading 장식

```css
.section h2 {
  position: relative;
  padding-left: 1rem;
}

.section h2::before {
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

---

## 3. 인터랙티브 요소

### 3-1. 스크롤 트리거 애니메이션 (향상)

기존 fade-in을 더 풍부하게. 요소별로 다른 딜레이와 방향.

```css
.reveal {
  opacity: 0;
  transform: translateY(30px);
  transition: opacity 0.8s cubic-bezier(0.4, 0, 0.2, 1),
              transform 0.8s cubic-bezier(0.4, 0, 0.2, 1);
}

.reveal.visible {
  opacity: 1;
  transform: translateY(0);
}

.reveal-left {
  opacity: 0;
  transform: translateX(-30px);
}

.reveal-right {
  opacity: 0;
  transform: translateX(30px);
}

.reveal-scale {
  opacity: 0;
  transform: scale(0.95);
}

/* staggered children */
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

.stagger-children.visible > * {
  opacity: 1;
  transform: translateY(0);
}
```

```javascript
const observer = new IntersectionObserver((entries) => {
  entries.forEach(entry => {
    if (entry.isIntersecting) {
      entry.target.classList.add('visible');
    }
  });
}, { threshold: 0.1, rootMargin: '0px 0px -50px 0px' });

document.querySelectorAll('.reveal, .reveal-left, .reveal-right, .reveal-scale, .stagger-children')
  .forEach(el => observer.observe(el));
```

### 3-2. 카운터 애니메이션 (숫자 카운트업)

데이터 카드의 수치가 스크롤 시 0에서 카운트업되는 효과.

```javascript
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
```

### 3-3. 툴팁

```css
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
  transition: opacity 0.2s, transform 0.2s;
  z-index: 500;
}

[data-tooltip]:hover::after {
  opacity: 1;
  transform: translateX(-50%) translateY(0);
}
```

### 3-4. 이미지 라이트박스

이미지 클릭 시 전체 화면 오버레이로 확대.

```css
.lightbox-overlay {
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.9);
  backdrop-filter: blur(8px);
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
  transition: transform 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.lightbox-overlay.active img {
  transform: scale(1);
}
```

### 3-5. 탭 전환 개선 (Sliding Indicator)

```css
.tabs {
  position: relative;
  display: flex;
  gap: 0;
  background: rgba(30, 41, 59, 0.5);
  border-radius: 0.75rem;
  padding: 0.25rem;
  border: 1px solid rgba(148, 163, 184, 0.1);
}

.tab {
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
}

.tab.active {
  color: var(--text-primary);
}

.tab-indicator {
  position: absolute;
  bottom: 0.25rem;
  height: calc(100% - 0.5rem);
  background: rgba(59, 130, 246, 0.15);
  border-radius: 0.5rem;
  transition: left 0.3s cubic-bezier(0.4, 0, 0.2, 1),
              width 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}
```

---

## 4. 백그라운드 애니메이션

### 4-1. Gradient Mesh 배경 (CSS only)

성능 부담이 적은 CSS 기반 그라디언트 메시.

```css
.bg-mesh {
  position: fixed;
  inset: 0;
  z-index: -1;
  overflow: hidden;
}

.bg-mesh::before,
.bg-mesh::after {
  content: '';
  position: absolute;
  border-radius: 50%;
  filter: blur(100px);
  opacity: 0.4;
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

### 4-2. 추가 Floating Orb (히어로 영역)

히어로 섹션에 추가 빛나는 구체 효과.

```css
.hero-orb {
  position: absolute;
  border-radius: 50%;
  filter: blur(80px);
  pointer-events: none;
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

### 4-3. Canvas Particle Network (선택적)

가벼운 파티클 네트워크. 성능 부담 시 비활성화 가능.

```javascript
class ParticleNetwork {
  constructor(canvas) {
    this.canvas = canvas;
    this.ctx = canvas.getContext('2d');
    this.particles = [];
    this.particleCount = 40;
    this.maxDistance = 150;
    this.resize();
    this.init();
    this.animate();

    window.addEventListener('resize', () => this.resize());
  }

  resize() {
    this.canvas.width = window.innerWidth;
    this.canvas.height = window.innerHeight;
  }

  init() {
    for (let i = 0; i < this.particleCount; i++) {
      this.particles.push({
        x: Math.random() * this.canvas.width,
        y: Math.random() * this.canvas.height,
        vx: (Math.random() - 0.5) * 0.3,
        vy: (Math.random() - 0.5) * 0.3,
        radius: Math.random() * 2 + 1,
        opacity: Math.random() * 0.3 + 0.1
      });
    }
  }

  animate() {
    this.ctx.clearRect(0, 0, this.canvas.width, this.canvas.height);

    this.particles.forEach(p => {
      p.x += p.vx;
      p.y += p.vy;

      if (p.x < 0 || p.x > this.canvas.width) p.vx *= -1;
      if (p.y < 0 || p.y > this.canvas.height) p.vy *= -1;

      this.ctx.beginPath();
      this.ctx.arc(p.x, p.y, p.radius, 0, Math.PI * 2);
      this.ctx.fillStyle = `rgba(59, 130, 246, ${p.opacity})`;
      this.ctx.fill();
    });

    // Draw connections
    for (let i = 0; i < this.particles.length; i++) {
      for (let j = i + 1; j < this.particles.length; j++) {
        const dx = this.particles[i].x - this.particles[j].x;
        const dy = this.particles[i].y - this.particles[j].y;
        const dist = Math.sqrt(dx * dx + dy * dy);

        if (dist < this.maxDistance) {
          const opacity = (1 - dist / this.maxDistance) * 0.15;
          this.ctx.beginPath();
          this.ctx.moveTo(this.particles[i].x, this.particles[i].y);
          this.ctx.lineTo(this.particles[j].x, this.particles[j].y);
          this.ctx.strokeStyle = `rgba(59, 130, 246, ${opacity})`;
          this.ctx.lineWidth = 0.5;
          this.ctx.stroke();
        }
      }
    }

    requestAnimationFrame(() => this.animate());
  }
}

// 초기화 (히어로 또는 전체 배경)
// const canvas = document.getElementById('particle-canvas');
// if (canvas) new ParticleNetwork(canvas);
```

### 4-4. 섹션별 배경 그라디언트 변화

스크롤에 따라 배경색이 미묘하게 변화하는 효과.

```css
.section[data-theme="blue"] {
  --section-accent: rgba(59, 130, 246, 0.05);
}
.section[data-theme="purple"] {
  --section-accent: rgba(139, 92, 246, 0.05);
}
.section[data-theme="emerald"] {
  --section-accent: rgba(16, 185, 129, 0.05);
}

.section::before {
  content: '';
  position: absolute;
  inset: 0;
  background: radial-gradient(ellipse at 50% 0%, var(--section-accent, transparent), transparent 70%);
  pointer-events: none;
}
```

---

## 5. 마이크로 인터랙션

### 5-1. 버튼/링크 리플 효과

```css
.ripple-btn {
  position: relative;
  overflow: hidden;
}

.ripple-btn::after {
  content: '';
  position: absolute;
  top: 50%;
  left: 50%;
  width: 0;
  height: 0;
  background: rgba(255, 255, 255, 0.1);
  border-radius: 50%;
  transform: translate(-50%, -50%);
  transition: width 0.6s ease, height 0.6s ease, opacity 0.6s ease;
  opacity: 0;
}

.ripple-btn:active::after {
  width: 300px;
  height: 300px;
  opacity: 1;
  transition: 0s;
}
```

### 5-2. 테이블 행 호버 Glow

```css
.report-table tr {
  transition: all 0.2s ease;
}

.report-table tbody tr:hover {
  background: rgba(59, 130, 246, 0.04);
  box-shadow: inset 3px 0 0 var(--accent-blue);
}
```

### 5-3. 배지 Pulse

```css
.risk-high {
  animation: riskPulse 2s ease-in-out infinite;
}

@keyframes riskPulse {
  0%, 100% { box-shadow: 0 0 0 0 rgba(239, 68, 68, 0.2); }
  50% { box-shadow: 0 0 0 4px rgba(239, 68, 68, 0); }
}
```

### 5-4. 스크롤 투 탑 버튼

```css
.scroll-top-btn {
  position: fixed;
  bottom: 2rem;
  right: 2rem;
  width: 3rem;
  height: 3rem;
  border-radius: 50%;
  background: rgba(59, 130, 246, 0.2);
  backdrop-filter: blur(8px);
  border: 1px solid rgba(59, 130, 246, 0.3);
  color: var(--accent-blue-light);
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  opacity: 0;
  transform: translateY(10px);
  transition: all 0.3s ease;
  z-index: 500;
}

.scroll-top-btn.visible {
  opacity: 1;
  transform: translateY(0);
}

.scroll-top-btn:hover {
  background: rgba(59, 130, 246, 0.35);
  transform: translateY(-2px);
}
```

---

## 6. 모던 카드 & 컨테이너

### 6-1. Gradient Border 카드

```css
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
  background: linear-gradient(135deg, rgba(59, 130, 246, 0.3), rgba(139, 92, 246, 0.3), rgba(16, 185, 129, 0.3));
  -webkit-mask: linear-gradient(#fff 0 0) content-box, linear-gradient(#fff 0 0);
  -webkit-mask-composite: xor;
  mask-composite: exclude;
  pointer-events: none;
}
```

### 6-2. 히어로 하이라이트 카드 개선

```css
.highlight-card {
  background: rgba(30, 41, 59, 0.5);
  backdrop-filter: blur(12px);
  border: 1px solid rgba(148, 163, 184, 0.08);
  border-radius: 1rem;
  padding: 1.75rem;
  position: relative;
  overflow: hidden;
  transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
}

.highlight-card::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 2px;
  background: linear-gradient(90deg, var(--accent-blue), var(--accent-purple));
  opacity: 0;
  transition: opacity 0.3s;
}

.highlight-card:hover::before {
  opacity: 1;
}

.highlight-card:hover {
  transform: translateY(-6px);
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
  border-color: rgba(59, 130, 246, 0.15);
}
```

---

## 7. 성능 최적화

### 7-1. Reduce Motion 대응

```css
@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important;
  }

  .bg-mesh::before,
  .bg-mesh::after,
  .hero-orb {
    animation: none;
  }
}
```

### 7-2. GPU 가속 힌트

```css
.bg-mesh::before,
.bg-mesh::after,
.hero-orb,
.reveal,
.highlight-card {
  will-change: transform;
}

/* 애니메이션 완료 후 will-change 제거 */
.reveal.visible {
  will-change: auto;
}
```

### 7-3. IntersectionObserver 최적화

```javascript
// 한 번 보이면 관찰 해제 (성능)
const revealObserver = new IntersectionObserver((entries, obs) => {
  entries.forEach(entry => {
    if (entry.isIntersecting) {
      entry.target.classList.add('visible');
      obs.unobserve(entry.target); // 한 번만 트리거
    }
  });
}, { threshold: 0.1 });
```

### 7-4. Canvas 파티클 성능 관리

```javascript
// 탭이 비활성일 때 애니메이션 일시정지
document.addEventListener('visibilitychange', () => {
  if (document.hidden) {
    cancelAnimationFrame(animationId);
  } else {
    animate();
  }
});

// 모바일에서 파티클 수 감소
const isMobile = window.innerWidth < 768;
const particleCount = isMobile ? 15 : 40;
```
