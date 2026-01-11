#!/usr/bin/env python3
"""
WordPress 추출 파일을 GitHub Pages용 정적 사이트로 변환합니다.
"""

import os
import shutil
import re
from pathlib import Path

# 경로 설정
EXTRACTED_DIR = Path("/Users/sohapark/Desktop/blog/dev/extracted")
DOCS_DIR = Path("/Users/sohapark/Desktop/blog/dev/docs")

# 원본 도메인
ORIGINAL_DOMAIN = "legoje.com"

# GitHub Pages 베이스 경로 (커스텀 도메인 사용시 빈 문자열)
BASE_PATH = ""


def clean_docs_dir():
    """docs 폴더 초기화"""
    if DOCS_DIR.exists():
        shutil.rmtree(DOCS_DIR)
    DOCS_DIR.mkdir(parents=True)
    print("docs 폴더 초기화 완료")


def copy_html_files():
    """HTML 파일 복사 (cache/all 폴더에서)"""
    cache_all = EXTRACTED_DIR / "cache" / "all"
    if not cache_all.exists():
        print("cache/all 폴더가 없습니다")
        return 0

    count = 0
    for src_file in cache_all.rglob("*.html"):
        # 상대 경로 계산
        rel_path = src_file.relative_to(cache_all)
        dst_file = DOCS_DIR / rel_path

        # 디렉토리 생성
        dst_file.parent.mkdir(parents=True, exist_ok=True)

        # 파일 복사
        shutil.copy2(src_file, dst_file)
        count += 1

    print(f"HTML 파일 {count}개 복사 완료")
    return count


def copy_uploads():
    """이미지 파일 복사 (uploads 폴더에서)"""
    uploads_src = EXTRACTED_DIR / "uploads"
    uploads_dst = DOCS_DIR / "wp-content" / "uploads"

    if not uploads_src.exists():
        print("uploads 폴더가 없습니다")
        return 0

    count = 0
    extensions = {'.jpg', '.jpeg', '.png', '.gif', '.webp', '.svg', '.ico', '.mp4', '.pdf'}

    for src_file in uploads_src.rglob("*"):
        if src_file.is_file() and src_file.suffix.lower() in extensions:
            rel_path = src_file.relative_to(uploads_src)
            dst_file = uploads_dst / rel_path
            dst_file.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(src_file, dst_file)
            count += 1

    print(f"업로드 파일 {count}개 복사 완료")
    return count


def copy_css_js():
    """CSS/JS 파일 복사"""
    cache_minified = EXTRACTED_DIR / "cache" / "wpfc-minified"
    dst_minified = DOCS_DIR / "wp-content" / "cache" / "wpfc-minified"

    count = 0
    if cache_minified.exists():
        for src_file in cache_minified.rglob("*"):
            if src_file.is_file() and src_file.suffix.lower() in {'.css', '.js'}:
                rel_path = src_file.relative_to(cache_minified)
                dst_file = dst_minified / rel_path
                dst_file.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(src_file, dst_file)
                count += 1

    # 테마 CSS/JS 복사
    themes_src = EXTRACTED_DIR / "themes"
    themes_dst = DOCS_DIR / "wp-content" / "themes"

    if themes_src.exists():
        for src_file in themes_src.rglob("*"):
            if src_file.is_file() and src_file.suffix.lower() in {'.css', '.js', '.woff', '.woff2', '.ttf', '.eot'}:
                rel_path = src_file.relative_to(themes_src)
                dst_file = themes_dst / rel_path
                dst_file.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(src_file, dst_file)
                count += 1

    print(f"CSS/JS 파일 {count}개 복사 완료")
    return count


def fix_html_links():
    """HTML 파일 내 링크 수정"""
    count = 0

    for html_file in DOCS_DIR.rglob("*.html"):
        with open(html_file, 'r', encoding='utf-8', errors='replace') as f:
            content = f.read()

        original_content = content

        # 1. https://legoje.com/ -> BASE_PATH/
        content = re.sub(
            r'https?://' + re.escape(ORIGINAL_DOMAIN) + r'/',
            BASE_PATH + '/',
            content
        )

        # 2. //legoje.com/ -> BASE_PATH/
        content = re.sub(
            r'//' + re.escape(ORIGINAL_DOMAIN) + r'/',
            BASE_PATH + '/',
            content
        )

        # 3. href="/" -> href="BASE_PATH/"
        content = re.sub(r'href="/"', f'href="{BASE_PATH}/"', content)

        # 4. src="/ 또는 href="/wp-content 등 절대경로 수정
        content = re.sub(r'(href|src|content)="(/[^"]*)"', lambda m: f'{m.group(1)}="{BASE_PATH}{m.group(2)}"', content)

        # 5. 중복 BASE_PATH 제거 (이미 변환된 경우)
        content = content.replace(BASE_PATH + BASE_PATH, BASE_PATH)

        # 6. -optimized 접미사 제거 (실제 파일에는 없음)
        content = re.sub(r'-optimized(\.(png|jpg|jpeg|webp|gif))', r'\1', content)

        if content != original_content:
            with open(html_file, 'w', encoding='utf-8') as f:
                f.write(content)
            count += 1

    print(f"HTML 파일 {count}개 링크 수정 완료")
    return count


def create_404_page():
    """404 페이지 생성"""
    page_404 = DOCS_DIR / "404.html"
    content = """<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>페이지를 찾을 수 없습니다</title>
    <style>
        body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
               display: flex; justify-content: center; align-items: center;
               height: 100vh; margin: 0; background: #f7f8f9; }
        .container { text-align: center; padding: 40px; }
        h1 { color: #333; font-size: 48px; margin-bottom: 16px; }
        p { color: #666; font-size: 18px; }
        a { color: #1e73be; text-decoration: none; }
        a:hover { text-decoration: underline; }
    </style>
</head>
<body>
    <div class="container">
        <h1>404</h1>
        <p>페이지를 찾을 수 없습니다.</p>
        <p><a href="/">홈으로 돌아가기</a></p>
    </div>
</body>
</html>
"""
    with open(page_404, 'w', encoding='utf-8') as f:
        f.write(content)
    print("404.html 생성 완료")


def create_nojekyll():
    """GitHub Pages Jekyll 처리 비활성화"""
    nojekyll = DOCS_DIR / ".nojekyll"
    nojekyll.touch()
    print(".nojekyll 생성 완료")


def main():
    print("=" * 50)
    print("WordPress -> GitHub Pages 정적 사이트 변환")
    print("=" * 50)

    clean_docs_dir()
    copy_html_files()
    copy_uploads()
    copy_css_js()
    fix_html_links()
    create_404_page()
    create_nojekyll()

    print("=" * 50)
    print("변환 완료!")
    print(f"결과물 위치: {DOCS_DIR}")
    print("=" * 50)


if __name__ == "__main__":
    main()
