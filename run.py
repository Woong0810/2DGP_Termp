from event_to_string import right_down, right_up, left_down, left_up
from characters_naruto_frames import FRAMES

RUN_FRAMES = [FRAMES[i] for i in range(26, 32)]

class Run:
    def __init__(self, naruto):
        self.naruto = naruto

    def enter(self, e):
        self.naruto.accum_time = 0.0
        self.naruto.frame_duration = 0.04
        if right_down(e) or left_up(e):
            self.naruto.dir = self.naruto.face_dir = 1
        elif left_down(e) or right_up(e):
            self.naruto.dir = self.naruto.face_dir = -1

    def exit(self, e):
        pass

    def do(self, dt):
        self.naruto.accum_time += dt
        if self.naruto.accum_time >= self.naruto.frame_duration:
            self.naruto.accum_time -= self.naruto.frame_duration
            self.naruto.frame = (self.naruto.frame + 1) % len(RUN_FRAMES)
            self.naruto.x += 10 * self.naruto.dir

    def draw(self):
        frame = RUN_FRAMES[self.naruto.frame]
        l, b, w, h = frame['left'], frame['bottom'], frame['width'], frame['height']

        if self.naruto.face_dir == 1:
            self.naruto.image.clip_draw(l, b, w, h, self.naruto.x, self.naruto.y)
        else:
            self.naruto.image.clip_composite_draw(l, b, w, h, 0.0, 'h',
                                                  self.naruto.x, self.naruto.y, w, h)
