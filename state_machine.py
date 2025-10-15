class StateMachine:
    def __init__(self, initial_state):
        self.cur_state = initial_state
        self.cur_state.enter()
    def update(self):
        self.cur_state.do()
    def draw(self):
        self.cur_state.draw()
