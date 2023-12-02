from pico2d import open_canvas, close_canvas
from game_utility import SCREEN_W, SCREEN_H

import game_engine

import logo_mode as start_mode
# import title_mode as start_mode
# import play_mode as start_mode


open_canvas(SCREEN_W, SCREEN_H)
game_engine.run(start_mode)
close_canvas()