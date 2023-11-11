from game_utility import load_image, SCREEN_W, SCREEN_H


class Background:
    def __init__(self):
        self.image = load_image('background.png')


    def draw(self):
        w = SCREEN_W
        h = SCREEN_H
        self.image.draw(SCREEN_W // 2, SCREEN_H // 2, w, h)


    def update(self):
        pass
