import os
import re
from datetime import datetime

# 포스트가 저장된 디렉토리
POSTS_DIR = '_posts'
# 타겟 카테고리 이름
TARGET_CATEGORY = "할인코드 & 추천코드"

def update_posts():
    today = datetime.now().strftime('%Y-%m-%d')
    count = 0

    if not os.path.exists(POSTS_DIR):
        print(f"에러: {POSTS_DIR} 디렉토리를 찾을 수 없습니다.")
        return

    for filename in os.listdir(POSTS_DIR):
        if filename.endswith('.md') or filename.endswith('.html'):
            filepath = os.path.join(POSTS_DIR, filename)

            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()

            # Front Matter 추출
            front_matter_match = re.search(r'^---(.*?)---', content, re.DOTALL)
            if front_matter_match:
                front_matter = front_matter_match.group(1)

                # '할인코드 & 추천코드' 카테고리가 포함된 경우만 실행
                if TARGET_CATEGORY in front_matter:
                    # last_modified_at 업데이트 또는 추가
                    if 'last_modified_at:' in front_matter:
                        new_front_matter = re.sub(
                            r'last_modified_at:.*',
                            f'last_modified_at: {today}',
                            front_matter
                        )
                    else:
                        # date: 항목 바로 다음에 last_modified_at 추가
                        new_front_matter = re.sub(
                            r'(date:.*)',
                            r'\1\nlast_modified_at: ' + today,
                            front_matter
                        )

                    new_content = content.replace(front_matter, new_front_matter)

                    with open(filepath, 'w', encoding='utf-8') as f:
                        f.write(new_content)
                    print(f"성공: {filename}")
                    count += 1

    print(f"\n--- 업데이트 완료 ---")
    print(f"총 {count}개의 '할인코드 & 추천코드' 포스트가 {today} 날짜로 갱신되었습니다.")

if __name__ == "__main__":
    update_posts()