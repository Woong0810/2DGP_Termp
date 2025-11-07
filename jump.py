from pico2d import draw_rectangle
from character_config import (GRAVITY_PPS2, JUMP_HEIGHT_PIXEL, JUMP_SPEED_PPS,
                              RUN_SPEED_PPS, ACTION_PER_TIME, JUMP_ANIMATION_SPEED)
import game_framework
import game_world
import math

class Jump:
    def __init__(self, character):
        self.character = character
        self.jump_count = 0
        self.vy = 0.0
        self.vx = 0.0
        self.ground_y = 0.0
        self.dir = 0

    def enter(self, e):
        self.jump_count = 1
        self.character.frame = 0

        # 물리 기반 점프 속도 계산: v = sqrt(2 * g * h)
        self.vy = math.sqrt(2 * GRAVITY_PPS2 * JUMP_HEIGHT_PIXEL)
        self.ground_y = self.character.y

        # 이전 상태가 RUN이었으면 수평 속도 유지, IDLE에서는 수직 점프
        prev_state = self.character.state_machine.prev_state
        if prev_state == self.character.RUN:
            self.vx = self.character.dir * RUN_SPEED_PPS
        else:
            self.vx = 0.0
        self.dir = 0

        game_world.add_collision_pairs('normal_attack:character', None, self.character)
        game_world.add_collision_pairs('special_attack:character', None, self.character)
        game_world.add_collision_pairs('ranged_attack:character', None, self.character)

    def exit(self, e):
        self.jump_count = 0
        self.dir = 0
        self.vx = 0.0
        game_world.remove_collision_object(self.character)

    def do(self):
        # 좌우 이동 처리
        if self.dir == -1:
            self.vx -= JUMP_SPEED_PPS * game_framework.frame_time
            if self.vx < -JUMP_SPEED_PPS:
                self.vx = -JUMP_SPEED_PPS
            self.character.face_dir = -1
        elif self.dir == 1:
            self.vx += JUMP_SPEED_PPS * game_framework.frame_time
            if self.vx > JUMP_SPEED_PPS:
                self.vx = JUMP_SPEED_PPS
            self.character.face_dir = 1

        jump_frames = self.character.config.jump_frames
        frames_per_action = len(jump_frames)
        self.character.frame = (self.character.frame + frames_per_action * ACTION_PER_TIME * JUMP_ANIMATION_SPEED * game_framework.frame_time) % frames_per_action

        self.character.x += self.vx * game_framework.frame_time

        self.vy -= GRAVITY_PPS2 * game_framework.frame_time
        self.character.y += self.vy * game_framework.frame_time

        # 착지 체크
        if self.character.y <= self.ground_y:
            self.character.y = self.ground_y
            self.character.frame = 0
            self.character.state_machine.handle_event(('LANDED', None))

    def handle_double_jump(self):
        if self.jump_count == 1:
            self.jump_count = 2
            self.character.frame = 0
            self.vy = math.sqrt(2 * GRAVITY_PPS2 * JUMP_HEIGHT_PIXEL)

    def draw(self):
        jump_frames = self.character.config.jump_frames
        all_frames = self.character.config.frames
        frame_idx = jump_frames[int(self.character.frame)]  # int로 변환
        frame = all_frames[frame_idx]

        l, b, w, h = frame['left'], frame['bottom'], frame['width'], frame['height']
        draw_w = int(w * self.character.config.scale_x)
        draw_h = int(h * self.character.config.scale_y)
        draw_y = self.character.y + self.character.config.draw_offset_y

        if self.character.face_dir == 1:
            self.character.image.clip_draw(l, b, w, h, self.character.x, draw_y, draw_w, draw_h)
        else:
            self.character.image.clip_composite_draw(l, b, w, h, 0.0, 'h',
                                                  self.character.x, draw_y, draw_w, draw_h)

    def get_bb(self):
        all_frames = self.character.config.frames
        jump_frames = self.character.config.jump_frames
        frame_idx = jump_frames[int(self.character.frame)]  # int로 변환
        frame = all_frames[frame_idx]

        hb = self.character.config.hitbox_jump
        hw = frame['width'] * self.character.config.scale_x * hb['scale_x'] / 2
        hh = frame['height'] * self.character.config.scale_y * hb['scale_y'] / 2
        return (
            self.character.x - hw + hb['x_offset'],
            self.character.y - hh + hb['y_offset'],
            self.character.x + hw + hb['x_offset'],
            self.character.y + hh + hb['y_offset']
        )

    def draw_bb(self):
        left, bottom, right, top = self.get_bb()
        draw_rectangle(left, bottom, right, top)

