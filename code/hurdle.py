from game_utility import load_image, SCREEN_X, SCREEN_Y
from pico2d import draw_rectangle


class Hurdle:
    image = None

    def __init__(self):
        self.x, self.y = SCREEN_X // 2 + 200, SCREEN_Y // 2
        if Hurdle.image == None:
            Hurdle.image = load_image('hurdle.png')
        self.w, self.h = 100, 100


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