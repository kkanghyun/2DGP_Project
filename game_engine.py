from pico2d import *
import game_input
import game_world
from player import Player


def init():
    global game_enable

    game_enable = True
    init_world()

    return True


def run():
    while game_enable:
        game_input.handle_events()
        update_world()
        render_world()
        delay(0.01)
        
        
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