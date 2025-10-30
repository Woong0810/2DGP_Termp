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
        self.segment_playing = False  # 세그먼트 재생 중인지 여부
        self.next_combo_requested = False  # 재생 중 다음 콤보 요청 여부

    def enter(self, e):
        # n키를 눌렀을 때 새로운 세그먼트 시작
        if n_down(e):
            self.start_segment()
        else:
            # 이전 콤보에서 이어서 재생
            self.start_segment()

    def start_segment(self):
        self.start_frame, self.end_frame = SEGMENTS[self.combo_index]
        self.cur = self.start_frame
        self.naruto.frame = self.cur
        self.naruto.accum_time = 0.0
        self.naruto.frame_duration = 0.13
        self.segment_playing = True
        self.next_combo_requested = False

    def exit(self, e):
        if up_down(e):
            self.naruto.jump_action()

    def do(self, dt):
        if self.naruto.JUMP.active:
            return

        if not self.segment_playing:
            return

        self.naruto.accum_time += dt
        if self.naruto.accum_time >= self.naruto.frame_duration:
            self.naruto.accum_time -= self.naruto.frame_duration
            if self.cur < self.end_frame:
                self.cur += 1
                self.naruto.frame = self.cur
            else:
                # 세그먼트 재생 완료
                self.segment_playing = False

                if self.next_combo_requested:
                    # 재생 중 n키가 눌렸다면 다음 콤보로
                    self.combo_index = (self.combo_index + 1) % len(SEGMENTS)
                    self.start_segment()
                else:
                    self.combo_index = 0  # 콤보 초기화
                    self.naruto.state_machine.add_event(('SEGMENT_END', None))

    def handle_n_key(self):
        if self.segment_playing:
            # 세그먼트 재생 중이면 다음 콤보 예약
            self.next_combo_requested = True
        else:
            self.combo_index = (self.combo_index + 1) % len(SEGMENTS)
            self.start_segment()

    def draw(self):
        frame = NORMAL_ATTACK_FRAME[self.naruto.frame]
        l, b, w, h = frame['left'], frame['bottom'], frame['width'], frame['height']

        if self.naruto.face_dir == 1:
            self.naruto.image.clip_draw(l, b, w, h, self.naruto.x, self.naruto.y)
        else:
            self.naruto.image.clip_composite_draw(l, b, w, h, 0.0, 'h',
                                                  self.naruto.x, self.naruto.y, w, h)
