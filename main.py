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

running = True

def reset_world():
    global world
    global character

    world = []
    character = Character()
    world.append(character)

def update_world():
    for o in world:
        o.update()

def render_world():
    clear_canvas()
    for o in world:
        o.draw()
    update_canvas()

open_canvas(800, 600)

reset_world()
while running:
    handle_events()
    update_world()
    render_world()
    delay(0.1)

close_canvas()