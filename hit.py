from pico2d import draw_rectangle
from character_config import ACTION_PER_TIME, HIT_ANIMATION_SPEED, HIT_DURATION, KNOCKBACK_DOWN_TIME, GRAVITY_PPS2
import game_framework
import game_world

class Hit:
    def __init__(self, character):
        self.character = character
        self.elapsed_time = 0.0
        self.is_knockback = False
        self.knockback_distance = 0
        self.knockback_dir = 0
        self.is_lying_down = False
        self.was_in_air = False
        self.ground_y = 0.0
        self.vy = 0.0
        self.hit_duration = HIT_DURATION
        self.will_knockdown = False

        self.chain_active = False
        self.chain_hold_last = False
        self.chain_force_knockdown = False

    def enter(self, event):
        self.character.frame = 0
        self.elapsed_time = 0.0
        self.is_lying_down = False

        self.chain_active = False
        self.chain_hold_last = False
        self.chain_force_knockdown = False

        prev_state = self.character.state_machine.prev_state
        if prev_state == self.character.JUMP or prev_state == self.character.JUMP_ATTACK:
            self.was_in_air = True
            self.ground_y = prev_state.ground_y
        elif prev_state == self.character.HIT:
            pass
        else:
            self.was_in_air = False
            self.ground_y = self.character.y

        if event and len(event) > 1 and isinstance(event[1], tuple):
            data = event[1]
            self.is_knockback = data[0] if len(data) > 0 else False
            self.knockback_distance = data[1] if len(data) > 1 else 0
            self.knockback_dir = data[2] if len(data) > 2 else 0
            self.hit_duration = data[3] if len(data) > 3 else HIT_DURATION
            self.will_knockdown = data[4] if len(data) > 4 else False
        else:
            self.is_knockback = False
            self.knockback_distance = 0
            self.knockback_dir = 0
            self.hit_duration = HIT_DURATION
            self.will_knockdown = False
        self.vy = 0.0

        if getattr(self.character, 'naruto_special_chain_active', False):
            self.chain_active = True
            self.chain_hold_last = True

        game_world.add_collision_pairs('normal_attack:character', None, self.character)
        game_world.add_collision_pairs('jump_attack:character', None, self.character)
        game_world.add_collision_pairs('special_attack:character', None, self.character)
        game_world.add_collision_pairs('special_attack2:character', None, self.character)
        game_world.add_collision_pairs('ranged_attack:character', None, self.character)
        game_world.add_collision_pairs('character:shuriken', self.character, None)

    def exit(self, event):
        game_world.remove_collision_object(self.character)

    def do(self):
        dt = game_framework.frame_time
        self.elapsed_time += dt

        if self.knockback_distance != 0 and self.elapsed_time < self.hit_duration:
            push_speed = self.knockback_distance / self.hit_duration
            self.character.x += self.knockback_dir * push_speed * dt

        if self.is_knockback:
            prev_bottom = None
            if self.was_in_air:
                _, prev_bottom, _, _ = self.get_bb()

            if self.chain_force_knockdown:
                knockback_frames = self.character.config.knockback_frames
                if len(knockback_frames) > 0:
                    self.character.frame = len(knockback_frames) - 1

                if self.was_in_air:
                    self.vy -= 2 * GRAVITY_PPS2 * dt
                    self.character.y += self.vy * dt
                    self.check_landing(prev_bottom)
                    if self.was_in_air:
                        return

                if not self.is_lying_down:
                    self.is_lying_down = True
                    self.elapsed_time = 0.0
                    return

                if self.elapsed_time < KNOCKBACK_DOWN_TIME:
                    return
                else:
                    self.character.state_machine.add_event(('STAND_UP', 0))
                    return

            if self.elapsed_time < self.hit_duration:
                knockback_frames = self.character.config.knockback_frames
                frames_per_action = len(knockback_frames)
                self.character.frame = (self.character.frame + frames_per_action * ACTION_PER_TIME
                                        * HIT_ANIMATION_SPEED * dt ) % frames_per_action
                if self.was_in_air:
                    self.vy -= GRAVITY_PPS2 * dt
                    self.character.y += self.vy * dt
                    self.check_landing(prev_bottom)
            else:
                if self.will_knockdown:
                    if self.was_in_air:
                        self.vy -= GRAVITY_PPS2 * dt
                        self.character.y += self.vy * dt
                        self.check_landing(prev_bottom)
                        if self.was_in_air:
                            return
                    if self.elapsed_time < self.hit_duration + KNOCKBACK_DOWN_TIME:
                        if not self.is_lying_down:
                            self.is_lying_down = True
                            knockback_frames = self.character.config.knockback_frames
                            self.character.frame = len(knockback_frames) - 1
                    else:
                        self.character.state_machine.add_event(('STAND_UP', 0))
                else:
                    if not self.chain_force_knockdown:
                        if self.was_in_air:
                            self.character.state_machine.add_event(('RESUME_JUMP', self.ground_y))
                        else:
                            self.character.state_machine.add_event(('HIT_END', 0))
        else:
            hit_frames = self.character.config.hit_frames
            frames_per_action = len(hit_frames)

            if self.chain_active:
                if not self.chain_hold_last:
                    self.character.frame = ( self.character.frame + frames_per_action * ACTION_PER_TIME
                                             * HIT_ANIMATION_SPEED * dt ) % frames_per_action
                    if self.elapsed_time >= self.hit_duration:
                        self.hold_last_frame()
                        if frames_per_action > 0:
                            self.character.frame = frames_per_action - 1
                else:
                    if frames_per_action > 0:
                        self.character.frame = frames_per_action - 1
                return
            self.character.frame = ( self.character.frame + frames_per_action * ACTION_PER_TIME
                                     * HIT_ANIMATION_SPEED * dt ) % frames_per_action
            if self.elapsed_time >= self.hit_duration:
                if self.chain_active or self.chain_force_knockdown:
                    return
                if self.was_in_air:
                    self.character.state_machine.add_event(('RESUME_JUMP', self.ground_y))
                else:
                    self.character.state_machine.add_event(('HIT_END', 0))

    def replay_hit(self):
        self.elapsed_time = 0.0
        self.character.frame = 0
        self.chain_hold_last = False

    def hold_last_frame(self):
        self.chain_hold_last = True

    def set_chain_with_knockdown(self, knockback_distance=60, knockback_dir=0):
        self.chain_active = False
        self.chain_hold_last = False
        self.chain_force_knockdown = True
        self.character.naruto_special_chain_active = False

        self.is_knockback = True
        self.knockback_distance = knockback_distance
        self.knockback_dir = knockback_dir
        self.will_knockdown = True
        self.was_in_air = True
        self.vy = 0.0
        self.elapsed_time = 0.0

    def check_landing(self, prev_bottom):
        if not (hasattr(self.character, 'stage') and self.character.stage is not None):
            return

        left, bottom, right, top = self.get_bb()

        if hasattr(self.character.stage, 'find_landing_platform'):
            ground_top = self.character.stage.find_landing_platform(left, prev_bottom, right, bottom, self.vy)
        else:
            ground_top = None

        if ground_top is not None:
            dy = ground_top - bottom
            self.character.y += dy

            self.vy = 0.0
            self.was_in_air = False
            self.ground_y = ground_top

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

        base_y = self.character.y + self.character.config.draw_offset_y
        draw_y = base_y + (self.character.config.knockback_draw_offset_y if self.is_knockback else 0)

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
        if self.is_knockback and hasattr(self.character.config, 'knockback_draw_offset_y'):
            y_offset += self.character.config.knockback_draw_offset_y

        return (
            self.character.x - width / 2 + x_offset,
            self.character.y - height / 2 + y_offset,
            self.character.x + width / 2 + x_offset,
            self.character.y + height / 2 + y_offset
        )
