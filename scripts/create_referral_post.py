#!/usr/bin/env python3
"""
추천코드 포스트 생성 스크립트

사용법:
    python3 scripts/create_referral_post.py _templates/referral-post-template.yml

yml 파일의 데이터를 읽어서 _posts/financial-and-investment/promo-code/ 폴더에
Jekyll 포스트를 생성합니다.

생성되는 파일은 라이펫 글과 동일한 구조:
- front matter: 기본 Jekyll 메타데이터만 (layout, title, date, permalink, image, categories, tags, description)
- 본문: 모든 값이 직접 삽입된 HTML
"""

import yaml
import os
import sys
from datetime import datetime


def load_yaml(yml_path):
    """yml 파일 로드"""
    with open(yml_path, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)


def build_front_matter(data, today_date):
    """front matter YAML 생성 (기본 메타데이터만)"""
    서비스명 = data.get('서비스명', '')
    코드 = data.get('코드', '')
    혜택요약 = data.get('혜택요약', '')
    date_path = today_date.replace('-', '/')

    fm = {
        'layout': 'post',
        'title': f"{서비스명} 초대코드 [{코드}] - {혜택요약} 및 최대 할인 방법 꿀팁 공유",
        'date': today_date,
        'permalink': f"/{서비스명}-추천링크-할인-혜택-정리/",
        'image': f"/assets/img/{date_path}/{서비스명}-썸네일.webp",
        'categories': ['할인코드 & 추천코드'],
        'tags': [
            f"{서비스명}-초대 코드",
            f"{서비스명}-추천인",
            f"{서비스명}-추천 코드"
        ],
        'description': f"{서비스명} 초대코드 [{코드}] 입력 시 {혜택요약} 지급! 직접 이용해보고 정리한 최대 할인 꿀팁을 확인하세요.",
    }

    return fm


def build_signup_benefits_html(benefits):
    """신규가입 혜택 리스트를 HTML로 변환"""
    if not benefits:
        return ""

    html_parts = []
    for i, benefit in enumerate(benefits, 1):
        title = benefit.get('title', '')
        items = benefit.get('items', [])

        html_parts.append(f'''
<h3 class="wp-block-heading">
    <span class="underline"><strong>* 신규가입 혜택 {i} – {title}</strong></span>
</h3>
<ul class="wp-block-list">''')
        for item in items:
            html_parts.append(f'    <li>{item}</li>')
        html_parts.append('</ul>')

    return '\n'.join(html_parts)


def build_existing_benefits_html(benefits, date_path, 서비스명):
    """기존회원 혜택 리스트를 HTML로 변환"""
    if not benefits:
        return ""

    html_parts = []
    for section in benefits:
        title = section.get('title', '')
        description = section.get('description', '')
        sub_items = section.get('sub_items', [])
        image_name = section.get('image_name', '')
        footer_text = section.get('footer_text', '')

        html_parts.append(f'<h3 class="wp-block-heading">{title}</h3>')

        if description:
            html_parts.append(f'<h4>{description}</h4>')

        for item in sub_items:
            html_parts.append(f'<h4>{item}</h4>')

        if image_name:
            html_parts.append(f'''<div class="wp-block-image">
    <figure class="aligncenter size-full is-resized">
        <img loading="lazy" decoding="async"
             width="1022" height="1778"
             src="/assets/img/{date_path}/{image_name}"
             alt="{서비스명} 기존회원 혜택 - {title}"
             style="width:500px"
            >
    </figure>
</div>''')

        if footer_text:
            html_parts.append(f'<p>{footer_text}</p>')

        html_parts.append('')  # 빈 줄 추가

    return '\n'.join(html_parts)


