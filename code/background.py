from game_utility import load_image

class Background:
    def __init__(self):
        self.image = load_image('background.png')

    def draw(self):
        w = self.image.w
        h = self.image.h
        self.image.clip_draw(0, 0, w, h, w, h, w * 2, h * 2)

    def update(self):
        pass
