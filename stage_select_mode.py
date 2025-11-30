# stage_select_mode.py
from pico2d import *

import game_framework
import play_mode
from player_config import PLAYER1_KEY_BINDINGS

P1_ATTACK = PLAYER1_KEY_BINDINGS['attack']

stage_select_bg = None
stage_images = []
stage_positions = []

stage_cursor_index = 0

STAGE_INFOS = [
    (0, 'background1.png'),
    (1, 'background2.png'),
    # (2, 'background3.png'),
]


def init():
    global stage_select_bg, stage_images, stage_positions, stage_cursor_index

    stage_select_bg = load_image('character_select_background.png')

    stage_images = []
    for stage_idx, image_path in STAGE_INFOS:
        img = load_image(image_path)
        stage_images.append(img)

    stage_cursor_index = 0

    n = len(STAGE_INFOS)
    cx = 400
    base_y = 400
    spacing = 170

    stage_positions = []
    for i in range(n):
        x = cx
        y = base_y - i * spacing
        stage_positions.append((x, y))

def finish():
    pass


def handle_events():
    global stage_cursor_index

    events = get_events()
    for e in events:
        if e.type == SDL_QUIT:
            game_framework.quit()

        elif e.type == SDL_KEYDOWN:
            key = e.key

            if key == SDLK_ESCAPE:
                import character_select_mode
                game_framework.change_mode(character_select_mode)
                return

            if key == SDLK_UP:
                stage_cursor_index = (stage_cursor_index - 1) % len(STAGE_INFOS)
            elif key == SDLK_DOWN:
                stage_cursor_index = (stage_cursor_index + 1) % len(STAGE_INFOS)

            elif key == P1_ATTACK:
                stage_index, _image_path = STAGE_INFOS[stage_cursor_index]
                play_mode.set_selected_stage(stage_index)
                game_framework.change_mode(play_mode)
                return


def update():
    pass


def draw():
    clear_canvas()

    if stage_select_bg:
        stage_select_bg.draw(400, 300)

    draw_w = 500
    draw_h = 150

    for i, img in enumerate(stage_images):
        x, y = stage_positions[i]
        img.draw(x, y, draw_w, draw_h)

    if 0 <= stage_cursor_index < len(stage_positions):
        x, y = stage_positions[stage_cursor_index]

        half_w = draw_w // 2
        half_h = draw_h // 2

        left = x - half_w
        right = x + half_w
        bottom = y - half_h
        top = y + half_h

        draw_rectangle(left, bottom, right, top)

    update_canvas()


def pause():
    pass


def resume():
    pass
