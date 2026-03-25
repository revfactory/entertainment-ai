#!/usr/bin/env python3
"""보고서 마크다운을 분석하여 필요한 이미지를 Gemini API로 일괄 생성하는 스크립트.

사용법:
  # 보고서 분석 후 이미지 생성
  python generate_report_images.py --report path/to/report.md --output-dir images/

  # 특정 유형만 생성
  python generate_report_images.py --report report.md --output-dir images/ --types cover sections

  # 고품질 모델 사용
  python generate_report_images.py --report report.md --output-dir images/ --model gemini-3-pro-image-preview

  # 프롬프트 목록만 확인 (이미지 생성 없이)
  python generate_report_images.py --report report.md --dry-run
"""

import argparse
import json
import os
import re
import sys
import time
from pathlib import Path

# 색상 팔레트 (보고서 이미지 공통)
COLOR_PALETTE = {
    "primary": "#1a237e",      # Navy Blue
    "secondary": "#42a5f5",    # Accent Blue
    "background": "#f5f5f5",   # Light Gray
    "white": "#ffffff",
    "dark": "#212121",
    "success": "#66bb6a",      # Green
    "warning": "#ffa726",      # Orange
    "danger": "#ef5350",       # Red
}

# 이미지 유형별 설정
IMAGE_CONFIGS = {
    "cover": {
        "subdir": "cover",
        "aspect": "16:9",
        "style_suffix": "Modern corporate design, gradient background from dark navy to deep blue. Abstract geometric patterns suggesting technology and innovation. Clean, professional, executive presentation quality. No text overlay. High contrast, dramatic lighting.",
    },
    "section": {
        "subdir": "sections",
        "aspect": "16:9",
        "style_suffix": "Minimalist section header illustration. Flat design style with single dominant icon/visual element. Clean background with subtle gradient. Corporate blue/gray/white palette. Professional and modern. No text. Suitable for widescreen presentation slide.",
    },
    "infographic": {
        "subdir": "infographics",
        "aspect": "3:4",
        "style_suffix": "Clean infographic concept visualization. Professional data visualization style. Color-coded elements, minimal design. Abstract representation using geometric shapes, icons, and visual metaphors. Corporate presentation quality. Modern flat design.",
    },
    "diagram": {
        "subdir": "diagrams",
        "aspect": "16:9",
        "style_suffix": "Professional business diagram concept. Clean layout with structured visual hierarchy. Grid-based design, color-coded quadrants or categories. Modern flat design, presentation-ready. Corporate blue palette with accent colors.",
    },
}


def extract_sections(report_text: str) -> list[dict]:
    """마크다운 보고서에서 주요 섹션(H2)을 추출합니다."""
    sections = []
    lines = report_text.split("\n")

    current_section = None
    current_content = []

    for line in lines:
        if line.startswith("## "):
            if current_section:
                current_section["content"] = "\n".join(current_content[:20])  # 처음 20줄만
                sections.append(current_section)
            title = line.lstrip("# ").strip()
            current_section = {"title": title, "level": 2, "content": ""}
            current_content = []
        elif current_section:
            current_content.append(line)

    if current_section:
        current_section["content"] = "\n".join(current_content[:20])
        sections.append(current_section)

    return sections