def build_body(data, today_date):
    """본문 HTML 생성 (모든 값 직접 삽입)"""
    date_path = today_date.replace('-', '/')

    서비스명 = data.get('서비스명', '')
    코드 = data.get('코드', '')
    서비스설명 = data.get('서비스설명', '')
    실사용장점 = data.get('실사용장점', '')
    초대코드혜택 = data.get('초대코드혜택', '')
    구매조건 = data.get('구매조건', '') or '금액 상관없이'
    iOS링크 = data.get('iOS링크', '')
    Android링크 = data.get('Android링크', '')
    image_1_url = data.get('image_1_url', '')
    신규혜택링크 = data.get('신규혜택링크', '')
    마무리글 = data.get('마무리글', '')
    추천글링크 = data.get('추천글링크', '')

    # 신규가입 혜택 HTML
    signup_benefits_html = build_signup_benefits_html(data.get('signup_benefits', []))

    # 기존회원 혜택 HTML
    existing_benefits_html = build_existing_benefits_html(
        data.get('existing_user_benefits', []),
        date_path,
        서비스명
    )

    # 이미지 링크 처리
    if image_1_url:
        image_1_html = f'''<h4> 해당 배너를 클릭 후 가입하시면 자동으로 포인트가 적립됩니다.</h4>
<div class="wp-block-image">
    <figure class="aligncenter size-full is-resized">
        <a href="{image_1_url}" target="_blank" rel="noopener noreferrer">
            <img loading="lazy" decoding="async"
                 width="1022" height="1624"
                 src="/assets/img/{date_path}/image-1.webp"
                 alt="{서비스명} 초대코드 회원가입"
                 style="width:400px"
                >
        </a>
    </figure>
</div>'''
    else:
        image_1_html = f'''<div class="wp-block-image">
    <figure class="aligncenter size-full is-resized">
        <img loading="lazy" decoding="async"
             width="1022" height="1624"
             src="/assets/img/{date_path}/image-1.webp"
             alt="{서비스명} 초대코드 회원가입"
             style="width:400px"
            >
    </figure>
</div>'''

    # 신규혜택링크 버튼 처리
    if 신규혜택링크:
        benefit_button_html = f'''
<div style="display: flex; justify-content: center; margin: 20px 0;">
    <a class="custom-button1-a-attribute"
       href="{신규혜택링크}"
       target="_blank"
       rel="noopener noreferrer">
        <div class="custom-button1-container" style="max-width:650px;">
            <div class="custom-button1-text-container">
                <span class="first-line">{서비스명}</span>
                <span class="second-line">신규가입 쿠폰팩 확인하기</span>
            </div>
        </div>
    </a>
</div>
'''
    else:
        benefit_button_html = ''

    # 본문 조립
    body = f'''
<p>{서비스설명}. 저도 직접 사용해 보니 {실사용장점}이 아주 유용하더라고요. 오늘은 신규 가입 시 놓치면 안 되는 <strong>초대코드 혜택</strong>과 <strong>결제 할인 꿀팁</strong>을 총정리해 드립니다.</p>

<h2 class="wp-block-heading">⭐ {서비스명} 초대코드</h2>
<h3 class="wp-block-heading">초대 코드 : <strong><strong>{코드}</strong></strong></h3>

{{% include promo-code-copy-box.html
label="EXCLUSIVE"
title="{서비스명} 초대 코드"
code="{코드}"
desc="{초대코드혜택}"
%}}

<span class="underline">-- 조건 : 신규가입 시 입력</span>
<p>초대 코드는 가입 시 입력이 가능하며, {서비스명} 이용이 처음이 아니시라면 하단에서 소개드리는 '기존 회원 쿠폰 받기' 부분을 참고하시어 이용해 보시기 바랍니다.</p>
<p style="font-size:18px">하단의 이미지와 같이 회원가입 시 가장 하단에 있는 초대코드 입력 부분에 [{코드}]를 입력하시면 됩니다.<br>
    <strong class="red">회원가입 이후에는 코드 입력이 불가하니 꼭 가입 시 입력하시기 바랍니다.</strong>
</p>

{image_1_html}
<p>초대코드 입력 시 혜택 : <strong>{초대코드혜택}</strong> ({구매조건} 적용)</p>

<h3 class=wp-block-heading>{서비스명} 앱 다운로드</h3>
<p>먼저 {서비스명} 앱을 다운로드 해주세요. <br>{서비스명}은 PC, 모바일 웹으로도 가능하나 편리하게 최대할인을 적용하시려면 앱을 설치하시는 것을 추천드립니다. (앱에서만 적용되는 쿠폰이 있습니다.)</p>
<p class=has-medium-font-size>다운로드 후 ⭐<strong class=red>회원가입시 초대 코드를 입력</strong>⭐하셔야 추가 쿠폰을 받으실 수 있습니다!</p>

{{% include app-download-button.html
app_name="{서비스명}"
ios_url="{iOS링크}"
android_url="{Android링크}"
%}}

<h2 class="wp-block-heading">🎁 신규 회원 가입 혜택</h2>
<h5 class=wp-block-heading><strong>✅ 신규 회원 가입시 아래 배너를 클릭하셔서 지급받으신 쿠폰 혜택을 확인하신 후 구매하시기 바랍니다&nbsp;</strong></h5>

<div class="wp-block-image">
    <figure class="aligncenter size-full is-resized">
        <img loading="lazy" decoding="async"
             width="1022" height="1778"
             src="/assets/img/{date_path}/image-2.webp"
             alt="{서비스명} 신규회원 혜택"
             style="width:500px"
            >
    </figure>
</div>
{benefit_button_html}
{signup_benefits_html}

<h2 class=wp-block-heading>⭐ {서비스명} 기존 회원 쿠폰 받기 (신규회원도 필수 적용)</h2>

{existing_benefits_html}
<p>{서비스명} 서비스는 {마무리글}</p>

{{% include recommended-post.html url="{추천글링크}" %}}'''

    return body.strip()


