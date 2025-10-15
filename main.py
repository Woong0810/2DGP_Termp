from pico2d import *
from characters_naruto_frames import FRAMES
# from characters_itachi_frames import FRAMES
# from characters_jiraiya_frames import FRAMES

class Character:
    def __init__(self):
        self.x, self.y = 400, 300
        self.frame = 0
        self.face_dir = 1
        self.image = None
        self.IDLE = None
        self.state_machine = None
    def update(self):
        self.state_machine.update()
    def draw(self):
        self.state_machine.draw()
        pass
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
    delay(0.01)

close_canvas()