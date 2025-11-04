from pico2d import draw_rectangle
import game_world
from shield_effect import ShieldEffect

class Defense:
    def __init__(self, character):
        self.character = character
        self.shield_effect = None

    def enter(self, e):
        self.character.accum_time = 0.0
        self.character.frame_duration = 0.1
        self.character.frame = 0
        # create and add shield effect behind the character (layer 0)
        self.shield_effect = ShieldEffect(self.character)
        game_world.add_object(self.shield_effect, 0)

    def exit(self, e):
        if self.shield_effect is not None:
            game_world.remove_object(self.shield_effect)
            self.shield_effect = None

    def do(self, dt):
        self.character.accum_time += dt
        if self.character.accum_time >= self.character.frame_duration:
            self.character.accum_time -= self.character.frame_duration
            defense_frames = self.character.config.defense_frames
            # 마지막 프레임에 도달하면 유지
            if self.character.frame < len(defense_frames) - 1:
                self.character.frame += 1

    def draw(self):
        defense_frames = self.character.config.defense_frames
        all_frames = self.character.config.frames
        frame_idx = defense_frames[self.character.frame]
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
