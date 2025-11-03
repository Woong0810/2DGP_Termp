from pico2d import *

import game_world
from character import Character
from character_config import NarutoConfig, ItachiConfig
import game_framework

def handle_events():
    event_list = get_events()
    for event in event_list:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.quit()
        else:
            # 1P는 player1, 2P는 player2가 처리
            player1.handle_event(event)
            # player2.handle_event(event)  # 2P 조작은 나중에 추가

def init():
    global player1, player2

    # 1P: 나루토 (왼쪽)
    player1 = Character(NarutoConfig(), x=200, y=90)
    game_world.add_object(player1, 1)

    # 2P: 이타치 (오른쪽) - 일단 IDLE만 동작
    player2 = Character(ItachiConfig(), x=600, y=90)
    player2.face_dir = -1  # 왼쪽을 향하도록
    game_world.add_object(player2, 1)

def update(dt):
    game_world.update(dt)

def draw():
    clear_canvas()
    game_world.render()
    update_canvas()

def finish():
    pass