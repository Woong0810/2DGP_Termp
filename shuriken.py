from pico2d import load_image, draw_rectangle
import game_framework
import game_world

class Shuriken:
    image = None
    FRAME = {'left': 0, 'bottom': 0, 'width': 26, 'height': 26}

    def __init__(self, owner, x, y, direction, speed=300):
        self.owner = owner
        if owner.config.name == 'Itachi':
            Shuriken.image = load_image('shuriken2.png')
            self.speed = 600
            self.rotation = 0
            self.rotation_speed = 0
            self.max_distance = 400
            self.l, self.b, self.w, self.h = Shuriken.FRAME['left'], Shuriken.FRAME['bottom'], Shuriken.FRAME['width'], int(Shuriken.FRAME['height'] / 2)

        elif owner.config.name == 'Naruto':
            Shuriken.image = load_image('shuriken.png')
            self.speed = speed
            self.rotation = 0  # 회전 각도
            self.rotation_speed = 720  # 초당 회전 속도 (도)
            self.max_distance = 400
            self.l, self.b, self.w, self.h = Shuriken.FRAME['left'], Shuriken.FRAME['bottom'], Shuriken.FRAME['width'] * 2, Shuriken.FRAME['height'] * 2
        self.x = x
        self.y = y
        self.start_x = x
        self.direction = direction
        self.damage = 10

        game_world.add_collision_pairs('character:shuriken', None, self)

    def update(self):
        self.x += self.speed * self.direction * game_framework.frame_time
        self.rotation += self.rotation_speed * game_framework.frame_time

        distance_traveled = abs(self.x - self.start_x)
        if distance_traveled >= self.max_distance:
            game_world.remove_object(self)
            return

    def draw(self):

        self.image.clip_composite_draw(
            self.l, self.b, self.w, self.h,
            self.rotation * 3.141592 / 180.0,
            '' if self.direction == 1 else 'h',
            self.x, self.y,
            self.w, self.h
        )

        draw_rectangle(*self.get_bb())

    def get_bb(self):
        size = 20
        return (
            self.x - size,
            self.y - size,
            self.x + size,
            self.y + size
        )

    def handle_collision(self, group, other):
        if other == self.owner:
            return

        game_world.remove_object(self)
