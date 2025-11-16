from pico2d import draw_rectangle, load_image
from character_config import ACTION_PER_TIME, SPECIAL_ATTACK_ANIMATION_SPEED, SPECIAL_ATTACK_LOOP_COUNT
import game_framework
import game_world

class SpecialAttack:
    def __init__(self, character):
        self.character = character
        self.owner = character
        self.loop_count = 0
        self.amaterasu = None

        self.special_image = None
        if hasattr(self.character.config, 'special_attack_image_path') and self.character.config.special_attack_image_path:
            self.special_image = load_image(self.character.config.special_attack_image_path)

    def enter(self, e):
        self.character.frame = 0
        self.loop_count = 0

        if self.character.config.name == "Itachi":
            from amaterasu import Amaterasu
            self.amaterasu = Amaterasu(self.character, self.character.x, self.character.y, self.character.face_dir)
            game_world.add_object(self.amaterasu, 1)

        game_world.add_collision_pairs('special_attack:character', self, None)

    def exit(self, e):
        game_world.remove_collision_object(self)

        if self.amaterasu:
            try:
                game_world.remove_object(self.amaterasu)
            except:
                pass
            self.amaterasu = None

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
            last_4_start = len(special_frames) - 4
            skip_before_last_4 = last_4_start - 3

            self.character.frame += len(special_frames) * ACTION_PER_TIME * SPECIAL_ATTACK_ANIMATION_SPEED * game_framework.frame_time

            if skip_before_last_4 - 3 <= self.character.frame < last_4_start:
                self.character.frame = last_4_start

            if self.character.frame >= len(special_frames):
                if self.loop_count < SPECIAL_ATTACK_LOOP_COUNT:
                    self.character.frame = last_4_start
                    self.loop_count += 1
                else:
                    self.character.state_machine.handle_event(('SPECIAL_ATTACK_END', None))

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
                image_to_use = self.special_image if self.special_image else self.character.image
            else:
                all_frames = self.character.config.frames
                current_frame = max(0, min(int(self.character.frame), len(special_attack_frames) - 1))
                frame_idx = special_attack_frames[current_frame]
                image_to_use = self.character.image

            frame = all_frames[frame_idx]

            l, b, w, h = frame['left'], frame['bottom'], frame['width'], frame['height']
            draw_w = int(w * self.character.config.scale_x)
            draw_h = int(h * self.character.config.scale_y)
            draw_y = self.character.y + self.character.config.draw_offset_y

            if self.character.face_dir == 1:
                image_to_use.clip_draw(l, b, w, h, self.character.x, draw_y, draw_w, draw_h)
            else:
                image_to_use.clip_composite_draw(l, b, w, h, 0.0, 'h',
                                                     self.character.x, draw_y, draw_w, draw_h)

        draw_rectangle(*self.get_bb())

    def get_bb(self):
        if self.character.config.name == "Itachi":
            if self.amaterasu:
                return self.amaterasu.get_bb()
            else:
                return (0, 0, 0, 0)
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
        pass

