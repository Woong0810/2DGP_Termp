from pico2d import draw_rectangle, load_image
import game_framework
import game_world
from character_config import ACTION_PER_TIME, SPECIAL_ATTACK_ANIMATION_SPEED

class SpecialAttack2:
    def __init__(self, character):
        self.character = character
        self.owner = character
        self.frames = getattr(self.character.config, 'special_attack2_frames', [])

        self.special_image = None
        if hasattr(self.character.config, 'special_attack2_image_path') and self.character.config.special_attack2_image_path:
            self.special_image = load_image(self.character.config.special_attack2_image_path)

        self.target = None
        self.naruto_hit_frames = [26, 29, 32, 35, 38, 41, 44, 47, 50]
        self.naruto_hit_done = {f: False for f in self.naruto_hit_frames}
        self.prev_frame_int = 0

    def is_naruto(self):
        return getattr(self.character.config, 'name', '') == "Naruto"

    def enter(self, e):
        self.character.frame = 0
        self.target = None
        self.prev_frame_int = 0
        self.naruto_hit_done = {f: False for f in self.naruto_hit_frames}
        game_world.add_collision_pairs('special_attack2:character', self, None)

    def exit(self, e):
        game_world.remove_collision_object(self)

    def do(self):
        if not self.frames:
            self.character.state_machine.handle_event(('SPECIAL_ATTACK2_END', None))
            return
        prev_int = int(self.character.frame)
        self.character.frame += len(self.frames) * ACTION_PER_TIME * SPECIAL_ATTACK_ANIMATION_SPEED * game_framework.frame_time
        cur_int = int(self.character.frame)

        if self.is_naruto():
            self.update_naruto_special(prev_int, cur_int)
        if self.character.frame >= len(self.frames):
            self.character.state_machine.handle_event(('SPECIAL_ATTACK2_END', None))
            return
        self.prev_frame_int = cur_int

    def update_naruto_special(self, prev_int, cur_int):
        if self.target is not None and cur_int == 0:
            target = self.target

            if target.x > self.character.x:
                self.character.face_dir = 1
            elif target.x < self.character.x:
                self.character.face_dir = -1

            desired_offset_x = 40
            desired_x = target.x - self.character.face_dir * desired_offset_x
            desired_y = target.y

            move_speed = 600
            dx = desired_x - self.character.x
            dy = desired_y - self.character.y
            max_move = move_speed * game_framework.frame_time

            if abs(dx) <= max_move:
                self.character.x = desired_x
            else:
                self.character.x += max_move if dx > 0 else -max_move

            if abs(dy) <= max_move:
                self.character.y = desired_y
            else:
                self.character.y += max_move if dy > 0 else -max_move

        for f in self.naruto_hit_frames:
            if self.naruto_hit_done.get(f, False):
                continue
            if prev_int < f <= cur_int:
                self.naruto_apply_hit(f)
                self.naruto_hit_done[f] = True

    def naruto_apply_hit(self, frame_int):
        target = self.target
        if target is None or target.hp <= 0:
            return

        data = None
        cfg_data = getattr(self.character.config, 'special_attack_data', None)
        if isinstance(cfg_data, list) and len(cfg_data) > 1:
            data = cfg_data[1]
        damage = data.get('damage', 3.5) if data else 3.5
        hitstop_frames = data.get('hitstop_frames', 20) if data else 20
        hitstun_frames = data.get('hitstun_frames', 40) if data else 40
        knockback = data.get('knockback', 60) if data else 60

        hit_state = getattr(target, 'HIT', None)

        if frame_int == self.naruto_hit_frames[-1]:
            if self.character.x < target.x:
                knockback_dir = 1
            elif self.character.x > target.x:
                knockback_dir = -1
            else:
                knockback_dir = -self.character.face_dir
            target.x += knockback_dir * knockback
            target.take_hit(
                is_knockback=True,
                knockback_distance=knockback,
                knockback_dir=knockback_dir,
                hitstun_frames=hitstun_frames,
                will_knockdown=True
            )
            if hit_state:
                hit_state.naruto_end_chain_with_knockdown()
            target.hp = max(0, target.hp - damage)
            game_framework.add_hitstop(hitstop_frames)
        else:
            if hit_state:
                hit_state.naruto_replay_hit()
            target.hp = max(0, target.hp - damage)
            game_framework.add_hitstop(hitstop_frames)

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

        draw_y = self.character.y + self.character.config.draw_offset_y + self.character.config.special_attack2_offset_y

        if self.character.face_dir == 1:
            image.clip_draw(l, b, w, h, self.character.x, draw_y, draw_w, draw_h)
        else:
            image.clip_composite_draw(l, b, w, h, 0.0, 'h', self.character.x, draw_y, draw_w, draw_h)
        draw_rectangle(*self.get_bb())

    def get_bb(self):
        if not self.frames:
            return (0,0,0,0)
        if self.is_naruto():
            return self.get_bb_naruto()

        hb = self.character.config.hitbox_special_attack2
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

        return (
            self.character.x - hw + hb['x_offset'],
            self.character.y - hh + hb['y_offset'] + self.character.config.special_attack2_offset_y,
            self.character.x + hw + hb['x_offset'],
            self.character.y + hh + hb['y_offset'] + self.character.config.special_attack2_offset_y
        )

    def get_bb_naruto(self):
        cur = int(self.character.frame)

        if self.target is None:
            if cur != 0:
                return (0, 0, 0, 0)

            if hasattr(self.character.config, 'special_attack2_frames_data'):
                frame_idx = self.frames[0]
                frame = self.character.config.special_attack2_frames_data[frame_idx]
            else:
                frame_idx = self.frames[0]
                frame = self.character.config.frames[frame_idx]

            hb = dict(self.character.config.hitbox_special_attack2)
            hb['scale_x'] *= 10.0
            hb['scale_y'] *= 1.0
            hw = frame['width'] * self.character.config.scale_x * hb['scale_x'] / 2
            hh = frame['height'] * self.character.config.scale_y * hb['scale_y'] / 2

            return (
                self.character.x - hw + hb['x_offset'],
                self.character.y - hh + hb['y_offset'],
                self.character.x + hw + hb['x_offset'],
                self.character.y + hh + hb['y_offset']
            )
        if cur not in self.naruto_hit_frames:
            return (0, 0, 0, 0)

        if hasattr(self.character.config,'special_attack2_frames_data'):
            frame_idx = self.frames[cur]
            frame = self.character.config.special_attack2_frames_data[frame_idx]
        else:
            frame_idx = self.frames[cur]
            frame = self.character.config.frames[frame_idx]

        hb = self.character.config.hitbox_special_attack
        hw = frame['width'] * self.character.config.scale_x * hb['scale_x'] / 2
        hh = frame['height'] * self.character.config.scale_y * hb['scale_y'] / 2

        return (
            self.character.x - hw + hb['x_offset'],
            self.character.y - hh + hb['y_offset'] + self.character.config.special_attack2_offset_y,
            self.character.x + hw + hb['x_offset'],
            self.character.y + hh + hb['y_offset'] + self.character.config.special_attack2_offset_y
        )

    def handle_collision(self, group, other):
        if not self.is_naruto():
            return

        cur = int(self.character.frame)
        if self.target is None and cur == 0:
            self.target = other

            if self.target.x > self.character.x:
                self.character.face_dir = 1
            elif self.target.x < self.character.x:
                self.character.face_dir = -1

            offset_x = 50
            self.character.x = self.target.x - self.character.face_dir * offset_x
            self.character.y = self.target.y

            self.target.naruto_special_chain_active = True
            self.target.take_hit(
                is_knockback=False,
                knockback_distance=0,
                knockback_dir=0,
                hitstun_frames=30,
                will_knockdown=False
            )
            return
