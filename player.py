from pico2d import load_image
from constant_value import SCREEN_W, SCREEN_H


class Player:
    def __init__(self):
        global image
        
        image = None
        self.x, self.y = SCREEN_W / 2, SCREEN_H // 2
        self.frame = 0
        self.action = 3
        if image == None:
            image = load_image('res\\player.png')

    def update(self):
        pass

    def handle_event(self, event):
        pass

    def draw(self):
        image.clip_draw(self.frame * 100, self.action * 100, 100, 100, self.x, self.y)
    