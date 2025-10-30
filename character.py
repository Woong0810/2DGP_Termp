from pico2d import load_image, SDL_KEYDOWN, SDL_KEYUP, SDLK_n, SDLK_LEFT, SDLK_RIGHT, SDLK_UP
from idle import Idle
from run import Run
from normal_attack import Normal_Attack
from jump import Jump
from defense import Defense
from special_attack import Special_Attack
from ranged_attack import Ranged_Attack
from state_machine import StateMachine
from event_to_string import (right_down, right_up, left_down, left_up,
                              n_down, up_down, down_down, down_up, v_down, b_down,
                              segment_end, landed, special_attack_end, ranged_attack_end)

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
        self.DEFENSE = Defense(self)
        self.SPECIAL_ATTACK = Special_Attack(self)
        self.RANGED_ATTACK = Ranged_Attack(self)

        self.state_machine = StateMachine(
            self.IDLE,
            {
                self.IDLE: {
                    n_down: self.NORMAL_ATTACK,
                    right_down: self.RUN,
                    left_down: self.RUN,
                    up_down: self.JUMP,
                    down_down: self.DEFENSE,
                    v_down: self.SPECIAL_ATTACK,
                    b_down: self.RANGED_ATTACK
                },
                self.RUN: {
                    right_up: self.IDLE,
                    left_up: self.IDLE,
                    n_down: self.NORMAL_ATTACK,
                    up_down: self.JUMP,
                    down_down: self.DEFENSE,
                    v_down: self.SPECIAL_ATTACK,
                    b_down: self.RANGED_ATTACK
                },
                self.NORMAL_ATTACK: {
                    segment_end: self.IDLE,
                    up_down: self.JUMP,
                    down_down: self.DEFENSE,
                    v_down: self.SPECIAL_ATTACK,
                    b_down: self.RANGED_ATTACK
                },
                self.JUMP: {
                    landed: self.IDLE
                    # 점프 중에는 방어, 스페셜 공격, 원거리 공격 불가
                },
                self.DEFENSE: {
                    down_up: self.IDLE,
                    v_down: self.SPECIAL_ATTACK,
                    b_down: self.RANGED_ATTACK
                },
                self.SPECIAL_ATTACK: {
                    special_attack_end: self.IDLE
                    # 스페셜 공격 중에는 모든 입력 무시
                },
                self.RANGED_ATTACK: {
                    ranged_attack_end: self.IDLE
                    # 원거리 공격 중에는 모든 입력 무시
                }
            }
        )

    def update(self, dt):
        self.state_machine.update(dt)

    def draw(self):
        self.state_machine.draw()

    def handle_event(self, event):
        # SPECIAL_ATTACK, RANGED_ATTACK 상태에서는 모든 입력 무시
        if self.state_machine.cur_state == self.SPECIAL_ATTACK or self.state_machine.cur_state == self.RANGED_ATTACK:
            return

        # NORMAL_ATTACK 상태에서 N키 DOWN/UP 추적
        if self.state_machine.cur_state == self.NORMAL_ATTACK:
            if event.type == SDL_KEYDOWN and event.key == SDLK_n:
                self.NORMAL_ATTACK.handle_n_key_down()
            elif event.type == SDL_KEYUP and event.key == SDLK_n:
                self.NORMAL_ATTACK.handle_n_key_up()

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
