from pico2d import load_font
import game_framework
from camera import camera

ROUND_INTRO_DURATION = 2.0
ROUND_END_DURATION   = 3.0

class RoundManager:
    STATE_INTRO = 0
    STATE_PLAY = 1
    STATE_END = 2
    STATE_MATCH_OVER = 3

    def __init__(self, p1, p2, stage, p1_spawn, p2_spawn, round_timer):
        self.p1 = p1
        self.p2 = p2
        self.stage = stage
        self.round_timer = round_timer

        self.p1_spawn = p1_spawn
        self.p2_spawn = p2_spawn

        self.current_round = 1
        self.p1_wins = 0
        self.p2_wins = 0

        self.state = RoundManager.STATE_INTRO
        self.timer = 0.0
        self.winner = None

        self.font_big = load_font('font.ttf', 60)
        self.font_small = load_font('font.ttf', 30)

        from pico2d import load_wav
        self.round_1_sound = load_wav('sound/round_1.wav')
        self.round_2_sound = load_wav('sound/round_2.wav')
        self.round_3_sound = load_wav('sound/round_3.wav')
        self.winner_sound = load_wav('sound/winner.wav')

        for sound in [self.round_1_sound, self.round_2_sound, self.round_3_sound, self.winner_sound]:
            sound.set_volume(64)

    def start_first_round(self):
        self.current_round = 1
        self.p1_wins = 0
        self.p2_wins = 0
        self.start_round(reset_score=False)

    def start_round(self, reset_score=False):
        self.state = RoundManager.STATE_INTRO
        self.timer = 0.0
        self.winner = None
        self.round_timer.reset()

        self.reset_character_for_round(self.p1, self.p1_spawn)
        self.reset_character_for_round(self.p2, self.p2_spawn)

        camera.set_targets(self.p1, self.p2)
        camera.initialized = True

        if self.current_round == 1:
            self.round_1_sound.play()
        elif self.current_round == 2:
            self.round_2_sound.play()
        elif self.current_round == 3:
            self.round_3_sound.play()

    def reset_character_for_round(self, ch, spawn_pos):
        ch.x, ch.y = spawn_pos
        ch.hp = ch.max_hp
        ch.invincible_time = 0.0
        ch.special_gauge = 0.0
        ch.jump_count = 0
        ch.special_chain_active = False

        ch.state_machine.cur_state.exit(('ROUND_RESET', None))
        ch.state_machine.prev_state = ch.state_machine.cur_state
        ch.state_machine.cur_state = ch.IDLE
        ch.IDLE.enter(('START', None))

        ch.align_to_stage()

    def update(self):
        dt = game_framework.frame_time
        self.timer += dt

        if self.state == RoundManager.STATE_INTRO:
            if self.timer >= ROUND_INTRO_DURATION:
                self.state = RoundManager.STATE_PLAY
                self.timer = 0.0

        elif self.state == RoundManager.STATE_PLAY:
            pass

        elif self.state == RoundManager.STATE_END:
            if self.timer >= ROUND_END_DURATION:
                self.decide_next()

        elif self.state == RoundManager.STATE_MATCH_OVER:
            pass

    def on_round_end(self, winner_str):
        if self.state != RoundManager.STATE_PLAY:
            return

        if winner_str == 'player1':
            self.winner = self.p1
            self.p1_wins += 1
        elif winner_str == 'player2':
            self.winner = self.p2
            self.p2_wins += 1
        else:
            self.winner = None

        if self.winner is not None:
            camera.set_targets(self.winner, self.winner)
            camera.initialized = True
            self.winner_sound.play()

        self.state = RoundManager.STATE_END
        self.timer = 0.0

    def is_match_over(self):
        if self.p1_wins >= 2 or self.p2_wins >= 2:
            return True
        if self.current_round >= 3:
            return True
        return False

    def decide_next(self):
        if self.is_match_over():
            self.state = RoundManager.STATE_MATCH_OVER
            self.timer = 0.0
        else:
            self.current_round += 1
            self.start_round(reset_score=False)

    def can_control(self):
        return self.state == RoundManager.STATE_PLAY

    def draw_ui(self):
        score_text = f"P1 {self.p1_wins}"
        self.draw_bold_text(self.font_small, 20, 500, score_text, (255, 255, 255), thickness=1)

        score_text = f"{self.p2_wins} P2"
        self.draw_bold_text(self.font_small, 730, 500, score_text, (255, 255, 255), thickness=1)

        if self.state == RoundManager.STATE_INTRO:
            msg = f"ROUND {self.current_round}"
            self.draw_bold_text(self.font_big, 280, 300, msg, (255, 0, 0), thickness=3)

        elif self.state in (RoundManager.STATE_END, RoundManager.STATE_MATCH_OVER):
            if self.winner is self.p1:
                msg = "PLAYER 1 WINS"
                self.draw_bold_text(self.font_big, 200, 300, msg, (255, 215, 0), thickness=2)
            elif self.winner is self.p2:
                msg = "PLAYER 2 WINS"
                self.draw_bold_text(self.font_big, 200, 300, msg, (255, 215, 0), thickness=2)
            else:
                msg = "DRAW"
                self.draw_bold_text(self.font_big, 330, 300, msg, (255, 215, 0), thickness=2)

    def draw_bold_text(self, font, x, y, text, color, thickness=1):
        for dx in range(-thickness, thickness + 1):
            for dy in range(-thickness, thickness + 1):
                font.draw(x + dx, y + dy, text, color)
