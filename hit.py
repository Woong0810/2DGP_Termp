from pico2d import draw_rectangle
from character_config import ACTION_PER_TIME, HIT_ANIMATION_SPEED, HIT_DURATION
import game_framework

class Hit:
    def __init__(self, character):
        self.character = character
        self.elapsed_time = 0.0

    def enter(self, event):
        self.character.frame = 0
        self.elapsed_time = 0.0

    def exit(self, event):
        pass

    def do(self):
        self.elapsed_time += game_framework.frame_time

        # 수업 방식: game_framework.frame_time 사용
        self.character.frame = (self.character.frame + 2 * ACTION_PER_TIME * HIT_ANIMATION_SPEED * game_framework.frame_time) % 2

        if self.elapsed_time >= HIT_DURATION:
            from event_to_string import hit_end
            self.character.state_machine.add_event(('HIT_END', 0))

    def draw(self):
        HIT_FRAMES = [self.character.config.frames[idx] for idx in self.character.config.hit_frames]
        frame = HIT_FRAMES[int(self.character.frame)]

        l, b, w, h = frame['left'], frame['bottom'], frame['width'], frame['height']
        draw_w = int(w * self.character.config.scale_x)
        draw_h = int(h * self.character.config.scale_y)
        draw_y = self.character.y + self.character.config.draw_offset_y

        if self.character.face_dir == 1:
            self.character.image.clip_draw(l, b, w, h, self.character.x, draw_y, draw_w, draw_h)
        else:
            self.character.image.clip_composite_draw(l, b, w, h, 0, 'h',
                                                      self.character.x, draw_y, draw_w, draw_h)

    def get_bb(self):
        frame = self.character.config.frames[self.character.config.hit_frames[int(self.character.frame)]]  # int로 변환
        hitbox = self.character.config.hitbox_hit

        width = frame['width'] * self.character.config.scale_x * hitbox['scale_x']
        height = frame['height'] * self.character.config.scale_y * hitbox['scale_y']
        x_offset = hitbox['x_offset'] * self.character.face_dir
        y_offset = hitbox['y_offset']

        return (
            self.character.x - width / 2 + x_offset,
            self.character.y - height / 2 + y_offset,
            self.character.x + width / 2 + x_offset,
            self.character.y + height / 2 + y_offset
        )

    def draw_bb(self):
        """디버그용 바운딩 박스 그리기"""
        left, bottom, right, top = self.get_bb()
        draw_rectangle(left, bottom, right, top)
