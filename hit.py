from pico2d import draw_rectangle
from character_config import ACTION_PER_TIME, HIT_ANIMATION_SPEED, HIT_DURATION
import game_framework
import game_world

class Hit:
    def __init__(self, character):
        self.character = character
        self.elapsed_time = 0.0
        self.is_knockback = False
        self.knockback_distance = 0
        self.knockback_dir = 0

    def enter(self, event):
        self.character.frame = 0
        self.elapsed_time = 0.0

        if event and len(event) > 1 and isinstance(event[1], tuple):
            self.is_knockback = event[1][0]
            self.knockback_distance = event[1][1] if len(event[1]) > 1 else 0
            self.knockback_dir = event[1][2] if len(event[1]) > 2 else 0
        else:
            self.is_knockback = False
            self.knockback_distance = 0
            self.knockback_dir = 0

        game_world.add_collision_pairs('normal_attack:character', None, self.character)
        game_world.add_collision_pairs('special_attack:character', None, self.character)
        game_world.add_collision_pairs('ranged_attack:character', None, self.character)
        game_world.add_collision_pairs('character:shuriken', self.character, None)

    def exit(self, event):
        game_world.remove_collision_object(self.character)

    def do(self):
        self.elapsed_time += game_framework.frame_time

        if self.is_knockback:
            knockback_frames = self.character.config.knockback_frames
            frames_per_action = len(knockback_frames)
            self.character.frame = (self.character.frame + frames_per_action * ACTION_PER_TIME * HIT_ANIMATION_SPEED * game_framework.frame_time) % frames_per_action

            if self.elapsed_time < HIT_DURATION:
                knockback_speed = self.knockback_distance / HIT_DURATION
                self.character.x += self.knockback_dir * knockback_speed * game_framework.frame_time
        else:
            hit_frames = self.character.config.hit_frames
            frames_per_action = len(hit_frames)
            self.character.frame = (self.character.frame + frames_per_action * ACTION_PER_TIME * HIT_ANIMATION_SPEED * game_framework.frame_time) % frames_per_action

        if self.elapsed_time >= HIT_DURATION:
            from event_to_string import hit_end
            self.character.state_machine.add_event(('HIT_END', 0))

    def draw(self):
        if self.is_knockback:
            frame_indices = self.character.config.knockback_frames
        else:
            frame_indices = self.character.config.hit_frames

        frame_idx = frame_indices[int(self.character.frame)]
        frame = self.character.config.frames[frame_idx]

        l, b, w, h = frame['left'], frame['bottom'], frame['width'], frame['height']
        draw_w = int(w * self.character.config.scale_x)
        draw_h = int(h * self.character.config.scale_y)
        draw_y = self.character.y + self.character.config.draw_offset_y

        if self.character.face_dir == 1:
            self.character.image.clip_draw(l, b, w, h, self.character.x, draw_y, draw_w, draw_h)
        else:
            self.character.image.clip_composite_draw(l, b, w, h, 0, 'h',
                                                      self.character.x, draw_y, draw_w, draw_h)
        draw_rectangle(*self.get_bb())

    def get_bb(self):
        if self.is_knockback:
            frame_indices = self.character.config.knockback_frames
        else:
            frame_indices = self.character.config.hit_frames

        frame_idx = frame_indices[int(self.character.frame)]
        frame = self.character.config.frames[frame_idx]
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

