from pico2d import load_image, draw_rectangle
from character_config import ACTION_PER_TIME, DASH_ANIMATION_SPEED
import game_framework
import game_world

DASH_EFFECT_FRAMES = [
    {'left': 0, 'bottom': 0, 'width': 27, 'height': 26},
    {'left': 32, 'bottom': 0, 'width': 28, 'height': 26},
    {'left': 65, 'bottom': 0, 'width': 29, 'height': 26},
    {'left': 100, 'bottom': 0, 'width': 29, 'height': 26},
    {'left': 135, 'bottom': 0, 'width': 32, 'height': 26},
    {'left': 168, 'bottom': 0, 'width': 33, 'height': 26},
    {'left': 203, 'bottom': 0, 'width': 31, 'height': 26},
    {'left': 236, 'bottom': 0, 'width': 263, 'height': 26},
]

class Dash:
    effect_image = None

    def __init__(self, character):
        self.character = character
        self.frame = 0.0

        if Dash.effect_image is None:
            Dash.effect_image = load_image('dash_effect.png')

        self.dash_speed = 500
        self.dash_duration = 0.3
        self.elapsed_time = 0.0

    def enter(self, e):
        self.character.frame = 0
        self.frame = 0.0
        self.elapsed_time = 0.0

        if hasattr(self.character, 'invincible_time'):
            if self.character.invincible_time < self.dash_duration:
                self.character.invincible_time = self.dash_duration
        game_world.add_collision_pairs('normal_attack:character', None, self.character)
        game_world.add_collision_pairs('special_attack:character', None, self.character)
        game_world.add_collision_pairs('ranged_attack:character', None, self.character)
        game_world.add_collision_pairs('character:shuriken', self.character, None)

    def exit(self, e):
        game_world.remove_collision_object(self.character)

    def do(self):
        dash_frames = self.character.config.dash_frames
        frame_count = len(dash_frames)

        self.frame = (self.frame + frame_count * ACTION_PER_TIME * DASH_ANIMATION_SPEED * game_framework.frame_time) % frame_count

        self.character.x += self.dash_speed * self.character.face_dir * game_framework.frame_time

        self.elapsed_time += game_framework.frame_time

        if self.elapsed_time >= self.dash_duration:
            from event_to_string import dash_end
            self.character.state_machine.add_event(('DASH_END', 0))

    def draw(self):
        effect_frame_idx = int(self.frame) % len(DASH_EFFECT_FRAMES)
        effect_frame = DASH_EFFECT_FRAMES[effect_frame_idx]

        effect_x = self.character.x - (20 * self.character.face_dir)
        effect_y = self.character.y

        if self.character.face_dir == 1:
            Dash.effect_image.clip_composite_draw(
                effect_frame['left'], effect_frame['bottom'],
                effect_frame['width'], effect_frame['height'],
                0.0, 'h',
                effect_x, effect_y,
                effect_frame['width'], effect_frame['height']
            )
        else:
            Dash.effect_image.clip_draw(
                effect_frame['left'], effect_frame['bottom'],
                effect_frame['width'], effect_frame['height'],
                effect_x, effect_y,
                effect_frame['width'], effect_frame['height']
            )

        dash_frames = self.character.config.dash_frames
        all_frames = self.character.config.frames

        char_frame_idx = int(self.frame) % len(dash_frames)
        frame_idx = dash_frames[char_frame_idx]
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
        dash_frames = self.character.config.dash_frames
        all_frames = self.character.config.frames
        char_frame_idx = int(self.frame) % len(dash_frames)
        frame_idx = dash_frames[char_frame_idx]
        frame = all_frames[frame_idx]
        if hasattr(self.character.config, 'hitbox_dash'):
            hitbox = self.character.config.hitbox_dash
        else:
            hitbox = self.character.config.hitbox_idle

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

    def handle_collision(self, group, other):
        pass
