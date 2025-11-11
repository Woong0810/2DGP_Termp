from pico2d import *
import game_framework
import title_mode

image = None
winner = None

def init():
    global image
    if winner == 'player1':
        image = load_image('player1_win.png')
    elif winner == 'player2':
        image = load_image('player2_win.png')
    else:
        image = load_image('player1_player2_draw.png')  # 무승부

def update():
    pass

def draw():
    clear_canvas()
    image.draw(400, 300)
    update_canvas()

def finish():
    global image
    del image

def handle_events():
    event_list = get_events()
    for event in event_list:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_SPACE:
            game_framework.change_mode(title_mode)

def pause():
    pass

def resume():
    pass

def set_winner(winner_name):
    global winner
    winner = winner_name

