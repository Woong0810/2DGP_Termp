from character_temp_frames_v3 import FRAMES

# 최소 크기 기준 (픽셀)
MIN_WIDTH = 10
MIN_HEIGHT = 10

# 유효한 프레임만 필터링
valid_frames = []
filtered_count = 0

for i, frame in enumerate(FRAMES):
    if frame['width'] >= MIN_WIDTH and frame['height'] >= MIN_HEIGHT:
        valid_frames.append(frame)
    else:
        filtered_count += 1
        print(f"필터링됨 - Frame {i}: {frame}")

print(f"\n원본 프레임 수: {len(FRAMES)}")
print(f"필터링된 프레임 수: {filtered_count}")
print(f"유효한 프레임 수: {len(valid_frames)}")

# 필터링된 결과를 새 파일로 저장
output_file = 'character_naruto_frames.py'
with open(output_file, 'w', encoding='utf-8') as f:
    f.write("# Filtered frame data for character_temp (minimum size: 10x10)\n")
    f.write("FRAMES = [\n")
    for frame in valid_frames:
        f.write(f"    {frame},\n")
    f.write("]\n")
    f.write(f"\n# Total frames: {len(valid_frames)}\n")

print(f"\n필터링된 프레임 정보가 '{output_file}'에 저장되었습니다.")

