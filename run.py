from character import right_down, right_up, left_down, left_up
from characters_naruto_frames import FRAMES
RUN_FRAMES = [FRAMES[i] for i in range(26, 32)]

class Run:
    def __init__(self, naruto):
        self.naruto = naruto
    def enter(self, e):
        if right_down(e) or left_up(e):
            self.naruto.dir = self.naruto.face_dir = 1
        elif left_down(e) or right_up(e):
            self.naruto.dir = self.naruto.face_dir = -1
    def exit(self, e):
        pass
    def do(self):
        self.naruto.frame = (self.naruto.frame + 1) % len(RUN_FRAMES)
        self.naruto.x += 5 * self.naruto.face_dir
        pass
    def draw(self):
        frame = RUN_FRAMES[self.naruto.frame]
        l, b, w, h = frame['left'], frame['bottom'], frame['width'], frame['height']

        if self.naruto.face_dir == 1:  # 오른쪽
            self.naruto.image.clip_draw(l, b, w, h, self.naruto.x, self.naruto.y)
        else:
            self.naruto.image.clip_composite_draw(l, b, w, h, 0.0, 'h',
                                                  self.naruto.x, self.naruto.y, w, h)
