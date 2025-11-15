from PIL import Image
import json

def extract_frames_from_transparent(image_path):
    """투명 배경 이미지에서 프레임 정보를 추출합니다."""
    img = Image.open(image_path)
    img = img.convert('RGBA')
    width, height = img.size

    print(f"\n처리 중: {image_path}")
    print(f"이미지 크기: {width} x {height}")

    # 각 행을 스캔하여 프레임 찾기
    frames = []
    y = 0

    while y < height:
        # 현재 y에서 불투명 픽셀이 있는지 확인
        has_content = False
        for x in range(width):
            if y < height:
                pixel = img.getpixel((x, y))
                if pixel[3] > 0:  # 알파 채널이 0보다 크면
                    has_content = True
                    break

        if not has_content:
            y += 1
            continue

        # 프레임의 상단을 찾음
        frame_top = y

        # 프레임의 하단을 찾음
        frame_bottom = frame_top
        while frame_bottom < height:
            row_has_content = False
            for x in range(width):
                if frame_bottom < height:
                    pixel = img.getpixel((x, frame_bottom))
                    if pixel[3] > 0:
                        row_has_content = True
                        break
            if not row_has_content:
                break
            frame_bottom += 1

        # 이 행에서 모든 프레임 찾기
        x = 0
        while x < width:
            # 불투명 픽셀 찾기
            has_pixel = False
            for check_y in range(frame_top, frame_bottom):
                if check_y < height and x < width:
                    pixel = img.getpixel((x, check_y))
                    if pixel[3] > 0:
                        has_pixel = True
                        break

            if not has_pixel:
                x += 1
                continue

            # 프레임의 왼쪽 찾음
            frame_left = x

            # 프레임의 오른쪽 찾음
            frame_right = frame_left
            while frame_right < width:
                col_has_content = False
                for check_y in range(frame_top, frame_bottom):
                    if check_y < height and frame_right < width:
                        pixel = img.getpixel((frame_right, check_y))
                        if pixel[3] > 0:
                            col_has_content = True
                            break
                if not col_has_content:
                    break
                frame_right += 1

            # 프레임 정보 저장 (Pico2D 좌표계: bottom-left 기준)
            frame_width = frame_right - frame_left
            frame_height = frame_bottom - frame_top

            if frame_width > 0 and frame_height > 0:
                frames.append({
                    'left': frame_left,
                    'bottom': height - frame_bottom,  # Pico2D는 bottom-left 기준
                    'width': frame_width,
                    'height': frame_height
                })

            x = frame_right + 1

        y = frame_bottom + 1

    return frames

# 3개의 이미지에서 프레임 추출
image_files = [
    'character_naruto_1.png',
    'character_naruto_2.png',
    'character_naruto_3.png'
]

all_frames = []

for img_file in image_files:
    try:
        frames = extract_frames_from_transparent(img_file)
        print(f"추출된 프레임 수: {len(frames)}")
        all_frames.extend(frames)
    except Exception as e:
        print(f"오류 발생 ({img_file}): {e}")

print(f"\n총 추출된 프레임 수: {len(all_frames)}")

# 결과를 파이썬 파일로 저장
output_file = 'character_temp_frames_v3.py'
with open(output_file, 'w', encoding='utf-8') as f:
    f.write("# Auto-generated frame data for character_temp\n")
    f.write("FRAMES = [\n")
    for frame in all_frames:
        f.write(f"    {frame},\n")
    f.write("]\n")

print(f"\n프레임 정보가 '{output_file}'에 저장되었습니다.")

# 처음 10개 프레임 출력
print("\n처음 10개 프레임:")
for i, frame in enumerate(all_frames[:10]):
    print(f"  Frame {i}: {frame}")

