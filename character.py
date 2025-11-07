from pico2d import load_image, SDL_KEYDOWN, SDL_KEYUP, SDLK_n, SDLK_LEFT, SDLK_RIGHT, SDLK_UP
from idle import Idle
from run import Run
from normal_attack import NormalAttack
from jump import Jump
from defense import Defense
from special_attack import SpecialAttack
from ranged_attack import RangedAttack
from hit import Hit
from state_machine import StateMachine
from event_to_string import *
from character_config import NarutoConfig

class Character:
    def __init__(self, character_config=None, x=400, y=90):
        # 캐릭터 설정 (기본값: Naruto)
        self.config = character_config if character_config else NarutoConfig()

        self.x, self.y = x, y
        self.frame = 0
        self.face_dir = 1
        self.dir = 0  # RUN 상태에서 사용할 방향
        self.image = load_image(self.config.image_path)

        self.accum_time = 0.0
        self.frame_duration = 0.1  # 기본값, 상태별로 변경 가능
        self.debug_draw = True  # 디버그 모드: 바운딩 박스 표시

        self.opponent = None  # 상대 캐릭터 참조

        self.IDLE = Idle(self)
        self.RUN = Run(self)
        self.NORMAL_ATTACK = NormalAttack(self)
        self.JUMP = Jump(self)
        self.DEFENSE = Defense(self)
        self.SPECIAL_ATTACK = SpecialAttack(self)
        self.RANGED_ATTACK = RangedAttack(self)
        self.HIT = Hit(self)

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
                    b_down: self.RANGED_ATTACK,
                    take_hit: self.HIT
                },
                self.RUN: {
                    right_up: self.IDLE,
                    left_up: self.IDLE,
                    n_down: self.NORMAL_ATTACK,
                    up_down: self.JUMP,
                    down_down: self.DEFENSE,
                    v_down: self.SPECIAL_ATTACK,
                    b_down: self.RANGED_ATTACK,
                    take_hit: self.HIT
                },
                self.NORMAL_ATTACK: {
                    segment_end: self.IDLE,
                    up_down: self.JUMP,
                    down_down: self.DEFENSE,
                    v_down: self.SPECIAL_ATTACK,
                    b_down: self.RANGED_ATTACK,
                    take_hit: self.HIT
                },
                self.JUMP: {
                    landed: self.IDLE,
                    take_hit: self.HIT
                },
                self.DEFENSE: {
                    down_up: self.IDLE,
                    v_down: self.SPECIAL_ATTACK,
                    b_down: self.RANGED_ATTACK,
                    take_hit: self.HIT
                },
                self.SPECIAL_ATTACK: {
                    special_attack_end: self.IDLE
                },
                self.RANGED_ATTACK: {
                    ranged_attack_end: self.IDLE
                },
                self.HIT: {
                    hit_end: self.IDLE
                }
            }
        )

    def take_hit(self):
        self.state_machine.add_event(('TAKE_HIT', 0))

    def update(self):
        self.state_machine.update()

    def draw(self):
        self.state_machine.draw()
        if self.debug_draw:
            self.draw_bb()

    def get_bb(self):
        # 현재 상태의 바운딩 박스 반환
        return self.state_machine.get_bb()

    def draw_bb(self):
        # 디버그용: 바운딩 박스 그리기
        self.state_machine.draw_bb()

    def handle_event(self, event):
        # HIT 상태에서는 모든 입력 무시
        if self.state_machine.cur_state == self.HIT:
            return

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

    def set_opponent(self, opponent):
        self.opponent = opponent
