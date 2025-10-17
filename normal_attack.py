from event_to_string import right_down, right_up, left_down, left_up
from characters_naruto_frames import FRAMES
NORMAL_ATTACK_FRAME = [FRAMES[i] for i in range(0, 12)]
SEGMENTS = [(0, 3), (4, 7), (8, 11)]

class Normal_Attack:
    def __init__(self, naruto):
        self.naruto = naruto
        self.combo_index = 0
    def enter(self, e):
        self.start_frame, self.end_frame = SEGMENTS[self.combo_index]
    def exit(self, e):
        pass
    def do(self):
        self.naruto.frame += 1
        if self.naruto.frame > self.end_frame:
            self.combo_index = (self.combo_index + 1) % len(SEGMENTS)
            self.naruto.frame = SEGMENTS[self.combo_index][0]
            self.start_frame, self.end_frame = SEGMENTS[self.combo_index]
    def draw(self):
        frame = NORMAL_ATTACK_FRAME[self.naruto.frame]
        l, b, w, h = frame['left'], frame['bottom'], frame['width'], frame['height']

        if self.naruto.face_dir == 1:  # 오른쪽
            self.naruto.image.clip_draw(l, b, w, h, self.naruto.x, self.naruto.y)
        else:
            self.naruto.image.clip_composite_draw(l, b, w, h, 0.0, 'h',
                                                  self.naruto.x, self.naruto.y, w, h)
