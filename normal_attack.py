from event_to_string import up_down, n_down
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
        self.next_combo_requested = False  # 다음 콤보 예약 플래그

    def enter(self, e):
        # 새로운 세그먼트 시작
        self.start_frame, self.end_frame = SEGMENTS[self.combo_index]
        self.cur = self.start_frame
        self.naruto.frame = self.cur
        self.naruto.accum_time = 0.0
        self.naruto.frame_duration = 0.13
        self.next_combo_requested = False  # 플래그 초기화

    def exit(self, e):
        # SEGMENT_END로 exit되면 콤보 초기화
        if not n_down(e):
            self.combo_index = 0

    def do(self, dt):
        self.naruto.accum_time += dt
        if self.naruto.accum_time >= self.naruto.frame_duration:
            self.naruto.accum_time -= self.naruto.frame_duration
            if self.cur < self.end_frame:
                self.cur += 1
                self.naruto.frame = self.cur
            else:
                # 세그먼트 재생 완료
                if self.next_combo_requested:
                    # 다음 콤보 요청이 있으면 콤보 증가 후 재시작
                    self.combo_index = (self.combo_index + 1) % 3
                    self.next_combo_requested = False
                    # 다시 enter 호출 (새 세그먼트 시작)
                    self.enter(('COMBO_CONTINUE', None))
                else:
                    # 아무 입력 없으면 IDLE로 복귀
                    self.naruto.state_machine.handle_event(('SEGMENT_END', None))

    def request_next_combo(self):
        """N키가 눌렸을 때 다음 콤보 예약"""
        self.next_combo_requested = True

    def draw(self):
        frame = NORMAL_ATTACK_FRAME[self.naruto.frame]
        l, b, w, h = frame['left'], frame['bottom'], frame['width'], frame['height']

        if self.naruto.face_dir == 1:
            self.naruto.image.clip_draw(l, b, w, h, self.naruto.x, self.naruto.y)
        else:
            self.naruto.image.clip_composite_draw(l, b, w, h, 0.0, 'h',
                                                  self.naruto.x, self.naruto.y, w, h)
