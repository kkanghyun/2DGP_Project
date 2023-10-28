from pico2d import *
import game_input


def init():
    global game_enable

    game_enable = True

    return True


def run():
    while game_enable:
        game_input.handle_events()
        