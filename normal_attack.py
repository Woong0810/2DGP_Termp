from event_to_string import up_down
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
        self.from_run = False
        self.up_attack = False
        self.down_attack = False

    def set_up_attack(self, is_up_attack):
        self.up_attack = is_up_attack

    def set_down_attack(self, is_down_attack):
        self.down_attack = is_down_attack

    def enter(self, e):
        from run import Run
        self.from_run = isinstance(self.character.state_machine.prev_state, Run)

        if self.down_attack and hasattr(self.character.config, 'down_attack_segments'):
            segments = self.character.config.down_attack_segments
            self.combo_index = 0
        elif self.up_attack and hasattr(self.character.config, 'up_attack_segments'):
            segments = self.character.config.up_attack_segments
            self.combo_index = 0
        elif self.from_run:
            segments = self.character.config.run_attack_segments
            self.combo_index = 0
        else:
            segments = self.character.config.normal_attack_segments

        self.start_frame, self.end_frame = segments[self.combo_index]
        self.character.frame = self.start_frame

        # 동적으로 attack 키 체크
        from sdl2 import SDL_KEYDOWN
        if e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == self.character.key_bindings['attack']:
            self.n_key_pressed = True

        game_world.add_collision_pairs('normal_attack:character', self, None)

    def exit(self, e):
        # 동적으로 attack 키 체크
        from sdl2 import SDL_KEYDOWN
        if not (e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == self.character.key_bindings['attack']):
            self.combo_index = 0
            self.from_run = False
            self.up_attack = False
            self.down_attack = False
        self.n_key_pressed = False

        game_world.remove_collision_object(self)

    def do(self):
        segment_length = self.end_frame - self.start_frame + 1
        self.character.frame += segment_length * ACTION_PER_TIME * NORMAL_ATTACK_ANIMATION_SPEED * game_framework.frame_time

        if self.character.frame >= self.end_frame + 1:
            # 윗 방향키 공격, 아래 방향키 공격, 달리기 공격은 콤보 없이 바로 종료
            if self.up_attack or self.down_attack or self.from_run:
                self.character.state_machine.handle_event(('SEGMENT_END', None))
            elif self.n_key_pressed:
                segments = self.character.config.normal_attack_segments
                self.combo_index = (self.combo_index + 1) % len(segments)
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

        # 현재 프레임을 세그먼트 범위 내로 제한
        current_frame_idx = max(self.start_frame, min(int(self.character.frame), self.end_frame))

        # 프레임 인덱스 범위 체크
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

        # 현재 프레임을 세그먼트 범위 내로 제한
        current_frame_idx = max(self.start_frame, min(int(self.character.frame), self.end_frame))

        # 프레임 인덱스 범위 체크
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

        # 범위를 벗어나면 빈 히트박스 반환
        return (0, 0, 0, 0)

    def is_last_segment(self):
        if self.from_run:
            segments = self.character.config.run_attack_segments
        elif self.up_attack or self.down_attack:
            return False
        else:
            segments = self.character.config.normal_attack_segments
        return self.combo_index == len(segments) - 1

    def is_run_attack(self):
        return self.from_run

    def handle_collision(self, group, other):
        pass

