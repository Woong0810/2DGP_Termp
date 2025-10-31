from characters_naruto_frames import FRAMES

CHARACTER_RANGED_FRAMES = [FRAMES[i] for i in range(91, 97)]
EFFECT_RANGED_FRAMES = [FRAMES[i] for i in range(67, 71)]

class RangedAttack:
    def __init__(self, naruto):
        self.naruto = naruto
        self.phase = 0  # 0: 캐릭터 애니메이션, 1: 이펙트 애니메이션, 2: 이동
        self.effect_x = 0
        self.effect_y = 0
        self.effect_frame = 0
        self.effect_accum_time = 0.0
        self.target_x = 0
        self.target_y = 0

    def enter(self, e):
        self.naruto.accum_time = 0.0
        self.naruto.frame_duration = 0.15
        self.naruto.frame = 0
        self.phase = 0

        # 목표 위치 설정 (일단 오른쪽으로 300픽셀 떨어진 곳)
        self.target_x = self.naruto.x + (300 if self.naruto.face_dir == 1 else -300)
        self.target_y = self.naruto.y

        # 이펙트 위치 설정 (목표 위치에서 약간 위)
        self.effect_x = self.target_x
        self.effect_y = self.target_y - 20
        self.effect_frame = 0
        self.effect_accum_time = 0.0

    def exit(self, e):
        pass

    def do(self, dt):
        if self.phase == 0:
            # 캐릭터 애니메이션 (91-97)
            self.naruto.accum_time += dt
            if self.naruto.accum_time >= self.naruto.frame_duration:
                self.naruto.accum_time -= self.naruto.frame_duration
                if self.naruto.frame < len(CHARACTER_RANGED_FRAMES) - 1:
                    self.naruto.frame += 1
                else:
                    # 캐릭터 애니메이션 끝 -> 이펙트 페이즈로
                    self.phase = 1
                    self.effect_frame = 0
                    self.effect_accum_time = 0.0

        elif self.phase == 1:
            # 이펙트 애니메이션 (67-71)
            self.effect_accum_time += dt
            if self.effect_accum_time >= 0.1:  # 이펙트는 좀 더 빠르게
                self.effect_accum_time -= 0.1
                if self.effect_frame < len(EFFECT_RANGED_FRAMES) - 1:
                    self.effect_frame += 1
                    self.effect_y += 5  # 프레임이 증가할 때마다 y값 5씩 증가
                else:
                    # 이펙트 애니메이션 끝 -> 이동 페이즈로
                    self.phase = 2

        elif self.phase == 2:
            # 캐릭터를 목표 위치로 순간 이동
            self.naruto.x = self.target_x
            self.naruto.y = self.target_y
            # IDLE로 복귀
            self.naruto.state_machine.handle_event(('RANGED_ATTACK_END', None))

    def draw(self):
        # 캐릭터 그리기
        if self.phase == 0:
            frame = CHARACTER_RANGED_FRAMES[self.naruto.frame]
        else:
            # 이동 중에는 마지막 프레임 유지
            frame = CHARACTER_RANGED_FRAMES[-1]

        l, b, w, h = frame['left'], frame['bottom'], frame['width'], frame['height']
        if self.naruto.face_dir == 1:
            self.naruto.image.clip_draw(l, b, w, h, self.naruto.x, self.naruto.y)
        else:
            self.naruto.image.clip_composite_draw(l, b, w, h, 0.0, 'h',
                                                  self.naruto.x, self.naruto.y, w, h)

        # 이펙트 그리기 (phase 1일 때만)
        if self.phase == 1:
            effect_frame = EFFECT_RANGED_FRAMES[self.effect_frame]
            el, eb, ew, eh = effect_frame['left'], effect_frame['bottom'], effect_frame['width'], effect_frame['height']
            if self.naruto.face_dir == 1:
                self.naruto.image.clip_draw(el, eb, ew, eh, self.effect_x, self.effect_y)
            else:
                self.naruto.image.clip_composite_draw(el, eb, ew, eh, 0.0, 'h',
                                                      self.effect_x, self.effect_y, ew, eh)
