import time


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


def run(start_mode):
    global running, stack
    global delta_time
    running = True
    stack = [start_mode]
    start_mode.init()

    delta_time = 0.0
    current_time = time.time()
    while (running):

        stack[-1].handle_events()
        stack[-1].update()
        stack[-1].draw()
        
        delta_time = time.time() - current_time     # 한 장의 프레임을 만드는데 걸리는 시간
        current_time += delta_time
        # frame_rate = 1.0 / delta_time     # 초당 프레임 개수

    # repeatedly delete the top of the stack
    while (len(stack) > 0):
        stack[-1].finish()
        stack.pop()
