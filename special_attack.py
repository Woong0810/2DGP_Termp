from pico2d import draw_rectangle
from character_config import ACTION_PER_TIME, SPECIAL_ATTACK_ANIMATION_SPEED, SPECIAL_ATTACK_LOOP_COUNT
import game_framework

class SpecialAttack:
    def __init__(self, character):
        self.character = character
        self.loop_count = 0

    def enter(self, e):
        self.character.frame = 0
        self.loop_count = 0

    def exit(self, e):
        pass

    def do(self):
        special_frames = self.character.config.special_attack_frames
        last_4_start = len(special_frames) - 4
        skip_before_last_4 = last_4_start - 3

        self.character.frame += len(special_frames) * ACTION_PER_TIME * SPECIAL_ATTACK_ANIMATION_SPEED * game_framework.frame_time

        # 스킵할 구간에 도달하면 마지막 4프레임으로 점프
        if skip_before_last_4 - 3 <= self.character.frame < last_4_start:
            self.character.frame = last_4_start

        # 마지막 프레임 도달 시 반복
        if self.character.frame >= len(special_frames):
            if self.loop_count < SPECIAL_ATTACK_LOOP_COUNT:
                self.character.frame = last_4_start
                self.loop_count += 1
            else:
                self.character.state_machine.handle_event(('SPECIAL_ATTACK_END', None))

    def draw(self):
        special_attack_frames = self.character.config.special_attack_frames
        all_frames = self.character.config.frames
        frame_idx = special_attack_frames[int(self.character.frame)]  # int로 변환
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
        if self.character.frame >= 120:
            special_attack_frames = self.character.config.special_attack_frames
            all_frames = self.character.config.frames
            frame_idx = special_attack_frames[int(self.character.frame)]  # int로 변환
            frame = all_frames[frame_idx]

            hb = self.character.config.hitbox_special_attack
            hw = frame['width'] * self.character.config.scale_x * hb['scale_x'] / 2
            hh = frame['height'] * self.character.config.scale_y * hb['scale_y'] / 2
            return (
                self.character.x - hw + hb['x_offset'],
                self.character.y - hh + hb['y_offset'],
                self.character.x + hw + hb['x_offset'],
                self.character.y + hh + hb['y_offset']
            )
        return (0, 0, 0, 0)

    def draw_bb(self):
        left, bottom, right, top = self.get_bb()
        draw_rectangle(left, bottom, right, top)
