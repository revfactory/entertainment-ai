---
name: website-redesign
description: "기존 웹사이트의 UX/UI를 전면 개선하는 리디자인 오케스트레이터. '디자인 개선', 'UX 개선', '리디자인', '디자인 업데이트', '모던하게', '인터랙티브 추가', '애니메이션 추가', '네비게이션 변경', '백그라운드 효과' 요청 시 사용. 네비게이션, 비주얼 디자인, 인터랙티브 요소, 백그라운드 애니메이션 등 웹사이트 전반의 UX를 현대적으로 개선한다."
---

# Website Redesign Orchestrator

기존 웹사이트의 UX/UI를 분석하고 모던 디자인으로 전면 개선하는 에이전트 팀 오케스트레이터.

## 실행 모드: 에이전트 팀

## 에이전트 구성

| 팀원 | 타입 | 역할 | 출력 |
|------|------|------|------|
| ux-designer | general-purpose | 현재 디자인 분석 + 리디자인 스펙 작성 | `_workspace/ux_redesign_spec.md` |
| frontend-engineer | general-purpose | 스펙 기반 구현 | `docs/index.html` (in-place 수정) |
| qa-reviewer | general-purpose | 개선 품질 검증 | `_workspace/redesign_qa_report.md` |

## 워크플로우

### Phase 1: 준비
1. 사용자 요청에서 개선 영역 파악 (네비게이션, 비주얼, 인터랙션, 애니메이션 등)
2. 현재 웹사이트 파일 존재 확인 (`docs/index.html`)
3. `_workspace/` 디렉토리 확인 (없으면 생성)

### Phase 2: 팀 구성

```
TeamCreate(
  team_name: "website-redesign-team",
  members: [
    {
      name: "ux-designer",
      agent_type: "general-purpose",
      prompt: "당신은 ux-designer 에이전트입니다. .claude/agents/ux-designer.md를 읽고 역할을 수행하세요. docs/index.html의 현재 디자인을 분석하고, 다음 영역의 리디자인 스펙을 작성하세요: {사용자 요청 영역}. .claude/skills/website-redesign/references/modern-design-patterns.md를 참조하세요. 스펙은 _workspace/ux_redesign_spec.md에 저장하세요."
    },
    {
      name: "frontend-engineer",
      agent_type: "general-purpose",
      prompt: "당신은 frontend-engineer 에이전트입니다. .claude/agents/frontend-engineer.md를 읽고 역할을 수행하세요. ux-designer가 완료 알림을 보내면 _workspace/ux_redesign_spec.md를 읽고 docs/index.html을 직접 수정하여 리디자인을 구현하세요. 기존 콘텐츠(HTML 구조, 텍스트, 이미지)는 보존하고 CSS와 JS만 개선하세요."
    },
    {
      name: "qa-reviewer",
      agent_type: "general-purpose",
      prompt: "당신은 qa-reviewer 에이전트입니다. .claude/agents/qa-reviewer.md를 읽고 역할을 수행하세요. frontend-engineer가 완료 알림을 보내면 개선된 docs/index.html을 검증하세요. 특히: (1) 기존 콘텐츠 보존 여부, (2) 새 CSS/JS의 문법 오류, (3) 반응형 레이아웃 유지, (4) 접근성 유지/개선을 확인하세요."
    }
  ]
)
```

### Phase 3: 작업 등록

