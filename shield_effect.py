from pico2d import load_image
from camera import camera

class ShieldEffect:
    def __init__(self, target):
        self.target = target
        self.image = load_image('shield_effect.png')
        self.width = self.image.w
        self.height = self.image.h

    def update(self):
        pass  # 단일 프레임이므로 업데이트 불필요

    def draw(self):
        x = self.target.x
        y = self.target.y
        draw_w = int(self.width * 3 / 4)
        draw_h = int(self.height * 3 / 4)

        sx, sy = camera.world_to_screen(x, y)

        if self.target.face_dir == 1:
            self.image.clip_draw(0, 0, self.width, self.height, sx, sy, draw_w, draw_h)
        else:
            self.image.clip_composite_draw(0, 0, self.width, self.height, 0.0, 'h', sx, sy, draw_w, draw_h)
