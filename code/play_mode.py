from pico2d import clear_canvas, update_canvas, get_events, get_time, SDL_QUIT, SDL_KEYDOWN, SDLK_ESCAPE
from background import FixedBackground
from player import Player
from player_AI import Player_AI
from hurdle import Hurdle

import game_engine
import game_world
import random
import game_utility


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
    global game_start
    global current_time
    global camera_scale

    game_start = False
    camera_scale = 1.0

    create_objects()

    current_time = get_time()


def finish():
    game_world.clear()
    pass


def update():
    global game_start
    global current_time
    global camera_scale

    if get_time() - current_time >= 1:
        if get_time() - current_time >= 5:
            game_start = True
        else:
            camera_scale += 2.0 * game_engine.delta_time
            if camera_scale >= 3.0:
                camera_scale = 3.0

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

    background = FixedBackground()
    game_world.add_object(background, 0)


def create_hurdles():
    global hurdles_list
    
    hurdles_list = []

    for i in range(3):
        hurdles = []
        for j in range(24):
            if j % 4 == 0 or j % 4 == 1:
                continue
            if random.randint(0, 100) <= 30:
                continue

            hurdle = Hurdle(i, 200 + (104 / 3 + 2) * j, (150 + 8) - i * 70)
            hurdles.append(hurdle)

            
        game_world.add_objects(hurdles, 2)

        for hurdle in hurdles:
            div = 4
            hurdle.set_size(104 / div, 91 / div)
            hurdle.set_bb(-18 / div, 93 / div, 48 / div, 0)
            game_world.add_collision_pair('player:hurdle', None, hurdle)

        hurdles_list.append(hurdles)


def create_player():
    global player
    
    player = Player(1, 100, 80)
    player.set_font('ENCR10B.TTF', 10)
    player.set_size(50, 50)
    player.set_bb(10, 18, 10, 23)
    game_world.add_object(player, 1)
    
    game_world.add_collision_pair('player:hurdle', player, None)


def create_AI():
    global player_AI_list
    
    player_AI_list = []

    player = Player_AI(0, 100, 150)
    player.set_images('player_AI_1.png')
    player.set_font('ENCR10B.TTF', 10)
    player.set_size(50, 50)
    player.set_bb(10, 18, 10, 23)
    game_world.add_object(player, 1)
    game_world.add_collision_pair('player:hurdle', player, None)

    player_AI_list.append(player)
    

    player = Player_AI(2, 100, 10)
    player.set_images('player_AI_2.png')
    player.set_font('ENCR10B.TTF', 10)
    player.set_size(50, 50)
    player.set_bb(10, 18, 10, 23)
    game_world.add_object(player, 1)
    game_world.add_collision_pair('player:hurdle', player, None)

    player_AI_list.append(player)