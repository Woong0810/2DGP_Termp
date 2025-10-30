from event_to_string import right_down, right_up, left_down, left_up, up_down
from characters_naruto_frames import FRAMES

RUN_FRAMES = [FRAMES[i] for i in range(26, 32)]

class Run:
    def __init__(self, naruto):
        self.naruto = naruto

    def enter(self, e):
        self.naruto.accum_time = 0.0
        self.naruto.frame_duration = 0.04
        self.naruto.frame = 0
        if right_down(e) or left_up(e):
            self.naruto.dir = self.naruto.face_dir = 1
        elif left_down(e) or right_up(e):
            self.naruto.dir = self.naruto.face_dir = -1

    def exit(self, e):
        if up_down(e):
            self.naruto.jump_action(move_dir=self.naruto.dir)  # RUN 중 점프 시 이동 방향 전달

    def do(self, dt):
        if self.naruto.JUMP.active:
            return

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
