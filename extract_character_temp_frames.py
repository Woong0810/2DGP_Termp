from PIL import Image
import os

# 추출할 원본 PNG 경로 (이타치 SA 이미지로 변경)
IMAGE_PATH = r"C:\Users\user\Documents\GitHub\2DGP_Termp\character_itachi_sa.png"

# 생성할 프레임 파일 경로
OUTPUT_PATH = r"C:\Users\user\Documents\GitHub\2DGP_Termp\character_itachi_sa_frames.py"

# 최소 너비(픽셀) – 노이즈 같은 얇은 세그라멘트는 무시
MIN_WIDTH = 3

img = Image.open(IMAGE_PATH).convert("RGBA")
w, h = img.size
pixels = img.load()

def column_has_sprite(x):
    """해당 x열에 투명 아닌 픽셀이 하나라도 있으면 True"""
    for y in range(h):
        r, g, b, a = pixels[x, y]
        if a > 10:          # 알파가 0이 아니면 스프라이트라고 가정
            return True
    return False

segments = []
in_seg = False
start = 0

for x in range(w):
    if column_has_sprite(x):
        if not in_seg:
            in_seg = True
            start = x
    else:
        if in_seg:
            in_seg = False
            width = x - start
            if width >= MIN_WIDTH:
                segments.append((start, width))

# 마지막 세그먼트 닫기
if in_seg:
    width = w - start
    if width >= MIN_WIDTH:
        segments.append((start, width))

print(f"총 세그먼트 개수: {len(segments)}")
frames = []
for i, (left, width) in enumerate(segments):
    frames.append({
        "left": left,
        "bottom": 0,
        "width": width,
        "height": h
    })

for i, f in enumerate(frames):
    print(i, f)

# 프레임 파일로 저장 (FRAMES = [ ... ])
with open(OUTPUT_PATH, 'w', encoding='utf-8') as out:
    out.write("# Auto-generated frame data from extract_character_temp_frames.py\n")
    out.write("FRAMES = [\n")
    for f in frames:
        out.write(f"    {{'left': {f['left']}, 'bottom': {f['bottom']}, 'width': {f['width']}, 'height': {f['height']}}},\n")
    out.write("]\n")

print(f"프레임 정보를 '{OUTPUT_PATH}'에 저장했습니다.")
