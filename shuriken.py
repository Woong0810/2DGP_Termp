from pico2d import load_image, draw_rectangle
import game_framework
import game_world

class Shuriken:
    image = None
    FRAME = {'left': 0, 'bottom': 0, 'width': 26, 'height': 26}

    def __init__(self, owner, x, y, direction, speed=300):
        if Shuriken.image is None:
            Shuriken.image = load_image('shuriken.png')

        self.owner = owner
        self.x = x
        self.y = y
        self.direction = direction
        self.speed = speed
        self.rotation = 0  # 회전 각도
        self.rotation_speed = 720  # 초당 회전 속도 (도)

        game_world.add_collision_pairs('shuriken:character', self, None)

    def update(self):
        self.x += self.speed * self.direction * game_framework.frame_time
        self.rotation += self.rotation_speed * game_framework.frame_time

        if self.x < -50 or self.x > 850:
            game_world.remove_object(self)

    def draw(self):
        l, b, w, h = Shuriken.FRAME['left'], Shuriken.FRAME['bottom'], Shuriken.FRAME['width'], Shuriken.FRAME['height']

        self.image.clip_composite_draw(
            l, b, w, h,
            self.rotation * 3.141592 / 180.0,
            '' if self.direction == 1 else 'h',
            self.x, self.y,
            w * 2, h * 2
        )

        draw_rectangle(*self.get_bb())

    def get_bb(self):
        size = 25
        return (
            self.x - size,
            self.y - size,
            self.x + size,
            self.y + size
        )

    def handle_collision(self, group, other):
        # 자신이 발사한 캐릭터와는 충돌하지 않음
        if other == self.owner:
            return

        # 상대 캐릭터와 충돌 시 제거
        if group == 'shuriken:character':
            print(f"Shuriken hit {other.config.name}!")
            game_world.remove_object(self)
            # TODO: 데미지 처리 추가
