from pico2d import load_image
from sdl2 import SDL_KEYDOWN, SDLK_RIGHT, SDL_KEYUP, SDLK_LEFT

from idle import Idle
from run import Run
from state_machine import StateMachine

def right_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_RIGHT
def right_up(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_RIGHT
def left_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_LEFT
def left_up(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_LEFT

class Character:
    def __init__(self):
        self.x, self.y = 400, 300
        self.frame = 0
        self.face_dir = 1
        self.image = load_image('Characters_Naruto_clean.png')
        self.IDLE = Idle(self)  # Idle 상태 객체 생성
        self.RUN = Run(self)
        self.state_machine = StateMachine(
            self.IDLE,
        {
                self.IDLE: {right_up: self.RUN, left_up: self.RUN, right_down: self.RUN, left_down: self.RUN},
                self.RUN: {right_up: self.IDLE, left_up: self.IDLE}
             }
        )
    def update(self):
        self.state_machine.update()
    def draw(self):
        self.state_machine.draw()
        pass
    def handle_event(self, event):
        self.state_machine.handle_event(('INPUT', event))
