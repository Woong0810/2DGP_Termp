import time
from pico2d import *

from character import Character
# from characters_itachi_frames import FRAMES
# from characters_jiraiya_frames import FRAMES

def handle_events():
    global running

    event_list = get_events()
    for event in event_list:
        if event.type == SDL_QUIT:
            running = False
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            running = False
        else:
            character.handle_event(event)

running = True

def reset_world():
    global world
    global character

    world = []
    character = Character()
    world.append(character)

def update_world(dt):
    for o in world:
        o.update(dt)

def render_world():
    clear_canvas()
    for o in world:
        o.draw()
    update_canvas()

open_canvas(800, 600)

reset_world()

last_time = time.time()
while running:
    current = time.time()
    dt = current - last_time
    last_time = current

    handle_events()
    update_world(dt)
    render_world()
    delay(0.001)

close_canvas()