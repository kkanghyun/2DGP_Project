from pico2d import *
import game_world
from player import Player
from constant_value import SCREEN_W, SCREEN_H


def init():
    global game_enable

    game_enable = True
    open_canvas(SCREEN_W, SCREEN_H)
    init_world()

    return True


def run():
    while game_enable:
        handle_events()
        update_world()
        render_world()
        delay(0.01)

    close_canvas()
        

def handle_events():
    global game_enable

    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_enable = False
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_enable = False
        else:
            player.handle_event(event)
        

def init_world():
    global player

    player = Player()
    game_world.add_object(player, 1)


def update_world():
    game_world.update_object()
    pass


def render_world():
    clear_canvas()
    game_world.render_object()
    update_canvas()