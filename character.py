from pico2d import load_image, SDL_KEYDOWN, SDL_KEYUP
from idle import Idle
from run import Run
from normal_attack import NormalAttack
from jump import Jump
from jump_attack import JumpAttack
from defense import Defense
from special_attack import SpecialAttack
from special_attack2 import SpecialAttack2
from ranged_attack import RangedAttack
from hit import Hit
from stand_up import StandUp
from dash import Dash
from state_machine import StateMachine
from event_to_string import *
from character_config import (
    NarutoConfig,
    NORMAL_ATTACK_DAMAGE,
    NORMAL_ATTACK_KNOCKBACK,
    JUMP_ATTACK_DAMAGE,
    JUMP_ATTACK_KNOCKBACK,
    SPECIAL_ATTACK_DAMAGE,
    RANGED_ATTACK_DAMAGE,
    HITSTOP_FRAMES_NORMAL,
    HITSTOP_FRAMES_JUMP,
    HITSTOP_FRAMES_SPECIAL,
    HITSTOP_FRAMES_RANGED,
    HITSTUN_FRAMES_NORMAL,
    HITSTUN_FRAMES_JUMP,
    HITSTUN_FRAMES_SPECIAL,
    HITSTUN_FRAMES_RANGED,
    HIT_DURATION, SPECIAL_ATTACK_KNOCKBACK,
)
from background import Background
import game_framework

