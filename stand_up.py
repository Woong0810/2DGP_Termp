from pico2d import draw_rectangle
from character_config import ACTION_PER_TIME, STAND_UP_ANIMATION_SPEED
import game_framework
from camera import camera

class StandUp:
    def __init__(self, character):
        self.character = character

    def enter(self, event):
        self.character.frame = 0

    def exit(self, event):
        if event and event[0] == 'STAND_UP_END':
            self.character.invincible_time = 0.5

    def do(self):
        stand_up_frames = self.character.config.stand_up_frames
        frames_per_action = len(stand_up_frames)

        self.character.frame += frames_per_action * ACTION_PER_TIME * STAND_UP_ANIMATION_SPEED * game_framework.frame_time

        if self.character.frame >= frames_per_action:
            self.character.state_machine.add_event(('STAND_UP_END', 0))

    def draw(self):
        stand_up_frames = self.character.config.stand_up_frames
        all_frames = self.character.config.frames

        current_idx = min(int(self.character.frame), len(stand_up_frames) - 1)
        frame_idx = stand_up_frames[current_idx]
        frame = all_frames[frame_idx]

        l, b, w, h = frame['left'], frame['bottom'], frame['width'], frame['height']
        draw_w = int(w * self.character.config.scale_x)
        draw_h = int(h * self.character.config.scale_y)

        world_y = self.character.y + self.character.config.draw_offset_y
        sx, sy = camera.world_to_screen(self.character.x, world_y)

        if self.character.face_dir == 1:
            self.character.image.clip_draw(l, b, w, h, sx, sy, draw_w, draw_h)
        else:
            self.character.image.clip_composite_draw(l, b, w, h, 0, 'h', sx, sy, draw_w, draw_h)
        left, bottom, right, top = self.get_bb()
        sx1, sy1 = camera.world_to_screen(left, bottom)
        sx2, sy2 = camera.world_to_screen(right, top)
        draw_rectangle(sx1, sy1, sx2, sy2)

    def get_bb(self):
        stand_up_frames = self.character.config.stand_up_frames
        all_frames = self.character.config.frames

        current_idx = min(int(self.character.frame), len(stand_up_frames) - 1)
        frame_idx = stand_up_frames[current_idx]
        frame = all_frames[frame_idx]

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

