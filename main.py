import game_engine
from pico2d import open_canvas, close_canvas

if __name__ == '__main__':
    if game_engine.init() == False:
        exit()

    open_canvas()
    game_engine.run()
    close_canvas()