def generate_image_plan(report_path: str) -> list[dict]:
    """보고서를 분석하여 생성할 이미지 계획을 수립합니다."""
    with open(report_path, "r", encoding="utf-8") as f:
        report_text = f.read()

    # 보고서 제목 추출
    title_match = re.search(r"^# (.+)$", report_text, re.MULTILINE)
    report_title = title_match.group(1) if title_match else "보고서"

    sections = extract_sections(report_text)
    plan = []

    # 1. 표지 이미지
    plan.append({
        "type": "cover",
        "filename": "report_cover.png",
        "prompt": f'Corporate report cover image about "{report_title}". {IMAGE_CONFIGS["cover"]["style_suffix"]}',
        "description": f"보고서 표지: {report_title}",
    })

    # 2. 섹션 헤더 이미지
    section_keywords = {
        "executive": "executive summary, key highlights, strategic overview",
        "시장": "global market, growth chart, market size, financial data",
        "기술": "technology landscape, innovation, AI chips and circuits",
        "영화": "film production, cinema, movie camera, VFX",
        "음악": "music production, sound waves, headphones, audio",
        "게임": "gaming, controller, virtual world, digital entertainment",
        "방송": "broadcasting, streaming, TV screens, content delivery",
        "공연": "live performance, concert stage, virtual concert",
        "웹툰": "webtoon, digital comics, illustration, creative art",
        "리스크": "risk assessment, shield, warning, balance scale",
        "투자": "investment, roadmap, timeline, growth trajectory",
        "전략": "strategy, chess, planning, roadmap arrows",
        "규제": "regulation, legal, compliance, gavel",
        "한국": "South Korea, K-content, Seoul skyline, Korean wave",
        "미래": "future, horizon, emerging technology, innovation",
    }

    for i, section in enumerate(sections):
        # 섹션 제목에서 키워드 매칭
        keywords = "technology and innovation"
        for key, val in section_keywords.items():
            if key in section["title"].lower() or key in section["title"]:
                keywords = val
                break

        safe_name = re.sub(r"[^\w가-힣]", "_", section["title"])[:30]
        plan.append({
            "type": "section",
            "filename": f"sec_{i+1:02d}_{safe_name}.png",
            "prompt": f'Section header for "{section["title"]}" in a technology report. Visual elements representing: {keywords}. {IMAGE_CONFIGS["section"]["style_suffix"]}',
            "description": f"섹션 헤더: {section['title']}",
        })

    # 3. 핵심 인포그래픽 (보고서에 테이블/수치 데이터가 많은 섹션)
    data_sections = [
        {
            "filename": "market_size_overview.png",
            "prompt": f'Infographic concept showing global market growth from $82B to $995B (2024-2030). Upward trending visualization with milestone markers. {IMAGE_CONFIGS["infographic"]["style_suffix"]}',
            "description": "글로벌 시장 규모 인포그래픽",
        },
        {
            "filename": "tech_maturity_matrix.png",
            "prompt": f'Technology maturity matrix with 4 stages: Experimental, Early Commercial, Mainstream Adoption, Mature. 8 technology items plotted across the spectrum. {IMAGE_CONFIGS["diagram"]["style_suffix"]}',
            "description": "기술 성숙도 매트릭스",
        },
        {
            "filename": "risk_matrix.png",
            "prompt": f'Risk assessment matrix visualization. Grid with HIGH/MEDIUM/LOW ratings across 4 categories: Technology, Regulation, Market, Operations. Color-coded cells (red=high, yellow=medium, green=low). {IMAGE_CONFIGS["diagram"]["style_suffix"]}',
            "description": "리스크 매트릭스",
        },
        {
            "filename": "build_vs_buy.png",
            "prompt": f'Build vs Buy decision framework diagram. Three categories: BUILD (left, blue), HYBRID (center, purple), BUY (right, green). Technology items distributed across categories with icons. {IMAGE_CONFIGS["diagram"]["style_suffix"]}',
            "description": "Build vs Buy 판단 가이드",
        },
        {
            "filename": "investment_roadmap.png",
            "prompt": f'Investment roadmap timeline visualization from Q2 2026 to 2027. Four phases: Quick Win, Short-term, Mid-term, Scale-up. Connected timeline with milestone markers. {IMAGE_CONFIGS["diagram"]["style_suffix"]}',
            "description": "투자 로드맵 타임라인",
        },
    ]

    for item in data_sections:
        item["type"] = "infographic" if "infographic" in item["filename"] or "market" in item["filename"] else "diagram"
        plan.append(item)

    return plan


def generate_image(client, model: str, prompt: str, output_path: str) -> bool:
    """Gemini API로 이미지를 생성합니다."""
    from google.genai import types
    from PIL import Image as PILImage
    from io import BytesIO

    try:
        response = client.models.generate_content(
            model=model,
            contents=[prompt],
            config=types.GenerateContentConfig(
                response_modalities=["TEXT", "IMAGE"],
            )
        )

        for part in response.candidates[0].content.parts:
            if part.inline_data is not None:
                image = PILImage.open(BytesIO(part.inline_data.data))
                image.save(output_path)
                return True

        return False

    except Exception as e:
        print(f"  오류: {e}")
        return False


