from pico2d import load_image

from idle import Idle
from run import Run
from state_machine import StateMachine
from event_to_string import right_down, right_up, left_down, left_up

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
