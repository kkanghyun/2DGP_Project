import game_engine
from pico2d import open_canvas, close_canvas

if __name__ == '__main__':
    if game_engine.init() == False:
        raise ValueError('초기화 실패')
    else:
        open_canvas()
        game_engine.run()
        close_canvas()