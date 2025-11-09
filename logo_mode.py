from pico2d import *

import game_framework
import title_mode

image = None
logo_start_time = 0

def init():
    global image, logo_start_time
    image = load_image('loading_screen.png')
    logo_start_time = get_time()

def update():
    if get_time() - logo_start_time > 2.0:
        game_framework.change_mode(title_mode)

def draw():
    clear_canvas()
    image.draw(400, 300)
    update_canvas()
    pass

def finish():
    global image
    del image
    pass

def handle_events():
    event_list = get_events() # 버퍼로부터 모든 입력을 갖고 온다 일단
    # do nothing 버퍼에서 지우려고 가져온거임

def pause(): pass
def resume(): pass