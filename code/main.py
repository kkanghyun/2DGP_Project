from pico2d import open_canvas, close_canvas
from game_value import SCREEN_X, SCREEN_Y
import play_mode as start_mode
import game_framework

open_canvas(SCREEN_X, SCREEN_Y)
game_framework.run(start_mode)
close_canvas()