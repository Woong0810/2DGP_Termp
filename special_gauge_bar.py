from pico2d import load_image

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

        # HP 캐싱 (HP가 변경될 때만 다시 계산)
        self.prev_hp = -1
        self.saved_clip_width = self.width
        self.saved_clip_left = 0
        self.saved_draw_x = self.x

    def update(self):
        pass

    def draw(self):
        self.empty_image.clip_draw(0, 0, self.width, self.height, self.x, self.y)

        if self.saved_clip_width > 0:
            self.full_image.clip_draw(
                self.saved_clip_left, 0, self.saved_clip_width,
                self.height, self.saved_draw_x, self.y)

    def handle_collision(self, group, other):
        pass