def main():
    parser = argparse.ArgumentParser(description="보고서 이미지 일괄 생성")
    parser.add_argument("--report", required=True, help="보고서 마크다운 파일 경로")
    parser.add_argument("--output-dir", default="images", help="이미지 출력 디렉토리")
    parser.add_argument("--model", default="gemini-3.1-flash-image-preview",
                        choices=["gemini-3.1-flash-image-preview",
                                 "gemini-3-pro-image-preview",
                                 "gemini-2.5-flash-image"])
    parser.add_argument("--types", nargs="*", default=["cover", "section", "infographic", "diagram"],
                        choices=["cover", "section", "infographic", "diagram"],
                        help="생성할 이미지 유형")
    parser.add_argument("--dry-run", action="store_true", help="프롬프트만 출력, 이미지 생성 안 함")
    parser.add_argument("--plan-output", help="이미지 생성 계획을 JSON으로 저장")
    args = parser.parse_args()

    if not os.path.exists(args.report):
        print(f"오류: 보고서 파일을 찾을 수 없습니다: {args.report}")
        sys.exit(1)

    # 이미지 생성 계획 수립
    plan = generate_image_plan(args.report)
    plan = [p for p in plan if p["type"] in args.types]

    print(f"보고서: {args.report}")
    print(f"생성할 이미지: {len(plan)}개")
    print(f"모델: {args.model}")
    print("=" * 60)

    # 계획 출력
    for i, item in enumerate(plan):
        print(f"\n[{i+1}/{len(plan)}] {item['description']}")
        print(f"  파일: {item['filename']}")
        print(f"  유형: {item['type']}")
        if args.dry_run:
            print(f"  프롬프트: {item['prompt'][:120]}...")

    # 계획 저장
    if args.plan_output:
        with open(args.plan_output, "w", encoding="utf-8") as f:
            json.dump(plan, f, ensure_ascii=False, indent=2)
        print(f"\n계획 저장됨: {args.plan_output}")

    if args.dry_run:
        print(f"\n[DRY RUN] 이미지 생성을 건너뜁니다.")
        return

    # API 키 확인
    api_key = os.environ.get("GOOGLE_API_KEY")
    if not api_key:
        print("\n오류: GOOGLE_API_KEY 환경변수가 설정되지 않았습니다.")
        print("설정: export GOOGLE_API_KEY='your-api-key'")
        print("발급: https://aistudio.google.com/apikey")
        sys.exit(1)

    # 패키지 확인
    try:
        from google import genai
    except ImportError:
        print("오류: pip install google-genai Pillow")
        sys.exit(1)

    client = genai.Client(api_key=api_key)

    # 디렉토리 생성
    output_base = Path(args.output_dir)
    for config in IMAGE_CONFIGS.values():
        (output_base / config["subdir"]).mkdir(parents=True, exist_ok=True)

    # 이미지 생성
    success = 0
    failed = 0

    for i, item in enumerate(plan):
        subdir = IMAGE_CONFIGS[item["type"]]["subdir"]
        output_path = output_base / subdir / item["filename"]

        print(f"\n[{i+1}/{len(plan)}] 생성 중: {item['description']}")

        retries = 3
        for attempt in range(retries):
            if generate_image(client, args.model, item["prompt"], str(output_path)):
                print(f"  저장됨: {output_path}")
                success += 1
                break
            else:
                if attempt < retries - 1:
                    print(f"  재시도 ({attempt+2}/{retries})...")
                    time.sleep(2)
                else:
                    print(f"  실패: {item['filename']}")
                    failed += 1

        # API 레이트 리밋 방지
        time.sleep(1)

    print("\n" + "=" * 60)
    print(f"완료: 성공 {success}개, 실패 {failed}개")
    print(f"출력 디렉토리: {output_base}/")

    # 마크다운 이미지 링크 생성
    md_links_path = output_base / "image_links.md"
    with open(md_links_path, "w", encoding="utf-8") as f:
        f.write("# 보고서 이미지 링크\n\n")
        f.write("아래 링크를 보고서 마크다운에 복사하여 사용하세요.\n\n")
        for item in plan:
            subdir = IMAGE_CONFIGS[item["type"]]["subdir"]
            f.write(f"### {item['description']}\n")
            f.write(f"![{item['description']}]({args.output_dir}/{subdir}/{item['filename']})\n\n")

    print(f"이미지 링크 파일: {md_links_path}")


if __name__ == "__main__":
    main()
