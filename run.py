from event_to_string import right_down, right_up, left_down, left_up
from pico2d import draw_rectangle
from character_config import RUN_SPEED_PPS, ACTION_PER_TIME, RUN_ANIMATION_SPEED
import game_framework

class Run:
    def __init__(self, character):
        self.character = character

    def enter(self, e):
        self.character.frame = 0
        if right_down(e) or left_up(e):
            self.character.dir = self.character.face_dir = 1
        elif left_down(e) or right_up(e):
            self.character.dir = self.character.face_dir = -1

    def exit(self, e):
        pass

    def do(self):
        self.character.x += RUN_SPEED_PPS * game_framework.frame_time * self.character.dir

        run_frames = self.character.config.run_frames
        frames_per_action = len(run_frames)
        self.character.frame = (self.character.frame + frames_per_action * ACTION_PER_TIME * RUN_ANIMATION_SPEED * game_framework.frame_time) % frames_per_action

    def draw(self):
        run_frames = self.character.config.run_frames
        all_frames = self.character.config.frames
        frame_idx = run_frames[int(self.character.frame)]  # int로 변환
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
        frame_idx = run_frames[int(self.character.frame)]  # int로 변환
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