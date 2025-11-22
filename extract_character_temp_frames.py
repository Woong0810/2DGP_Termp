from PIL import Image

# 네가 실제 게임에서 쓰는 원본 PNG 경로
IMAGE_PATH = r"C:\Users\user\Documents\GitHub\2DGP_Termp\character_naruto_sa_2.png"

# 최소 너비(픽셀) – 노이즈 같은 얇은 세그먼트는 무시하고 싶으면 5~8 정도로 올려도 됨
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

# 필요하면 파이썬 리스트로 저장할 수 있게 한 번에 출력
print("\nframes_data = [")
for f in frames:
    print(f"    {f},")
print("]")
