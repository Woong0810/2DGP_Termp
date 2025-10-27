from pico2d import load_image

from idle import Idle
from run import Run
from normal_attack import Normal_Attack
from jump import Jump
from state_machine import StateMachine
from event_to_string import right_down, right_up, left_down, left_up, n_down, n_up, up_down, up_up, landed

class Character:
    def __init__(self):
        self.x, self.y = 400, 300
        self.frame = 0
        self.face_dir = 1
        self.image = load_image('Characters_Naruto_clean.png')

        self.accum_time = 0.0
        self.frame_duration = 0.1  # 기본값, 상태별로 변경 가능

        self.IDLE = Idle(self)  # Idle 상태 객체 생성
        self.RUN = Run(self)
        self.NORMAL_ATTACK = Normal_Attack(self)
        self.JUMP = Jump(self)
        self.state_machine = StateMachine(
            self.IDLE,
        {
                self.IDLE: {n_down: self.NORMAL_ATTACK, right_up: self.RUN,
                            left_up: self.RUN, right_down: self.RUN, left_down: self.RUN,
                            up_down: self.JUMP},
                self.RUN: {right_up: self.IDLE, left_up: self.IDLE, right_down: self.IDLE,
                           left_down: self.IDLE, n_down: self.NORMAL_ATTACK,
                           },
                self.NORMAL_ATTACK: {n_up: self.IDLE},
                self.JUMP: {up_down: self.JUMP, landed: self.IDLE}
             }
        )
    def update(self, dt):
        self.state_machine.update(dt)
    def draw(self):
        self.state_machine.draw()
        pass
    def handle_event(self, event):
        self.state_machine.handle_event(('INPUT', event))
