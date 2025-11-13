from pico2d import load_image

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
        draw_w = int(self.width * 2 / 3)
        draw_h = int(self.height * 2 / 3)

        if self.target.face_dir == 1:
            self.image.clip_draw(0, 0, self.width, self.height, x, y, draw_w, draw_h)
        else:
            self.image.clip_composite_draw(0, 0, self.width, self.height, 0.0, 'h', x, y, draw_w, draw_h)
