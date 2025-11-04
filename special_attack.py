from pico2d import draw_rectangle

class SpecialAttack:
    def __init__(self, character):
        self.character = character
        self.loop_count = 0  # 마지막 4프레임 반복 횟수

    def enter(self, e):
        self.character.accum_time = 0.0
        self.character.frame_duration = 0.15
        self.character.frame = 0
        self.loop_count = 0

    def exit(self, e):
        pass

    def do(self, dt):
        self.character.accum_time += dt
        if self.character.accum_time >= self.character.frame_duration:
            self.character.accum_time -= self.character.frame_duration

            special_frames = self.character.config.special_attack_frames
            last_4_start = len(special_frames) - 4
            skip_before_last_4 = last_4_start - 3

            if self.character.frame < skip_before_last_4 - 1:
                self.character.frame += 1
            elif self.character.frame == skip_before_last_4 - 1:
                self.character.frame = last_4_start
            elif self.character.frame < len(special_frames) - 1:
                # 마지막 4프레임 구간: 진행
                self.character.frame += 1
            else:
                # 마지막 프레임에 도달
                if self.loop_count < 3:
                    self.character.frame = last_4_start
                    self.loop_count += 1
                else:
                    # 반복 완료: IDLE로 복귀
                    self.character.state_machine.handle_event(('SPECIAL_ATTACK_END', None))

    def draw(self):
        special_attack_frames = self.character.config.special_attack_frames
        all_frames = self.character.config.frames
        frame_idx = special_attack_frames[self.character.frame]
        frame = all_frames[frame_idx]

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
        # 120번 프레임부터만 히트박스 설정
        if self.character.frame >= 120:
            special_attack_frames = self.character.config.special_attack_frames
            all_frames = self.character.config.frames
            frame_idx = special_attack_frames[self.character.frame]
            frame = all_frames[frame_idx]

            hb = self.character.config.hitbox_special_attack
            hw = frame['width'] * self.character.config.scale_x * hb['scale_x'] / 2
            hh = frame['height'] * self.character.config.scale_y * hb['scale_y'] / 2
            return (
                self.character.x - hw + hb['x_offset'],
                self.character.y - hh + hb['y_offset'],
                self.character.x + hw + hb['x_offset'],
                self.character.y + hh + hb['y_offset']
            )
        return (0, 0, 0, 0)  # 히트박스 없음

    def draw_bb(self):
        # 디버그용: 바운딩 박스를 화면에 그리기
        left, bottom, right, top = self.get_bb()
        draw_rectangle(left, bottom, right, top)
