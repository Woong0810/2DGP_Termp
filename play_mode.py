from pico2d import *

import game_world
from character import Character
# from characters_itachi_frames import FRAMES
# from characters_jiraiya_frames import FRAMES
import game_framework

def handle_events():
    event_list = get_events()
    for event in event_list:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.quit()
        else:
            character.handle_event(event)

def init():
    global character

    character = Character()
    game_world.add_object(character, 1)

def update(dt):
    game_world.update(dt)

def draw():
    clear_canvas()
    game_world.render()
    update_canvas()

def finish():
    pass