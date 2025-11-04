from pico2d import draw_rectangle

class Jump:
    def __init__(self, character):
        self.character = character
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

        jump_frames = self.character.config.jump_frames
        self.character.frame = jump_frames[self.cur]

        self.vy = 400.0
        self.ground_y = self.character.y  # 최초 점프 시작 지점을 착지점으로 기억

        # 이전 상태가 RUN이었으면 수평 속도 유지, IDLE에서는 수직 점프
        prev_state = self.character.state_machine.prev_state
        if prev_state == self.character.RUN:
            self.vx = self.character.dir * 200.0
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
            self.character.face_dir = -1
        elif self.dir == 1:
            self.vx += 300.0 * dt
            if self.vx > 400.0:
                self.vx = 400.0
            self.character.face_dir = 1

        self.accum_time += dt
        if self.accum_time >= self.frame_duration:
            self.accum_time -= self.frame_duration
            jump_frames = self.character.config.jump_frames
            if self.cur < len(jump_frames) - 1:
                self.cur += 1
                self.character.frame = jump_frames[self.cur]

        # 수평 이동 적용
        self.character.x += self.vx * dt

        # 중력 적용
        self.vy += self.g * dt
        self.character.y += self.vy * dt

        # 착지 체크
        if self.character.y <= self.ground_y:
            self.character.y = self.ground_y
            self.character.frame = 0
            # IDLE 상태로 전환하기 위한 이벤트 발생
            self.character.state_machine.handle_event(('LANDED', None))

    def handle_double_jump(self):
        if self.jump_count == 1:
            self.jump_count = 2
            self.cur = 0
            self.accum_time = 0.0
            jump_frames = self.character.config.jump_frames
            self.character.frame = jump_frames[self.cur]
            self.vy = 400.0

    def draw(self):
        jump_frames = self.character.config.jump_frames
        all_frames = self.character.config.frames
        frame = all_frames[self.character.frame]

        l, b, w, h = frame['left'], frame['bottom'], frame['width'], frame['height']
        draw_w = int(w * self.character.config.scale_x)
        draw_h = int(h * self.character.config.scale_y)
        draw_y = self.character.y + self.character.config.draw_offset_y

        if self.character.face_dir == 1:
            self.character.image.clip_draw(l, b, w, h, self.character.x, draw_y, draw_w, draw_h)
        else:
            self.character.image.clip_composite_draw(l, b, w, h, 0.0, 'h',
                                                  self.character.x, draw_y, draw_w, draw_h)

    def get_bb(self):
        all_frames = self.character.config.frames
        frame = all_frames[self.character.frame]

        hb = self.character.config.hitbox_jump
        hw = frame['width'] * self.character.config.scale_x * hb['scale_x'] / 2
        hh = frame['height'] * self.character.config.scale_y * hb['scale_y'] / 2
        return (
            self.character.x - hw + hb['x_offset'],
            self.character.y - hh + hb['y_offset'],
            self.character.x + hw + hb['x_offset'],
            self.character.y + hh + hb['y_offset']
        )

    def draw_bb(self):
        # 디버그용: 바운딩 박스를 화면에 그리기
        left, bottom, right, top = self.get_bb()
        draw_rectangle(left, bottom, right, top)
