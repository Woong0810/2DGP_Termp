from pico2d import load_image

class HPBar:
    def __init__(self, x, y, character=None, is_flipped=False):
        self.empty_image = load_image('empty_hp_bar.png')
        self.full_image = load_image('full_hp_bar.png')
        self.x = x
        self.y = y
        self.width = 250
        self.height = 20
        self.character = character
        self.is_flipped = is_flipped  # Player2는 오른쪽에서 왼쪽으로 감소

    def update(self):
        pass

    def draw(self):
        self.empty_image.clip_draw(0, 0, self.width - 1, self.height, self.x, self.y)

        if self.character and self.character.max_hp > 0:
            hp_ratio = self.character.hp / self.character.max_hp
        else:
            hp_ratio = 1.0

        if hp_ratio > 0:
            hp_width = int(self.width * hp_ratio)

            if self.is_flipped:
                # Player2: 오른쪽에서 왼쪽으로 감소
                clip_left = self.width - hp_width
                draw_x = self.x + (self.width - hp_width) // 2
                self.full_image.clip_draw(clip_left, 0, hp_width, self.height, draw_x, self.y)
            else:
                # Player1: 왼쪽에서 오른쪽
                draw_x = self.x - (self.width - hp_width) // 2
                self.full_image.clip_draw(0, 0, hp_width, self.height, draw_x, self.y)

    def handle_collision(self, group, other):
        pass