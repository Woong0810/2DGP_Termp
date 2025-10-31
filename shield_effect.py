from pico2d import load_image

class ShieldEffect:
    def __init__(self, target):
        self.target = target
        self.image = load_image('shield_effect.png')
        self.frame_count = 8
        self.frame_w = self.image.w // 8
        self.frame_h = self.image.h
        self.frame = 0
        self.accum = 0.0
        self.frame_duration = 0.06
        self.y_offset = 10

    def update(self, dt):
        self.accum += dt
        if self.accum >= self.frame_duration:
            self.accum -= self.frame_duration
            self.frame = (self.frame + 1) % self.frame_count

    def draw(self):
        l = self.frame * self.frame_w
        b = 0
        x = self.target.x
        y = self.target.y + self.y_offset

        # draw behind the character; flipping handled so effect faces same dir
        if self.target.face_dir == 1:
            self.image.clip_draw(l, b, self.frame_w, self.frame_h, x, y)
        else:
            self.image.clip_composite_draw(l, b, self.frame_w, self.frame_h, 0.0, 'h', x, y, self.frame_w, self.frame_h)
