from pico2d import load_image

class HPBar:
    def __init__(self, x, y):
        self.empty_image = load_image('empty_hp_bar.png')
        self.full_image = load_image('full_hp_bar.png')
        self.x = x
        self.y = y
        self.width = 200
        self.height = 30

    def update(self):
        pass

    def draw(self):
        hp_ratio = 1
        hp_width = int(self.width * hp_ratio)
        self.empty_image.clip_draw(0, 0, hp_width, self.height, self.x + hp_width // 2, self.y)
        self.full_image.clip_draw(0, 0, hp_width, self.height, 500 + hp_width // 2, 500)

    def handle_collision(self, group, other):
        pass