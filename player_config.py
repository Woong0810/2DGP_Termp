from sdl2 import SDLK_LEFT, SDLK_RIGHT, SDLK_UP, SDLK_DOWN
from sdl2 import SDLK_j, SDLK_k, SDLK_l, SDLK_u, SDLK_i, SDLK_o
from sdl2 import SDLK_a, SDLK_d, SDLK_w, SDLK_s
from sdl2 import SDLK_b, SDLK_c, SDLK_v, SDLK_g, SDLK_f, SDLK_h

# Player 2 키 바인딩 (방향키 + J, K, L, U, I, O)
PLAYER2_KEY_BINDINGS = {
    'left': SDLK_LEFT,
    'right': SDLK_RIGHT,
    'up': SDLK_UP,
    'down': SDLK_DOWN,
    'attack': SDLK_j,      # 일반공격
    'jump_key': SDLK_k,    # 점프 (UP키와 별도)
    'dash': SDLK_l,        # 대쉬
    'ranged': SDLK_u,      # 원거리공격
    'special': SDLK_i,     # 필살기1
    'special2': SDLK_o     # 필살기2
}

# Player 1 키 바인딩 (WASD + C, V, B, F, G, H)
PLAYER1_KEY_BINDINGS = {
    'left': SDLK_a,
    'right': SDLK_d,
    'up': SDLK_w,
    'down': SDLK_s,
    'attack': SDLK_c,      # 일반공격
    'jump_key': SDLK_v,    # 점프
    'ranged': SDLK_f,      # 원거리공격
    'dash': SDLK_b,        # 대쉬
    'special': SDLK_g,     # 필살기1
    'special2': SDLK_h     # 필살기2
}


def get_player_key_bindings(player_number):
    if player_number == 1:
        return PLAYER1_KEY_BINDINGS
    elif player_number == 2:
        return PLAYER2_KEY_BINDINGS
    else:
        raise ValueError(f"Invalid player number: {player_number}")
