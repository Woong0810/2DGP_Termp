from characters_naruto_frames import FRAMES

JUMP1_IDX = [33, 34]
JUMP2_IDX = [35, 36]

class Jump:
    def __init__(self, naruto):
        self.naruto = naruto
        self.phase = 0  # 0: 점프 안함, 1: 1단 점프 중, 2: 2단 점프 중
        self.seq = []  # 재생중인 프레임 인덱스 리스트
        self.cur = 0  # seq 안에서 현재 프레임 위치

        self.vy = 0.0  # 수직 속도
        self.g = -800.0  # 중력 가속도
        self.ground_y = 0.0  # 착지 기준 y

    def enter(self, e):
        if self.phase == 0:
            self.phase = 1
            self.seq = JUMP1_IDX[:]  # [33,34]
            self.ground_y = self.naruto.y  # 현재 y로 다시 착지

        elif self.phase == 1:
            self.phase = 2
            self.seq = JUMP2_IDX[:]  # [35,36]

        else:
            pass

        self.cur = 0
        self.naruto.accum_time = 0.0
        self.naruto.frame_duration = 0.08
        self.naruto.frame = self.seq[self.cur]
        self.vy = 400.0

    def exit(self, e):
        self.phase = 0

    def do(self, dt):
        self.naruto.accum_time += dt
        if self.naruto.accum_time >= self.naruto.frame_duration:
            self.naruto.accum_time -= self.naruto.frame_duration
            if self.cur < len(self.seq) - 1:
                self.cur += 1
                self.naruto.frame = self.seq[self.cur]

        self.vy += self.g * dt
        self.naruto.y += self.vy * dt

        if self.naruto.y <= self.ground_y:
            self.naruto.y = self.ground_y
            self.naruto.state_machine.handle_event(('JUMP', 'LAND'))

    def draw(self):
        frame = FRAMES[self.naruto.frame]
        l, b, w, h = frame['left'], frame['bottom'], frame['width'], frame['height']

        if self.naruto.face_dir == 1:
            self.naruto.image.clip_draw(l, b, w, h, self.naruto.x, self.naruto.y)
        else:
            self.naruto.image.clip_composite_draw(l, b, w, h, 0.0, 'h',
                                                  self.naruto.x, self.naruto.y, w, h)
