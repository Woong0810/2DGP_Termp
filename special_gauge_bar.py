from pico2d import load_image
from character_config import SPECIAL_GAUGE_MAX

class SpecialGaugeBar:
    def __init__(self, x, y, character=None, is_flipped=False):
        self.empty_image = load_image('special_gauge_bar_empty.png')
        self.full_image = load_image('special_gauge_bar_full.png')
        self.x = x
        self.y = y
        self.width = self.empty_image.w
        self.height = self.empty_image.h
        self.character = character
        self.is_flipped = is_flipped

        self.prev_gauge = -1.0
        self.saved_clip_width = 0
        self.saved_clip_left = 0
        self.saved_draw_x = self.x

    def update(self):
        if self.character:
            current_gauge = self.character.special_gauge
            if current_gauge != self.prev_gauge:
                self.prev_gauge = current_gauge

                if SPECIAL_GAUGE_MAX  > 0:
                    gauge_ratio = current_gauge / SPECIAL_GAUGE_MAX
                else:
                    gauge_ratio = 0.0

                self.saved_clip_width = int(self.width * gauge_ratio)

                if self.is_flipped:
                    self.saved_clip_left = self.width - self.saved_clip_width
                    self.saved_draw_x = self.x + (self.width - self.saved_clip_width) // 2
                else:
                    self.saved_clip_left = 0
                    self.saved_draw_x = self.x - (self.width - self.saved_clip_width) // 2

    def draw(self):
        if self.empty_image:
            self.empty_image.draw(self.x, self.y, self.width, self.height)

        if self.saved_clip_width <= 0:
            return

        self.full_image.clip_draw(
            self.saved_clip_left, 0,
            self.saved_clip_width, self.height,
            self.saved_draw_x, self.y
        )

    def handle_collision(self, group, other):
        pass