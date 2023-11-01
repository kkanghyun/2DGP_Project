from pico2d import *

import game_world
from player import Player


# Game object class here


def handle_events():
    global running

    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            running = False
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            running = False
        else:
            player.handle_event(event)


def create_world():
    global running
    global player

    running = True

    player = Player()
    game_world.add_object(player, 1)


open_canvas()
create_world()
# game loop
while running:
    handle_events()
    game_world.update()
    clear_canvas()
    game_world.render()
    update_canvas()
    delay(0.01)
# finalization code
close_canvas()
