# camera.py

class Camera:
    def __init__(self, width=800, height=600):
        self.width = width
        self.height = height

        self.x = width * 0.5
        self.y = height * 0.5

        self.stage_left = 0.0
        self.stage_right = width

        self.p1 = None
        self.p2 = None

        self.smooth = 0.15
        self.initialized = True

    def set_stage_bounds(self, left, right):
        self.stage_left = float(left)
        self.stage_right = float(right)

    def set_targets(self, p1, p2):
        self.p1 = p1
        self.p2 = p2
        self.initialized = True

    def update(self):
        target_x = (self.p1.x + self.p2.x) * 0.5

        half_w = self.width * 0.5
        min_x = self.stage_left + half_w
        max_x = self.stage_right - half_w

        if target_x < min_x:
            target_x = min_x
        elif target_x > max_x:
            target_x = max_x

        if self.initialized:
            self.x = target_x
            self.initialized = False
            return

        self.x += (target_x - self.x) * self.smooth
        self.clamp_character_position(self.p1)
        self.clamp_character_position(self.p2)

    # 카메라 중심을 항상 스크린 중앙으로
    def world_to_screen(self, x, y):
        sx = x - self.x + self.width * 0.5
        sy = y - self.y + self.height * 0.5
        return sx, sy

    def clamp_character_position(self, character):
        margin = 20
        half_w = self.width * 0.5
        window_left = self.x - half_w + margin
        window_right = self.x + half_w - margin

        if character.x < window_left:
            character.x = window_left
        elif character.x > window_right:
            character.x = window_right

camera = Camera()
