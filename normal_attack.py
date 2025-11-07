from event_to_string import up_down, n_down, n_up
from pico2d import draw_rectangle
from character_config import ACTION_PER_TIME, NORMAL_ATTACK_ANIMATION_SPEED
import game_framework
import game_world

class NormalAttack:
    def __init__(self, character):
        self.character = character
        self.combo_index = 0
        self.start_frame = 0
        self.end_frame = 0
        self.n_key_pressed = False

    def enter(self, e):
        # 새로운 세그먼트 시작
        segments = self.character.config.normal_attack_segments
        self.start_frame, self.end_frame = segments[self.combo_index]
        self.character.frame = self.start_frame

        if n_down(e):
            self.n_key_pressed = True

        game_world.add_collision_pairs('normal_attack:character', self, None)

    def exit(self, e):
        if not n_down(e):
            self.combo_index = 0
        self.n_key_pressed = False

        game_world.remove_collision_object(self)

    def do(self):
        segment_length = self.end_frame - self.start_frame + 1
        self.character.frame += segment_length * ACTION_PER_TIME * NORMAL_ATTACK_ANIMATION_SPEED * game_framework.frame_time

        if self.character.frame >= self.end_frame + 1:
            if self.n_key_pressed:
                self.combo_index = (self.combo_index + 1) % 3
                segments = self.character.config.normal_attack_segments
                self.start_frame, self.end_frame = segments[self.combo_index]
                self.character.frame = self.start_frame
            else:
                self.character.state_machine.handle_event(('SEGMENT_END', None))

    def handle_n_key_down(self):
        self.n_key_pressed = True

    def handle_n_key_up(self):
        self.n_key_pressed = False

    def draw(self):
        all_frames = self.character.config.frames
        normal_attack_frames = self.character.config.normal_attack_frames

        frame_idx = normal_attack_frames[int(self.character.frame)]  # int로 변환
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
        draw_rectangle(*self.get_bb())

    def get_bb(self):
        all_frames = self.character.config.frames
        normal_attack_frames = self.character.config.normal_attack_frames

        frame_idx = normal_attack_frames[int(self.character.frame)]  # int로 변환
        frame = all_frames[frame_idx]

        hb = self.character.config.hitbox_normal_attack
        hw = frame['width'] * self.character.config.scale_x * hb['scale_x'] / 2
        hh = frame['height'] * self.character.config.scale_y * hb['scale_y'] / 2
        return (
            self.character.x - hw + hb['x_offset'],
            self.character.y - hh + hb['y_offset'],
            self.character.x + hw + hb['x_offset'],
            self.character.y + hh + hb['y_offset']
        )

    def handle_collision(self, group, other):
        pass

