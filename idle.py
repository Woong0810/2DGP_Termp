from characters_naruto_frames import FRAMES

IDLE_FRAMES = [FRAMES[i] for i in range(41, 47)]

class Idle:
    def __init__(self, naruto):
        self.naruto = naruto
        self.accum_time = 0.0
        self.frame_duration = 0.1  # 프레임당 0.1초

    def enter(self, e):
        self.accum_time = 0.0

    def exit(self, e):
        pass

    def do(self, dt):
        self.accum_time += dt
        if self.accum_time >= self.frame_duration:
            self.accum_time -= self.frame_duration
            self.naruto.frame = (self.naruto.frame + 1) % len(IDLE_FRAMES)

    def draw(self):
        frame = IDLE_FRAMES[self.naruto.frame]
        l, b, w, h = frame['left'], frame['bottom'], frame['width'], frame['height']

        if self.naruto.face_dir == 1:
            self.naruto.image.clip_draw(l, b, w, h, self.naruto.x, self.naruto.y)
        else:
            self.naruto.image.clip_composite_draw(l, b, w, h, 0.0, 'h',
                                                  self.naruto.x, self.naruto.y, w, h)
