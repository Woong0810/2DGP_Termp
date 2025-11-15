from PIL import Image

# 3개의 투명 배경 이미지 로드
img1 = Image.open('character_naruto_1.png')
img2 = Image.open('character_naruto_2.png')
img3 = Image.open('character_naruto_3.png')

print(f"Image 1 크기: {img1.size}")
print(f"Image 2 크기: {img2.size}")
print(f"Image 3 크기: {img3.size}")

# 최대 너비 찾기
max_width = max(img1.width, img2.width, img3.width)

# 총 높이 계산
total_height = img1.height + img2.height + img3.height

print(f"\n합친 이미지 크기: {max_width} x {total_height}")

# 새 이미지 생성 (RGBA 모드, 투명 배경)
merged_image = Image.new('RGBA', (max_width, total_height), (0, 0, 0, 0))

# 이미지들을 위에서 아래로 붙이기
current_y = 0

# Image 1 붙이기
merged_image.paste(img1, (0, current_y))
current_y += img1.height
print(f"Image 1 붙임: y={0} ~ {img1.height}")

# Image 2 붙이기
merged_image.paste(img2, (0, current_y))
print(f"Image 2 붙임: y={current_y} ~ {current_y + img2.height}")
current_y += img2.height

# Image 3 붙이기
merged_image.paste(img3, (0, current_y))
print(f"Image 3 붙임: y={current_y} ~ {current_y + img3.height}")

# 저장
output_filename = 'character_temp_transparent.png'
merged_image.save(output_filename)

print(f"\n✅ 합친 이미지가 '{output_filename}'로 저장되었습니다.")

