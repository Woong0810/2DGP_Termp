from pico2d import load_image, draw_rectangle
from camera import camera

class Background:
    def __init__(self, stage_index = 0):
        self.stage_index = stage_index

        if self.stage_index == 0:
            self.image = load_image('background1.png')
            self.platforms = [
                {'left': 0, 'bottom': 0, 'right': 2000, 'top': 20},
                {'left': 470, 'bottom': 180, 'right': 700, 'top': 200},
                {'left': 870, 'bottom': 240, 'right': 1080, 'top': 260},
                {'left': 800, 'bottom': 180, 'right': 1150, 'top': 200},
                {'left': 1230, 'bottom': 180, 'right': 1470, 'top': 200},
            ]
        else:
            self.image = load_image('background2.png')
            self.platforms = [
                {'left': 0, 'bottom': 0, 'right': 2000, 'top': 20},
                {'left': 470, 'bottom': 180, 'right': 700, 'top': 200},
                {'left': 870, 'bottom': 240, 'right': 1080, 'top': 260},
                {'left': 800, 'bottom': 180, 'right': 1150, 'top': 200},
                {'left': 1230, 'bottom': 180, 'right': 1470, 'top': 200},
                {'left': 100, 'bottom': 150, 'right': 300, 'top': 170},
                {'left': 50, 'bottom': 250, 'right': 100, 'top': 270},
                {'left': 170, 'bottom': 370, 'right': 230, 'top': 390},
                {'left': 1700, 'bottom': 150, 'right': 1900, 'top': 170},
                {'left': 1900, 'bottom': 250, 'right': 1950, 'top': 270},
                {'left': 1770, 'bottom': 370, 'right': 1900, 'top': 390},
            ]
        self.width = self.image.w
        self.height = self.image.h

    def update(self):
        pass

    def draw(self):
        cx, cy = camera.world_to_screen(self.width * 0.5, self.height * 0.5)
        self.image.draw(cx, cy)

        for box in self.platforms:
            left, bottom, right, top = box['left'], box['bottom'], box['right'], box['top']
            sx1, sy1 = camera.world_to_screen(left, bottom)
            sx2, sy2 = camera.world_to_screen(right, top)
            draw_rectangle(sx1, sy1, sx2, sy2)

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

            if bottom <= b_top <= prev_bottom:
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