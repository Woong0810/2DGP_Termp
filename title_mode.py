from pico2d import *
import game_framework
import character_select_mode

image = None
font = None
selected_mode = 0

def draw_bold_text(font, x, y, text, color, thickness=1):
    for dx in range(-thickness, thickness + 1):
        for dy in range(-thickness, thickness + 1):
            font.draw(x + dx, y + dy, text, color)

def init():
    global image, font, selected_mode
    image = load_image('title.png')
    font = load_font('font.ttf', 40)
    selected_mode = 0

def update():
    pass

def draw():
    clear_canvas()
    image.draw(400, 300)

    if selected_mode == 0:
        draw_bold_text(font, 30, 250, '> 2P MODE <', (255, 255, 0), thickness=1)
        draw_bold_text(font, 30, 200, '  AI MODE  ', (200, 200, 200), thickness=1)
    else:
        draw_bold_text(font, 30, 250, '  2P MODE  ', (200, 200, 200), thickness=1)
        draw_bold_text(font, 30, 200, '> AI MODE <', (255, 255, 0), thickness=1)

    small_font = load_font('font.ttf', 25)
    draw_bold_text(small_font, 30, 130, 'UP/DOWN: Select', (255, 255, 255), thickness = 1)
    draw_bold_text(small_font, 30, 90, 'SPACE: Start', (255, 255, 255), thickness = 1)
    
    update_canvas()

def finish():
    global image, font
    del image
    del font
    pass

def handle_events():
    global selected_mode
    event_list = get_events()
    for event in event_list:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_SPACE:
            character_select_mode.game_mode = 'AI' if selected_mode == 1 else '2P'
            game_framework.change_mode(character_select_mode)
        elif event.type == SDL_KEYDOWN and event.key == SDLK_UP:
            selected_mode = (selected_mode - 1) % 2
        elif event.type == SDL_KEYDOWN and event.key == SDLK_DOWN:
            selected_mode = (selected_mode + 1) % 2

def pause(): pass
def resume(): pass