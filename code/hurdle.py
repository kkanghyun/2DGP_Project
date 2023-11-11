from game_utility import load_image, SCREEN_W, SCREEN_H
from pico2d import draw_rectangle
import math


class Hurdle:
    image = None
    image_offset_x = 50
    image_offset_y = 10

    def __init__(self, pos_x = SCREEN_W // 2, pos_y = SCREEN_H // 2):
        self.x, self.y = pos_x, pos_y
        if Hurdle.image == None:
            Hurdle.image = load_image('hurdle.png')
        self.w, self.h = 100, 100
        self.action = 'up'


    def update(self):
        pass


    def handle_event(self, event):
        pass


    def draw(self):
        match self.action:
            case 'up':
                Hurdle.image.draw(self.x, self.y + Hurdle.image_offset_y, self.w, self.h)
            case 'down':
                Hurdle.image.rotate_draw(math.radians(-90.0), self.x + Hurdle.image_offset_x, self.y, self.w, self.h)
        draw_rectangle(*self.get_bb())

        
    def get_bb(self):
        return self.x - Hurdle.image_offset_x + 30, self.y + Hurdle.image_offset_y - 45, self.x + 35, self.y + Hurdle.image_offset_y + 5


    def handle_collision(self, group, other):
        if group == 'player:hurdle':
            self.action = 'down'
        pass