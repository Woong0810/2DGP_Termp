from characters_naruto_frames import FRAMES

JUMP_IDX = [33, 34]

class Jump:
    def __init__(self, naruto):
        self.naruto = naruto
        self.jump_count = 0     # 0: 지상, 1: 1단 점프, 2: 2단 점프
        self.cur = 0            # 애니메이션 프레임 인덱스
        self.accum_time = 0.0
        self.frame_duration = 0.08

        self.vy = 0.0           # 수직 속도
        self.vx = 0.0           # 수평 속도 (포물선 점프용)
        self.g = -800.0         # 중력 가속도
        self.ground_y = 0.0     # 착지할 y (1단 점프 시작 지점으로 고정)

        self.dir = 0  # 이동 방향 (-1: 왼쪽, 0: 정지, 1: 오른쪽)

    def enter(self, e):
        # 지상에서 첫 점프만 초기화
        self.jump_count = 1
        self.cur = 0
        self.accum_time = 0.0
        self.naruto.frame = JUMP_IDX[self.cur]
        self.vy = 400.0
        self.ground_y = self.naruto.y  # 최초 점프 시작 지점을 착지점으로 기억

        # 이전 상태가 RUN이었으면 수평 속도 유지, IDLE에서는 수직 점프
        prev_state = self.naruto.state_machine.prev_state
        if prev_state == self.naruto.RUN:
            self.vx = self.naruto.dir * 200.0
        else:
            self.vx = 0.0
        self.dir = 0

    def exit(self, e):
        # 착지 시 초기화
        self.jump_count = 0
        self.dir = 0
        self.vx = 0.0

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
            if self.cur < len(JUMP_IDX) - 1:
                self.cur += 1
                self.naruto.frame = JUMP_IDX[self.cur]

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
            self.naruto.state_machine.handle_event(('LANDED', None))

    def handle_double_jump(self):
        """2단 점프 처리 - do()에서 호출"""
        if self.jump_count == 1:
            self.jump_count = 2
            self.cur = 0
            self.accum_time = 0.0
            self.naruto.frame = JUMP_IDX[self.cur]
            self.vy = 400.0
            # ground_y는 변경하지 않음 - 1단 점프 시작점이 최종 착지점

    def draw(self):
        frame = FRAMES[JUMP_IDX[self.cur]]
        l, b, w, h = frame['left'], frame['bottom'], frame['width'], frame['height']

        if self.naruto.face_dir == 1:
            self.naruto.image.clip_draw(l, b, w, h, self.naruto.x, self.naruto.y)
        else:
            self.naruto.image.clip_composite_draw(l, b, w, h, 0.0, 'h',
                                                  self.naruto.x, self.naruto.y, w, h)
