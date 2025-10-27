from event_to_string import right_down, right_up, left_down, left_up, up_down
from characters_naruto_frames import FRAMES

NORMAL_ATTACK_FRAME = [FRAMES[i] for i in range(0, 12)]
SEGMENTS = [(0, 3), (4, 7), (8, 11)]

class Normal_Attack:
    def __init__(self, naruto):
        self.naruto = naruto
        self.combo_index = 0
        self.start_frame = 0
        self.end_frame = 0
        self.cur = 0

    def enter(self, e):
        self.start_frame, self.end_frame = SEGMENTS[self.combo_index]
        self.cur = self.start_frame
        self.naruto.frame = self.cur
        self.naruto.accum_time = 0.0
        self.naruto.frame_duration = 0.13

    def exit(self, e):
        if up_down(e):
            self.naruto.jump_action()

    def do(self, dt):
        if self.naruto.JUMP.active:
            return

        self.naruto.accum_time += dt
        if self.naruto.accum_time >= self.naruto.frame_duration:
            self.naruto.accum_time -= self.naruto.frame_duration
            if self.cur < self.end_frame:
                self.cur += 1
                self.naruto.frame = self.cur
            else:
                self.combo_index = (self.combo_index + 1) % len(SEGMENTS)
                self.start_frame, self.end_frame = SEGMENTS[self.combo_index]
                self.cur = self.start_frame
                self.naruto.frame = self.cur

    def draw(self):
        frame = NORMAL_ATTACK_FRAME[self.naruto.frame]
        l, b, w, h = frame['left'], frame['bottom'], frame['width'], frame['height']

        if self.naruto.face_dir == 1:
            self.naruto.image.clip_draw(l, b, w, h, self.naruto.x, self.naruto.y)
        else:
            self.naruto.image.clip_composite_draw(l, b, w, h, 0.0, 'h',
                                                  self.naruto.x, self.naruto.y, w, h)
