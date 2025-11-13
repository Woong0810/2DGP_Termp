from pico2d import draw_rectangle
from character_config import ACTION_PER_TIME, RANGED_ATTACK_CHAR_ANIMATION_SPEED
import game_framework
from shuriken import Shuriken
import game_world

class RangedAttack:
    def __init__(self, character):
        self.character = character
        self.shuriken_spawned = False

    def enter(self, e):
        self.character.frame = 0
        self.shuriken_spawned = False

    def exit(self, e):
        pass

    def do(self):
        frames = self.character.config.ranged_attack_frames

        if not frames:
            self.character.state_machine.handle_event(('RANGED_ATTACK_END', None))
            return

        self.character.frame += len(frames) * ACTION_PER_TIME * RANGED_ATTACK_CHAR_ANIMATION_SPEED * game_framework.frame_time

        if not self.shuriken_spawned and self.character.frame >= len(frames) / 2:
            self.spawn_shuriken()
            self.shuriken_spawned = True

        if self.character.frame >= len(frames):
            self.character.state_machine.handle_event(('RANGED_ATTACK_END', None))

    def spawn_shuriken(self):
        offset_x = 30 * self.character.face_dir
        shuriken = Shuriken(
            self.character,
            self.character.x + offset_x,
            self.character.y + 20,
            self.character.face_dir
        )
        game_world.add_object(shuriken, 1)

    def draw(self):
        frames = self.character.config.ranged_attack_frames
        all_frames = self.character.config.frames

        if not frames:
            return

        current_frame = max(0, min(int(self.character.frame), len(frames) - 1))
        frame_idx = frames[current_frame]

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

        draw_rectangle(*self.get_bb())

    def get_bb(self):
        frames = self.character.config.ranged_attack_frames
        all_frames = self.character.config.frames

        if not frames:
            return (0, 0, 0, 0)

        current_frame = max(0, min(int(self.character.frame), len(frames) - 1))
        frame_idx = frames[current_frame]
        frame = all_frames[frame_idx]

        hb = self.character.config.hitbox_ranged_attack
        hw = frame['width'] * self.character.config.scale_x * hb['scale_x'] / 2
        hh = frame['height'] * self.character.config.scale_y * hb['scale_y'] / 2
        return (
            self.character.x - hw + hb['x_offset'],
            self.character.y - hh + hb['y_offset'],
            self.character.x + hw + hb['x_offset'],
            self.character.y + hh + hb['y_offset']
        )

    def handle_collision(self, group, other):
        pass
