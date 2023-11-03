import play_mode as start_mode
import game_framework
from pico2d import open_canvas, close_canvas
from game_utility import SCREEN_X, SCREEN_Y


open_canvas(SCREEN_X, SCREEN_Y)
game_framework.run(start_mode)
close_canvas()