from pico2d import draw_rectangle

class Hit:
    def __init__(self, character):
        self.character = character
        self.hit_duration = 0.3
        self.elapsed_time = 0.0

    def enter(self, event):
        self.character.frame = 0
        self.elapsed_time = 0.0
        self.character.frame_duration = 0.15
        self.character.accum_time = 0.0

    def exit(self, event):
        pass

    def do(self, dt):
        self.elapsed_time += dt
        self.character.accum_time += dt

        if self.character.accum_time >= self.character.frame_duration:
            self.character.accum_time = 0.0
            self.character.frame = (self.character.frame + 1) % 2  # 47, 48 프레임 2개만 반복

        if self.elapsed_time >= self.hit_duration:
            from event_to_string import hit_end
            self.character.state_machine.add_event(('HIT_END', 0))

    def draw(self):
        HIT_FRAMES = [self.character.config.frames[idx] for idx in self.character.config.hit_frames]
        frame = HIT_FRAMES[self.character.frame]

        if self.character.face_dir == 1:
            self.character.image.clip_draw(
                frame['left'], frame['bottom'], frame['width'], frame['height'],
                self.character.x, self.character.y)
        else:
            self.character.image.clip_composite_draw(
                frame['left'], frame['bottom'], frame['width'], frame['height'],
                0, 'h', self.character.x, self.character.y, frame['width'], frame['height'])

    def get_bb(self):
        frame = self.character.config.frames[self.character.config.hit_frames[self.character.frame]]
        hitbox = self.character.config.hitbox_hit

        width = frame['width'] * hitbox['scale_x']
        height = frame['height'] * hitbox['scale_y']
        x_offset = hitbox['x_offset'] * self.character.face_dir
        y_offset = hitbox['y_offset']

        return (
            self.character.x - width / 2 + x_offset,
            self.character.y - height / 2 + y_offset,
            self.character.x + width / 2 + x_offset,
            self.character.y + height / 2 + y_offset
        )

    def draw_bb(self):
        """디버그용 바운딩 박스 그리기"""
        left, bottom, right, top = self.get_bb()
        draw_rectangle(left, bottom, right, top)
