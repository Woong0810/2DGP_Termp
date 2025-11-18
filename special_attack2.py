from pico2d import draw_rectangle, load_image
import game_framework
import game_world
from character_config import ACTION_PER_TIME, SPECIAL_ATTACK_ANIMATION_SPEED

class SpecialAttack2:
    def __init__(self, character):
        self.character = character
        self.owner = character
        self.loop_count = 0

        # 별도 이미지가 있는 경우 로드 (이타치 등)
        self.special_image = None
        if hasattr(self.character.config, 'special_attack2_image_path') and self.character.config.special_attack2_image_path:
            self.special_image = load_image(self.character.config.special_attack2_image_path)

    def enter(self, e):
        self.character.frame = 0
        self.loop_count = 0
        self.frames = getattr(self.character.config, 'special_attack2_frames', [])
        game_world.add_collision_pairs('special_attack2:character', self, None)

    def exit(self, e):
        game_world.remove_collision_object(self)

    def do(self):
        if not self.frames:
            self.character.state_machine.handle_event(('SPECIAL_ATTACK2_END', None))
            return
        self.character.frame += len(self.frames) * ACTION_PER_TIME * SPECIAL_ATTACK_ANIMATION_SPEED * game_framework.frame_time
        if self.character.frame >= len(self.frames):
            self.character.state_machine.handle_event(('SPECIAL_ATTACK2_END', None))

    def draw(self):
        if not self.frames:
            return

        idx = int(self.character.frame)
        if idx >= len(self.frames):
            idx = len(self.frames) - 1

        if hasattr(self.character.config, 'special_attack2_frames_data') and self.character.config.special_attack2_frames_data:
            frame_idx = self.frames[idx]
            frame = self.character.config.special_attack2_frames_data[frame_idx]
            image = self.special_image if self.special_image else self.character.image
        else:
            frame_idx = self.frames[idx]
            frame = self.character.config.frames[frame_idx]
            image = self.character.image

        l, b, w, h = frame['left'], frame['bottom'], frame['width'], frame['height']
        draw_w = int(w * self.character.config.scale_x)
        draw_h = int(h * self.character.config.scale_y)

        special_attack2_y_offset = 10
        draw_y = self.character.y + self.character.config.draw_offset_y + special_attack2_y_offset

        if self.character.face_dir == 1:
            image.clip_draw(l, b, w, h, self.character.x, draw_y, draw_w, draw_h)
        else:
            image.clip_composite_draw(l, b, w, h, 0.0, 'h', self.character.x, draw_y, draw_w, draw_h)
        draw_rectangle(*self.get_bb())

    def get_bb(self):
        if not self.frames:
            return (0,0,0,0)

        hb = self.character.config.hitbox_special_attack
        hb_scale_x = hb['scale_x'] * 0.9
        hb_scale_y = hb['scale_y'] * 0.9
        idx = int(self.character.frame)
        if idx >= len(self.frames):
            idx = len(self.frames) - 1

        if hasattr(self.character.config, 'special_attack2_frames_data') and self.character.config.special_attack2_frames_data:
            frame_idx = self.frames[idx]
            frame = self.character.config.special_attack2_frames_data[frame_idx]
        else:
            frame_idx = self.frames[idx]
            frame = self.character.config.frames[frame_idx]

        hw = frame['width'] * self.character.config.scale_x * hb_scale_x / 2
        hh = frame['height'] * self.character.config.scale_y * hb_scale_y / 2

        special_attack2_y_offset = 10

        return (
            self.character.x - hw + hb['x_offset'],
            self.character.y - hh + hb['y_offset'] + special_attack2_y_offset,
            self.character.x + hw + hb['x_offset'],
            self.character.y + hh + hb['y_offset'] + special_attack2_y_offset
        )

    def handle_collision(self, group, other):
        pass
