from pico2d import *
from character_naruto_frames import FRAMES

open_canvas(800, 600)

# 합쳐진 이미지 로드
img = load_image('character_temp_transparent.png')

current_frame = 0
running = True

print(f"총 프레임 수: {len(FRAMES)}")
print("조작법: 방향키(←→) - 프레임 이동, SPACE - 애니메이션 재생/정지, ESC - 종료")

animating = False
frame_time = 0

while running:
    clear_canvas()

    frame = FRAMES[current_frame]

    # 화면 중앙에 출력 (3배 확대)
    x, y = 400, 300
    scale = 3  # 3배 확대

    img.clip_draw(
        frame['left'],
        frame['bottom'],
        frame['width'],
        frame['height'],
        x, y,
        frame['width'] * scale,
        frame['height'] * scale
    )

    # 프레임 정보 출력
    print(f"\rFrame {current_frame}/{len(FRAMES)-1}: "
          f"left={frame['left']}, bottom={frame['bottom']}, "
          f"width={frame['width']}, height={frame['height']}", end='')

    update_canvas()

    # 이벤트 처리
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            running = False
        elif event.type == SDL_KEYDOWN:
            if event.key == SDLK_ESCAPE:
                running = False
            elif event.key == SDLK_RIGHT:
                current_frame = (current_frame + 1) % len(FRAMES)
            elif event.key == SDLK_LEFT:
                current_frame = (current_frame - 1) % len(FRAMES)
            elif event.key == SDLK_SPACE:
                animating = not animating
                frame_time = 0

    # 애니메이션 모드
    if animating:
        frame_time += 0.05
        if frame_time > 0.1:  # 10fps
            current_frame = (current_frame + 1) % len(FRAMES)
            frame_time = 0

    delay(0.05)

print("\n프로그램 종료")
close_canvas()

