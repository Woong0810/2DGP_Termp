from pico2d import load_image

from idle import Idle
from state_machine import StateMachine

class Character:
    def __init__(self):
        self.x, self.y = 400, 300
        self.frame = 0
        self.face_dir = 1
        self.image = load_image('Characters_Naruto_clean.png')
        self.IDLE = Idle(self)  # Idle 상태 객체 생성
        self.state_machine = StateMachine(self.IDLE)
    def update(self):
        self.state_machine.update()
    def draw(self):
        self.state_machine.draw()
        pass
