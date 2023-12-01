from pico2d import clear_canvas, update_canvas, get_events, get_time
from game_utility import load_image, SCREEN_W, SCREEN_H
from background import Background

import game_engine
import title_mode


def init():
    global background
    global signature
    global running
    global current_time
    global opacify_value

    running = True
    background = Background()
    background.set_image('background_white.png')
    signature = load_image('signature.png')
    opacify_value = 0.0
    signature.opacify(opacify_value)

    current_time = get_time()


def update():
    global signature
    global current_time
    global opacify_value
    
    t = get_time() - current_time
    if t >= 10.0:
        game_engine.change_mode(title_mode)
        return

    if t > 1.0:
        if t > 4.0:
            if t > 6.0:
                opacify_value -= (1.0 / 3) * game_engine.delta_time
                if opacify_value <= 0.0:
                    opacify_value = 0.0
        else:
            opacify_value += (1.0 / 3) * game_engine.delta_time
            if opacify_value >= 1.0:
                opacify_value = 1.0
        
        signature.opacify(opacify_value)


def draw():
    global background
    global signature

    clear_canvas()
    background.draw()
    signature.draw(SCREEN_W // 2, SCREEN_H // 2)
    update_canvas()


def finish():
    pass


def handle_events():
    pass