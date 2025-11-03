from pico2d import draw_rectangle

class Idle:
    def __init__(self, character):
        self.character = character

    def enter(self, e):
        self.character.accum_time = 0.0
        self.character.frame_duration = 0.1
        self.character.frame = 0

    def exit(self, e):
        pass

    def do(self, dt):
        self.character.accum_time += dt
        if self.character.accum_time >= self.character.frame_duration:
            self.character.accum_time -= self.character.frame_duration
            idle_frames = self.character.config.idle_frames
            self.character.frame = (self.character.frame + 1) % len(idle_frames)

    def draw(self):
        idle_frames = self.character.config.idle_frames
        all_frames = self.character.config.frames
        frame_idx = idle_frames[self.character.frame]
        frame = all_frames[frame_idx]

        l, b, w, h = frame['left'], frame['bottom'], frame['width'], frame['height']

        if self.character.face_dir == 1:
            self.character.image.clip_draw(l, b, w, h, self.character.x, self.character.y)
        else:
            self.character.image.clip_composite_draw(l, b, w, h, 0.0, 'h',
                                                  self.character.x, self.character.y, w, h)

    def get_bb(self):
        idle_frames = self.character.config.idle_frames
        all_frames = self.character.config.frames
        frame_idx = idle_frames[self.character.frame]
        frame = all_frames[frame_idx]

        # 캐릭터 설정에서 히트박스 정보 가져오기
        hb = self.character.config.hitbox_idle
        hw = frame['width'] * hb['scale_x'] / 2
        hh = frame['height'] * hb['scale_y'] / 2
        return (
            self.character.x - hw + hb['x_offset'],  # left
            self.character.y - hh + hb['y_offset'],  # bottom
            self.character.x + hw + hb['x_offset'],  # right
            self.character.y + hh + hb['y_offset']   # top
        )

    def draw_bb(self):
        # 디버그용: 바운딩 박스를 화면에 그리기
        left, bottom, right, top = self.get_bb()
        draw_rectangle(left, bottom, right, top)
