import os
import subprocess

def convert_2026_assets():
    # 1. 대상 폴더 경로 설정 (사용자의 실제 로컬 경로에 맞춰 수정 필요)
    # 예: "C:/Users/name/blog/assets/img/2026" 또는 "./assets/img/2026"
    target_dir = "./assets/img/2026"

    if not os.path.exists(target_dir):
        print(f"오류: {target_dir} 폴더를 찾을 수 없습니다.")
        return

    # 2. 변환할 파일 확장자 정의
    valid_extensions = ('.png', '.jpg', '.jpeg')
    files = [f for f in os.listdir(target_dir) if f.lower().endswith(valid_extensions)]

    if not files:
        print("변환할 이미지가 없습니다.")
        return

    print(f"총 {len(files)}개의 이미지를 변환합니다...")

    for file in files:
        # 전체 파일 경로 생성
        input_path = os.path.join(target_dir, file)
        output_path = os.path.join(target_dir, os.path.splitext(file)[0] + ".webp")

        # cwebp 명령어
        # -q 85: 화질과 용량 사이의 최적 지점
        # -m 6: 가장 느리지만 최상의 압축 품질
        command = f'cwebp -q 85 -m 6 "{input_path}" -o "{output_path}"'

        try:
            subprocess.run(command, shell=True, check=True)
            print(f"성공: {file} -> {os.path.basename(output_path)}")

            # (선택 사항) 변환 완료 후 원본 파일 삭제를 원하시면 아래 주석을 해제하세요.
            # os.remove(input_path)

        except subprocess.CalledProcessError:
            print(f"오류 발생: {file} 변환 실패")

if __name__ == "__main__":
    convert_2026_assets()