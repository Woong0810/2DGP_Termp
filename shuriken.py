from pico2d import load_image, draw_rectangle
import game_framework
import game_world
from camera import camera

class Shuriken:
    _image_cache = {}

    def __init__(self, owner, x, y, direction, speed=None):
        self.owner = owner
        cfg = getattr(owner, 'config', None)
        sh_cfg = cfg.shuriken if cfg and hasattr(cfg, 'shuriken') else {}

        image_path = sh_cfg.get('image_path') if sh_cfg.get('image_path') else 'shuriken.png'
        if image_path not in Shuriken._image_cache:
            Shuriken._image_cache[image_path] = load_image(image_path)
        self.image = Shuriken._image_cache[image_path]

        self.speed = speed if speed is not None else sh_cfg.get('speed', 300)
        self.rotation = 0.0
        self.rotation_speed = sh_cfg.get('rotation_speed', 720)
        self.max_distance = sh_cfg.get('max_distance', 400)
        self.damage = sh_cfg.get('damage', 10)
        self.use_rotation = sh_cfg.get('use_rotation', True)

        draw_size = sh_cfg.get('draw_size')
        if draw_size:
            self.w, self.h = draw_size
        else:
            self.w, self.h = 26, 26

        self.bbox_size = sh_cfg.get('bbox_size', 20)

        self.x = x
        self.y = y
        self.start_x = x
        self.direction = direction

        game_world.add_collision_pairs('character:shuriken', None, self)

    def update(self):
        self.x += self.speed * self.direction * game_framework.frame_time
        if self.use_rotation:
            self.rotation += self.rotation_speed * game_framework.frame_time

        distance_traveled = abs(self.x - self.start_x)
        if distance_traveled >= self.max_distance:
            game_world.remove_object(self)
            return

    def draw(self):
        angle = self.rotation * 3.141592 / 180.0 if self.use_rotation else 0
        flip = '' if self.direction == 1 else 'h'

        sx, sy = camera.world_to_screen(self.x, self.y)
        self.image.clip_composite_draw(0, 0, self.w, self.h, angle, flip, sx, sy, self.w, self.h)
        left, bottom, right, top = self.get_bb()
        sx1, sy1 = camera.world_to_screen(left, bottom)
        sx2, sy2 = camera.world_to_screen(right, top)
        draw_rectangle(sx1, sy1, sx2, sy2)

    def get_bb(self):
        s = self.bbox_size
        return (self.x - s, self.y - s, self.x + s, self.y + s)

    def handle_collision(self, group, other):
        if other == self.owner:
            return

        game_world.remove_object(self)
