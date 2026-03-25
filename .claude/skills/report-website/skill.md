---
name: report-website
description: "CTO 보고서 마크다운을 모던 인터랙티브 웹사이트로 변환하는 오케스트레이터. '웹사이트로 만들어줘', '보고서를 웹으로', '웹 보고서', '사이트 구축', '보고서 웹사이트', '인터랙티브 보고서' 요청 시 사용. 마크다운 보고서를 다크 테마 싱글페이지 웹사이트로 변환하며, Mermaid 차트 렌더링, 이미지 삽입, 반응형 디자인을 포함한다."
---

# Report Website Orchestrator

CTO 보고서를 프레젠테이션급 모던 웹사이트로 변환하는 에이전트 팀 오케스트레이터.

## 실행 모드: 에이전트 팀

## 에이전트 구성

| 팀원 | 타입 | 역할 | 출력 |
|------|------|------|------|
| content-architect | general-purpose | 마크다운→구조화 데이터 | `_workspace/0*.json` |
| frontend-engineer | general-purpose | UI 구현 | `website/` |
| qa-reviewer | general-purpose | 품질 검증 | `_workspace/qa_report.md` |

## 입력 요구사항

- CTO 보고서 마크다운 파일 (프로젝트 루트)
- `images/` 디렉토리 (Gemini 생성 이미지)

## 워크플로우

### Phase 1: 준비
1. 프로젝트 루트에서 보고서 마크다운 파일 확인
2. `_workspace/` 디렉토리 생성
3. `website/` 디렉토리 생성
4. `images/`를 `website/images/`로 복사

### Phase 2: 팀 구성

```
TeamCreate(
  team_name: "report-website-team",
  members: [
    {
      name: "content-architect",
      agent_type: "general-purpose",
      prompt: "당신은 content-architect 에이전트입니다. .claude/agents/content-architect.md를 읽고 역할을 수행하세요. CTO_보고서_엔터테인먼트_AI.md를 파싱하여 _workspace/ 에 구조화된 JSON 파일들을 생성하세요."
    },
    {
      name: "frontend-engineer",
      agent_type: "general-purpose",
      prompt: "당신은 frontend-engineer 에이전트입니다. .claude/agents/frontend-engineer.md를 읽고 역할을 수행하세요. content-architect가 완료 알림을 보내면 _workspace/ 데이터와 원본 마크다운을 기반으로 website/ 에 모던 웹사이트를 구현하세요."
    },
    {
      name: "qa-reviewer",
      agent_type: "general-purpose",
      prompt: "당신은 qa-reviewer 에이전트입니다. .claude/agents/qa-reviewer.md를 읽고 역할을 수행하세요. frontend-engineer가 완료 알림을 보내면 website/와 원본 마크다운을 비교 검증하세요."
    }
  ]
)
```

### Phase 3: 작업 등록

```
TaskCreate(tasks: [
  {
    title: "콘텐츠 구조화",
    description: "CTO 보고서 마크다운을 파싱하여 섹션별 JSON, 차트 데이터, 네비게이션 구조, Mermaid 코드, 이미지 매니페스트, 각주 매핑을 생성",
    assignee: "content-architect"
  },
  {
    title: "웹사이트 UI 구현",
    description: "구조화된 데이터를 기반으로 다크 테마 싱글페이지 웹사이트 구현. HTML+CSS+JS, Mermaid.js CDN, 반응형 디자인, 사이드바 TOC",
    assignee: "frontend-engineer",
    depends_on: ["콘텐츠 구조화"]
  },
  {
    title: "품질 검증",
    description: "원본 마크다운과 웹사이트를 라인 바이 라인 비교. 수치 정확성, 이미지 렌더링, Mermaid 동작, 반응형 레이아웃 검증",
    assignee: "qa-reviewer",
    depends_on: ["웹사이트 UI 구현"]
  },
  {
    title: "이슈 수정",
    description: "QA에서 발견된 Critical/Major 이슈 수정",
    assignee: "frontend-engineer",
    depends_on: ["품질 검증"]
  }
])
```

### Phase 4: 실행 및 모니터링
1. 팀원들이 자체 조율하며 작업 수행
2. 리더는 TaskGet으로 진행 상황 모니터링
3. 팀원 간 통신 흐름:
   ```
   content-architect → (완료 알림) → frontend-engineer
   frontend-engineer → (완료 알림) → qa-reviewer
   qa-reviewer → (이슈 목록) → frontend-engineer (수정)
   qa-reviewer → (최종 보고) → 리더
   ```

### Phase 5: 최종 산출물 확인
1. `website/index.html`이 브라우저에서 정상 동작하는지 확인
2. QA 리포트에 Critical 이슈가 0건인지 확인
3. 사용자에게 결과 안내

## 데이터 전달 프로토콜

| 단계 | 출발 | 도착 | 방식 | 데이터 |
|------|------|------|------|--------|
| 1 | content-architect | _workspace/ | 파일 기반 | JSON 구조화 데이터 |
| 2 | content-architect | frontend-engineer | SendMessage | "구조화 완료" 알림 |
| 3 | frontend-engineer | website/ | 파일 기반 | HTML/CSS/JS |
| 4 | frontend-engineer | qa-reviewer | SendMessage | "구현 완료" 알림 |
| 5 | qa-reviewer | _workspace/ | 파일 기반 | qa_report.md |
| 6 | qa-reviewer | frontend-engineer | SendMessage | Critical 이슈 목록 |

## 에러 핸들링

| 에러 | 전략 |
|------|------|
| content-architect 실패 | frontend-engineer가 원본 마크다운에서 직접 구현 |
| frontend-engineer 실패 | 1회 재시도, 실패 시 리더가 직접 구현 |
| qa-reviewer 실패 | 리더가 기본 검증 수행 |
| Mermaid CDN 실패 | 코드블록 폴백으로 구현 |
| 이미지 누락 | 플레이스홀더로 대체, QA 보고서에 명시 |

## 최종 산출물

```
website/
├── index.html        ← 메인 웹사이트 (브라우저에서 직접 열기)
├── styles.css        ← 스타일시트
├── app.js           ← 인터랙션 로직
└── images/          ← 보고서 이미지
    ├── tech_maturity_matrix.png
    ├── build_vs_buy.png
    ├── risk_matrix.png
    └── sora_alternative_strategy.png
```

## 테스트 시나리오

### 정상 흐름
1. 리더가 팀 구성 및 작업 등록
2. content-architect가 마크다운 파싱 → JSON 생성 → frontend-engineer에 알림
3. frontend-engineer가 웹사이트 구현 → qa-reviewer에 알림
4. qa-reviewer가 검증 → 이슈 0건 → 리더에 완료 보고
5. 리더가 `open website/index.html`로 결과 확인

### 에러 흐름
1. content-architect 타임아웃 발생
2. 리더가 감지, frontend-engineer에게 "원본 마크다운에서 직접 구현하라" 지시
3. frontend-engineer가 마크다운을 직접 파싱하여 구현
4. qa-reviewer가 검증 진행 (정상 흐름으로 복귀)
