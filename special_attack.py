from characters_naruto_frames import FRAMES

SPECIAL_ATTACK_FRAMES = [FRAMES[i] for i in range(98, 136)]ㅁㄴ

class Special_Attack:
    def __init__(self, naruto):
        self.naruto = naruto

    def enter(self, e):
        self.naruto.accum_time = 0.0
        self.naruto.frame_duration = 0.15
        self.naruto.frame = 0

    def exit(self, e):
        pass

    def do(self, dt):
        self.naruto.accum_time += dt
        if self.naruto.accum_time >= self.naruto.frame_duration:
            self.naruto.accum_time -= self.naruto.frame_duration
            if self.naruto.frame < len(SPECIAL_ATTACK_FRAMES) - 1:
                self.naruto.frame += 1
            else:
                # 애니메이션이 끝나면 IDLE로 복귀
                self.naruto.state_machine.handle_event(('SPECIAL_ATTACK_END', None))

    def draw(self):
        frame = SPECIAL_ATTACK_FRAMES[self.naruto.frame]
        l, b, w, h = frame['left'], frame['bottom'], frame['width'], frame['height']

        if self.naruto.face_dir == 1:
            self.naruto.image.clip_draw(l, b, w, h, self.naruto.x, self.naruto.y)
        else:
            self.naruto.image.clip_composite_draw(l, b, w, h, 0.0, 'h',
                                                  self.naruto.x, self.naruto.y, w, h)
