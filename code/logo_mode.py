from pico2d import clear_canvas, update_canvas, get_events, get_time
from game_utility import load_image, SCREEN_W, SCREEN_H
import game_engine
import play_mode


def init():
    global image
    global running
    global logo_start_time

    running = True
    image = load_image('tuk_credit.png')
    image.opacify(0)
    logo_start_time = get_time()


def update():
    if get_time() - logo_start_time >= 3.0:
        game_engine.change_mode(play_mode)


def draw():
    clear_canvas()
    image.draw(SCREEN_W // 2, SCREEN_H // 2, SCREEN_W, SCREEN_H)
    update_canvas()


def finish():
    pass


def handle_events():
    pass