def create_post(yml_path, template_path=None, output_dir=None):
    """포스트 생성 메인 함수"""

    # 기본 경로 설정
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    if output_dir is None:
        output_dir = os.path.join(base_dir, '_posts', 'financial-and-investment', 'promo-code')

    # 데이터 로드
    data = load_yaml(yml_path)

    # 오늘 날짜
    today = datetime.now().strftime('%Y-%m-%d')

    # front matter 생성 (기본 메타데이터만)
    front_matter = build_front_matter(data, today)

    # 본문 생성 (값 직접 삽입)
    body = build_body(data, today)

    # 출력 파일 경로
    서비스명 = data.get('서비스명', 'unknown')
    filename = f"{today}-{서비스명}-초대코드.html"
    output_path = os.path.join(output_dir, filename)

    # 디렉토리 생성
    os.makedirs(output_dir, exist_ok=True)

    # 파일 작성
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write('---\n')
        yaml.dump(front_matter, f, allow_unicode=True, default_flow_style=False, sort_keys=False)
        f.write('---\n')
        f.write(body)

    print(f"포스트 생성 완료: {output_path}")
    print(f"")
    print(f"다음 단계:")
    print(f"1. 이미지 준비: /assets/img/{today.replace('-', '/')}/")
    print(f"   - {서비스명}-썸네일.webp")
    print(f"   - image-1.webp")
    print(f"   - image-2.webp")

    # existing_user_benefits에서 image_name이 있는 경우 안내
    existing_benefits = data.get('existing_user_benefits', [])
    for benefit in existing_benefits:
        if benefit.get('image_name'):
            print(f"   - {benefit['image_name']}")

    print(f"2. Jekyll 빌드: bundle exec jekyll serve")

    return output_path


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("사용법: python3 scripts/create_referral_post.py <yml파일경로>")
        print("예시: python3 scripts/create_referral_post.py _templates/referral-post-template.yml")
        sys.exit(1)

    yml_path = sys.argv[1]

    if not os.path.exists(yml_path):
        print(f"오류: 파일을 찾을 수 없습니다 - {yml_path}")
        sys.exit(1)

    create_post(yml_path)