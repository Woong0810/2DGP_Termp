from pico2d import load_image, SDL_KEYDOWN, SDL_KEYUP, SDLK_n, SDLK_LEFT, SDLK_RIGHT, SDLK_UP
from idle import Idle
from run import Run
from normal_attack import Normal_Attack
from jump import Jump
from state_machine import StateMachine
from event_to_string import (right_down, right_up, left_down, left_up,
                              n_down, up_down, segment_end, landed)

class Character:
    def __init__(self):
        self.x, self.y = 400, 90
        self.frame = 0
        self.face_dir = 1
        self.dir = 0  # RUN 상태에서 사용할 방향
        self.image = load_image('Characters_Naruto_clean.png')

        self.accum_time = 0.0
        self.frame_duration = 0.1  # 기본값, 상태별로 변경 가능

        self.IDLE = Idle(self)
        self.RUN = Run(self)
        self.NORMAL_ATTACK = Normal_Attack(self)
        self.JUMP = Jump(self)

        self.state_machine = StateMachine(
            self.IDLE,
            {
                self.IDLE: {
                    n_down: self.NORMAL_ATTACK,
                    right_down: self.RUN,
                    left_down: self.RUN,
                    up_down: self.JUMP
                },
                self.RUN: {
                    right_up: self.IDLE,
                    left_up: self.IDLE,
                    n_down: self.NORMAL_ATTACK,
                    up_down: self.JUMP
                },
                self.NORMAL_ATTACK: {
                    segment_end: self.IDLE,
                    n_down: self.NORMAL_ATTACK,  # 다음 콤보
                    up_down: self.JUMP
                },
                self.JUMP: {
                    landed: self.IDLE
                    # up_down은 제거 - handle_event에서 처리
                }
            }
        )

    def update(self, dt):
        self.state_machine.update(dt)

    def draw(self):
        self.state_machine.draw()

    def handle_event(self, event):
        # NORMAL_ATTACK 상태에서 N키를 누르면 다음 콤보 예약
        if self.state_machine.cur_state == self.NORMAL_ATTACK and event.type == SDL_KEYDOWN and event.key == SDLK_n:
            self.NORMAL_ATTACK.request_next_combo()
            return  # 상태 머신에 이벤트 전달하지 않음 (상태 전환 방지)

        # JUMP 상태에서 처리
        if self.state_machine.cur_state == self.JUMP:
            # 윗 방향키 - 2단 점프
            if event.type == SDL_KEYDOWN and event.key == SDLK_UP:
                self.JUMP.handle_double_jump()
            # 좌우 방향키
            elif event.type == SDL_KEYDOWN:
                if event.key == SDLK_LEFT:
                    self.JUMP.dir = -1
                elif event.key == SDLK_RIGHT:
                    self.JUMP.dir = 1
            elif event.type == SDL_KEYUP:
                if event.key == SDLK_LEFT and self.JUMP.dir == -1:
                    self.JUMP.dir = 0
                elif event.key == SDLK_RIGHT and self.JUMP.dir == 1:
                    self.JUMP.dir = 0

        self.state_machine.handle_event(('INPUT', event))
