from game_utility import load_image, SCREEN_W, SCREEN_H


class Background:
    def __init__(self):
        self.image = load_image('background.jpg')
        self.w = SCREEN_W
        self.h = SCREEN_H


    def draw(self):
        self.image.draw(SCREEN_W // 2, SCREEN_H // 2, self.w, self.h)


    def update(self):
        pass


    def set_image(self, name):
        self.image = load_image(name)


    def set_scale(self, w, h):
        self.w, self.h = w, h
