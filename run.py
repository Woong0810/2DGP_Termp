from event_to_string import right_down, right_up, left_down, left_up
from pico2d import draw_rectangle

class Run:
    def __init__(self, character):
        self.character = character

    def enter(self, e):
        self.character.accum_time = 0.0
        self.character.frame_duration = 0.04
        self.character.frame = 0
        if right_down(e) or left_up(e):
            self.character.dir = self.character.face_dir = 1
        elif left_down(e) or right_up(e):
            self.character.dir = self.character.face_dir = -1

    def exit(self, e):
        pass

    def do(self, dt):
        self.character.accum_time += dt
        if self.character.accum_time >= self.character.frame_duration:
            self.character.accum_time -= self.character.frame_duration
            run_frames = self.character.config.run_frames
            self.character.frame = (self.character.frame + 1) % len(run_frames)
            self.character.x += 10 * self.character.dir

    def draw(self):
        run_frames = self.character.config.run_frames
        all_frames = self.character.config.frames
        frame_idx = run_frames[self.character.frame]
        frame = all_frames[frame_idx]

        l, b, w, h = frame['left'], frame['bottom'], frame['width'], frame['height']

        if self.character.face_dir == 1:
            self.character.image.clip_draw(l, b, w, h, self.character.x, self.character.y)
        else:
            self.character.image.clip_composite_draw(l, b, w, h, 0.0, 'h',
                                                  self.character.x, self.character.y, w, h)

    def get_bb(self, scale_x=0.7, scale_y=0.8, x_offset=0, y_offset=0):
        run_frames = self.character.config.run_frames
        all_frames = self.character.config.frames
        frame_idx = run_frames[self.character.frame]
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