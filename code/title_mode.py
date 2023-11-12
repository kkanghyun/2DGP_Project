from pico2d import clear_canvas, update_canvas, get_events, get_time, SDL_QUIT, SDL_KEYDOWN, SDLK_ESCAPE, SDLK_RETURN, SDLK_SPACE
from game_utility import load_image, SCREEN_W, SCREEN_H
import game_engine
import play_mode
from background import Background


def init():
    global background
    global press_start
    global current_time

    background = Background()
    background.set_image('title_back.png')

    press_start = load_image('press_start.png')
    
    current_time = get_time()


def update():
    global current_time
    global press_start

    if get_time() - current_time >= 1.0:
        if press_start == None:
            press_start = load_image('press_start.png')
        else:
            press_start = None
        
        current_time = get_time()


def draw():
    clear_canvas()
    background.draw()
    if press_start:
        press_start.draw(SCREEN_W // 2, SCREEN_H // 4)
    update_canvas()


def finish():
    pass


def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_engine.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_engine.quit()
        elif event.type == SDL_KEYDOWN and (event.key == SDLK_RETURN or event.key == SDLK_SPACE):
            game_engine.change_mode(play_mode)