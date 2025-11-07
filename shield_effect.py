from pico2d import load_image
import game_framework
from character_config import ACTION_PER_TIME, SHIELD_EFFECT_ANIMATION_SPEED

class ShieldEffect:
    def __init__(self, target):
        self.target = target
        self.image = load_image('shield_effect.png')
        self.frame_count = 8
        self.frame_w = self.image.w // 8
        self.frame_h = self.image.h
        self.frame = 0.0

    def update(self):
        self.frame = (self.frame + self.frame_count * ACTION_PER_TIME * SHIELD_EFFECT_ANIMATION_SPEED * game_framework.frame_time) % self.frame_count

    def draw(self):
        l = int(self.frame) * self.frame_w
        b = 0
        x = self.target.x
        y = self.target.y
        draw_w = int(self.frame_w * 2 / 3)
        draw_h = int(self.frame_h * 2 / 3)

        if self.target.face_dir == 1:
            self.image.clip_draw(l, b, self.frame_w, self.frame_h, x, y, draw_w, draw_h)
        else:
            self.image.clip_composite_draw(l, b, self.frame_w, self.frame_h, 0.0, 'h', x, y, draw_w, draw_h)
