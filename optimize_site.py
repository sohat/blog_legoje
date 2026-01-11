#!/usr/bin/env python3
"""
웹사이트 최적화 스크립트
1. 이미지 리사이징 및 압축 (800px 초과 -> 800px, 메타데이터 제거)
2. HTML img 태그 최적화 (loading="lazy", fetchpriority 제거)
3. srcset 경로 점검
4. 워드프레스 주석/빈 태그 제거
5. CSS/JS defer 속성 추가
6. @font-face에 font-display: swap 추가
7. HTML/CSS/JS Minify
"""

import os
import re
import glob
from pathlib import Path
from PIL import Image
import io

# 프로젝트 루트 경로
PROJECT_ROOT = Path("/Users/sohapark/Desktop/DEV/blog_legoje")
DOCS_DIR = PROJECT_ROOT / "docs"
UPLOADS_DIR = DOCS_DIR / "wp-content" / "uploads"

# 통계
stats = {
    "images_resized": 0,
    "images_compressed": 0,
    "html_files_processed": 0,
    "lazy_added": 0,
    "fetchpriority_removed": 0,
    "srcset_fixed": 0,
    "wp_comments_removed": 0,
    "empty_tags_removed": 0,
    "defer_added": 0,
    "font_display_added": 0,
    "files_minified": 0,
}


def optimize_images():
    """이미지 리사이징 및 압축 (800px 초과 리사이징, 메타데이터 제거)"""
    print("\n[1/7] 이미지 리사이징 및 압축 중...")

    webp_files = list(UPLOADS_DIR.rglob("*.webp"))
    total = len(webp_files)

    for i, img_path in enumerate(webp_files, 1):
        if i % 100 == 0:
            print(f"  처리 중: {i}/{total}")

        try:
            with Image.open(img_path) as img:
                original_size = os.path.getsize(img_path)
                width, height = img.size

                # 가로 800px 초과시 리사이징
                if width > 800:
                    ratio = 800 / width
                    new_height = int(height * ratio)
                    img = img.resize((800, new_height), Image.LANCZOS)
                    stats["images_resized"] += 1

                # 메타데이터 제거 및 재압축
                # 새 이미지 객체로 복사하여 메타데이터 제거
                output = io.BytesIO()

                # RGBA -> RGB 변환 (투명 배경 처리)
                if img.mode in ('RGBA', 'LA', 'P'):
                    background = Image.new('RGB', img.size, (255, 255, 255))
                    if img.mode == 'P':
                        img = img.convert('RGBA')
                    if img.mode in ('RGBA', 'LA'):
                        background.paste(img, mask=img.split()[-1])
                        img = background

                # WebP로 저장 (quality=85로 좋은 품질 유지)
                img.save(output, format='WEBP', quality=85, method=6)

                # 파일 크기가 줄었으면 저장
                new_size = output.tell()
                if new_size < original_size:
                    with open(img_path, 'wb') as f:
                        f.write(output.getvalue())
                    stats["images_compressed"] += 1

        except Exception as e:
            # 손상된 이미지는 건너뜀
            continue

    print(f"  완료: {stats['images_resized']}개 리사이징, {stats['images_compressed']}개 압축")


def check_file_exists(src_path, html_file_path):
    """srcset 경로가 실제 파일로 존재하는지 확인"""
    if src_path.startswith('http://') or src_path.startswith('https://'):
        return True  # 외부 URL은 체크하지 않음

    # 상대 경로 처리
    if src_path.startswith('/'):
        # 절대 경로 (도메인 루트 기준)
        full_path = DOCS_DIR / src_path.lstrip('/')
    else:
        # 상대 경로
        full_path = html_file_path.parent / src_path

    return full_path.exists()


