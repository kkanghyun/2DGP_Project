import game_engine
from constant_value import SCREEN_W, SCREEN_H


if __name__ == '__main__':
    if game_engine.init() == False:
        raise ValueError('초기화 실패')
    else:
        game_engine.run()