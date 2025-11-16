import time

running = None
stack = None

frame_time = 0.0
hitstop_time = 0.0

def change_mode(mode):
    global stack
    if (len(stack) > 0):
        # execute the current mode's finish function
        stack[-1].finish()
        # remove the current mode
        stack.pop()
    stack.append(mode)
    mode.init()


def push_mode(mode):
    global stack
    if (len(stack) > 0):
        stack[-1].pause()
    stack.append(mode)
    mode.init()


def pop_mode():
    global stack
    if (len(stack) > 0):
        # execute the current mode's finish function
        stack[-1].finish()
        # remove the current mode
        stack.pop()

    # execute resume function of the previous mode
    if (len(stack) > 0):
        stack[-1].resume()


def quit():
    global running
    running = False

def add_hitstop(frames):
    global hitstop_time
    seconds = frames / 60.0
    # 이미 더 긴 hitstop이 걸려 있다면 덮어쓰지 않음
    if seconds > hitstop_time:
        hitstop_time = seconds

def run(start_mode):
    global running, stack
    running = True
    stack = [start_mode]
    start_mode.init()

    global frame_time, hitstop_time
    frame_time = 0.0
    current_time = time.time()
    while running:
        now = time.time()
        frame_time = now - current_time
        current_time = now

        stack[-1].handle_events()

        if hitstop_time > 0.0:
            hitstop_time -= frame_time
            if hitstop_time < 0.0:
                hitstop_time = 0.0
            stack[-1].draw()
            continue

        stack[-1].update()
        stack[-1].draw()

        frame_rate = 1.0 / frame_time if frame_time > 0 else 0

    # repeatedly delete the top of the stack
    while (len(stack) > 0):
        stack[-1].finish()
        stack.pop()
