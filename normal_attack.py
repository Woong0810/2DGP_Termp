from event_to_string import up_down, n_down, n_up
from characters_naruto_frames import FRAMES
from pico2d import draw_rectangle

NORMAL_ATTACK_FRAME = [FRAMES[i] for i in range(0, 12)]
SEGMENTS = [(0, 3), (4, 7), (8, 11)]

class NormalAttack:
    def __init__(self, naruto):
        self.naruto = naruto
        self.combo_index = 0
        self.start_frame = 0
        self.end_frame = 0
        self.cur = 0
        self.n_key_pressed = False  # N키 눌림 상태 추적

    def enter(self, e):
        # 새로운 세그먼트 시작
        self.start_frame, self.end_frame = SEGMENTS[self.combo_index]
        self.cur = self.start_frame
        self.naruto.frame = self.cur
        self.naruto.accum_time = 0.0
        self.naruto.frame_duration = 0.13
        # n_down 이벤트로 진입했으면 N키가 눌려있음
        if n_down(e):
            self.n_key_pressed = True

    def exit(self, e):
        # SEGMENT_END로 exit되면 콤보 초기화
        if not n_down(e):
            self.combo_index = 0
        self.n_key_pressed = False

    def do(self, dt):
        self.naruto.accum_time += dt
        if self.naruto.accum_time >= self.naruto.frame_duration:
            self.naruto.accum_time -= self.naruto.frame_duration
            if self.cur < self.end_frame:
                self.cur += 1
                self.naruto.frame = self.cur
            else:
                # 세그먼트 재생 완료 - N키가 눌려있는지 확인
                if self.n_key_pressed:
                    # N키가 눌려있으면 다음 콤보로
                    self.combo_index = (self.combo_index + 1) % 3
                    self.enter(('COMBO_CONTINUE', None))
                else:
                    # N키가 안 눌려있으면 IDLE로 복귀
                    self.naruto.state_machine.handle_event(('SEGMENT_END', None))

    def handle_n_key_down(self):
        self.n_key_pressed = True

    def handle_n_key_up(self):
        self.n_key_pressed = False

    def draw(self):
        frame = NORMAL_ATTACK_FRAME[self.naruto.frame]
        l, b, w, h = frame['left'], frame['bottom'], frame['width'], frame['height']

        if self.naruto.face_dir == 1:
            self.naruto.image.clip_draw(l, b, w, h, self.naruto.x, self.naruto.y)
        else:
            self.naruto.image.clip_composite_draw(l, b, w, h, 0.0, 'h',
                                                  self.naruto.x, self.naruto.y, w, h)

    def get_bb(self, scale_x=0.7, scale_y=0.8, x_offset=0, y_offset=0):
        frame = NORMAL_ATTACK_FRAME[self.naruto.frame]
        hw = frame['width'] * scale_x / 2
        hh = frame['height'] * scale_y / 2
        return (
            self.naruto.x - hw + x_offset,  # left
            self.naruto.y - hh + y_offset,  # bottom
            self.naruto.x + hw + x_offset,  # right
            self.naruto.y + hh + y_offset   # top
        )

    def draw_bb(self):
        # 디버그용: 바운딩 박스를 화면에 그리기
        left, bottom, right, top = self.get_bb()
        draw_rectangle(left, bottom, right, top)
