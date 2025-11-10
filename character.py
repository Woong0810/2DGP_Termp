from pico2d import load_image, SDL_KEYDOWN, SDL_KEYUP
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
    def __init__(self, character_config=None, key_bindings=None, x=400, y=90):
        # 캐릭터 설정 (기본값: Naruto)
        self.config = character_config if character_config else NarutoConfig()

        # 키 바인딩 (플레이어별로 외부에서 주입)
        self.key_bindings = key_bindings
        if self.key_bindings is None:
            # 기본값: Player 1 키 바인딩
            from player_config import PLAYER1_KEY_BINDINGS
            self.key_bindings = PLAYER1_KEY_BINDINGS

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

        # 키 바인딩 기반 rules 생성
        from event_to_string import key_down, key_up
        kb = self.key_bindings

        self.state_machine = StateMachine(
            self.IDLE,
            {
                self.IDLE: {
                    key_down(kb['attack']): self.NORMAL_ATTACK,
                    key_down(kb['right']): self.RUN,
                    key_down(kb['left']): self.RUN,
                    key_down(kb['up']): self.JUMP,
                    key_down(kb['down']): self.DEFENSE,
                    key_down(kb['special']): self.SPECIAL_ATTACK,
                    key_down(kb['ranged']): self.RANGED_ATTACK,
                    take_hit: self.HIT
                },
                self.RUN: {
                    key_up(kb['right']): self.IDLE,
                    key_up(kb['left']): self.IDLE,
                    key_down(kb['attack']): self.NORMAL_ATTACK,
                    key_down(kb['up']): self.JUMP,
                    key_down(kb['down']): self.DEFENSE,
                    key_down(kb['special']): self.SPECIAL_ATTACK,
                    key_down(kb['ranged']): self.RANGED_ATTACK,
                    take_hit: self.HIT
                },
                self.NORMAL_ATTACK: {
                    segment_end: self.IDLE,
                    key_down(kb['up']): self.JUMP,
                    key_down(kb['down']): self.DEFENSE,
                    key_down(kb['special']): self.SPECIAL_ATTACK,
                    key_down(kb['ranged']): self.RANGED_ATTACK,
                    take_hit: self.HIT
                },
                self.JUMP: {
                    landed: self.IDLE,
                    take_hit: self.HIT
                },
                self.DEFENSE: {
                    key_up(kb['down']): self.IDLE,
                    key_down(kb['special']): self.SPECIAL_ATTACK,
                    key_down(kb['ranged']): self.RANGED_ATTACK,
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
        # 키 바인딩이 있는 경우, 자신의 키인지 확인
        if self.key_bindings:
            # 자신의 키가 아니면 무시
            if not self.is_my_key(event):
                return

        # HIT 상태에서는 모든 입력 무시
        if self.state_machine.cur_state == self.HIT:
            return

        # SPECIAL_ATTACK, RANGED_ATTACK 상태에서는 모든 입력 무시
        if self.state_machine.cur_state == self.SPECIAL_ATTACK or self.state_machine.cur_state == self.RANGED_ATTACK:
            return

        # NORMAL_ATTACK 상태에서 attack키 DOWN/UP 추적
        if self.state_machine.cur_state == self.NORMAL_ATTACK:
            if event.type == SDL_KEYDOWN and event.key == self.key_bindings['attack']:
                self.NORMAL_ATTACK.handle_n_key_down()
            elif event.type == SDL_KEYUP and event.key == self.key_bindings['attack']:
                self.NORMAL_ATTACK.handle_n_key_up()

        # JUMP 상태에서 처리
        if self.state_machine.cur_state == self.JUMP:
            # 윗 방향키 - 2단 점프
            if event.type == SDL_KEYDOWN and event.key == self.key_bindings['up']:
                self.JUMP.handle_double_jump()
            # 좌우 방향키
            elif event.type == SDL_KEYDOWN:
                if event.key == self.key_bindings['left']:
                    self.JUMP.dir = -1
                elif event.key == self.key_bindings['right']:
                    self.JUMP.dir = 1
            elif event.type == SDL_KEYUP:
                if event.key == self.key_bindings['left'] and self.JUMP.dir == -1:
                    self.JUMP.dir = 0
                elif event.key == self.key_bindings['right'] and self.JUMP.dir == 1:
                    self.JUMP.dir = 0

        self.state_machine.handle_event(('INPUT', event))

    def is_my_key(self, event):
        if not self.key_bindings:
            return True  # 키 바인딩이 없으면 모든 키 허용
        # 키 이벤트만 체크
        if event.type not in (SDL_KEYDOWN, SDL_KEYUP):
            return False
        # 자신의 키 바인딩에 포함된 키인지 확인
        return event.key in self.key_bindings.values()

    def set_opponent(self, opponent):
        self.opponent = opponent

    def handle_collision(self, group, other):
        if group == 'normal_attack:character':
            if self.state_machine.cur_state == self.DEFENSE:
                return
            if self.state_machine.cur_state == self.HIT:    # 이미 Hit 상태면 무시
                return
            self.take_hit()

        elif group == 'special_attack:character':
            if self.state_machine.cur_state == self.DEFENSE:
                return
            if self.state_machine.cur_state == self.HIT:
                return
            self.take_hit()

        elif group == 'ranged_attack:character':
            if self.state_machine.cur_state == self.DEFENSE:
                return
            if self.state_machine.cur_state == self.HIT:
                return
            self.take_hit()

