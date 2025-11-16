from pico2d import draw_rectangle
from character_config import (GRAVITY_PPS2, JUMP_HEIGHT_PIXEL, JUMP_SPEED_PPS,
                              RUN_SPEED_PPS, ACTION_PER_TIME, JUMP_ANIMATION_SPEED)
import game_framework
import game_world
import math

class Jump:
    def __init__(self, character):
        self.character = character
        self.vy = 0.0
        self.vx = 0.0
        self.ground_y = 0.0
        self.dir = 0

    def enter(self, e):
        if e and (e[0] == 'RESUME_JUMP' or e[0] == 'SEGMENT_END'):
            self.character.frame = 0
            self.dir = 0
            return

        if e and e[0] == 'INPUT':
            event = e[1]
            try:
                from pico2d import SDL_KEYDOWN
                if event.type == SDL_KEYDOWN and hasattr(self.character, 'key_bindings') and 'jump_key' in self.character.key_bindings and event.key == self.character.key_bindings['jump_key']:
                    self.character.jump_count = 1
                    self.character.frame = 0

                    from character_config import GRAVITY_PPS2, JUMP_HEIGHT_PIXEL
                    self.vy = math.sqrt(2 * GRAVITY_PPS2 * JUMP_HEIGHT_PIXEL)
                    self.ground_y = self.character.y

                    prev_state = self.character.state_machine.prev_state
                    if prev_state == self.character.RUN:
                        from character_config import RUN_SPEED_PPS
                        self.vx = self.character.dir * RUN_SPEED_PPS
                    else:
                        self.vx = 0.0
                    self.dir = 0

                    game_world.add_collision_pairs('normal_attack:character', None, self.character)
                    game_world.add_collision_pairs('jump_attack:character', None, self.character)
                    game_world.add_collision_pairs('special_attack:character', None, self.character)
                    game_world.add_collision_pairs('ranged_attack:character', None, self.character)
                    game_world.add_collision_pairs('character:shuriken', self.character, None)
                    return
            except Exception:
                pass

        self.character.frame = 0
        if self.vy == 0.0:
            from character_config import GRAVITY_PPS2, JUMP_HEIGHT_PIXEL
            self.vy = math.sqrt(2 * GRAVITY_PPS2 * JUMP_HEIGHT_PIXEL)
            self.ground_y = self.character.y
        self.dir = 0

    def exit(self, e):
        self.dir = 0
        game_world.remove_collision_object(self.character)

    def do(self):
        if self.dir == -1:
            self.vx -= JUMP_SPEED_PPS * game_framework.frame_time
            if self.vx < -JUMP_SPEED_PPS:
                self.vx = -JUMP_SPEED_PPS
            self.character.face_dir = -1
        elif self.dir == 1:
            self.vx += JUMP_SPEED_PPS * game_framework.frame_time
            if self.vx > JUMP_SPEED_PPS:
                self.vx = JUMP_SPEED_PPS
            self.character.face_dir = 1

        # 점프 프레임 업데이트
        jump_frames = self.character.config.jump_frames
        frames_per_action = len(jump_frames)
        self.character.frame = (self.character.frame + frames_per_action * ACTION_PER_TIME * JUMP_ANIMATION_SPEED * game_framework.frame_time) % frames_per_action

        self.character.x += self.vx * game_framework.frame_time

        self.vy -= GRAVITY_PPS2 * game_framework.frame_time
        self.character.y += self.vy * game_framework.frame_time

        # 착지 체크
        if self.character.y <= self.ground_y:
            self.character.y = self.ground_y
            self.character.frame = 0
            # 착지 시 character.jump_count를 초기화하여 지상에서 다시 점프 가능하도록 함
            self.character.jump_count = 0
            self.character.state_machine.handle_event(('LANDED', None))

    def handle_double_jump(self):
        if getattr(self.character, 'jump_count', 0) == 1:
            self.character.jump_count = 2
            self.character.frame = 0
            self.vy = math.sqrt(2 * GRAVITY_PPS2 * JUMP_HEIGHT_PIXEL)

    def draw(self):
        all_frames = self.character.config.frames
        jump_frames = self.character.config.jump_frames
        frame_idx = jump_frames[int(self.character.frame)]
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
        all_frames = self.character.config.frames
        jump_frames = self.character.config.jump_frames
        frame_idx = jump_frames[int(self.character.frame)]
        frame = all_frames[frame_idx]

        hb = self.character.config.hitbox_jump
        hw = frame['width'] * self.character.config.scale_x * hb['scale_x'] / 2
        hh = frame['height'] * self.character.config.scale_y * hb['scale_y'] / 2
        return (
            self.character.x - hw + hb['x_offset'],
            self.character.y - hh + hb['y_offset'],
            self.character.x + hw + hb['x_offset'],
            self.character.y + hh + hb['y_offset']
        )
