import game_engine
import game_world
from pico2d import *
from background import Background
from player import Player
from hurdle import Hurdle


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
    global background
    global player
    global hurdle

    background = Background()
    game_world.add_object(background, 0)

    player = Player(100, 100)
    game_world.add_object(player, 1)
    
    hurdle = Hurdle(500, 100)
    game_world.add_object(hurdle, 2)

    game_world.add_collision_pair('player:hurdle', player, hurdle)


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