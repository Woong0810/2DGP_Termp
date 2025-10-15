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

open_canvas(800, 600)



close_canvas()