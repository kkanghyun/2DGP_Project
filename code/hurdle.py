from game_utility import load_image, SCREEN_W, SCREEN_H
from pico2d import draw_rectangle

import math
import game_engine
import game_world


class Hurdle:
    image = None

    def __init__(self, pos_x = SCREEN_W // 2, pos_y = SCREEN_H // 2):
        self.x, self.y = pos_x, pos_y
        if Hurdle.image == None:
            Hurdle.image = load_image('hurdle.png')
        self.w, self.h = 50, 50
        self.action = 'up'
        self.rotate = 0.0
        self.velocity = 500
        self.collision_bb = []


    def update(self):
        if self.action == 'down' and self.rotate < 90:
            self.rotate += self.velocity * game_engine.delta_time
            self.x += self.w * game_engine.delta_time
            if self.rotate > 90:
                self.rotate = 90.0


    def handle_event(self, event):
        pass


    def draw(self):
        match self.action:
            case 'up':
                Hurdle.image.draw_to_origin(self.x, self.y, self.w, self.h)
                draw_rectangle(*self.get_bb())
            case 'down':
                Hurdle.image.rotate_draw(math.radians(-self.rotate), self.x + self.w, self.y + self.h / 2, self.w, self.h)


    def set_size(self, w, h):
        self.w, self.h = w, h


    def set_bb(self, left, bottom, right, top):
        self.collision_bb = {'left' : left, 'bottom' : bottom, 'right' : right, 'top' : top}

        
    def get_bb(self):
        return [self.x - self.collision_bb['left'] + self.w / 2, self.y - self.collision_bb['bottom'] + self.h, 
                self.x + self.collision_bb['right'] + self.w / 2, self.y + self.collision_bb['top'] + self.h]


    def handle_collision(self, group, other):
        if group == 'player:hurdle':
            self.action = 'down'
            other.set_velocity(other.get_velocity() / 2)
            game_world.remove_collision_object(self)