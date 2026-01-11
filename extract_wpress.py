#!/usr/bin/env python3
"""
.wpress 파일 압축 해제 스크립트
All-in-One WP Migration 백업 파일을 로컬 폴더에 풀어줍니다.

사용법:
    python extract_wpress.py <wpress_file> <output_dir>

예시:
    python extract_wpress.py backup.wpress ./extracted
"""

import sys
import os


def extract_wpress(wpress_file, output_dir):
    """wpress 파일을 지정된 디렉토리에 압축 해제합니다."""

    if not os.path.exists(wpress_file):
        print(f"오류: 파일을 찾을 수 없습니다: {wpress_file}")
        sys.exit(1)

    os.makedirs(output_dir, exist_ok=True)

    file_count = 0
    total_size = 0

    with open(wpress_file, 'rb') as f:
        while True:
            # wpress 헤더 구조 (4377 bytes):
            # - 파일명: 255 bytes
            # - 파일 크기: 14 bytes
            # - mtime: 12 bytes
            # - prefix: 4096 bytes
            header = f.read(4377)

            if len(header) < 4377:
                break

            # 파일명 추출 (첫 255 bytes)
            name = header[0:255].rstrip(b'\x00').decode('utf-8', errors='replace')

            # 파일 크기 추출 (255-269 bytes)
            size_str = header[255:269].rstrip(b'\x00')
            if not size_str:
                break
            size = int(size_str)

            # prefix (경로) 추출 (281-4377 bytes)
            prefix = header[281:4377].rstrip(b'\x00').decode('utf-8', errors='replace')

            if not name:
                break

            # 파일 내용 읽기
            content = f.read(size)

            # 전체 경로 구성
            if prefix:
                full_path = os.path.join(output_dir, prefix, name)
            else:
                full_path = os.path.join(output_dir, name)

            # 디렉토리 생성
            dir_path = os.path.dirname(full_path)
            if dir_path:
                os.makedirs(dir_path, exist_ok=True)

            # 파일 저장
            with open(full_path, 'wb') as out:
                out.write(content)

            file_count += 1
            total_size += size
            print(f"추출: {prefix}/{name}" if prefix else f"추출: {name}")

    print(f"\n완료! {file_count}개 파일 추출됨 (총 {total_size / 1024 / 1024:.2f} MB)")


def main():
    if len(sys.argv) != 3:
        print("사용법: python extract_wpress.py <wpress_file> <output_dir>")
        print("예시:   python extract_wpress.py backup.wpress ./extracted")
        sys.exit(1)

    wpress_file = sys.argv[1]
    output_dir = sys.argv[2]

    print(f"압축 해제 중: {wpress_file}")
    print(f"출력 디렉토리: {output_dir}\n")

    extract_wpress(wpress_file, output_dir)


if __name__ == "__main__":
    main()
