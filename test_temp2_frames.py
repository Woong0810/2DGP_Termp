from pico2d import *
from character_naruto_sa_frames import FRAMES

# 설정
SPRITE_SHEET = 'character_naruto_2.png'
SCALE = 2  # 화면 표시 배율
FPS = 12   # 자동재생 시 초당 프레임
CANVAS_W, CANVAS_H = 960, 540
CENTER_X, CENTER_Y = CANVAS_W // 2, CANVAS_H // 2

# 메인
open_canvas(CANVAS_W, CANVAS_H)
image = load_image(SPRITE_SHEET)

print("character_temp_2 프레임 뷰어")
print("- 방향키 오른쪽: 다음 프레임, 왼쪽: 이전 프레임")
print("- A: 자동 재생 토글, HOME: 처음으로, END: 마지막으로, ESC: 종료")
print(f"총 프레임 수: {len(FRAMES)}")

idx = 0
autoplay = False

running = True
while running:
    clear_canvas()

    # 현재 프레임 정보
    frame = FRAMES[idx]

    # 프레임 그리기 (중앙, SCALE 배)
    image.clip_draw(frame['left'], frame['bottom'], frame['width'], frame['height'],
                    CENTER_X, CENTER_Y, frame['width'] * SCALE, frame['height'] * SCALE)

    # 화면 갱신
    update_canvas()

    # 자동 재생 처리
    if autoplay:
        delay(1.0 / FPS)
        idx = (idx + 1) % len(FRAMES)
        print(f"\rFrame {idx}: left={frame['left']}, bottom={frame['bottom']}, w={frame['width']}, h={frame['height']}   ", end='')
    else:
        # 입력 기다림 (폴링)
        events = get_events()
        if not events:
            delay(0.01)
            continue
        for e in events:
            if e.type == SDL_QUIT:
                running = False
                break
            if e.type == SDL_KEYDOWN:
                if e.key == SDLK_ESCAPE:
                    running = False
                    break
                elif e.key == SDLK_RIGHT:
                    idx = (idx + 1) % len(FRAMES)
                    print(f"Frame {idx}: left={frame['left']}, bottom={frame['bottom']}, w={frame['width']}, h={frame['height']}")
                elif e.key == SDLK_LEFT:
                    idx = (idx - 1 + len(FRAMES)) % len(FRAMES)
                    print(f"Frame {idx}: left={frame['left']}, bottom={frame['bottom']}, w={frame['width']}, h={frame['height']}")
                elif e.key == SDLK_HOME:
                    idx = 0
                    print(f"Frame {idx}: left={frame['left']}, bottom={frame['bottom']}, w={frame['width']}, h={frame['height']}")
                elif e.key == SDLK_END:
                    idx = len(FRAMES) - 1
                    print(f"Frame {idx}: left={frame['left']}, bottom={frame['bottom']}, w={frame['width']}, h={frame['height']}")
                elif e.key == SDLK_a:
                    autoplay = not autoplay
                    print(f"자동 재생: {'ON' if autoplay else 'OFF'} (FPS={FPS})")

close_canvas()
print("\n종료")