```
TaskCreate(tasks: [
  {
    title: "UX 분석 및 리디자인 스펙",
    description: "현재 docs/index.html의 디자인을 분석하고 개선 스펙을 작성. 네비게이션, 비주얼, 인터랙션, 백그라운드 애니메이션 영역을 포함. 구체적 CSS/JS 코드 스펙 필수.",
    assignee: "ux-designer"
  },
  {
    title: "리디자인 구현",
    description: "ux_redesign_spec.md를 기반으로 docs/index.html의 CSS/JS를 수정. 기존 HTML 구조와 콘텐츠는 보존하되 스타일과 인터랙션을 전면 개선.",
    assignee: "frontend-engineer",
    depends_on: ["UX 분석 및 리디자인 스펙"]
  },
  {
    title: "리디자인 품질 검증",
    description: "개선된 웹사이트의 콘텐츠 보존, CSS/JS 오류, 반응형 레이아웃, 접근성을 검증. 이슈를 Critical/Major/Minor로 분류.",
    assignee: "qa-reviewer",
    depends_on: ["리디자인 구현"]
  },
  {
    title: "이슈 수정",
    description: "QA에서 발견된 Critical/Major 이슈 수정",
    assignee: "frontend-engineer",
    depends_on: ["리디자인 품질 검증"]
  }
])
```

### Phase 4: 실행 및 모니터링

팀원 간 통신 흐름:
```
ux-designer → (스펙 완료 + SendMessage) → frontend-engineer
frontend-engineer → (구현 완료 + SendMessage) → qa-reviewer
qa-reviewer → (이슈 목록 + SendMessage) → frontend-engineer (수정)
qa-reviewer → (최종 보고) → 리더
```

리더 모니터링:
- TaskGet으로 진행 상황 확인
- 팀원 유휴 시 자동 알림 수신
- 필요 시 개입하여 방향 조정

### Phase 5: 최종 확인
1. `docs/index.html`을 브라우저에서 열어 시각적 확인
2. QA 리포트에 Critical 이슈 0건 확인
3. 기존 콘텐츠(텍스트, 이미지, Mermaid 차트)가 100% 보존되었는지 확인
4. 사용자에게 개선 사항 요약 보고

## 핵심 제약 (모든 팀원 필독)

**콘텐츠 보존 원칙**: 리디자인은 CSS와 JS만 변경한다. HTML 구조와 텍스트 콘텐츠, 이미지 경로, Mermaid 다이어그램은 절대 수정하지 않는다. 디자인을 위해 wrapper div를 추가하는 것은 허용하되, 기존 요소를 삭제하거나 텍스트를 변경하는 것은 금지한다.

## 데이터 전달 프로토콜

| 단계 | 출발 | 도착 | 방식 | 데이터 |
|------|------|------|------|--------|
| 1 | ux-designer | _workspace/ | 파일 기반 | ux_redesign_spec.md |
| 2 | ux-designer | frontend-engineer | SendMessage | "스펙 완료" 알림 |
| 3 | frontend-engineer | docs/ | 파일 기반 | 수정된 index.html |
| 4 | frontend-engineer | qa-reviewer | SendMessage | "구현 완료" 알림 |
| 5 | qa-reviewer | _workspace/ | 파일 기반 | redesign_qa_report.md |
| 6 | qa-reviewer | frontend-engineer | SendMessage | Critical 이슈 목록 |

## 에러 핸들링

| 에러 | 전략 |
|------|------|
| ux-designer 실패 | frontend-engineer가 modern-design-patterns.md를 직접 참조하여 구현 |
| frontend-engineer 실패 | 1회 재시도. 실패 시 리더가 직접 구현 |
| qa-reviewer 실패 | 리더가 기본 검증 수행 |
| CSS 호환성 문제 | @supports 쿼리로 폴백 구현 |
| 성능 저하 | will-change 최적화, 애니메이션 reduce-motion 미디어쿼리 대응 |

## 테스트 시나리오

### 정상 흐름
1. 리더가 팀 구성 및 작업 등록
2. ux-designer가 현재 디자인 분석 → 스펙 작성 → frontend-engineer에 알림
3. frontend-engineer가 CSS/JS 수정 → qa-reviewer에 알림
4. qa-reviewer가 검증 → 이슈 0건 → 리더에 완료 보고
5. 리더가 브라우저에서 결과 확인

### 에러 흐름
1. qa-reviewer가 "네비게이션 호버 시 텍스트 사라짐" Critical 이슈 보고
2. frontend-engineer가 수정 → qa-reviewer에 재검증 요청
3. qa-reviewer가 재검증 → 통과 → 리더에 완료 보고
