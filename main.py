from pico2d import *

open_canvas(800, 600)
img = load_image('Characters_Naruto.png')

frames = [
    {'left': 0, 'bottom': 1938, 'width': 56, 'height': 48},
    {'left': 58, 'bottom': 1938, 'width': 56, 'height': 48},
    {'left': 116, 'bottom': 1938, 'width': 56, 'height': 48},
    {'left': 174, 'bottom': 1938, 'width': 56, 'height': 48},
    {'left': 0, 'bottom': 1888, 'width': 48, 'height': 48},
]
while True:
    clear_canvas()
    for frame in frames:
        img.clip_draw(frame['left'], frame['bottom'], frame['width'], frame['height'], 400, 300)
        update_canvas()
        delay(0.1)

close_canvas()