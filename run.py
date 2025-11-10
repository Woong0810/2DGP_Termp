from pico2d import draw_rectangle
from character_config import RUN_SPEED_PPS, ACTION_PER_TIME, RUN_ANIMATION_SPEED
import game_framework
import game_world

class Run:
    def __init__(self, character):
        self.character = character

    def enter(self, e):
        self.character.frame = 0
        kb = self.character.key_bindings

        if e[0] == 'INPUT':
            from sdl2 import SDL_KEYDOWN, SDL_KEYUP
            if e[1].type == SDL_KEYDOWN:
                if e[1].key == kb['right']:
                    self.character.dir = self.character.face_dir = 1
                elif e[1].key == kb['left']:
                    self.character.dir = self.character.face_dir = -1
            elif e[1].type == SDL_KEYUP:
                if e[1].key == kb['left']:
                    self.character.dir = self.character.face_dir = 1
                elif e[1].key == kb['right']:
                    self.character.dir = self.character.face_dir = -1

        game_world.add_collision_pairs('normal_attack:character', None, self.character)
        game_world.add_collision_pairs('special_attack:character', None, self.character)
        game_world.add_collision_pairs('ranged_attack:character', None, self.character)

    def exit(self, e):
        game_world.remove_collision_object(self.character)

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
        draw_rectangle(*self.get_bb())

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

