from pico2d import load_image, draw_rectangle


class Background:
    def __init__(self):
        self.image = load_image('background1.png')

        self.platforms = [
            {'left': 0, 'bottom': 0, 'right': 800, 'top': 20},
            {'left': 0, 'bottom': 180, 'right': 200, 'top': 200},
            {'left': 300, 'bottom': 180, 'right': 650, 'top': 200},
            {'left': 360, 'bottom': 240, 'right': 600, 'top': 260},
            {'left': 730, 'bottom': 180, 'right': 800, 'top': 200},
        ]

    def update(self):
        pass

    def draw(self):
        self.image.draw(400, 300)

        for box in self.platforms:
            draw_rectangle(box['left'], box['bottom'], box['right'], box['top'])

    def get_bb(self):
        b = self.platforms[0]
        return (b['left'], b['bottom'], b['right'], b['top'])

    def handle_collision(self, group, other):
        pass

    def find_landing_platform(self, left, prev_bottom, right, bottom, vy):
        if vy > 0:
            return None

        landing_top = None

        for box in self.platforms:
            b_left, b_bottom, b_right, b_top = box['left'], box['bottom'], box['right'], box['top']

            if right <= b_left or left >= b_right:
                continue

            if prev_bottom >= b_top and bottom <= b_top:
                if landing_top is None or b_top > landing_top:
                    landing_top = b_top
        return landing_top

    def get_ground_top_under(self, left, bottom, right, tolerance=12):
        best_top = None

        for box in self.platforms:
            b_left, b_bottom, b_right, b_top = box['left'], box['bottom'], box['right'], box['top']

            if right <= b_left or left >= b_right:
                continue

            if b_top - tolerance <= bottom <= b_top + tolerance:
                if best_top is None or b_top > best_top:
                    best_top = b_top

        return best_top