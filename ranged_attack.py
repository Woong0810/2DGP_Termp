from pico2d import draw_rectangle
from character_config import ACTION_PER_TIME, RANGED_ATTACK_CHAR_ANIMATION_SPEED
import game_framework
from shuriken import Shuriken
import game_world
from camera import camera

class RangedAttack:
    def __init__(self, character):
        self.character = character
        self.shuriken_spawned = False
        self.shuriken = None

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
        offset_x = 20 * self.character.face_dir
        self.shuriken = Shuriken(
            self.character,
            self.character.x + offset_x,
            self.character.y,
            self.character.face_dir
        )
        game_world.add_object(self.shuriken, 1)

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

        world_y = self.character.y + self.character.config.draw_offset_y
        sx, sy = camera.world_to_screen(self.character.x, world_y)

        if self.character.face_dir == 1:
            self.character.image.clip_draw(l, b, w, h, sx, sy, draw_w, draw_h)
        else:
            self.character.image.clip_composite_draw(l, b, w, h, 0.0, 'h', sx, sy, draw_w, draw_h)

        left, bottom, right, top = self.get_bb()
        sx1, sy1 = camera.world_to_screen(left, bottom)
        sx2, sy2 = camera.world_to_screen(right, top)
        draw_rectangle(sx1, sy1, sx2, sy2)

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