# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

한국어 라이프스타일 블로그 (legoje.com)를 WordPress에서 Jekyll 기반 GitHub Pages로 마이그레이션한 프로젝트입니다.

## Build Commands

```bash
# Jekyll 로컬 서버 실행
bundle exec jekyll serve

# Jekyll 빌드 (정적 파일 생성)
bundle exec jekyll build
```

## Architecture

```
blog_legoje/
├── _config.yml              # Jekyll 설정 파일
├── _layouts/                # 레이아웃 템플릿
│   ├── default.html         # 기본 레이아웃 (head, header, footer 포함)
│   ├── post.html            # 개별 포스트 레이아웃
│   └── category.html        # 카테고리 페이지 레이아웃
├── _includes/               # 재사용 컴포넌트
│   ├── head.html            # <head> 태그 (메타, CSS 로드) - 화면에 안 보임
│   ├── header.html          # <header> 태그 (로고, 사이트 제목) - 화면에 보임
│   ├── nav.html             # 네비게이션 메뉴
│   ├── footer.html          # 푸터
│   ├── analytics.html       # Google Analytics
│   └── adsense.html         # Google AdSense
├── _posts/                  # 블로그 포스트 (~139개)
│   └── YYYY-MM-DD-slug.html # 포스트 파일 (front matter + HTML 콘텐츠)
├── category/                # 카테고리 페이지
│   ├── financial-and-investment.html  # 나의 경제 생활
│   ├── interest.html                   # 나의 문화 생활
│   └── financial-and-investment/
│       ├── event.html                  # 이벤트 (서브카테고리)
│       └── promo-code.html             # 할인코드 & 추천코드 (서브카테고리)
├── assets/
│   └── css/
│       ├── combined.css     # 메인 CSS (리셋, WP블록, 테마, TOC, 커스텀)
│       ├── header.css       # 헤더/네비게이션 스타일
│       └── footer.css       # 푸터 스타일
├── docs/                    # 원본 WordPress 데이터 (참조용, 수정 금지)
├── wp-content/              # WordPress 에셋 (이미지, 테마 파일)
│   └── uploads/             # 업로드된 이미지들
├── index.html               # 홈페이지 (페이지네이션 포함)
└── 404.html                 # 404 에러 페이지
```

## Key Files

### Front Matter 구조 (_posts/*.html)
```yaml
---
layout: post
title: "포스트 제목"
date: 2024-07-16
image: "/wp-content/uploads/2024/07/thumbnail.webp"
categories:
  - "나의 경제 생활"
tags:
  - "태그1"
  - "태그2"
---
```

### 카테고리 구조
- **나의 경제 생활** (`financial-and-investment`)
  - 이벤트 (`event`)
  - 할인코드 & 추천코드 (`promo-code`)
- **나의 문화 생활** (`interest`)

## CSS 구조

CSS는 분리 진행 중:
- `combined.css` - 베이스/콘텐츠 스타일 (정리 중)
- `header.css` - 헤더, 네비게이션, 모바일 메뉴
- `footer.css` - 푸터, 사이트 정보

CSS 변수 (`combined.css`):
```css
:root {
    --contrast: #222222;
    --contrast-2: #575760;
    --base: #f0f0f0;
    --base-2: #f7f8f9;
    --base-3: #ffffff;
    --accent: #1e73be;
}
```

## Python 스크립트

```bash
# 포스트 날짜 수정 (docs에서 추출)
python3 fix_dates.py

# 포스트 이미지 추가 (docs에서 og:image 추출)
python3 fix_images.py

# 포스트 카테고리/태그 수정 (docs에서 추출)
python3 fix_categories.py
```

## 주의사항

- **docs 폴더 수정 금지** - 원본 WordPress 데이터 참조용
- **_site 폴더 수정 금지** - Jekyll 빌드 출력물 (자동 생성)
- **한글 카테고리명 사용** - 포스트의 categories는 한글로 저장됨
- **Jekyll 페이지네이션** - 카테고리 페이지는 JavaScript 기반 페이지네이션 사용