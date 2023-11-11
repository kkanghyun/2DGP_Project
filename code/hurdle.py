from game_utility import load_image, SCREEN_W, SCREEN_H
from pico2d import draw_rectangle


class Hurdle:
    image = None

    def __init__(self, pos_x = SCREEN_W // 2, pos_y = SCREEN_H // 2):
        self.x, self.y = pos_x, pos_y
        if Hurdle.image == None:
            Hurdle.image = load_image('hurdle.png')
        self.w, self.h = 100, 100
        self.action = 0


    def update(self):
        pass


    def handle_event(self, event):
        pass


    def draw(self):
        Hurdle.image.draw(self.x, self.y, self.w, self.h)
        draw_rectangle(*self.get_bb())

        
    def get_bb(self):
        return self.x - 20, self.y - 45, self.x + 35, self.y + 5


    def handle_collision(self, group, other):
        pass