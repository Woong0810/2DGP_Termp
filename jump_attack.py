from pico2d import draw_rectangle
from character_config import (GRAVITY_PPS2, JUMP_SPEED_PPS, ACTION_PER_TIME,
                              NORMAL_ATTACK_ANIMATION_SPEED)
import game_framework
import game_world

class JumpAttack:
    def __init__(self, character):
        self.character = character
        self.combo_index = 0
        self.start_frame = 0
        self.end_frame = 0
        self.attack_frame = 0.0

        self.vy = 0.0
        self.vx = 0.0
        self.ground_y = 0.0
        self.jump_count = 0

        self.n_key_pressed = False

    def enter(self, e):
        jump_state = self.character.JUMP
        self.vy = jump_state.vy
        self.vx = jump_state.vx
        self.ground_y = jump_state.ground_y
        self.jump_count = jump_state.jump_count


        if hasattr(self.character.config, 'jump_attack_segments'):
            segments = self.character.config.jump_attack_segments
            self.combo_index = 0
            self.start_frame, self.end_frame = segments[self.combo_index]
            self.attack_frame = 0.0

        game_world.add_collision_pairs('jump_attack:character', self, None)
        game_world.add_collision_pairs('normal_attack:character', None, self.character)
        game_world.add_collision_pairs('special_attack:character', None, self.character)
        game_world.add_collision_pairs('ranged_attack:character', None, self.character)
        game_world.add_collision_pairs('character:shuriken', self.character, None)

    def exit(self, e):
        jump_state = self.character.JUMP
        jump_state.vy = self.vy
        jump_state.vx = self.vx
        jump_state.ground_y = self.ground_y
        jump_state.jump_count = self.jump_count

        game_world.remove_collision_object(self)
        game_world.remove_collision_object(self.character)

    def do(self):
        segment_length = self.end_frame - self.start_frame + 1
        self.attack_frame += segment_length * ACTION_PER_TIME * NORMAL_ATTACK_ANIMATION_SPEED * game_framework.frame_time

        if self.attack_frame >= segment_length:
            if hasattr(self.character.config, 'jump_attack_segments'):
                segments = self.character.config.jump_attack_segments
                if self.n_key_pressed and self.combo_index < len(segments) - 1:
                    self.combo_index += 1
                    self.start_frame, self.end_frame = segments[self.combo_index]
                    self.attack_frame = 0.0
                elif not self.n_key_pressed:
                    self.attack_frame = segment_length - 0.01

        self.character.x += self.vx * game_framework.frame_time
        self.vy -= GRAVITY_PPS2 * game_framework.frame_time
        self.character.y += self.vy * game_framework.frame_time

        if self.character.y <= self.ground_y:
            self.character.y = self.ground_y
            self.character.frame = 0
            self.character.state_machine.handle_event(('LANDED', None))

    def draw(self):
        all_frames = self.character.config.frames
        current_frame_idx = max(self.start_frame, min(int(self.start_frame + self.attack_frame), self.end_frame))

        if current_frame_idx >= len(all_frames):
            current_frame_idx = len(all_frames) - 1

        frame = all_frames[current_frame_idx]
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
        current_frame_idx = max(self.start_frame, min(int(self.start_frame + self.attack_frame), self.end_frame))

        if current_frame_idx < len(all_frames):
            frame = all_frames[current_frame_idx]
            hb = self.character.config.hitbox_normal_attack
            hw = frame['width'] * self.character.config.scale_x * hb['scale_x'] / 2
            hh = frame['height'] * self.character.config.scale_y * hb['scale_y'] / 2
            return (
                self.character.x - hw + hb['x_offset'],
                self.character.y - hh + hb['y_offset'],
                self.character.x + hw + hb['x_offset'],
                self.character.y + hh + hb['y_offset']
            )
        return (0, 0, 0, 0)

    def is_last_segment(self):
        if hasattr(self.character.config, 'jump_attack_segments'):
            segments = self.character.config.jump_attack_segments
            return self.combo_index == len(segments) - 1
        return False

    def handle_n_key_down(self):
        self.n_key_pressed = True

    def handle_n_key_up(self):
        self.n_key_pressed = False

    def handle_collision(self, group, other):
        pass


