import game_framework
import game_world
from pico2d import *
from background import Background
from player import Player


def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        else:
            player.handle_event(event)


def init():
    global background
    global player

    background = Background()
    game_world.add_object(background, 1)

    player = Player()
    game_world.add_object(player, 1)


def finish():
    game_world.clear()
    pass


def update():
    game_world.update()


def draw():
    clear_canvas()
    game_world.render()
    update_canvas()
    pico2d.delay(0.01)


def pause():
    pass


def resume():
    pass