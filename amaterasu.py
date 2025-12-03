from pico2d import load_image, draw_rectangle
import game_world
from character_config import ACTION_PER_TIME, SPECIAL_ATTACK_ANIMATION_SPEED
import game_framework
from camera import camera

class Amaterasu:
    def __init__(self, owner, x, y, face_dir):
        self.owner = owner
        self.face_dir = face_dir
        self.frame = 0

        offset_distance = 100
        self.x = x + (offset_distance * face_dir)
        self.y = y

        self.image = load_image('character_itachi_sa.png')

        from character_itachi_sa_frames import FRAMES
        self.frames = FRAMES
        self.effect_frames = list(range(0, 42))

        self.scale_x = owner.config.scale_x
        self.scale_y = owner.config.scale_y
        self.draw_offset_y = owner.config.draw_offset_y

    def update(self):
        self.frame += len(self.effect_frames) * ACTION_PER_TIME * SPECIAL_ATTACK_ANIMATION_SPEED * game_framework.frame_time
        if self.frame >= len(self.effect_frames):
            game_world.remove_object(self)

    def draw(self):
        effect_idx = min(int(self.frame), len(self.effect_frames) - 1)
        effect_frame_idx = self.effect_frames[effect_idx]
        effect_frame = self.frames[effect_frame_idx]

        el, eb, ew, eh = effect_frame['left'], effect_frame['bottom'], effect_frame['width'], effect_frame['height']
        effect_draw_w = int(ew * self.scale_x)
        effect_draw_h = int(eh * self.scale_y)

        world_y = self.y + self.draw_offset_y + self.owner.config.special_attack_offset_y
        sx, sy = camera.world_to_screen(self.x, world_y)

        if self.face_dir == 1:
            self.image.clip_draw(el, eb, ew, eh, sx, sy, effect_draw_w, effect_draw_h)
        else:
            self.image.clip_composite_draw(el, eb, ew, eh, 0.0, 'h', sx, sy, effect_draw_w, effect_draw_h)

    def get_bb(self):
        effect_idx = min(int(self.frame), len(self.effect_frames) - 1)
        effect_frame_idx = self.effect_frames[effect_idx]
        frame = self.frames[effect_frame_idx]

        hb = self.owner.config.hitbox_special_attack
        hw = frame['width'] * self.scale_x * hb['scale_x'] / 2
        hh = frame['height'] * self.scale_y * hb['scale_y'] / 2
        return (
            self.x - hw + hb['x_offset'],
            self.y - hh + hb['y_offset'],
            self.x + hw + hb['x_offset'],
            self.y + hh + hb['y_offset']
        )

    def handle_collision(self, group, other):
        pass


