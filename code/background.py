from pico2d import get_canvas_width, get_canvas_height, clamp
from game_utility import load_image, SCREEN_W, SCREEN_H, CAMERA_SCALE

import play_mode


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




class FixedBackground:
    def __init__(self):
        self.image = load_image('background.jpg')
        self.cw = get_canvas_width()
        self.ch = get_canvas_height()
        self.w = self.image.w
        self.h = self.image.h
        # fill here


    def draw(self):
        self.image.clip_draw_to_origin(self.window_left, self.window_bottom, self.w, self.h, 0, 0, self.cw, self.ch)


    def update(self):
        self.window_left = clamp(0, int(play_mode.player.x) - self.cw // 2, self.w - self.cw - 1)
        self.window_bottom = clamp(0, int(play_mode.player.y) - self.ch // 2, self.h - self.ch - 1)


    def handle_event(self, event):
        pass