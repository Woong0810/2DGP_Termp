from event_to_string import up_down, n_down, n_up
from pico2d import draw_rectangle

class NormalAttack:
    def __init__(self, character):
        self.character = character
        self.combo_index = 0
        self.start_frame = 0
        self.end_frame = 0
        self.cur = 0
        self.n_key_pressed = False  # N키 눌림 상태 추적

    def enter(self, e):
        # 새로운 세그먼트 시작
        segments = self.character.config.normal_attack_segments
        self.start_frame, self.end_frame = segments[self.combo_index]
        self.cur = self.start_frame
        self.character.frame = self.cur
        self.character.accum_time = 0.0
        self.character.frame_duration = 0.13
        # n_down 이벤트로 진입했으면 N키가 눌려있음
        if n_down(e):
            self.n_key_pressed = True

    def exit(self, e):
        # SEGMENT_END로 exit되면 콤보 초기화
        if not n_down(e):
            self.combo_index = 0
        self.n_key_pressed = False

    def do(self, dt):
        self.character.accum_time += dt
        if self.character.accum_time >= self.character.frame_duration:
            self.character.accum_time -= self.character.frame_duration
            if self.cur < self.end_frame:
                self.cur += 1
                self.character.frame = self.cur
            else:
                # 세그먼트 재생 완료 - N키가 눌려있는지 확인
                if self.n_key_pressed:
                    # N키가 눌려있으면 다음 콤보로
                    self.combo_index = (self.combo_index + 1) % 3
                    self.enter(('COMBO_CONTINUE', None))
                else:
                    # N키가 안 눌려있으면 IDLE로 복귀
                    self.character.state_machine.handle_event(('SEGMENT_END', None))

    def handle_n_key_down(self):
        self.n_key_pressed = True

    def handle_n_key_up(self):
        self.n_key_pressed = False

    def draw(self):
        attack_frames = self.character.config.normal_attack_frames
        all_frames = self.character.config.frames
        frame_idx = attack_frames[self.character.frame]
        frame = all_frames[frame_idx]

        l, b, w, h = frame['left'], frame['bottom'], frame['width'], frame['height']

        if self.character.face_dir == 1:
            self.character.image.clip_draw(l, b, w, h, self.character.x, self.character.y)
        else:
            self.character.image.clip_composite_draw(l, b, w, h, 0.0, 'h',
                                                  self.character.x, self.character.y, w, h)

    def get_bb(self, scale_x=0.7, scale_y=0.8, x_offset=0, y_offset=0):
        attack_frames = self.character.config.normal_attack_frames
        all_frames = self.character.config.frames
        frame_idx = attack_frames[self.character.frame]
        frame = all_frames[frame_idx]

        hw = frame['width'] * scale_x / 2
        hh = frame['height'] * scale_y / 2
        return (
            self.character.x - hw + x_offset,  # left
            self.character.y - hh + y_offset,  # bottom
            self.character.x + hw + x_offset,  # right
            self.character.y + hh + y_offset   # top
        )

    def draw_bb(self):
        # 디버그용: 바운딩 박스를 화면에 그리기
        left, bottom, right, top = self.get_bb()
        draw_rectangle(left, bottom, right, top)
