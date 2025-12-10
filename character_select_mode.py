from pico2d import *

import game_framework
import play_mode
import title_mode
from character_config import CHARACTER_CONFIGS
from player_config import PLAYER1_KEY_BINDINGS, PLAYER2_KEY_BINDINGS
import stage_select_mode

CHAR_NAMES = list(CHARACTER_CONFIGS.keys())
CHAR_CLASSES = list(CHARACTER_CONFIGS.values())

game_mode = '2P'

char_select_mode_bg = None
bgm = None

char_icons_unselected = []
char_icons_selected = []
char_illusts = []
char_name_images = []

icon_positions = []

p1_cursor_image = None
p2_cursor_image = None

p1_cursor_index = 0
p2_cursor_index = 0

p1_selected_index = None
p2_selected_index = None

p1_locked = False
p2_locked = False

P1_LEFT = PLAYER1_KEY_BINDINGS['left']
P1_RIGHT = PLAYER1_KEY_BINDINGS['right']
P1_ATTACK = PLAYER1_KEY_BINDINGS['attack']

P2_LEFT = PLAYER2_KEY_BINDINGS['left']
P2_RIGHT = PLAYER2_KEY_BINDINGS['right']
P2_ATTACK = PLAYER2_KEY_BINDINGS['attack']

def init():
    global char_select_mode_bg, bgm
    global char_icons_unselected, char_icons_selected, char_illusts, char_name_images, icon_positions
    global p1_cursor_index, p2_cursor_index
    global p1_selected_index, p2_selected_index, p1_locked, p2_locked
    global p1_cursor_image, p2_cursor_image

    char_select_mode_bg = load_image('character_select_background.png')

    bgm = load_music('select_screen_bgm.mp3')
    bgm.set_volume(64)
    bgm.repeat_play()

    p1_cursor_image = load_image('player1_mark.png')
    p2_cursor_image = load_image('player2_mark.png')

    p1_cursor_index = 0
    p2_cursor_index = 1

    p1_selected_index = None
    p2_selected_index = None

    p1_locked = False
    p2_locked = False

    # ---- 캐릭터별 이미지 로드 ----
    char_icons_unselected = []
    char_icons_selected = []
    char_illusts = []
    char_name_images = []

    for name, cls in zip(CHAR_NAMES, CHAR_CLASSES):
        cfg = cls()

        icon_def_path = getattr(cfg, 'icon_default_path', cfg.image_path)
        icon_def_img = load_image(icon_def_path)

        icon_un_path = getattr(cfg, 'icon_unselected_path', None) or icon_def_path
        icon_un_img = load_image(icon_un_path)

        illust_path = getattr(cfg, 'illust_image_path', None) or icon_def_path
        illust_img = load_image(illust_path)

        name_path = getattr(cfg, 'name_image_path', None)
        name_img = load_image(name_path) if name_path else None

        char_icons_unselected.append(icon_un_img)
        char_icons_selected.append(icon_def_img)
        char_illusts.append(illust_img)
        char_name_images.append(name_img)

    n = len(CHAR_NAMES)
    cx = 400   # 화면 중앙 (800 x 600 기준)
    spacing = 100
    base_y = 50

    icon_positions = []
    for i in range(n):
        x = cx + (i - (n - 1) / 2) * spacing
        icon_positions.append((x, base_y))


def finish():
    global bgm
    stage_select_mode.bgm = bgm


def lock_if_select_done(key):
    global p1_locked, p2_locked, p1_selected_index, p2_selected_index

    if key == P1_ATTACK and not p1_locked:
        p1_selected_index = p1_cursor_index
        p1_locked = True

    if key == P2_ATTACK and not p2_locked:
        p2_selected_index = p2_cursor_index
        p2_locked = True


def handle_events():
    global p1_cursor_index, p2_cursor_index
    global p1_selected_index, p2_selected_index, p1_locked, p2_locked

    events = get_events()
    for e in events:
        if e.type == SDL_QUIT:
            game_framework.quit()

        elif e.type == SDL_KEYDOWN:
            key = e.key

            if key == SDLK_ESCAPE:
                game_framework.change_mode(title_mode)
                return

            if not p1_locked:
                if key == P1_LEFT:
                    p1_cursor_index = (p1_cursor_index - 1) % len(CHAR_NAMES)
                elif key == P1_RIGHT:
                    p1_cursor_index = (p1_cursor_index + 1) % len(CHAR_NAMES)

            if not p2_locked:
                if key == P2_LEFT:
                    p2_cursor_index = (p2_cursor_index - 1) % len(CHAR_NAMES)
                elif key == P2_RIGHT:
                    p2_cursor_index = (p2_cursor_index + 1) % len(CHAR_NAMES)

            lock_if_select_done(key)

            if p1_locked and p2_locked:
                if p1_selected_index is None:
                    p1_selected_index = p1_cursor_index
                if p2_selected_index is None:
                    p2_selected_index = p2_cursor_index

                play_mode.set_selected_characters(p1_selected_index, p2_selected_index)
                play_mode.set_game_mode(game_mode)

                game_framework.change_mode(stage_select_mode)
                return


def update():
    pass


def draw():
    clear_canvas()

    if char_select_mode_bg:
        char_select_mode_bg.draw(400, 300)

    for i in range(len(CHAR_NAMES)):
        x, y = icon_positions[i]

        # 이 인덱스가 강조(커서/선택) 상태인지 판단
        is_highlighted = (
            i == p1_cursor_index or
            i == p2_cursor_index or
            (p1_locked and i == p1_selected_index) or
            (p2_locked and i == p2_selected_index)
        )

        icon_img = char_icons_selected[i] if is_highlighted else char_icons_unselected[i]

        if icon_img:
            icon_img.draw(x, y, 50, 50)

    if p1_cursor_image and 0 <= p1_cursor_index < len(icon_positions):
        x, y = icon_positions[p1_cursor_index]
        p1_cursor_image.draw(x, y + 30, 20, 20)

    if p2_cursor_image and 0 <= p2_cursor_index < len(icon_positions):
        x, y = icon_positions[p2_cursor_index]
        p2_cursor_image.draw(x, y + 30, 20, 20)

    def get_display_index(locked, selected_idx, cursor_idx):
        if locked and selected_idx is not None:
            return selected_idx
        return cursor_idx

    p1_disp = get_display_index(p1_locked, p1_selected_index, p1_cursor_index)
    p2_disp = get_display_index(p2_locked, p2_selected_index, p2_cursor_index)

    # 1P 왼쪽
    if 0 <= p1_disp < len(char_illusts) and char_illusts[p1_disp]:
        char_illusts[p1_disp].draw(180, 360, 260, 360)
        if 0 <= p1_disp < len(char_name_images) and char_name_images[p1_disp]:
            char_name_images[p1_disp].draw(180, 130, 200, 60)

    # 2P 오른쪽
    if 0 <= p2_disp < len(char_illusts) and char_illusts[p2_disp]:
        char_illusts[p2_disp].draw(620, 360, 260, 360)
        if 0 <= p2_disp < len(char_name_images) and char_name_images[p2_disp]:
            char_name_images[p2_disp].draw(620, 130, 200, 60)

    update_canvas()


def pause():
    pass

def resume():
    pass
