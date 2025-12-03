from pico2d import draw_rectangle
from character_config import (GRAVITY_PPS2, JUMP_SPEED_PPS, ACTION_PER_TIME,
                              NORMAL_ATTACK_ANIMATION_SPEED)
import game_framework
import game_world
from camera import camera

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

        self.n_key_pressed = False

        self.segment_move_speed = 0.0
        self.segment_move_elapsed = 0.0

    def enter(self, e):
        jump_state = self.character.JUMP
        self.vy = jump_state.vy
        self.vx = jump_state.vx
        self.ground_y = jump_state.ground_y

        if hasattr(self.character.config, 'jump_attack_segments'):
            segments = self.character.config.jump_attack_segments
            self.combo_index = 0
            self.start_frame, self.end_frame = segments[self.combo_index]
            self.attack_frame = 0.0
        else:
            self.start_frame, self.end_frame = 0, 0
            self.attack_frame = 0.0

        self.segment_move_elapsed = 0.0
        self.segment_move_speed = 0.0
        self.update_segment_move()

        game_world.add_collision_pairs('jump_attack:character', self, None)

    def exit(self, e):
        jump_state = self.character.JUMP
        jump_state.vy = self.vy
        jump_state.vx = self.vx
        jump_state.ground_y = self.ground_y

        game_world.remove_collision_object(self)

    def do(self):
        segment_length = self.end_frame - self.start_frame + 1
        self.attack_frame += segment_length * ACTION_PER_TIME * NORMAL_ATTACK_ANIMATION_SPEED * game_framework.frame_time

        if self.segment_move_speed != 0.0:
            self.segment_move_elapsed += game_framework.frame_time
            segment_duration = 1.0 / (ACTION_PER_TIME * NORMAL_ATTACK_ANIMATION_SPEED)
            if self.segment_move_elapsed < segment_duration:
                self.character.x += self.character.face_dir * self.segment_move_speed * game_framework.frame_time

        if self.attack_frame >= segment_length:
            if hasattr(self.character.config, 'jump_attack_segments'):
                segments = self.character.config.jump_attack_segments
                if self.combo_index < len(segments) - 1:
                    self.combo_index += 1
                    self.start_frame, self.end_frame = segments[self.combo_index]
                    self.attack_frame = 0.0
                    self.update_segment_move()
                else:
                    self.character.state_machine.handle_event(('SEGMENT_END', None))

        prev_left, prev_bottom, prev_right, prev_top = self.character.get_feet_bb()
        self.character.x += self.vx * game_framework.frame_time
        self.vy -= GRAVITY_PPS2 * game_framework.frame_time
        self.character.y += self.vy * game_framework.frame_time

        self.check_landing(prev_bottom)

    def update_segment_move(self):
        self.segment_move_elapsed = 0.0
        self.segment_move_speed = 0.0

        cfg = getattr(self.character, 'config', None)
        if cfg is None:
            return
        if not hasattr(cfg, 'jump_attack_data'):
            return

        data_list = cfg.jump_attack_data
        idx = getattr(self, 'segment_index', 0)
        if not (0 <= idx < len(data_list)):
            return

        data = data_list[idx]
        push = data.get('attacker_push', 0)
        if push == 0:
            return

        from character_config import ACTION_PER_TIME, NORMAL_ATTACK_ANIMATION_SPEED
        segment_duration = 1.0 / (ACTION_PER_TIME * NORMAL_ATTACK_ANIMATION_SPEED)
        self.segment_move_speed = push / segment_duration

    def check_landing(self, prev_bottom):
        if hasattr(self.character, 'stage') and \
                self.character.stage is not None and \
                hasattr(self.character.stage, 'find_landing_platform'):

            left, bottom, right, top = self.character.get_feet_bb()
            ground_top = self.character.stage.find_landing_platform(
                left, prev_bottom, right, bottom, self.vy
            )

            if ground_top is not None:
                dy = ground_top - bottom
                self.character.y += dy
                self.vy = 0.0
                self.character.frame = 0
                # 점프 공격 중 착지하면 점프 카운트도 초기화
                self.character.jump_count = 0
                self.ground_y = self.character.y
                self.character.state_machine.handle_event(('LANDED', None))
            return

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

        world_y = self.character.y + self.character.config.draw_offset_y
        sx, sy = camera.world_to_screen(self.character.x, world_y)

        if self.character.face_dir == 1:
            self.character.image.clip_draw(l, b, w, h, sx, sy, draw_w, draw_h)
        else:
            self.character.image.clip_composite_draw(l, b, w, h, 0.0, 'h', sx, sy, draw_w, draw_h)
        left, bottom, right, top = self.get_bb()
        sx1, sy1 = camera.world_to_screen(left, bottom)
        sx2, sy2 = camera.world_to_screen(right, top)
        draw_rectangle(sx1, sy1, sx2, sy2)

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
