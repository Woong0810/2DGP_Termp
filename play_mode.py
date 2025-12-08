from pico2d import *

import game_world
from background import Background
from character import Character
from character_config import NarutoConfig, ItachiConfig, JiraiyaConfig, CHARACTER_CONFIGS
import game_framework
import title_mode
from hp_bar import HPBar
from round_timer import RoundTimer
from camera import camera
from special_gauge_bar import SpecialGaugeBar
from round_manager import RoundManager

def handle_events():
    event_list = get_events()
    for event in event_list:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.change_mode(title_mode)
        else:
            if round_manager is None or not round_manager.can_control():
                continue
            player1.handle_event(event)
            player2.handle_event(event)

CHAR_CONFIG_LIST = list(CHARACTER_CONFIGS.values())
selected_player1_index = 0
selected_player2_index = 1
selected_stage_index = 0

player1_icon_image = None
player2_icon_image = None
round_manager = None

def set_selected_characters(p1_idx, p2_idx):
    global selected_player1_index, selected_player2_index
    selected_player1_index = p1_idx
    selected_player2_index = p2_idx

def set_selected_stage(stage_index):
    global selected_stage_index
    selected_stage_index = stage_index

def init():
    global player1, player2, background, player1_hp_bar, player2_hp_bar, round_timer
    global player1_icon_image, player2_icon_image, player1_gauge_bar, player2_gauge_bar, round_manager

    background = Background(stage_index = selected_stage_index)
    game_world.add_object(background, 0)

    camera.set_stage_bounds(0, background.width)

    from player_config import PLAYER1_KEY_BINDINGS, PLAYER2_KEY_BINDINGS

    player1_config = CHAR_CONFIG_LIST[selected_player1_index]
    player2_config = CHAR_CONFIG_LIST[selected_player2_index]

    player1 = Character(player1_config(), key_bindings=PLAYER1_KEY_BINDINGS, x=800, y=30, stage=background)
    game_world.add_object(player1, 1)

    player2 = Character(player2_config(), key_bindings=PLAYER2_KEY_BINDINGS, x=1200, y=30, stage=background)
    player2.face_dir = -1
    game_world.add_object(player2, 1)

    camera.set_targets(player1, player2)

    game_world.add_collision_pairs('normal_attack:character', None, player1)
    game_world.add_collision_pairs('normal_attack:character', None, player2)
    game_world.add_collision_pairs('jump_attack:character', None, player1)
    game_world.add_collision_pairs('jump_attack:character', None, player2)
    game_world.add_collision_pairs('special_attack:character', None, player1)
    game_world.add_collision_pairs('special_attack:character', None, player2)
    game_world.add_collision_pairs('special_attack2:character', None, player1)
    game_world.add_collision_pairs('special_attack2:character', None, player2)
    game_world.add_collision_pairs('ranged_attack:character', None, player1)
    game_world.add_collision_pairs('ranged_attack:character', None, player2)
    game_world.add_collision_pairs('character:shuriken', player1, None)
    game_world.add_collision_pairs('character:shuriken', player2, None)
    game_world.add_collision_pairs('character:character', player1, player2)

    # 서로를 상대로 설정
    player1.set_opponent(player2)
    player2.set_opponent(player1)

    player1_hp_bar = HPBar(200, 550, character=player1, is_flipped=False)
    game_world.add_object(player1_hp_bar, 2)

    player2_hp_bar = HPBar(600, 550, character=player2, is_flipped=True)
    game_world.add_object(player2_hp_bar, 2)

    player1_gauge_bar = SpecialGaugeBar(80, 10, character=player1, is_flipped=False)
    game_world.add_object(player1_gauge_bar, 2)

    player2_gauge_bar = SpecialGaugeBar(720, 10, character=player2, is_flipped=True)
    game_world.add_object(player2_gauge_bar, 2)

    player1_icon_image = load_image(player1_config().icon_default_path)
    player2_icon_image = load_image(player2_config().icon_default_path)

    round_timer = RoundTimer(400, 550, round_time=60)
    game_world.add_object(round_timer, 2)

    round_manager = RoundManager(player1, player2, background, (800, 30), (1200, 30), round_timer)
    round_manager.start_first_round()

def update():
    game_world.update()
    camera.update()
    game_world.handle_collision()
    check_win_condition()
    round_manager.update()
    if round_manager.state == RoundManager.STATE_MATCH_OVER:
        if round_manager.timer > 2.0:
            game_framework.change_mode(title_mode)

def draw():
    clear_canvas()
    game_world.render()
    player1_icon_image.draw(40, 550, 60, 60)
    player2_icon_image.draw(760, 550, 60, 60)
    if round_manager:
        round_manager.draw_ui()
    update_canvas()

def finish():
    game_world.clear()

def check_win_condition():
    winner_str = None

    if player1.hp <= 0 and player2.hp <= 0:
        winner_str = 'draw'
    elif player2.hp <= 0:
        winner_str = 'player1'
    elif player1.hp <= 0:
        winner_str = 'player2'
    elif round_timer.is_time_over():
        if player1.hp > player2.hp:
            winner_str = 'player1'
        elif player2.hp > player1.hp:
            winner_str = 'player2'
        else:
            winner_str = 'draw'

    if winner_str is not None:
        round_manager.on_round_end(winner_str)

def pause(): pass
def resume(): pass