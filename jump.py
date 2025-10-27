from characters_naruto_frames import FRAMES

JUMP1_IDX = [33, 34]
JUMP2_IDX = [35, 36]

class Jump:
    def __init__(self, naruto):
        self.naruto = naruto
        self.active = False     # 지금 공중에 떠있는 중인지
        self.phase = 0          # 0=지상, 1=1단 점프 중, 2=2단 점프 중
        self.seq = []           # 현재 애니 프레임 인덱스 시퀀스
        self.cur = 0            # seq 안에서 현재 위치
        self.accum_time = 0.0
        self.frame_duration = 0.08

        self.vy = 0.0           # 수직 속도
        self.g = -800.0         # 중력 가속도
        self.ground_y = 0.0     # 착지할 y

    def start_or_double_jump(self):
        if not self.active:
            # 지상에서 처음 점프
            self.active = True
            self.phase = 1
            self.seq = JUMP1_IDX[:]   # [33,34]
            self.cur = 0

            self.accum_time = 0.0
            self.frame_duration = 0.08
            self.naruto.frame = self.seq[self.cur]

            self.vy = 400.0
            self.ground_y = self.naruto.y  # 지금 y를 착지 기준으로 기억

        elif self.phase == 1:
            # 공중에서 2단 점프
            self.phase = 2
            self.seq = JUMP2_IDX[:]   # [35,36]
            self.cur = 0

            self.accum_time = 0.0
            self.frame_duration = 0.08
            self.naruto.frame = self.seq[self.cur]

            self.vy = 400.0
            # ground_y는 건드리지 않는다. 착지는 여전히 첫 점프 시작 y로.

        else:
            # 이미 phase==2면 더 이상 점프 안 늘어난다
            pass

    def update(self, dt):
        if not self.active:
            return

        self.accum_time += dt
        if self.accum_time >= self.frame_duration:
            self.accum_time -= self.frame_duration
            if self.cur < len(self.seq) - 1:
                self.cur += 1
                self.naruto.frame = self.seq[self.cur]
            # 마지막 프레임이면 그냥 유지

        self.vy += self.g * dt
        self.naruto.y += self.vy * dt

        if self.naruto.y <= self.ground_y:
            self.naruto.y = self.ground_y
            self.active = False
            self.phase = 0

    def draw(self):
        if not self.active:
            return

        frame = FRAMES[self.seq[self.cur]]
        l, b, w, h = frame['left'], frame['bottom'], frame['width'], frame['height']

        if self.naruto.face_dir == 1:
            self.naruto.image.clip_draw(l, b, w, h, self.naruto.x, self.naruto.y)
        else:
            self.naruto.image.clip_composite_draw(l, b, w, h, 0.0, 'h',
                                                  self.naruto.x, self.naruto.y, w, h)
