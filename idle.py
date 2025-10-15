from characters_naruto_frames import FRAMES

class Idle:
    def __init__(self, naruto):
        self.naruto = naruto
    def enter(self):
        pass
    def exit(self):
        pass
    def do(self):
        self.naruto.frame = (self.naruto.frame + 1) % 8
    def draw(self):
        if self.naruto.face_dir == 1:
            frame = FRAMES[self.naruto.frame]
            self.naruto.image.clip_draw(frame['left'], frame['bottom'], frame['width'], frame['height'], self.naruto.x, self.naruto.y)
        # else:
        #     self.naruto.image.clip_draw(frame['left'], frame['bottom'], frame['width'], frame['height'], self.naruto.x, self.naruto.y)
