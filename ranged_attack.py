from pico2d import draw_rectangle

class RangedAttack:
    def __init__(self, character):
        self.character = character
        self.phase = 0  # 0: 캐릭터 애니메이션, 1: 이펙트 애니메이션
        self.effect_x = 0
        self.effect_y = 0
        self.effect_frame = 0
        self.effect_accum_time = 0.0
        self.target_x = 0
        self.target_y = 0

    def enter(self, e):
        # 상대 캐릭터가 없으면 attack이 안됨
        if not self.character.opponent:
            self.character.state_machine.handle_event(('RANGED_ATTACK_END', None))
            return

        self.character.accum_time = 0.0
        self.character.frame_duration = 0.15
        self.character.frame = 0
        self.phase = 0

        self.target_x = self.character.opponent.x
        self.target_y = self.character.opponent.y

        self.effect_x = self.target_x
        self.effect_y = self.target_y - 20

        self.effect_frame = 0
        self.effect_accum_time = 0.0

    def exit(self, e):
        pass

    def do(self, dt):
        char_frames = self.character.config.ranged_attack_char_frames
        effect_frames = self.character.config.ranged_attack_effect_frames

        if self.phase == 0:
            # 캐릭터 애니메이션
            self.character.accum_time += dt
            if self.character.accum_time >= self.character.frame_duration:
                self.character.accum_time -= self.character.frame_duration
                if self.character.frame < len(char_frames) - 1:
                    self.character.frame += 1
                else:
                    # 캐릭터 애니메이션 끝 -> 이펙트 페이즈로
                    self.phase = 1
                    self.effect_frame = 0
                    self.effect_accum_time = 0.0

        elif self.phase == 1:
            # 이펙트 애니메이션
            self.effect_accum_time += dt
            if self.effect_accum_time >= 0.1:  # 이펙트는 좀 더 빠르게
                self.effect_accum_time -= 0.1
                if self.effect_frame < len(effect_frames) - 1:
                    self.effect_frame += 1
                    self.effect_y += 5  # 프레임이 증가할 때마다 y값 5씩 증가
                else:
                    # 이펙트 애니메이션 끝 -> 목표 위치로 이동하고 IDLE로 복귀
                    self.character.x = self.target_x
                    self.character.y = self.target_y
                    self.character.state_machine.handle_event(('RANGED_ATTACK_END', None))

    def draw(self):
        char_frames = self.character.config.ranged_attack_char_frames
        effect_frames = self.character.config.ranged_attack_effect_frames
        all_frames = self.character.config.frames

        # 캐릭터 그리기
        if self.phase == 0:
            frame_idx = char_frames[self.character.frame]
        else:
            # 이동 중에는 마지막 프레임 유지
            frame_idx = char_frames[-1]

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

        # 이펙트 그리기 (phase 1일 때만)
        if self.phase == 1:
            effect_frame_idx = effect_frames[self.effect_frame]
            effect_frame = all_frames[effect_frame_idx]
            el, eb, ew, eh = effect_frame['left'], effect_frame['bottom'], effect_frame['width'], effect_frame['height']
            effect_draw_w = int(ew * self.character.config.scale_x)
            effect_draw_h = int(eh * self.character.config.scale_y)

            if self.character.face_dir == 1:
                self.character.image.clip_draw(el, eb, ew, eh, self.effect_x, self.effect_y, effect_draw_w, effect_draw_h)
            else:
                self.character.image.clip_composite_draw(el, eb, ew, eh, 0.0, 'h',
                                                      self.effect_x, self.effect_y, effect_draw_w, effect_draw_h)

    def get_bb(self):
        char_frames = self.character.config.ranged_attack_char_frames
        effect_frames = self.character.config.ranged_attack_effect_frames
        all_frames = self.character.config.frames
        hb = self.character.config.hitbox_ranged_attack

        if self.phase == 0:
            # phase 0: 첫 번째 프레임만 히트박스 있음
            if self.character.frame == 0:
                frame_idx = char_frames[0]
                frame = all_frames[frame_idx]
                hw = frame['width'] * self.character.config.scale_x * hb['scale_x'] / 2
                hh = frame['height'] * self.character.config.scale_y * hb['scale_y'] / 2
                return (
                    self.character.x - hw + hb['x_offset'],
                    self.character.y - hh + hb['y_offset'],
                    self.character.x + hw + hb['x_offset'],
                    self.character.y + hh + hb['y_offset']
                )
            else:
                return (0, 0, 0, 0)

        elif self.phase == 1:
            # phase 1: 이펙트의 히트박스
            frame_idx = effect_frames[self.effect_frame]
            frame = all_frames[frame_idx]
            hw = frame['width'] * self.character.config.scale_x * hb['scale_x'] / 2
            hh = frame['height'] * self.character.config.scale_y * hb['scale_y'] / 2
            return (
                self.effect_x - hw + hb['x_offset'],
                self.effect_y - hh + hb['y_offset'],
                self.effect_x + hw + hb['x_offset'],
                self.effect_y + hh + hb['y_offset']
            )
        return (0, 0, 0, 0)
    def draw_bb(self):
        left, bottom, right, top = self.get_bb()
        draw_rectangle(left, bottom, right, top)