def optimize_html_files():
    """HTML 파일 최적화"""
    print("\n[2/7] HTML 파일 최적화 중...")

    html_files = list(DOCS_DIR.rglob("*.html"))
    total = len(html_files)

    for i, html_path in enumerate(html_files, 1):
        if i % 50 == 0:
            print(f"  처리 중: {i}/{total}")

        try:
            with open(html_path, 'r', encoding='utf-8') as f:
                content = f.read()

            original_content = content

            # 1. loading="lazy" 추가 (첫 번째 이미지 제외)
            img_pattern = re.compile(r'<img\s+([^>]*?)>', re.IGNORECASE | re.DOTALL)
            matches = list(img_pattern.finditer(content))

            for idx, match in enumerate(matches):
                img_tag = match.group(0)
                attrs = match.group(1)

                # 첫 번째 이미지는 제외 (LCP 이미지)
                if idx == 0:
                    continue

                # 이미 loading 속성이 있으면 건너뜀
                if 'loading=' in attrs.lower():
                    continue

                # loading="lazy" 추가
                new_img_tag = img_tag.replace('<img ', '<img loading="lazy" ')
                content = content.replace(img_tag, new_img_tag, 1)
                stats["lazy_added"] += 1

            # 2. fetchpriority="high" 제거
            fetchpriority_pattern = re.compile(r'\s*fetchpriority\s*=\s*["\']high["\']', re.IGNORECASE)
            new_content, count = fetchpriority_pattern.subn('', content)
            if count > 0:
                content = new_content
                stats["fetchpriority_removed"] += count

            # 3. srcset 경로 점검 및 수정
            srcset_pattern = re.compile(r'srcset\s*=\s*["\']([^"\']+)["\']', re.IGNORECASE)

            def fix_srcset(match):
                srcset_value = match.group(1)
                sources = srcset_value.split(',')
                valid_sources = []

                for source in sources:
                    source = source.strip()
                    if not source:
                        continue

                    parts = source.split()
                    if not parts:
                        continue

                    src_path = parts[0]

                    # URL 디코딩이 필요한 경우
                    if check_file_exists(src_path, html_path):
                        valid_sources.append(source)
                    else:
                        stats["srcset_fixed"] += 1

                if valid_sources:
                    return f'srcset="{", ".join(valid_sources)}"'
                else:
                    # 모든 srcset이 유효하지 않으면 srcset 속성 자체를 제거
                    return ''

            content = srcset_pattern.sub(fix_srcset, content)

            # 4. 워드프레스 주석 제거
            # <!-- wp:xxx --> 형태의 주석 제거
            wp_comment_pattern = re.compile(r'<!--\s*/?wp:[^>]*-->', re.IGNORECASE)
            new_content, count = wp_comment_pattern.subn('', content)
            if count > 0:
                content = new_content
                stats["wp_comments_removed"] += count

            # 5. 빈 태그 제거 (빈 p, span, div 등)
            empty_tag_pattern = re.compile(r'<(p|span|div)(\s+[^>]*)?>\s*</\1>', re.IGNORECASE)
            while empty_tag_pattern.search(content):
                content, count = empty_tag_pattern.subn('', content)
                stats["empty_tags_removed"] += count

            # 6. CSS/JS에 defer 속성 추가
            # 외부 JS 파일에 defer 추가 (async가 없는 경우)
            script_pattern = re.compile(
                r'<script\s+([^>]*?)src\s*=\s*["\']([^"\']+)["\']([^>]*)>',
                re.IGNORECASE
            )

            def add_defer_to_script(match):
                before_src = match.group(1)
                src = match.group(2)
                after_src = match.group(3)

                full_attrs = before_src + after_src

                # 이미 defer나 async가 있으면 건너뜀
                if 'defer' in full_attrs.lower() or 'async' in full_attrs.lower():
                    return match.group(0)

                # inline script가 아닌 외부 스크립트에만 적용
                if src:
                    stats["defer_added"] += 1
                    return f'<script defer {before_src}src="{src}"{after_src}>'

                return match.group(0)

            content = script_pattern.sub(add_defer_to_script, content)

            if content != original_content:
                with open(html_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                stats["html_files_processed"] += 1

        except Exception as e:
            continue

    print(f"  완료: {stats['html_files_processed']}개 HTML 파일 처리")
    print(f"    - loading='lazy' 추가: {stats['lazy_added']}개")
    print(f"    - fetchpriority 제거: {stats['fetchpriority_removed']}개")
    print(f"    - srcset 수정: {stats['srcset_fixed']}개")
    print(f"    - WP 주석 제거: {stats['wp_comments_removed']}개")
    print(f"    - 빈 태그 제거: {stats['empty_tags_removed']}개")
    print(f"    - defer 추가: {stats['defer_added']}개")


def add_font_display_swap():
    """@font-face에 font-display: swap 추가"""
    print("\n[3/7] @font-face에 font-display: swap 추가 중...")

    css_files = list(DOCS_DIR.rglob("*.css"))

    for css_path in css_files:
        try:
            with open(css_path, 'r', encoding='utf-8') as f:
                content = f.read()

            original_content = content

            # @font-face 블록 찾기
            font_face_pattern = re.compile(
                r'(@font-face\s*\{)([^}]*?)(\})',
                re.IGNORECASE | re.DOTALL
            )

            def add_font_display(match):
                start = match.group(1)
                body = match.group(2)
                end = match.group(3)

                # 이미 font-display가 있으면 건너뜀
                if 'font-display' in body.lower():
                    return match.group(0)

                stats["font_display_added"] += 1
                return f'{start}{body}font-display:swap;{end}'

            content = font_face_pattern.sub(add_font_display, content)

            if content != original_content:
                with open(css_path, 'w', encoding='utf-8') as f:
                    f.write(content)

        except Exception as e:
            continue

    print(f"  완료: font-display: swap {stats['font_display_added']}개 추가")


def minify_files():
    """HTML/CSS/JS 파일 최소화"""
    print("\n[4/7] 파일 Minify 중...")

    try:
        import htmlmin
        has_htmlmin = True
    except ImportError:
        has_htmlmin = False
        print("  htmlmin 라이브러리 없음 - HTML minify 건너뜀")

    try:
        import csscompressor
        has_csscompressor = True
    except ImportError:
        has_csscompressor = False
        print("  csscompressor 라이브러리 없음 - CSS minify 건너뜀")

    try:
        import rjsmin
        has_rjsmin = True
    except ImportError:
        has_rjsmin = False
        print("  rjsmin 라이브러리 없음 - JS minify 건너뜀")

    # HTML Minify
    if has_htmlmin:
        html_files = list(DOCS_DIR.rglob("*.html"))
        for html_path in html_files:
            try:
                with open(html_path, 'r', encoding='utf-8') as f:
                    content = f.read()

                minified = htmlmin.minify(
                    content,
                    remove_comments=True,
                    remove_empty_space=True,
                    remove_all_empty_space=False,
                    reduce_boolean_attributes=True
                )

                if len(minified) < len(content):
                    with open(html_path, 'w', encoding='utf-8') as f:
                        f.write(minified)
                    stats["files_minified"] += 1

            except Exception as e:
                continue

    # CSS Minify
    if has_csscompressor:
        css_files = list(DOCS_DIR.rglob("*.css"))
        for css_path in css_files:
            try:
                with open(css_path, 'r', encoding='utf-8') as f:
                    content = f.read()

                minified = csscompressor.compress(content)

                if len(minified) < len(content):
                    with open(css_path, 'w', encoding='utf-8') as f:
                        f.write(minified)
                    stats["files_minified"] += 1

            except Exception as e:
                continue

    # JS Minify
    if has_rjsmin:
        js_files = list(DOCS_DIR.rglob("*.js"))
        for js_path in js_files:
            try:
                with open(js_path, 'r', encoding='utf-8') as f:
                    content = f.read()

                minified = rjsmin.jsmin(content)

                if len(minified) < len(content):
                    with open(js_path, 'w', encoding='utf-8') as f:
                        f.write(minified)
                    stats["files_minified"] += 1

            except Exception as e:
                continue

    print(f"  완료: {stats['files_minified']}개 파일 minify")


def main():
    print("=" * 50)
    print("웹사이트 최적화 시작")
    print("=" * 50)

    # 1. 이미지 최적화
    optimize_images()

    # 2. HTML 최적화 (lazy loading, fetchpriority, srcset, WP주석, 빈태그, defer)
    optimize_html_files()

    # 3. font-display: swap 추가
    add_font_display_swap()

    # 4. Minify
    minify_files()

    print("\n" + "=" * 50)
    print("최적화 완료 요약")
    print("=" * 50)
    print(f"이미지 리사이징: {stats['images_resized']}개")
    print(f"이미지 압축: {stats['images_compressed']}개")
    print(f"HTML 파일 처리: {stats['html_files_processed']}개")
    print(f"loading='lazy' 추가: {stats['lazy_added']}개")
    print(f"fetchpriority 제거: {stats['fetchpriority_removed']}개")
    print(f"srcset 수정: {stats['srcset_fixed']}개")
    print(f"WP 주석 제거: {stats['wp_comments_removed']}개")
    print(f"빈 태그 제거: {stats['empty_tags_removed']}개")
    print(f"defer 추가: {stats['defer_added']}개")
    print(f"font-display: swap 추가: {stats['font_display_added']}개")
    print(f"파일 minify: {stats['files_minified']}개")


if __name__ == "__main__":
    main()
