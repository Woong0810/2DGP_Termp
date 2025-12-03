from pico2d import draw_rectangle, clamp
from character_config import RUN_SPEED_PPS, ACTION_PER_TIME, RUN_ANIMATION_SPEED
import game_framework
import game_world
from camera import camera

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
        game_world.add_collision_pairs('jump_attack:character', None, self.character)
        game_world.add_collision_pairs('special_attack:character', None, self.character)
        game_world.add_collision_pairs('special_attack2:character', None, self.character)
        game_world.add_collision_pairs('ranged_attack:character', None, self.character)
        game_world.add_collision_pairs('character:shuriken', self.character, None)
        game_world.add_collision_pairs('character:character', self.character, self.character.opponent)

    def exit(self, e):
        game_world.remove_collision_object(self.character)

    def do(self):
        self.character.x += RUN_SPEED_PPS * game_framework.frame_time * self.character.dir
        self.character.x = clamp(camera.window_left, self.character.x, camera.window_right)
        run_frames = self.character.config.run_frames
        frames_per_action = len(run_frames)
        self.character.frame = (self.character.frame + frames_per_action * ACTION_PER_TIME * RUN_ANIMATION_SPEED * game_framework.frame_time) % frames_per_action

        self.check_fall_or_snap_to_ground()

    def check_fall_or_snap_to_ground(self):
        if not hasattr(self.character, 'stage') or self.character.stage is None:
            return

        left, bottom, right, top = self.character.get_feet_bb()
        ground_top = self.character.stage.get_ground_top_under(left, bottom, right)

        if ground_top is None:
            jump_state = self.character.JUMP
            jump_state.vy = 0.0
            jump_state.dir = self.character.dir
            jump_state.ground_y = -1000

            self.character.state_machine.handle_event(('FALL', None))
        else:
            dy = ground_top - bottom
            if abs(dy) > 1:
                self.character.y += dy

    def draw(self):
        run_frames = self.character.config.run_frames
        all_frames = self.character.config.frames
        frame_idx = run_frames[int(self.character.frame)]
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

