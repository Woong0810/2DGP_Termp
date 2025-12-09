from pico2d import SDL_KEYDOWN, SDL_KEYUP
from types import SimpleNamespace

import game_framework
from behavior_tree import BehaviorTree, Selector, Sequence, Condition, Action
from character import Character


class AiCharacter(Character):
    CLOSE_RANGE = 50.0
    MID_RANGE = 300.0
    FAR_RANGE = 450.0

    GUARD_DURATION = 0.4
    MOVE_PULSE = 0.30
    ATTACK_COOLDOWN = 0.5
    RANGED_COOLDOWN = 10.0
    DASH_COOLDOWN = 3.0

    WAIT_MIN = 0.3
    WAIT_MAX = 1.0
    BACK_STEP_CHANCE = 0.15

    def __init__(self, character_config=None, key_bindings=None, x=400, y=90, stage=None):
        super().__init__(character_config, key_bindings, x, y, stage)

        self.bt = self.build_behavior_tree()

        self.move_dir = 0
        self.move_timer = 0.0

        self.guarding = False
        self.guard_timer = 0.0

        self.attack_cooldown = 0.0
        self.ranged_cooldown = 0.0
        self.dash_cooldown = 0.0

        self.wait_timer = 0.0
        self.backing_off = False
        self.back_timer = 0.0

    def build_behavior_tree(self):
        main_logic = Selector("메인 로직",
            Sequence("필살기 쓰기",
                Condition("필살기 사용 가능", self.can_use_special_check),
                Condition("상대와 Y좌표 같음", self.is_same_y),
                Action("필살기 사용", self.use_special),
            ),
            Sequence("위험 방어",
                Condition("상대 공격 중", self.is_opponent_attacking),
                Condition("근거리", self.is_close),
                Action("방어", self.guard),
            ),
            Sequence("점프 공격",
                Condition("근거리", self.is_close),
                Condition("상대 방어 중", self.is_opponent_defending),
                Action("점프 후 공격", self.jump_attack),
            ),
            Sequence("근거리 콤보",
                Condition("근거리", self.is_close),
                Condition("상대 공격 가능", self.is_opponent_attackable),
                Action("지상 콤보", self.ground_combo),
            ),
            Sequence("중거리",
                Condition("중거리", self.is_mid),
                Selector("중거리 전략",
                    Sequence("후퇴",
                        Condition("후퇴 중", self.is_backing_off),
                        Action("뒤로 물러나기", self.back_off),
                    ),
                    Sequence("관찰 대기",
                        Condition("대기 중", self.is_waiting),
                        Action("잠시 관찰", self.wait_and_watch),
                    ),
                    Action("접근", self.approach),
                ),
            ),
            Sequence("원거리",
                Condition("거리가 충분히 먼지", self.is_far),
                Selector("원거리 공격할지 접근할지",
                    Sequence("원거리 공격",
                        Condition("원거리 공격 가능", self.is_ranged_ready),
                        Action("수리검", self.throw_shuriken),
                    ),
                    Selector("접근 방법",
                        Sequence("대쉬 접근",
                            Condition("대쉬 가능", self.is_dash_ready),
                            Action("대쉬", self.dash),
                        ),
                        Action("걸어서 접근", self.approach),
                    ),
                ),
            ),
        )

        root = Selector("루트",
            Sequence("제어 및 로직",
                Condition("제어 가능", self.can_control),
                main_logic
            ),
            Action("대기", self.do_idle)
        )

        return BehaviorTree(root)

    def update(self):
        if self.hp <= 0:
            super().update()
            return

        self.update_timers()

        if self.opponent is not None:
            self.bt.run()

        super().update()

    def update_timers(self):
        dt = game_framework.frame_time

        if self.move_dir != 0:
            self.move_timer -= dt
            if self.move_timer <= 0.0:
                key = self.key_bindings['right'] if self.move_dir == 1 else self.key_bindings['left']
                self.send_key(key, down=False)
                self.move_dir = 0

        if self.guarding:
            self.guard_timer -= dt
            if self.guard_timer <= 0.0:
                self.send_key(self.key_bindings['down'], down=False)
                self.guarding = False

        if self.attack_cooldown > 0.0:
            self.attack_cooldown -= dt

        if self.ranged_cooldown > 0.0:
            self.ranged_cooldown -= dt

        if self.dash_cooldown > 0.0:
            self.dash_cooldown -= dt

        if self.wait_timer > 0.0:
            self.wait_timer -= dt

        if self.backing_off:
            self.back_timer -= dt
            if self.back_timer <= 0.0:
                self.backing_off = False

    def send_key(self, key, down=True):
        ev_type = SDL_KEYDOWN if down else SDL_KEYUP
        ev = SimpleNamespace(type=ev_type, key=key)
        self.handle_event(ev)

    def get_distance(self):
        return abs(self.x - self.opponent.x)

    def face_opponent(self):
        if self.x < self.opponent.x:
            self.face_dir = 1
        elif self.x > self.opponent.x:
            self.face_dir = -1

    def start_move(self, direction):
        kb = self.key_bindings

        if self.move_dir == direction:
            self.move_timer = self.MOVE_PULSE
            return

        if self.move_dir != 0 and self.move_dir != direction:
            old_key = kb['right'] if self.move_dir == 1 else kb['left']
            self.send_key(old_key, down=False)

        key = kb['right'] if direction == 1 else kb['left']
        self.send_key(key, down=True)

        self.move_dir = direction
        self.move_timer = self.MOVE_PULSE

    def can_control(self):
        cs = self.state_machine.cur_state
        controllable_states = (self.IDLE, self.RUN, self.JUMP, self.DEFENSE)
        if cs in controllable_states:
            return BehaviorTree.SUCCESS
        return BehaviorTree.FAIL

    def can_use_special_check(self):
        return BehaviorTree.SUCCESS if self.can_use_special_attack() else BehaviorTree.FAIL

    def is_same_y(self):
        if abs(self.y - self.opponent.y) < 10:
            return BehaviorTree.SUCCESS
        return BehaviorTree.FAIL

    def is_close(self):
        d = self.get_distance()
        return BehaviorTree.SUCCESS if d < self.CLOSE_RANGE else BehaviorTree.FAIL

    def is_mid(self):
        d = self.get_distance()
        return BehaviorTree.SUCCESS if self.CLOSE_RANGE <= d < self.MID_RANGE else BehaviorTree.FAIL

    def is_far(self):
        d = self.get_distance()
        return BehaviorTree.SUCCESS if d >= self.MID_RANGE else BehaviorTree.FAIL

    def is_opponent_attacking(self):

        opp = self.opponent
        cs = opp.state_machine.cur_state
        attack_states = (
            opp.NORMAL_ATTACK,
            opp.JUMP_ATTACK,
            opp.RANGED_ATTACK,
        )

        if cs in attack_states:
            return BehaviorTree.SUCCESS
        return BehaviorTree.FAIL

    def is_attack_ready(self):
        return BehaviorTree.SUCCESS if self.attack_cooldown <= 0.0 else BehaviorTree.FAIL

    def is_ranged_ready(self):
        return BehaviorTree.SUCCESS if self.ranged_cooldown <= 0.0 else BehaviorTree.FAIL

    def is_dash_ready(self):
        return BehaviorTree.SUCCESS if self.dash_cooldown <= 0.0 else BehaviorTree.FAIL

    def is_waiting(self):
        return BehaviorTree.SUCCESS if self.wait_timer > 0.0 else BehaviorTree.FAIL

    def is_backing_off(self):
        return BehaviorTree.SUCCESS if self.backing_off else BehaviorTree.FAIL

    def is_opponent_attackable(self):
        opp = self.opponent
        cs = opp.state_machine.cur_state
        unattackable_states = (opp.HIT, opp.STAND_UP)

        if cs in unattackable_states:
            return BehaviorTree.FAIL
        return BehaviorTree.SUCCESS

    def is_opponent_defending(self):
        opp = self.opponent
        cs = opp.state_machine.cur_state

        if cs == opp.DEFENSE:
            return BehaviorTree.SUCCESS
        return BehaviorTree.FAIL

    def do_idle(self):
        return BehaviorTree.RUNNING

    def use_special(self):
        if not self.can_use_special_attack():
            return BehaviorTree.FAIL

        self.face_opponent()
        key = self.key_bindings['special']

        self.send_key(key, down=True)
        self.send_key(key, down=False)

        return BehaviorTree.SUCCESS

    def guard(self):
        kb = self.key_bindings
        down_key = kb['down']

        if not self.guarding:
            self.send_key(down_key, down=True)

        self.guarding = True
        self.guard_timer = self.GUARD_DURATION

        return BehaviorTree.RUNNING

    def ground_combo(self):
        if self.attack_cooldown > 0.0:
            return BehaviorTree.FAIL

        kb = self.key_bindings
        atk = kb['attack']

        self.face_opponent()
        self.send_key(atk, down=True)
        self.send_key(atk, down=False)

        self.attack_cooldown = self.ATTACK_COOLDOWN

        import random
        if random.random() < self.BACK_STEP_CHANCE:
            self.backing_off = True
            self.back_timer = 0.5

        return BehaviorTree.SUCCESS

    def wait_and_watch(self):
        return BehaviorTree.RUNNING

    def back_off(self):
        direction = -1 if self.x < self.opponent.x else 1
        self.start_move(direction)
        return BehaviorTree.RUNNING

    def approach(self):
        import random

        if self.wait_timer <= 0.0 and random.random() < 0.2:
            self.wait_timer = random.uniform(self.WAIT_MIN, self.WAIT_MAX)
            return BehaviorTree.SUCCESS

        direction = 1 if self.x < self.opponent.x else -1
        self.face_opponent()
        self.start_move(direction)

        return BehaviorTree.RUNNING

    def throw_shuriken(self):
        self.face_opponent()

        self.send_key(self.key_bindings['ranged'], down=True)
        self.send_key(self.key_bindings['ranged'], down=False)

        self.ranged_cooldown = self.RANGED_COOLDOWN

        return BehaviorTree.SUCCESS

    def dash(self):
        self.face_opponent()

        self.send_key(self.key_bindings['dash'], down=True)
        self.send_key(self.key_bindings['dash'], down=False)

        self.dash_cooldown = self.DASH_COOLDOWN

        return BehaviorTree.SUCCESS

    def jump_attack(self):
        self.face_opponent()

        self.send_key(self.key_bindings['jump_key'], down=True)
        self.send_key(self.key_bindings['jump_key'], down=False)

        self.send_key(self.key_bindings['attack'], down=True)
        self.send_key(self.key_bindings['attack'], down=False)

        return BehaviorTree.SUCCESS

