from characters_naruto_frames import FRAMES
from event_to_string import up_down, left_down, right_down, left_up, right_up

JUMP1_IDX = [33, 34]
JUMP2_IDX = [35, 36]

class Jump:
    def __init__(self, naruto):
        self.naruto = naruto
        self.phase = 0          # 0: 초기화, 1: 1단 점프 중, 2: 2단 점프 중
        self.seq = []           # 현재 애니 프레임 인덱스 시퀀스
        self.cur = 0            # seq 안에서 현재 위치
        self.accum_time = 0.0
        self.frame_duration = 0.08

        self.vy = 0.0           # 수직 속도
        self.vx = 0.0           # 수평 속도 (포물선 점프용)
        self.g = -800.0         # 중력 가속도
        self.ground_y = 0.0     # 착지할 y

        self.dir = 0  # 이동 방향 (-1: 왼쪽, 0: 정지, 1: 오른쪽)

    def enter(self, e):
        # 이전 상태에 따라 점프 초기화
        if self.phase == 0:
            self.phase = 1
            self.seq = JUMP1_IDX[:]
            self.cur = 0
            self.accum_time = 0.0
            self.naruto.frame = self.seq[self.cur]
            self.vy = 400.0
            self.ground_y = self.naruto.y

            # RUN 상태에서 점프했으면 수평 속도 유지
            if hasattr(self.naruto, 'dir'):
                self.vx = self.naruto.dir * 200.0
            else:
                self.vx = 0.0
            self.dir = 0

        elif self.phase == 1 and up_down(e):  # 공중에서 2단 점프
            self.phase = 2
            self.seq = JUMP2_IDX[:]
            self.cur = 0
            self.accum_time = 0.0
            self.naruto.frame = self.seq[self.cur]
            self.vy = 400.0

    def exit(self, e):
        # 착지 시 초기화
        self.phase = 0
        self.dir = 0

    def do(self, dt):
        # 좌우 이동 처리
        if self.dir == -1:
            self.vx -= 300.0 * dt
            if self.vx < -400.0:
                self.vx = -400.0
            self.naruto.face_dir = -1
        elif self.dir == 1:
            self.vx += 300.0 * dt
            if self.vx > 400.0:
                self.vx = 400.0
            self.naruto.face_dir = 1

        # 애니메이션 프레임 진행
        self.accum_time += dt
        if self.accum_time >= self.frame_duration:
            self.accum_time -= self.frame_duration
            if self.cur < len(self.seq) - 1:
                self.cur += 1
                self.naruto.frame = self.seq[self.cur]

        # 수평 이동 적용
        self.naruto.x += self.vx * dt

        # 중력 적용
        self.vy += self.g * dt
        self.naruto.y += self.vy * dt

        # 착지 체크
        if self.naruto.y <= self.ground_y:
            self.naruto.y = self.ground_y
            self.naruto.frame = 0
            # IDLE 상태로 전환하기 위한 이벤트 발생
            from event_to_string import landed
            self.naruto.state_machine.handle_event(('LANDED', None))

    def draw(self):
        frame = FRAMES[self.seq[self.cur]]
        l, b, w, h = frame['left'], frame['bottom'], frame['width'], frame['height']

        if self.naruto.face_dir == 1:
            self.naruto.image.clip_draw(l, b, w, h, self.naruto.x, self.naruto.y)
        else:
            self.naruto.image.clip_composite_draw(l, b, w, h, 0.0, 'h',
                                                  self.naruto.x, self.naruto.y, w, h)
