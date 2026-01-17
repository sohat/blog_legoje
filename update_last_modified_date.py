import os
import re
from datetime import datetime

def update_all_dates():
    posts_dir = "./_posts"
    today = datetime.now().strftime('%Y-%m-%d')

    if not os.path.exists(posts_dir):
        return

    files = [f for f in os.listdir(posts_dir) if f.lower().endswith(('.html', '.md'))]

    for file in files:
        filepath = os.path.join(posts_dir, file)
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()

        parts = re.split(r'---', content, maxsplit=2)
        if len(parts) < 3: continue

        front_matter = parts[1]
        body = parts[2]

        # last_modified_at이 있으면 업데이트, 없으면 새로 추가
        if 'last_modified_at:' in front_matter:
            new_front_matter = re.sub(r'last_modified_at:.*', f'last_modified_at: {today}', front_matter)
        else:
            new_front_matter = front_matter.rstrip() + f'\nlast_modified_at: {today}'

        new_content = f"---{new_front_matter}\n---{body}"
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)

    print(f"✅ 모든 포스트의 날짜를 {today}로 업데이트했습니다.")

if __name__ == "__main__":
    update_all_dates()