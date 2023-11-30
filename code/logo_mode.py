from pico2d import clear_canvas, update_canvas, get_events, get_time
from game_utility import load_image, SCREEN_W, SCREEN_H
import game_engine
import title_mode


def init():
    global image_background
    global image_signature
    global running
    global logo_start_time

    running = True
    image_background = load_image('background_white.png')
    image_signature = load_image('signature.jpg')
    image_signature.opacify(0)
    logo_start_time = get_time()


def update():
    if get_time() - logo_start_time >= 3.0:
        game_engine.change_mode(title_mode)


def draw():
    global image_background
    global image_signature

    clear_canvas()
    image_background.draw(SCREEN_W // 2, SCREEN_H // 2)
    image_signature.draw(SCREEN_W // 2, SCREEN_H // 2)
    update_canvas()


def finish():
    pass


def handle_events():
    pass