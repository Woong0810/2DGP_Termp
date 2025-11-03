from characters_naruto_frames import FRAMES
from pico2d import draw_rectangle

SPECIAL_ATTACK_FRAMES = [FRAMES[i] for i in range(98, 136)]

class Special_Attack:
    def __init__(self, naruto):
        self.naruto = naruto
        self.loop_count = 0  # 마지막 4프레임 반복 횟수

    def enter(self, e):
        self.naruto.accum_time = 0.0
        self.naruto.frame_duration = 0.15
        self.naruto.frame = 0
        self.loop_count = 0

    def exit(self, e):
        pass

    def do(self, dt):
        self.naruto.accum_time += dt
        if self.naruto.accum_time >= self.naruto.frame_duration:
            self.naruto.accum_time -= self.naruto.frame_duration

            last_4_start = len(SPECIAL_ATTACK_FRAMES) - 4
            skip_before_last_4 = last_4_start - 3 # 프레임 3개 안쓰고 싶음

            if self.naruto.frame < skip_before_last_4 - 1:
                self.naruto.frame += 1
            elif self.naruto.frame == skip_before_last_4 - 1:
                self.naruto.frame = last_4_start
            elif self.naruto.frame < len(SPECIAL_ATTACK_FRAMES) - 1:
                # 마지막 4프레임 구간: 진행
                self.naruto.frame += 1
            else:
                # 마지막 프레임에 도달
                if self.loop_count < 3:
                    self.naruto.frame = last_4_start
                    self.loop_count += 1
                else:
                    # 반복 완료: IDLE로 복귀
                    self.naruto.state_machine.handle_event(('SPECIAL_ATTACK_END', None))

    def draw(self):
        frame = SPECIAL_ATTACK_FRAMES[self.naruto.frame]
        l, b, w, h = frame['left'], frame['bottom'], frame['width'], frame['height']

        if self.naruto.face_dir == 1:
            self.naruto.image.clip_draw(l, b, w, h, self.naruto.x, self.naruto.y)
        else:
            self.naruto.image.clip_composite_draw(l, b, w, h, 0.0, 'h',
                                                  self.naruto.x, self.naruto.y, w, h)

    def get_bb(self, scale_x=1.2, scale_y=1.2, x_offset=0, y_offset=0):
        frame = SPECIAL_ATTACK_FRAMES[self.naruto.frame]
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
