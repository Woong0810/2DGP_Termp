from characters_naruto_frames import FRAMES
from pico2d import draw_rectangle
import game_world
from shield_effect import ShieldEffect

DEFENSE_FRAMES = [FRAMES[i] for i in range(12, 17)]

class Defense:
    def __init__(self, naruto):
        self.naruto = naruto
        self.shield_effect = None

    def enter(self, e):
        self.naruto.accum_time = 0.0
        self.naruto.frame_duration = 0.1
        self.naruto.frame = 0
        # create and add shield effect behind the character (layer 0)
        self.shield_effect = ShieldEffect(self.naruto)
        game_world.add_object(self.shield_effect, 0)

    def exit(self, e):
        if self.shield_effect is not None:
            game_world.remove_object(self.shield_effect)
            self.shield_effect = None

    def do(self, dt):
        self.naruto.accum_time += dt
        if self.naruto.accum_time >= self.naruto.frame_duration:
            self.naruto.accum_time -= self.naruto.frame_duration
            # 마지막 프레임에 도달하면 유지
            if self.naruto.frame < len(DEFENSE_FRAMES) - 1:
                self.naruto.frame += 1

    def draw(self):
        frame = DEFENSE_FRAMES[self.naruto.frame]
        l, b, w, h = frame['left'], frame['bottom'], frame['width'], frame['height']

        if self.naruto.face_dir == 1:
            self.naruto.image.clip_draw(l, b, w, h, self.naruto.x, self.naruto.y)
        else:
            self.naruto.image.clip_composite_draw(l, b, w, h, 0.0, 'h',
                                                  self.naruto.x, self.naruto.y, w, h)

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
            self.naruto.x - hw + x_offset,  # left
            self.naruto.y - hh + y_offset,  # bottom
            self.naruto.x + hw + x_offset,  # right
            self.naruto.y + hh + y_offset   # top
        )

    def draw_bb(self):
        # 디버그용: 바운딩 박스를 화면에 그리기
        left, bottom, right, top = self.get_bb()
        draw_rectangle(left, bottom, right, top)
