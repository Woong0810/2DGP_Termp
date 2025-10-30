from event_to_string import event_to_string

class StateMachine:
    def __init__(self, initial_state, rules):
        self.cur_state = initial_state
        self.rules = rules
        self.cur_state.enter(('START', None))

    def update(self, dt):
        self.cur_state.do(dt)

    def draw(self):
        self.cur_state.draw()

    def add_event(self, state_event):
        """내부적으로 이벤트를 추가하는 메서드"""
        self.handle_event(state_event)

    def handle_event(self, state_event):
        for check_event in self.rules[self.cur_state].keys():
            if check_event(state_event):
                next_state = self.rules[self.cur_state][check_event]
                self.cur_state.exit(state_event)
                next_state.enter(state_event)
                print(f'{self.cur_state.__class__.__name__} ============== {event_to_string(state_event)} =============> {next_state.__class__.__name__}')
                self.cur_state = next_state
                return
        print(f'처리되지 않은 이벤트 {event_to_string(state_event)}가 있습니다')
