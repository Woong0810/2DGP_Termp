from event_to_string import event_to_string

class StateMachine:
    def __init__(self, initial_state, rules):
        self.cur_state = initial_state
        self.rules = rules
        self.cur_state.enter()
    def update(self):
        self.cur_state.do()
    def draw(self):
        self.cur_state.draw()
    def handle_event(self, state_event):
        pass

