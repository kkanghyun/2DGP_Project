from pico2d import clear_canvas, update_canvas, get_events, get_time, load_font, SDL_QUIT, SDL_KEYDOWN, SDLK_ESCAPE
from background import FixedBackground
from player import Player
from player_AI import Player_AI
from hurdle import Hurdle
from game_utility import SCREEN_W, SCREEN_H

import game_engine
import game_world
import random
import title_mode


def handle_events():
    global game_start

    events = get_events()
    if game_start == False:
        events.clear()

    for event in events:
        if event.type == SDL_QUIT:
            game_engine.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            # game_engine.quit()
            game_engine.change_mode(title_mode)
        else:
            player.handle_event(event)


def init():
    global game_start
    global current_time
    global camera_scale
    global time_font
    global real_time
    global end_time
    global player1_font
    global player2_font
    global player3_font

    game_start = False
    current_time = 0.0
    camera_scale = 1.0
    time_font = load_font(".\\res\\ENCR10B.TTF", 30)
    real_time = 0.0
    end_time = 0.0
    player1_font = load_font(".\\res\\ENCR10B.TTF", 40)
    player2_font = load_font(".\\res\\ENCR10B.TTF", 40)
    player3_font = load_font(".\\res\\ENCR10B.TTF", 40)

    create_objects()

    current_time = get_time()


def finish():
    global player
    global player_AI_list
    global hurdles_list

    game_world.remove_object(player)
    for ai in player_AI_list:
        game_world.remove_object(ai)
    for hurdles in hurdles_list:
        for hurdle in hurdles:
            game_world.remove_object(hurdle)

    game_world.clear()


def update():
    global game_start
    global current_time
    global camera_scale
    global player
    global player_AI_list
    global real_time
    global end_time

    if get_time() - current_time >= 1:
        if get_time() - current_time >= 5:
            game_start = True
            real_time += game_engine.delta_time
        else:
            camera_scale += 2.0 * game_engine.delta_time
            if camera_scale >= 3.0:
                camera_scale = 3.0
            player.set_font('ENCR10B.TTF', 10)
            for ai in player_AI_list:
                ai.set_font('ENCR10B.TTF', 10)

    if player.goal == True:
        end_time += game_engine.delta_time

    game_world.update()
    game_world.handle_collisions()


def draw():
    global time_font
    global real_time
    global player
    global player_AI_list
    global player1_font
    global player2_font
    global player3_font
    global camera_scale
    global background

    clear_canvas()
    game_world.render()
    time_font.draw(SCREEN_W // 2, SCREEN_H - 20, f'{real_time:.2f}', (255, 0, 0))
    if end_time >= 2.0:
        if end_time >= 10.0:
            game_engine.change_mode(title_mode)
            return
        
        y1 = player_AI_list[0].y * camera_scale - background.window_bottom + 20
        y2 = player.y * camera_scale - background.window_bottom + 20
        y3 = player_AI_list[1].y * camera_scale - background.window_bottom + 20
        player1_font.draw(SCREEN_W // 2, y1, f'TIME : {player_AI_list[0].record:.2f}', (100, 255, 100))
        player2_font.draw(SCREEN_W // 2, y2, f'TIME : {player.record:.2f}', (100, 255, 100))
        player3_font.draw(SCREEN_W // 2, y3, f'TIME : {player_AI_list[1].record:.2f}', (100, 255, 100))

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