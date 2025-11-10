"""
플레이어별 키 바인딩 설정
캐릭터와 독립적으로 플레이어 번호에 따라 키 바인딩을 제공
"""
from sdl2 import SDLK_LEFT, SDLK_RIGHT, SDLK_UP, SDLK_DOWN
from sdl2 import SDLK_p, SDLK_i, SDLK_o
from sdl2 import SDLK_a, SDLK_d, SDLK_w, SDLK_s
from sdl2 import SDLK_u, SDLK_f, SDLK_g

# Player 1 키 바인딩 (방향키 + P, I, O)
PLAYER1_KEY_BINDINGS = {
    'left': SDLK_LEFT,
    'right': SDLK_RIGHT,
    'up': SDLK_UP,
    'down': SDLK_DOWN,
    'attack': SDLK_p,
    'special': SDLK_i,
    'ranged': SDLK_o
}

# Player 2 키 바인딩 (WASD + U, F, G)
PLAYER2_KEY_BINDINGS = {
    'left': SDLK_a,
    'right': SDLK_d,
    'up': SDLK_w,
    'down': SDLK_s,
    'attack': SDLK_u,
    'special': SDLK_f,
    'ranged': SDLK_g
}

def get_player_key_bindings(player_number):
    if player_number == 1:
        return PLAYER1_KEY_BINDINGS
    elif player_number == 2:
        return PLAYER2_KEY_BINDINGS
    else:
        raise ValueError(f"Invalid player number: {player_number}")


