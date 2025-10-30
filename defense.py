from characters_naruto_frames import FRAMES

IDLE_FRAMES = [FRAMES[i] for i in range(12, 16)]

class Defense:
    def __init__(self, naruto):
        pass

    def enter(self, e):
        self.naruto.accum_time = 0.0
        self.naruto.frame_duration = 0.1
        self.naruto.frame = 0

    def exit(self, e):
        pass

    def do(self, dt):
        self.naruto.accum_time += dt
        if self.naruto.accum_time >= self.naruto.frame_duration:
            self.naruto.accum_time -= self.naruto.frame_duration
            self.naruto.frame = (self.naruto.frame + 1) % len(IDLE_FRAMES)

    def draw(self):
        frame = IDLE_FRAMES[self.naruto.frame]
        l, b, w, h = frame['left'], frame['bottom'], frame['width'], frame['height']

        if self.naruto.face_dir == 1:
            self.naruto.image.clip_draw(l, b, w, h, self.naruto.x, self.naruto.y)
        else:
            self.naruto.image.clip_composite_draw(l, b, w, h, 0.0, 'h',
                                                  self.naruto.x, self.naruto.y, w, h)
