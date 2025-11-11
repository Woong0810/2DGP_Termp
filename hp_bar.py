from pico2d import load_image

class HPBar:
    def __init__(self, x, y, character=None, is_flipped=False):
        self.empty_image = load_image('empty_hp_bar.png')
        self.full_image = load_image('full_hp_bar.png')
        self.x = x
        self.y = y
        self.width = self.empty_image.w
        self.height = self.empty_image.h
        self.character = character
        self.is_flipped = is_flipped  # Player2는 오른쪽에서 왼쪽으로 감소

        # HP 캐싱 (HP가 변경될 때만 다시 계산)
        self.prev_hp = -1
        self.saved_clip_width = self.width
        self.saved_clip_left = 0
        self.saved_draw_x = self.x

    def update(self):
        if self.character:
            current_hp = self.character.hp
            if current_hp != self.prev_hp:
                self.prev_hp = current_hp

                if self.character.max_hp > 0:
                    hp_ratio = current_hp / self.character.max_hp
                else:
                    hp_ratio = 0.0

                self.saved_clip_width = int(self.width * hp_ratio)

                if self.is_flipped:
                    self.saved_clip_left = self.width - self.saved_clip_width
                    self.saved_draw_x = self.x + (self.width - self.saved_clip_width) // 2
                else:
                    self.saved_clip_left = 0
                    self.saved_draw_x = self.x - (self.width - self.saved_clip_width) // 2

    def draw(self):
        self.empty_image.clip_draw(0, 0, self.width, self.height, self.x, self.y)

        if self.saved_clip_width > 0:
            self.full_image.clip_draw(
                self.saved_clip_left, 0, self.saved_clip_width,
                self.height, self.saved_draw_x, self.y)

    def handle_collision(self, group, other):
        pass