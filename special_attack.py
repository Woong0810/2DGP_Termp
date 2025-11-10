from pico2d import draw_rectangle, load_image
from character_config import ACTION_PER_TIME, SPECIAL_ATTACK_ANIMATION_SPEED, SPECIAL_ATTACK_LOOP_COUNT
import game_framework
import game_world

class SpecialAttack:
    def __init__(self, character):
        self.character = character
        self.loop_count = 0

        # 이타치의 경우 스페셜 공격 전용 이미지 로드
        self.special_image = None
        if hasattr(self.character.config, 'special_attack_image_path') and self.character.config.special_attack_image_path:
            self.special_image = load_image(self.character.config.special_attack_image_path)

    def enter(self, e):
        self.character.frame = 0
        self.loop_count = 0

        game_world.add_collision_pairs('special_attack:character', self, None)

    def exit(self, e):
        game_world.remove_collision_object(self)

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

        # 이타치의 경우 스페셜 프레임 데이터 사용, 아니면 기본 프레임 데이터 사용
        if hasattr(self.character.config, 'special_attack_frames_data') and self.character.config.special_attack_frames_data:
            all_frames = self.character.config.special_attack_frames_data
            frame_idx = int(self.character.frame)  # 직접 인덱스 사용
        else:
            all_frames = self.character.config.frames
            frame_idx = special_attack_frames[int(self.character.frame)]  # 매핑 사용

        frame = all_frames[frame_idx]

        l, b, w, h = frame['left'], frame['bottom'], frame['width'], frame['height']
        draw_w = int(w * self.character.config.scale_x)
        draw_h = int(h * self.character.config.scale_y)
        draw_y = self.character.y + self.character.config.draw_offset_y

        # 이타치의 경우 스페셜 이미지 사용, 아니면 기본 이미지 사용
        image_to_use = self.special_image if self.special_image else self.character.image

        if self.character.face_dir == 1:
            image_to_use.clip_draw(l, b, w, h, self.character.x, draw_y, draw_w, draw_h)
        else:
            image_to_use.clip_composite_draw(l, b, w, h, 0.0, 'h',
                                                  self.character.x, draw_y, draw_w, draw_h)
        draw_rectangle(*self.get_bb())

    def get_bb(self):
        # 나루토는 120프레임부터, 이타치는 처음부터 히트박스 활성화
        threshold = 0 if self.special_image else 120

        if self.character.frame >= threshold:
            special_attack_frames = self.character.config.special_attack_frames

            # 이타치의 경우 스페셜 프레임 데이터 사용
            if hasattr(self.character.config, 'special_attack_frames_data') and self.character.config.special_attack_frames_data:
                all_frames = self.character.config.special_attack_frames_data
                frame_idx = int(self.character.frame)
            else:
                all_frames = self.character.config.frames
                frame_idx = special_attack_frames[int(self.character.frame)]

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

    def handle_collision(self, group, other):
        pass

