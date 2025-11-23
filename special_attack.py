from pico2d import draw_rectangle, load_image
from character_config import ACTION_PER_TIME, SPECIAL_ATTACK_ANIMATION_SPEED
import game_framework
import game_world

class SpecialAttack:
    def __init__(self, character):
        self.character = character
        self.owner = character
        self.amaterasu = None

        self.special_image = None
        if hasattr(self.character.config, 'special_attack_image_path') and self.character.config.special_attack_image_path:
            self.special_image = load_image(self.character.config.special_attack_image_path)

        self.target = None
        self.naruto_hit_frames = [43, 44, 59, 67, 73, 78]
        self.naruto_hit_done = {f: False for f in self.naruto_hit_frames}
        self.prev_frame_int = 0

    def enter(self, e):
        self.character.frame = 0
        self.prev_frame_int = 0

        if self.character.config.name == "Naruto":
            self.target = None
            self.naruto_hit_done = {f: False for f in self.naruto_hit_frames}

        if self.character.config.name == "Itachi":
            from amaterasu import Amaterasu
            self.amaterasu = Amaterasu(self.character, self.character.x, self.character.y, self.character.face_dir)
            game_world.add_object(self.amaterasu, 1)

        game_world.add_collision_pairs('special_attack:character', self, None)

    def exit(self, e):
        game_world.remove_collision_object(self)

        if self.amaterasu:
            game_world.remove_object(self.amaterasu)
        self.target = None

    def do(self):
        if self.character.config.name == "Itachi":
            char_frames = self.character.config.special_attack_frames

            self.character.frame += len(char_frames) * ACTION_PER_TIME * SPECIAL_ATTACK_ANIMATION_SPEED * game_framework.frame_time

            if self.character.frame >= len(char_frames):
                self.character.frame = 0

            if not self.amaterasu or self.amaterasu not in game_world.world[1]:
                self.character.state_machine.handle_event(('SPECIAL_ATTACK_END', None))
        else:
            special_frames = self.character.config.special_attack_frames

            prev_int = int(self.character.frame)
            self.character.frame += len(special_frames) * ACTION_PER_TIME * SPECIAL_ATTACK_ANIMATION_SPEED * game_framework.frame_time
            cur_int = int(self.character.frame)

            # 나루토 스페셜 1 전용 로직 (충돌은 탐색으로만 처리, 실제 데미지는 프레임에 따라 직접 처리)
            if self.character.config.name == "Naruto":
                self.update_naruto_special1(prev_int, cur_int)

            if self.character.frame >= len(special_frames):
                self.character.state_machine.handle_event(('SPECIAL_ATTACK_END', None))

            self.prev_frame_int = cur_int

    def is_search_phase(self):
        if self.character.config.name != "Naruto":
            return False
        return self.target is None and int(self.character.frame) < 43

    def update_naruto_special1(self, prev_frame_int, cur_frame_int):
        if self.target is not None and cur_frame_int < 43:
            if self.target.x > self.character.x:
                self.character.face_dir = 1
            elif self.target.x < self.character.x:
                self.character.face_dir = -1

            desired_offset_x = 40
            desired_x = self.target.x - self.character.face_dir * desired_offset_x
            dx = desired_x - self.character.x
            desired_y = self.target.y - self.character.face_dir
            dy = desired_y - self.character.y

            move_speed = 600
            max_move = move_speed * game_framework.frame_time

            if abs(dx) <= max_move and abs(dy) <= max_move:
                self.character.x = desired_x
                self.character.y = desired_y
            else:
                self.character.x += max_move if dx > 0 else -max_move
                self.character.y += max_move if dy > 0 else -max_move

        for f in self.naruto_hit_frames:
            if self.naruto_hit_done.get(f, False):
                continue
            if prev_frame_int < f <= cur_frame_int:
                self.naruto_apply_hit(f)
                self.naruto_hit_done[f] = True

    def naruto_apply_hit(self, frame_int):
        target = self.target
        if target is None or target.hp <= 0:
            return

        data = None
        if hasattr(self.character.config, 'special_attack_data'):
            sad = self.character.config.special_attack_data
            if isinstance(sad, list) and len(sad) > 0:
                data = sad[0]

        damage = data.get('damage', 15) if data else 15
        hitstop_frames = data.get('hitstop_frames', 6) if data else 6

        if frame_int == 43:
            dir1 = self.character.face_dir
            target.take_hit(
                is_knockback=False,
                knockback_distance=0,
                knockback_dir=0,
                hitstun_frames=30,
                will_knockdown=False
            )
            # x좌표를 직접 밀어서 넉백처럼 보이게
            target.x += dir1 * 40
            target.hp = max(0, target.hp - damage)
            game_framework.add_hitstop(hitstop_frames)
            return

        hit_state = getattr(target, 'HIT', None)
        if frame_int == 44:
            dir2 = -self.character.face_dir
            target.x += dir2 * 40
            hit_state.naruto_replay_hit()
            target.hp = max(0, target.hp - damage)
            game_framework.add_hitstop(hitstop_frames)
            return

        if frame_int == 59:
            target.y += 100

            hit_state.naruto_replay_hit()
            target.hp = max(0, target.hp - damage)
            game_framework.add_hitstop(hitstop_frames)
            return

        if frame_int in (67, 73):
            hit_state.naruto_replay_hit()
            target.hp = max(0, target.hp - damage)
            game_framework.add_hitstop(hitstop_frames)
            return

        if frame_int == 78:
            target.take_hit(
                is_knockback=True,
                knockback_distance=0,
                knockback_dir=0,
                hitstun_frames=30,
                will_knockdown=True
            )
            hit_state.naruto_end_chain_with_knockdown()
            target.hp = max(0, target.hp - damage)
            game_framework.add_hitstop(hitstop_frames)
            return


    def draw(self):
        if self.character.config.name == "Itachi":
            char_frames = self.character.config.special_attack_frames

            char_idx = min(int(self.character.frame), len(char_frames) - 1)
            char_frame_idx = char_frames[char_idx]
            char_frame = self.character.config.frames[char_frame_idx]

            cl, cb, cw, ch = char_frame['left'], char_frame['bottom'], char_frame['width'], char_frame['height']
            draw_w = int(cw * self.character.config.scale_x)
            draw_h = int(ch * self.character.config.scale_y)
            draw_y = self.character.y + self.character.config.draw_offset_y

            if self.character.face_dir == 1:
                self.character.image.clip_draw(cl, cb, cw, ch, self.character.x, draw_y, draw_w, draw_h)
            else:
                self.character.image.clip_composite_draw(cl, cb, cw, ch, 0.0, 'h',
                                                         self.character.x, draw_y, draw_w, draw_h)
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
            draw_y = self.character.y + self.character.config.draw_offset_y + self.character.config.special_attack_offset_y

            if self.character.face_dir == 1:
                image_to_use.clip_draw(l, b, w, h, self.character.x, draw_y, draw_w, draw_h)
            else:
                image_to_use.clip_composite_draw(l, b, w, h, 0.0, 'h',
                                                 self.character.x, draw_y, draw_w, draw_h)

        draw_rectangle(*self.get_bb())

    def get_bb_naruto(self):
        current = int(self.character.frame)

        SEARCH_END_FRAME = 1
        if self.target is None and current < SEARCH_END_FRAME:
            if hasattr(self.character.config, 'special_attack_frames_data') and self.character.config.special_attack_frames_data:
                all_frames = self.character.config.special_attack_frames_data
                frame_idx = max(0, min(current, len(all_frames) - 1))
                frame = all_frames[frame_idx]
            else:
                all_frames = self.character.config.frames
                frame_indices = self.character.config.special_attack_frames
                idx = max(0, min(current, len(frame_indices) - 1))
                frame_idx = frame_indices[idx]
                frame = all_frames[frame_idx]

            hb = dict(self.character.config.hitbox_special_attack)
            hb['scale_x'] *= 1.6
            hb['scale_y'] *= 1.2

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
        if self.character.config.name == "Itachi":
            if self.amaterasu:
                return self.amaterasu.get_bb()
            else:
                return (0, 0, 0, 0)
        elif self.character.config.name == "Naruto":
            return self.get_bb_naruto()
        else:
            threshold = 120
            if self.character.frame < threshold:
                return (0, 0, 0, 0)

            special_attack_frames = self.character.config.special_attack_frames

            if hasattr(self.character.config, 'special_attack_frames_data') and self.character.config.special_attack_frames_data:
                all_frames = self.character.config.special_attack_frames_data
                current_frame = max(0, min(int(self.character.frame), len(all_frames) - 1))
                frame_idx = current_frame
                frame = all_frames[frame_idx]
            else:
                all_frames = self.character.config.frames
                current_frame = max(0, min(int(self.character.frame), len(special_attack_frames) - 1))
                frame_idx = special_attack_frames[current_frame]
                frame = all_frames[frame_idx]

            hb = self.character.config.hitbox_special_attack
            hw = frame['width'] * self.character.config.scale_x * hb['scale_x'] / 2
            hh = frame['height'] * self.character.config.scale_y * hb['scale_y'] / 2
            return (
                self.character.x - hw + hb['x_offset'],
                self.character.y - hh + hb['y_offset'],
                self.character.x + hw + hb['x_offset'],
                self.character.y + hh + hb['y_offset']
            )

    def handle_collision(self, group, other):
        # 아직은 나루토만
        if group == 'special_attack:character' and self.character.config.name == "Naruto":
            if self.target is None and self.is_search_phase():
                self.target = other
                other.naruto_special_chain_active = True

                other.take_hit(
                    is_knockback=False,
                    knockback_distance=0,
                    knockback_dir=0,
                    hitstun_frames=30,
                    will_knockdown=False
                )
