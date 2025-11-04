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
        draw_w = int(w * self.character.config.scale_x)
        draw_h = int(h * self.character.config.scale_y)
        draw_y = self.character.y + self.character.config.draw_offset_y

        if self.character.face_dir == 1:
            self.character.image.clip_draw(l, b, w, h, self.character.x, draw_y, draw_w, draw_h)
        else:
            self.character.image.clip_composite_draw(l, b, w, h, 0.0, 'h',
                                                  self.character.x, draw_y, draw_w, draw_h)

    def get_bb(self):
        run_frames = self.character.config.run_frames
        all_frames = self.character.config.frames
        frame_idx = run_frames[self.character.frame]
        frame = all_frames[frame_idx]

        hb = self.character.config.hitbox_run
        hw = frame['width'] * self.character.config.scale_x * hb['scale_x'] / 2
        hh = frame['height'] * self.character.config.scale_y * hb['scale_y'] / 2
        return (
            self.character.x - hw + hb['x_offset'],
            self.character.y - hh + hb['y_offset'],
            self.character.x + hw + hb['x_offset'],
            self.character.y + hh + hb['y_offset']
        )

    def draw_bb(self):
        # 디버그용: 바운딩 박스를 화면에 그리기
        left, bottom, right, top = self.get_bb()
        draw_rectangle(left, bottom, right, top)