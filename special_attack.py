from pico2d import draw_rectangle, load_image
from character_config import ACTION_PER_TIME, SPECIAL_ATTACK_ANIMATION_SPEED, SPECIAL_GAUGE_COST
import game_framework
import game_world
from camera import camera

class SpecialAttack:
    def __init__(self, character):
        self.character = character
        self.owner = character
        self.amaterasu = None

        self.special_image = None
        if hasattr(self.character.config, 'special_attack_image_path') and self.character.config.special_attack_image_path:
            self.special_image = load_image(self.character.config.special_attack_image_path)

        self.target = None
        self.hit_frames = getattr(self.character.config, 'special1_hit_frames', [])
        self.hit_done = {f: False for f in self.hit_frames}
        self.prev_frame_int = 0
        self.prev_effect_frame_int = 0

    def enter(self, e):
        self.character.do_special_attack(SPECIAL_GAUGE_COST)
        self.character.frame = 0
        self.prev_frame_int = 0
        self.prev_effect_frame_int = 0
        self.target = None
        self.hit_done = {f: False for f in self.hit_frames}
        self.character.special_timer = 1.0

        game_world.add_collision_pairs('special_attack:character', self, None)
        game_world.add_collision_pairs('normal_attack:character', None, self.character)
        game_world.add_collision_pairs('jump_attack:character', None, self.character)
        game_world.add_collision_pairs('special_attack:character', None, self.character)
        game_world.add_collision_pairs('special_attack2:character', None, self.character)
        game_world.add_collision_pairs('ranged_attack:character', None, self.character)
        game_world.add_collision_pairs('character:shuriken', self.character, None)

    def exit(self, e):
        game_world.remove_collision_object(self)
        if self.target:
            self.target.special_chain_active = False
        self.target = None

    def do(self):
        special_frames = self.character.config.special_attack_frames

        prev_int = int(self.character.frame)
        self.character.frame += len(special_frames) * ACTION_PER_TIME * SPECIAL_ATTACK_ANIMATION_SPEED * game_framework.frame_time
        cur_int = int(self.character.frame)

        self.update_special(prev_int, cur_int)

        if self.character.frame >= len(special_frames):
            self.character.state_machine.handle_event(('SPECIAL_ATTACK_END', None))

        self.prev_frame_int = cur_int

    def update_special(self, prev_frame_int, cur_frame_int):
        if self.character.config.name == "Itachi" and self.amaterasu is not None:
            prev_effect_int = self.prev_effect_frame_int
            cur_effect_int = int(self.amaterasu.frame)

            for f in self.hit_frames:
                if self.hit_done.get(f, False):
                    continue
                if prev_effect_int < f <= cur_effect_int:
                    self.apply_hit_at_frame(f)
                    self.hit_done[f] = True
            self.prev_effect_frame_int = cur_effect_int
            return
        for f in self.hit_frames:
            if self.hit_done.get(f, False):
                continue
            if prev_frame_int < f <= cur_frame_int:
                self.apply_hit_at_frame(f)
                self.hit_done[f] = True

    def apply_hit_at_frame(self, frame_int):
        target = self.target
        if target is None or target.hp <= 0:
            return

        data = None
        if hasattr(self.character.config, 'special_attack_data'):
            sad = self.character.config.special_attack_data
            if isinstance(sad, list) and len(sad) > 0:
                data = sad[0]

        damage = data.get('damage', 5) if data else 5
        hitstun_frames = data.get('hitstun_frames', 32) if data else 32
        hitstop_frames = data.get('hitstop_frames', 15) if data else 15
        knockback = data.get('knockback', 40) if data else 40

        if self.character.config.name != "Naruto":
            hit_state = getattr(target, 'HIT', None)

            if frame_int == self.hit_frames[-1]:
                if self.character.x < target.x:
                    knockback_dir = 1
                elif self.character.x > target.x:
                    knockback_dir = -1
                else:
                    knockback_dir = -self.character.face_dir
                target.take_hit(
                    is_knockback=True,
                    knockback_distance=knockback,
                    knockback_dir=knockback_dir,
                    hitstun_frames=hitstun_frames,
                    will_knockdown=True
                )
                if hit_state:
                    hit_state.set_chain_with_knockdown(knockback, self.character.face_dir, False)
                target.hp = max(0, target.hp - damage)
                game_framework.add_hitstop(hitstop_frames)
            else:
                if hit_state:
                    hit_state.replay_hit()
                target.hp = max(0, target.hp - damage)
                game_framework.add_hitstop(hitstop_frames)
            return
        if self.character.config.name == 'Naruto':
            if frame_int == 43:
                dir1 = self.character.face_dir
                target.take_hit(
                    is_knockback=False,
                    knockback_distance=0,
                    knockback_dir=0,
                    hitstun_frames=hitstun_frames,
                    will_knockdown=False
                )
                target.x += dir1 * 40
                target.hp = max(0, target.hp - damage)
                game_framework.add_hitstop(hitstop_frames)
                return

            hit_state = getattr(target, 'HIT', None)
            if frame_int == 44:
                dir2 = -self.character.face_dir
                target.x += dir2 * 40
                hit_state.replay_hit()
                target.hp = max(0, target.hp - damage)
                game_framework.add_hitstop(hitstop_frames)
                return

            if frame_int == 59:
                target.y += 100

                hit_state.replay_hit()
                target.hp = max(0, target.hp - damage)
                game_framework.add_hitstop(hitstop_frames)
                return

            if frame_int in (67, 73):
                hit_state.replay_hit()
                target.hp = max(0, target.hp - damage)
                game_framework.add_hitstop(hitstop_frames)
                return

            if frame_int == 78:
                target.take_hit(
                    is_knockback=True,
                    knockback_distance=knockback,
                    knockback_dir=0,
                    hitstun_frames=hitstun_frames,
                    will_knockdown=True
                )
                hit_state.set_chain_with_knockdown(knockback, self.character.face_dir, True)
                target.hp = max(0, target.hp - damage)
                game_framework.add_hitstop(hitstop_frames)
                return
        else:
            pass

    def draw(self):
        if self.character.config.name == "Itachi":
            char_frames = self.character.config.special_attack_frames

            char_idx = min(int(self.character.frame), len(char_frames) - 1)
            char_frame_idx = char_frames[char_idx]
            char_frame = self.character.config.frames[char_frame_idx]

            cl, cb, cw, ch = char_frame['left'], char_frame['bottom'], char_frame['width'], char_frame['height']
            draw_w = int(cw * self.character.config.scale_x)
            draw_h = int(ch * self.character.config.scale_y)

            world_y = self.character.y + self.character.config.draw_offset_y
            sx, sy = camera.world_to_screen(self.character.x, world_y)

            if self.character.face_dir == 1:
                self.character.image.clip_draw(cl, cb, cw, ch, sx, sy, draw_w, draw_h)
            else:
                self.character.image.clip_composite_draw(cl, cb, cw, ch, 0.0, 'h', sx, sy, draw_w, draw_h)
        else:
            special_attack_frames = self.character.config.special_attack_frames

            if hasattr(self.character.config, 'special_attack_frames_data') and self.character.config.special_attack_frames_data:
                all_frames = self.character.config.special_attack_frames_data
                current_frame = max(0, min(int(self.character.frame), len(all_frames) - 1))
                frame_idx = current_frame
                image_to_use = self.special_image
            else:
                all_frames = self.character.config.frames
                current_frame = max(0, min(int(self.character.frame), len(special_attack_frames) - 1))
                frame_idx = special_attack_frames[current_frame]
                image_to_use = self.character.image

            frame = all_frames[frame_idx]

            l, b, w, h = frame['left'], frame['bottom'], frame['width'], frame['height']
            draw_w = int(w * self.character.config.scale_x)
            draw_h = int(h * self.character.config.scale_y)

            world_y = self.character.y + self.character.config.draw_offset_y + self.character.config.special_attack_offset_y
            sx, sy = camera.world_to_screen(self.character.x, world_y)

            if self.character.face_dir == 1:
                image_to_use.clip_draw(l, b, w, h, sx, sy, draw_w, draw_h)
            else:
                image_to_use.clip_composite_draw(l, b, w, h, 0.0, 'h', sx, sy, draw_w, draw_h)

        left, bottom, right, top = self.get_bb()
        sx1, sy1 = camera.world_to_screen(left, bottom)
        sx2, sy2 = camera.world_to_screen(right, top)
        draw_rectangle(sx1, sy1, sx2, sy2)

    def get_bb_search_special(self):
        current = int(self.character.frame)

        if self.target is None and current == 0:
            special_frames = self.character.config.special_attack_frames
            all_frames = self.character.config.frames

            if special_frames:
                frame_idx = special_frames[0]
            else:
                frame_idx = 0
            frame = all_frames[frame_idx]
            hb = dict(self.character.config.hitbox_special_attack)

            hw = frame['width'] * self.character.config.scale_x * hb['scale_x'] / 2
            hh = frame['height'] * self.character.config.scale_y * hb['scale_y'] / 2
            return (
                self.character.x - hw + hb['x_offset'],
                self.character.y - hh + hb['y_offset'],
                self.character.x + hw + hb['x_offset'],
                self.character.y + hh + hb['y_offset'],
            )

        return (0, 0, 0, 0)

    def get_bb(self):
        return self.get_bb_search_special()

    def handle_collision(self, group, other):
        cur = int(self.character.frame)
        if self.target is None and cur == 0:
            self.target = other

            if self.target.x > self.character.x:
                self.character.face_dir = 1
            elif self.target.x < self.character.x:
                self.character.face_dir = -1

            offset_x = getattr(self.character.config, 'special1_offset_x', 50)
            self.character.x = self.target.x - self.character.face_dir * offset_x
            self.character.y = self.target.y

            if self.character.config.name == "Itachi":
                from amaterasu import Amaterasu
                self.amaterasu = Amaterasu(self.character, self.character.x, self.character.y, self.character.face_dir)
                game_world.add_object(self.amaterasu, 1)

            other.special_chain_active = True

            other.take_hit(
                is_knockback=False,
                knockback_distance=0,
                knockback_dir=0,
                hitstun_frames=30,
                will_knockdown=False
            )
