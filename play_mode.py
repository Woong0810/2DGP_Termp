from pico2d import *

import game_world
from background import Background
from character import Character
from character_config import NarutoConfig, ItachiConfig
import game_framework
import title_mode
from hp_bar import HPBar
from round_timer import RoundTimer
import result_mode


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
    global player1, player2, background, player1_hp_bar, player2_hp_bar, round_timer
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

    player1_hp_bar = HPBar(200, 550, character=player1, is_flipped=False)
    game_world.add_object(player1_hp_bar, 2)

    player2_hp_bar = HPBar(600, 550, character=player2, is_flipped=True)
    game_world.add_object(player2_hp_bar, 2)

    round_timer = RoundTimer(400, 550, round_time=5)
    game_world.add_object(round_timer, 2)

def update():
    game_world.update()
    game_world.handle_collision()
    check_win_condition()

def draw():
    clear_canvas()
    game_world.render()
    update_canvas()

def finish():
    game_world.clear()

def check_win_condition():
    if player2.hp <= 0:
        result_mode.set_winner('player1')
        game_framework.change_mode(result_mode)
        return

    if player1.hp <= 0:
        result_mode.set_winner('player2')
        game_framework.change_mode(result_mode)
        return

    if round_timer.is_time_over():
        if player1.hp > player2.hp:
            result_mode.set_winner('player1')
        elif player2.hp > player1.hp:
            result_mode.set_winner('player2')
        else:
            result_mode.set_winner('draw')  # 무승부
        game_framework.change_mode(result_mode)
        return

def pause(): pass
def resume(): pass