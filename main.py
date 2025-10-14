from pico2d import *
# from naruto_frames import FRAMES
from characters_itachi_frames import FRAMES

open_canvas(800, 600)
# img = load_image('Characters_Naruto_clean.png')
img = load_image('Characters_Itachi_clean.png')

while True:
    for frame in FRAMES:
        clear_canvas()
        img.clip_draw(frame['left'], frame['bottom'], frame['width'], frame['height'], 400, 300)
        update_canvas()
        delay(0.1)

close_canvas()