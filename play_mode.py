from pico2d import *

import game_world
from background import Background
from character import Character
from character_config import NarutoConfig, ItachiConfig
import game_framework
import title_mode

def handle_events():
    event_list = get_events()
    for event in event_list:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.change_mode(title_mode)
        elif event.type == SDL_KEYDOWN and event.key == SDLK_h:
            player1.take_hit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_j:
            player2.take_hit()
        else:
            player1.handle_event(event)
            player2.handle_event(event)

def init():
    global player1, player2, background
    background = Background()
    game_world.add_object(background, 0)

    from player_config import PLAYER1_KEY_BINDINGS, PLAYER2_KEY_BINDINGS

    player1 = Character(NarutoConfig(), key_bindings=PLAYER1_KEY_BINDINGS, x=200, y=30)
    game_world.add_object(player1, 1)

    player2 = Character(ItachiConfig(), key_bindings=PLAYER2_KEY_BINDINGS, x=600, y=30)
    player2.face_dir = -1  # 왼쪽을 향하도록
    game_world.add_object(player2, 1)

    # 서로를 상대로 설정
    player1.set_opponent(player2)
    player2.set_opponent(player1)

def update():
    game_world.update()
    game_world.handle_collision()

def draw():
    clear_canvas()
    game_world.render()
    update_canvas()

def finish():
    game_world.clear()

def pause(): pass
def resume(): pass