class Character:
    def __init__(self, character_config=None, key_bindings=None, x=400, y=90, stage=None):
        self.config = character_config if character_config else NarutoConfig()

        self.key_bindings = key_bindings
        if self.key_bindings is None:
            from player_config import PLAYER1_KEY_BINDINGS
            self.key_bindings = PLAYER1_KEY_BINDINGS

        self.x, self.y = x, y
        self.frame = 0
        self.face_dir = 1
        self.dir = 0
        self.image = load_image(self.config.image_path)
        self.stage = stage

        self.debug_draw = True  # 디버그 모드: 바운딩 박스 표시

        self.up_pressed = False
        self.down_pressed = False

        self.opponent = None  # 상대 캐릭터 참조

        self.max_hp = 100
        self.hp = self.max_hp

        self.invincible_time = 0.0
        self.jump_count = 0

        self.IDLE = Idle(self)
        self.RUN = Run(self)
        self.NORMAL_ATTACK = NormalAttack(self)
        self.JUMP = Jump(self)
        self.JUMP_ATTACK = JumpAttack(self)
        self.DEFENSE = Defense(self)
        self.SPECIAL_ATTACK = SpecialAttack(self)
        self.SPECIAL_ATTACK2 = SpecialAttack2(self)
        self.RANGED_ATTACK = RangedAttack(self)
        self.HIT = Hit(self)
        self.STAND_UP = StandUp(self)
        self.DASH = Dash(self)

        self.naruto_special_chain_active = False

        kb = self.key_bindings
        idle_rules = {
            key_down(kb['attack']): self.NORMAL_ATTACK,
            key_down(kb['right']): self.RUN,
            key_down(kb['left']): self.RUN,
            key_down(kb['down']): self.DEFENSE,
            key_down(kb['special']): self.SPECIAL_ATTACK,
            key_down(kb.get('special2', -1)): self.SPECIAL_ATTACK2,
            key_down(kb['ranged']): self.RANGED_ATTACK,
            key_down(kb['dash']): self.DASH,
            key_down(kb['jump_key']): self.JUMP,
            fall: self.JUMP,
            take_hit: self.HIT
        }
        run_rules = {
            key_up(kb['right']): self.IDLE,
            key_up(kb['left']): self.IDLE,
            key_down(kb['attack']): self.NORMAL_ATTACK,
            key_down(kb['down']): self.DEFENSE,
            key_down(kb['special']): self.SPECIAL_ATTACK,
            key_down(kb.get('special2', -1)): self.SPECIAL_ATTACK2,
            key_down(kb['ranged']): self.RANGED_ATTACK,
            key_down(kb['dash']): self.DASH,
            key_down(kb['jump_key']): self.JUMP,
            fall: self.JUMP,
            take_hit: self.HIT
        }
        attack_rules = {
            segment_end: self.IDLE,
            key_down(kb['down']): self.DEFENSE,
            key_down(kb['special']): self.SPECIAL_ATTACK,
            key_down(kb.get('special2', -1)): self.SPECIAL_ATTACK2,
            key_down(kb['ranged']): self.RANGED_ATTACK,
            key_down(kb['dash']): self.DASH,
            key_down(kb['jump_key']): self.JUMP,
            take_hit: self.HIT
        }
        jump_rules = {
            key_down(kb['attack']): self.JUMP_ATTACK,
            landed: self.IDLE,
            take_hit: self.HIT
        }
        defense_rules = {
            key_up(kb['down']): self.IDLE,
            key_down(kb['attack']): self.NORMAL_ATTACK,
            key_down(kb['special']): self.SPECIAL_ATTACK,
            key_down(kb.get('special2', -1)): self.SPECIAL_ATTACK2,
            key_down(kb['ranged']): self.RANGED_ATTACK,
            key_down(kb['dash']): self.DASH,
            take_hit: self.HIT
        }
        self.state_machine = StateMachine(
            self.IDLE,
            {
                self.IDLE: idle_rules,
                self.RUN: run_rules,
                self.NORMAL_ATTACK: attack_rules,
                self.JUMP: jump_rules,
                self.JUMP_ATTACK: {
                    landed: self.IDLE,
                    take_hit: self.HIT,
                    segment_end: self.JUMP,
                    key_down(kb['dash']): self.DASH
                },
                self.DEFENSE: defense_rules,
                self.SPECIAL_ATTACK: {
                    special_attack_end: self.IDLE,
                    key_down(kb.get('special2', -1)): self.SPECIAL_ATTACK2
                },
                self.SPECIAL_ATTACK2: {
                    special_attack2_end: self.IDLE,
                    key_down(kb['special']): self.SPECIAL_ATTACK
                },
                self.RANGED_ATTACK: {
                    ranged_attack_end: self.IDLE,
                    key_down(kb['dash']): self.DASH
                },
                self.HIT: {
                    hit_end: self.IDLE,
                    stand_up: self.STAND_UP,
                    key_down(kb['dash']): self.DASH,
                    resume_jump: self.JUMP,
                    take_hit: self.HIT
                },
                self.STAND_UP: {
                    stand_up_end: self.IDLE
                },
                self.DASH: {
                    dash_end: self.IDLE
                }
            }
        )
        self.align_to_stage()

    def align_to_stage(self):
        if self.stage is None:
            return
        left, bottom, right, top = self.get_bb()
        ground_top = self.stage.get_ground_top_under(left, bottom, right, tolerance=100)
        if ground_top is None:
            return

        dy = ground_top - bottom
        self.y += dy

    def take_hit(self, is_knockback=False,
                 knockback_distance=0,
                 knockback_dir=None,
                 hitstun_frames=None,
                 will_knockdown=False):

        if knockback_dir is None:
            if is_knockback:
                knockback_dir = -self.face_dir
            else:
                knockback_dir = 0

        if hitstun_frames is not None:
            hit_duration = hitstun_frames / 60.0
        else:
            hit_duration = HIT_DURATION

        self.state_machine.add_event(
            ('TAKE_HIT', (is_knockback, knockback_distance, knockback_dir, hit_duration, will_knockdown))
        )

    def update(self):
        self.state_machine.update()

        import game_framework
        if self.invincible_time > 0:
            self.invincible_time -= game_framework.frame_time
            if self.invincible_time < 0:
                self.invincible_time = 0

    def draw(self):
        self.state_machine.draw()
        if self.debug_draw:
            self.draw_bb()

    def get_bb(self):
        return self.state_machine.get_bb()

    def get_feet_bb(self):
        all_frames = self.config.frames
        idle_frames = self.config.idle_frames
        frame_idx = idle_frames[0]
        frame = all_frames[frame_idx]

        hb = self.config.hitbox_idle
        hw = frame['width'] * self.config.scale_x * hb['scale_x'] / 2
        hh = frame['height'] * self.config.scale_y * hb['scale_y'] / 2

        left = self.x - hw + hb['x_offset']
        right = self.x + hw + hb['x_offset']
        bottom = self.y - hh + hb['y_offset']
        top = bottom + 5  # 발 두께는 5픽셀 정도

        return left, bottom, right, top

    def draw_bb(self):
        self.state_machine.draw_bb()

    def handle_event(self, event):
        if self.key_bindings:
            if not self.is_my_key(event):
                return

        if event.type == SDL_KEYDOWN and event.key == self.key_bindings['up']:
            self.up_pressed = True
        elif event.type == SDL_KEYUP and event.key == self.key_bindings['up']:
            self.up_pressed = False

        if event.type == SDL_KEYDOWN and event.key == self.key_bindings['down']:
            self.down_pressed = True
        elif event.type == SDL_KEYUP and event.key == self.key_bindings['down']:
            self.down_pressed = False

        in_attack_state = self.state_machine.cur_state in (self.NORMAL_ATTACK, self.JUMP_ATTACK, self.SPECIAL_ATTACK, self.SPECIAL_ATTACK2, self.RANGED_ATTACK)

        if self.state_machine.cur_state == self.HIT:
            if getattr(self, 'naruto_special_chain_active', False):
                return
            if not (event.type == SDL_KEYDOWN and event.key == self.key_bindings['dash']):
                return

        if in_attack_state:
            if event.type == SDL_KEYDOWN and event.key == self.key_bindings['dash']:
                if self.state_machine.cur_state == self.JUMP_ATTACK:
                    return
                if self.state_machine.cur_state == self.SPECIAL_ATTACK and self.config.name == "Naruto" and getattr(self.SPECIAL_ATTACK, 'target', None) is not None:
                    return
            else:
                if self.state_machine.cur_state == self.NORMAL_ATTACK:
                    if event.type == SDL_KEYDOWN and event.key == self.key_bindings['attack']:
                        self.NORMAL_ATTACK.handle_n_key_down()
                        return
                    elif event.type == SDL_KEYUP and event.key == self.key_bindings['attack']:
                        self.NORMAL_ATTACK.handle_n_key_up()
                        return
                if self.state_machine.cur_state == self.JUMP_ATTACK:
                    if event.type == SDL_KEYDOWN and event.key == self.key_bindings['attack']:
                        self.JUMP_ATTACK.handle_n_key_down()
                        return
                    elif event.type == SDL_KEYUP and event.key == self.key_bindings['attack']:
                        self.JUMP_ATTACK.handle_n_key_up()
                        return
                return

        if event.type == SDL_KEYDOWN and event.key == self.key_bindings['attack'] and not in_attack_state:
            if self.down_pressed:
                self.NORMAL_ATTACK.set_down_attack(True)
                self.NORMAL_ATTACK.set_up_attack(False)
            elif self.up_pressed:
                self.NORMAL_ATTACK.set_up_attack(True)
                self.NORMAL_ATTACK.set_down_attack(False)
            else:
                self.NORMAL_ATTACK.set_up_attack(False)
                self.NORMAL_ATTACK.set_down_attack(False)

        if self.state_machine.cur_state == self.NORMAL_ATTACK:
            if event.type == SDL_KEYDOWN and event.key == self.key_bindings['attack']:
                self.NORMAL_ATTACK.handle_n_key_down()
            elif event.type == SDL_KEYUP and event.key == self.key_bindings['attack']:
                self.NORMAL_ATTACK.handle_n_key_up()

        if self.state_machine.cur_state == self.JUMP:
            if event.type == SDL_KEYDOWN:
                if 'jump_key' in self.key_bindings and event.key == self.key_bindings['jump_key']:
                    self.JUMP.handle_double_jump()
                elif event.key == self.key_bindings['left']:
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
            return True
        if event.type not in (SDL_KEYDOWN, SDL_KEYUP):
            return False
        return event.key in self.key_bindings.values()

    def set_opponent(self, opponent):
        self.opponent = opponent

    def handle_collision(self, group, other):
        if self.invincible_time > 0 or self.state_machine.cur_state == self.DASH:
            return

        if group == 'normal_attack:character':
            attacker = getattr(other, 'character', None)
            if self.state_machine.cur_state == self.DEFENSE:
                if attacker is not None:
                    self.block_attacker_on_guard(attacker)
                return
            if self.state_machine.cur_state == self.HIT:
                return

            damage = NORMAL_ATTACK_DAMAGE
            knockback_distance = NORMAL_ATTACK_KNOCKBACK
            hitstun_frames = HITSTUN_FRAMES_NORMAL
            hitstop_frames = HITSTOP_FRAMES_NORMAL
            will_knockdown = False

            if attacker is not None and hasattr(attacker, 'config'):
                cfg = attacker.config
                data_list = None
                idx = 0

                if getattr(other, 'from_run', False) and hasattr(cfg, 'run_attack_data'):
                    data_list = cfg.run_attack_data
                    idx = 0
                elif getattr(other, 'up_attack', False) and hasattr(cfg, 'up_attack_data'):
                    data_list = cfg.up_attack_data
                    idx = 0
                elif getattr(other, 'down_attack', False) and hasattr(cfg, 'down_attack_data'):
                    data_list = cfg.down_attack_data
                    idx = 0
                elif hasattr(cfg, 'normal_attack_data'):
                    data_list = cfg.normal_attack_data
                    idx = getattr(other, 'combo_index', 0)

                if data_list:
                    if idx < 0 or idx >= len(data_list):
                        idx = len(data_list) - 1
                    data = data_list[idx]

                    damage = data.get('damage', damage)
                    knockback_distance = data.get('knockback', knockback_distance)
                    hitstun_frames = data.get('hitstun_frames', hitstun_frames)
                    hitstop_frames = data.get('hitstop_frames', hitstop_frames)
                    will_knockdown = data.get('knockdown', False)

            knockback_dir = 0
            if knockback_distance != 0 and attacker is not None:
                if attacker.x > self.x:
                    knockback_dir = -1
                elif attacker.x < self.x:
                    knockback_dir = 1
                else:
                    knockback_dir = -self.face_dir

            self.hp -= damage
            game_framework.add_hitstop(hitstop_frames)
            self.take_hit(
                is_knockback=will_knockdown,
                knockback_distance=knockback_distance,
                knockback_dir=knockback_dir,
                hitstun_frames=hitstun_frames,
                will_knockdown=will_knockdown
            )

        elif group == 'jump_attack:character':
            attacker = getattr(other, 'character', None)
            if self.state_machine.cur_state == self.DEFENSE:
                if self.state_machine.cur_state == self.DEFENSE:
                    if attacker is not None:
                        self.block_attacker_on_guard(attacker)
                    return
            if self.state_machine.cur_state == self.HIT:
                return

            damage = JUMP_ATTACK_DAMAGE
            knockback_distance = JUMP_ATTACK_KNOCKBACK
            hitstun_frames = HITSTUN_FRAMES_JUMP
            hitstop_frames = HITSTOP_FRAMES_JUMP
            will_knockdown = False

            if attacker is not None and hasattr(attacker, 'config'):
                cfg = attacker.config
                if hasattr(cfg, 'jump_attack_data'):
                    data_list = cfg.jump_attack_data
                    idx = getattr(other, 'combo_index', 0)
                    if data_list:
                        if idx < 0 or idx >= len(data_list):
                            idx = len(data_list) - 1
                        data = data_list[idx]
                        damage = data.get('damage', damage)
                        knockback_distance = data.get('knockback', knockback_distance)
                        hitstun_frames = data.get('hitstun_frames', hitstun_frames)
                        hitstop_frames = data.get('hitstop_frames', hitstop_frames)
                        will_knockdown = data.get('knockdown', will_knockdown)

            knockback_dir = 0
            if knockback_distance != 0 and attacker is not None:
                if attacker.x > self.x:
                    knockback_dir = -1
                elif attacker.x < self.x:
                    knockback_dir = 1
                else:
                    knockback_dir = -self.face_dir

            self.hp -= damage
            game_framework.add_hitstop(hitstop_frames)
            self.take_hit(
                is_knockback=will_knockdown,
                knockback_distance=knockback_distance,
                knockback_dir=knockback_dir,
                hitstun_frames=hitstun_frames,
                will_knockdown=will_knockdown
            )

        elif group == 'special_attack:character':
            attacker = getattr(other, 'character', None)
            if attacker and hasattr(attacker, 'config') and attacker.config.name == "Naruto":
                return
            if hasattr(other, 'owner') and other.owner == self:
                return
            if self.state_machine.cur_state == self.DEFENSE:
                if attacker is not None:
                    self.block_attacker_on_guard(attacker)
                return
            if self.state_machine.cur_state == self.HIT:
                return

            damage = SPECIAL_ATTACK_DAMAGE
            knockback_distance = SPECIAL_ATTACK_KNOCKBACK
            hitstun_frames = HITSTUN_FRAMES_SPECIAL
            hitstop_frames = HITSTOP_FRAMES_SPECIAL
            will_knockdown = True

            if attacker is not None and hasattr(attacker, 'config'):
                cfg = attacker.config
                if hasattr(cfg, 'special_attack_data'):
                    data_list = cfg.special_attack_data
                    if isinstance(data_list, list) and len(data_list) > 0:
                        data = data_list[0]
                        damage = data.get('damage', damage)
                        knockback_distance = data.get('knockback', knockback_distance)
                        hitstun_frames = data.get('hitstun_frames', hitstun_frames)
                        hitstop_frames = data.get('hitstop_frames', hitstop_frames)
                        will_knockdown = data.get('knockdown', will_knockdown)

            knockback_dir = 0
            if knockback_distance != 0 and attacker is not None:
                if attacker.x > self.x:
                    knockback_dir = -1
                elif attacker.x < self.x:
                    knockback_dir = 1
                else:
                    knockback_dir = -self.face_dir

            self.hp -= damage
            game_framework.add_hitstop(hitstop_frames)
            self.take_hit(
                is_knockback=will_knockdown,
                knockback_distance=knockback_distance,
                knockback_dir=knockback_dir,
                hitstun_frames=hitstun_frames,
                will_knockdown=will_knockdown
            )

        elif group == 'special_attack2:character':
            attacker = getattr(other, 'character', None)
            if attacker and hasattr(attacker, 'config') and attacker.config.name == "Naruto":
                return
            if hasattr(other, 'owner') and other.owner == self:
                return
            if self.state_machine.cur_state == self.DEFENSE:
                if attacker is not None:
                    self.block_attacker_on_guard(attacker)
                return
            if self.state_machine.cur_state == self.HIT:
                return

            damage = SPECIAL_ATTACK_DAMAGE
            knockback_distance = SPECIAL_ATTACK_KNOCKBACK
            hitstun_frames = HITSTUN_FRAMES_SPECIAL
            hitstop_frames = HITSTOP_FRAMES_SPECIAL
            will_knockdown = True

            if attacker is not None and hasattr(attacker, 'config'):
                cfg = attacker.config

                if hasattr(cfg, 'special_attack_data'):
                    data_list = cfg.special_attack_data
                    if isinstance(data_list, list) and len(data_list) > 1:
                        data = data_list[1]
                        damage = data.get('damage', damage)
                        knockback_distance = data.get('knockback', knockback_distance)
                        hitstun_frames = data.get('hitstun_frames', hitstun_frames)
                        hitstop_frames = data.get('hitstop_frames', hitstop_frames)
                        will_knockdown = data.get('knockdown', will_knockdown)

            knockback_dir = 0
            if knockback_distance != 0 and attacker is not None:
                if attacker.x > self.x:
                    knockback_dir = -1
                elif attacker.x < self.x:
                    knockback_dir = 1
                else:
                    knockback_dir = -self.face_dir

            self.hp -= damage
            game_framework.add_hitstop(hitstop_frames)
            self.take_hit(
                is_knockback=will_knockdown,
                knockback_distance=knockback_distance,
                knockback_dir=knockback_dir,
                hitstun_frames=hitstun_frames,
                will_knockdown=will_knockdown
            )

        elif group == 'character:shuriken':
            attacker = getattr(other, 'character', None)
            if hasattr(other, 'owner') and other.owner == self:
                return
            if self.state_machine.cur_state == self.DEFENSE:
                if attacker is not None:
                    self.block_attacker_on_guard(attacker)
                return
            if self.state_machine.cur_state == self.HIT:
                return

            damage = RANGED_ATTACK_DAMAGE
            knockback_distance = 0
            hitstun_frames = HITSTUN_FRAMES_RANGED
            hitstop_frames = HITSTOP_FRAMES_RANGED
            will_knockdown = False

            owner = getattr(other, 'owner', None)
            if owner is not None and hasattr(owner, 'config'):
                cfg = owner.config
                if hasattr(cfg, 'ranged_attack_data'):
                    data = cfg.ranged_attack_data
                    damage = data.get('damage', damage)
                    knockback_distance = data.get('knockback', knockback_distance)
                    hitstun_frames = data.get('hitstun_frames', hitstun_frames)
                    hitstop_frames = data.get('hitstop_frames', hitstop_frames)
                    will_knockdown = data.get('knockdown', will_knockdown)

            knockback_dir = 0
            if knockback_distance != 0 and owner is not None:
                if owner.x > self.x:
                    knockback_dir = -1
                elif owner.x < self.x:
                    knockback_dir = 1
                else:
                    knockback_dir = -self.face_dir

            self.hp -= damage
            game_framework.add_hitstop(hitstop_frames)
            self.take_hit(
                is_knockback=will_knockdown,
                knockback_distance=knockback_distance,
                knockback_dir=knockback_dir,
                hitstun_frames=hitstun_frames,
                will_knockdown=will_knockdown
            )

        if self.hp < 0:
            self.hp = 0

    def block_attacker_on_guard(self, attacker):
        l_def, b_def, r_def, t_def = self.get_bb()
        l_att, b_att, r_att, t_att = attacker.get_bb()
        margin = 1.0

        if attacker.face_dir > 0:
            overlap = r_att - l_def
            if overlap > 0:
                attacker.x -= overlap + margin
        elif attacker.face_dir < 0:
            overlap = r_def - l_att
            if overlap > 0:
                attacker.x += overlap + margin

