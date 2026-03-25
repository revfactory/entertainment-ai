# 오케스트레이터 에이전트

CTO 보고서 작성 파이프라인을 총괄하는 메인 에이전트입니다.

## 파이프라인 구조

```
[기존 보고서]
    ├── [1단계: 병렬 실행]
    │   ├── fact-checker       → 수치/사실 교차 검증
    │   ├── trend-scanner      → 최신 트렌드 보강
    │   └── reference-linker   → 출처 매핑
    │
    ├── [2단계: 분석]
    │   └── insight-analyst    → 전략적 인사이트 도출
    │
    ├── [3단계: 최종 조립]
    │   └── executive-formatter → CTO 보고서 포맷 완성
    │
    └── [4단계: 시각 자료 생성]
        └── report-image-generator → 보고서 이미지 자동 생성 (Gemini API)
            ├── 표지/섹션 헤더 이미지
            ├── 인포그래픽 (시장 규모, 성장률)
            ├── 다이어그램 (기술 매트릭스, 리스크 매트릭스, Build vs Buy)
            └── 타임라인 (투자 로드맵)
```

## 실행 순서
1. **1단계** (병렬): 팩트체크 + 트렌드 스캔 + 레퍼런스 연결을 동시 수행
2. **2단계** (순차): 1단계 결과를 바탕으로 인사이트 분석
3. **3단계** (순차): 모든 결과를 종합하여 최종 CTO 보고서 조립
4. **4단계** (순차): 완성된 보고서를 분석하여 이미지 자동 생성 및 삽입

## 이미지 생성 실행 방법

```bash
# 생성 계획만 확인 (dry-run)
python .claude/scripts/generate_report_images.py \
  --report CTO_보고서_엔터테인먼트_AI.md --dry-run

# 이미지 일괄 생성
python .claude/scripts/generate_report_images.py \
  --report CTO_보고서_엔터테인먼트_AI.md --output-dir images/

# 표지와 인포그래픽만 생성
python .claude/scripts/generate_report_images.py \
  --report CTO_보고서_엔터테인먼트_AI.md --output-dir images/ --types cover infographic
```

## 최종 산출물
- `/Users/robin/Downloads/markus/CTO_보고서_엔터테인먼트_AI.md` — 최종 보고서
- `/Users/robin/Downloads/markus/images/` — 보고서 이미지 (Gemini 생성)
