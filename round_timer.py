from pico2d import load_font
import game_framework
import os

class RoundTimer:
    def __init__(self, x, y, round_time=60):
        self.font = load_font('font.ttf', 50)

        self.x = x
        self.y = y
        self.max_time = round_time
        self.time = round_time

    def update(self):
        self.time -= game_framework.frame_time
        if self.time < 0:
            self.time = 0

    def draw(self):
        time_int = int(self.time)
        self.draw_bold_text(self.font, self.x - 25, self.y, f'{time_int:02d}', (0, 0, 0), thickness=2)

    def is_time_over(self):
        return self.time <= 0

    def reset(self):
        self.time = self.max_time

    def handle_collision(self, group, other):
        pass

    def draw_bold_text(self, font, x, y, text, color, thickness=1):
        for dx in range(-thickness, thickness + 1):
            for dy in range(-thickness, thickness + 1):
                font.draw(x + dx, y + dy, text, color)

