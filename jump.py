from characters_naruto_frames import FRAMES
from sdl2 import SDL_KEYDOWN, SDL_KEYUP, SDLK_LEFT, SDLK_RIGHT

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
        self.vx = 0.0           # 수평 속도 (포물선 점프용)
        self.g = -800.0         # 중력 가속도
        self.ground_y = 0.0     # 착지할 y

        # 공중 이동 관련
        self.move_left = False
        self.move_right = False
        self.air_accel = 300.0  # 공중 가속도
        self.max_air_speed = 400.0  # 공중 최대 속도

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

            # RUN 상태에서 점프했을 때만 수평 속도 설정
            if self.naruto.state_machine.cur_state == self.naruto.RUN:
                self.vx = self.naruto.dir * 200.0  # 달리는 방향으로 수평 속도 설정
            else:
                self.vx = 0.0  # IDLE이나 다른 상태에서는 수직 점프

        elif self.phase == 1:
            # 공중에서 2단 점프
            self.phase = 2
            self.seq = JUMP2_IDX[:]   # [35,36]
            self.cur = 0

            self.accum_time = 0.0
            self.frame_duration = 0.08
            self.naruto.frame = self.seq[self.cur]

            self.vy = 400.0
            # ground_y와 vx는 건드리지 않는다. 수평 속도 유지.

        else:
            # 이미 phase==2면 더 이상 점프 안 늘어난다
            pass

    def handle_event(self, event):
        if not self.active:
            return

        if event.type == SDL_KEYDOWN:
            if event.key == SDLK_LEFT:
                self.move_left = True
                self.naruto.face_dir = -1
            elif event.key == SDLK_RIGHT:
                self.move_right = True
                self.naruto.face_dir = 1
        elif event.type == SDL_KEYUP:
            if event.key == SDLK_LEFT:
                self.move_left = False
            elif event.key == SDLK_RIGHT:
                self.move_right = False

    def update(self, dt):
        if not self.active:
            return

        # 애니메이션 프레임 진행
        self.accum_time += dt
        if self.accum_time >= self.frame_duration:
            self.accum_time -= self.frame_duration
            if self.cur < len(self.seq) - 1:
                self.cur += 1
                self.naruto.frame = self.seq[self.cur]
            # 마지막 프레임이면 그냥 유지

        # 공중 좌우 이동 (키 입력으로 vx 조절)
        if self.move_left:
            self.vx -= self.air_accel * dt
            # 최대 속도 제한
            if self.vx < -self.max_air_speed:
                self.vx = -self.max_air_speed
        elif self.move_right:
            self.vx += self.air_accel * dt
            # 최대 속도 제한
            if self.vx > self.max_air_speed:
                self.vx = self.max_air_speed

        # 수평 이동 적용
        self.naruto.x += self.vx * dt

        # 중력 적용
        self.vy += self.g * dt
        self.naruto.y += self.vy * dt

        # 착지 체크
        if self.naruto.y <= self.ground_y:
            self.naruto.y = self.ground_y
            self.active = False
            self.phase = 0
            self.naruto.frame = 0  # 착지 시 프레임 초기화
            self.move_left = False
            self.move_right = False
            self.vx = 0.0  # 수평 속도 초기화

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
