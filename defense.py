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

        if self.character.face_dir == 1:
            self.character.image.clip_draw(l, b, w, h, self.character.x, self.character.y)
        else:
            self.character.image.clip_composite_draw(l, b, w, h, 0.0, 'h',
                                                  self.character.x, self.character.y, w, h)

    def get_bb(self, scale_x=1.0, scale_y=1.0, x_offset=0, y_offset=0):
        if self.shield_effect is None:
            return (0, 0, 0, 0)

        frame_w = self.shield_effect.frame_w
        frame_h = self.shield_effect.frame_h

        draw_w = int(frame_w * 2 / 3)
        draw_h = int(frame_h * 2 / 3)

        hw = draw_w * scale_x / 2
        hh = draw_h * scale_y / 2
        return (
            self.character.x - hw + x_offset,  # left
            self.character.y - hh + y_offset,  # bottom
            self.character.x + hw + x_offset,  # right
            self.character.y + hh + y_offset   # top
        )

    def draw_bb(self):
        # 디버그용: 바운딩 박스를 화면에 그리기
        left, bottom, right, top = self.get_bb()
        draw_rectangle(left, bottom, right, top)
