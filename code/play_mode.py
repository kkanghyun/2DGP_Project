from pico2d import *
from background import Background
from player import Player
from hurdle import Hurdle

import game_engine
import game_world
import random


def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_engine.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_engine.quit()
        else:
            player.handle_event(event)


def init():
    create_objects()


def finish():
    game_world.clear()
    pass


def update():
    game_world.update()
    game_world.handle_collisions()


def draw():
    clear_canvas()
    game_world.render()
    update_canvas()


def pause():
    pass


def resume():
    pass


def create_objects():
    create_background()
    create_hurdles()
    create_player()
    create_AI()


def create_background():
    global background

    background = Background()
    game_world.add_object(background, 0)


def create_hurdles():
    global hurdles
    
    hurdles = []
    for i in range(24):
        if i % 4 == 0 or i % 4 == 1:
            continue
        if random.randint(0, 100) <= 30:
            continue

        hurdle = Hurdle(200 + (104 / 3 + 2) * i, 80 + 8)
        hurdles.append(hurdle)

        
    game_world.add_objects(hurdles, 2)

    for hurdle in hurdles:
        hurdle.set_size(104 / 3, 91 / 3)
        hurdle.set_bb(-6, 31, 16, 0)
        game_world.add_collision_pair('player:hurdle', None, hurdle)


def create_player():
    global player
    
    player = Player(100, 80)
    player.set_font('ENCR10B.TTF', 10)
    player.set_size(50, 50)
    player.set_bb(10, 18, 10, 23)
    game_world.add_object(player, 1)
    
    game_world.add_collision_pair('player:hurdle', player, None)


def create_AI():
    pass