from pico2d import draw_rectangle
import game_world
from shield_effect import ShieldEffect
from character_config import ACTION_PER_TIME, DEFENSE_ANIMATION_SPEED
import game_framework

class Defense:
    def __init__(self, character):
        self.character = character
        self.shield_effect = None

    def enter(self, e):
        self.character.frame = 0
        # create and add shield effect behind the character (layer 0)
        self.shield_effect = ShieldEffect(self.character)
        game_world.add_object(self.shield_effect, 0)

        game_world.add_collision_pairs('normal_attack:character', None, self.character)
        game_world.add_collision_pairs('special_attack:character', None, self.character)
        game_world.add_collision_pairs('ranged_attack:character', None, self.character)

    def exit(self, e):
        if self.shield_effect is not None:
            game_world.remove_object(self.shield_effect)
            self.shield_effect = None

        game_world.remove_collision_object(self.character)

    def do(self):
        defense_frames = self.character.config.defense_frames
        frames_per_action = len(defense_frames)

        self.character.frame += frames_per_action * ACTION_PER_TIME * DEFENSE_ANIMATION_SPEED * game_framework.frame_time

        # 마지막 프레임에 도달하면 유지
        if self.character.frame >= frames_per_action - 1:
            self.character.frame = frames_per_action - 1

    def draw(self):
        defense_frames = self.character.config.defense_frames
        all_frames = self.character.config.frames
        frame_idx = defense_frames[int(self.character.frame)]  # int로 변환
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
        if self.shield_effect is not None:
            draw_w = int(self.shield_effect.frame_w * 2 / 3)
            draw_h = int(self.shield_effect.frame_h * 2 / 3)

            hb = self.character.config.hitbox_defense
            hw = draw_w * hb['scale_x'] / 2
            hh = draw_h * hb['scale_y'] / 2

            return (
                self.character.x - hw,
                self.character.y - hh,
                self.character.x + hw,
                self.character.y + hh
            )
        else:
            # 실드가 없으면 히트박스 없음
            return (0, 0, 0, 0)

    def draw_bb(self):
        # 디버그용: 바운딩 박스를 화면에 그리기
        left, bottom, right, top = self.get_bb()
        draw_rectangle(left, bottom, right, top)

