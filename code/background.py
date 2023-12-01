from pico2d import get_canvas_width, get_canvas_height, clamp
from game_utility import load_image, SCREEN_W, SCREEN_H

import play_mode


class Background:
    goal_line = 190

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


    def draw(self):
        l = int(self.window_left + self.window_left / play_mode.camera_scale * (play_mode.camera_scale - 1))
        b = int(self.window_bottom + self.window_bottom / play_mode.camera_scale * (play_mode.camera_scale - 1))
        w = int(self.w / play_mode.camera_scale)
        h = int(self.h / play_mode.camera_scale)
        self.image.clip_draw_to_origin(l, b, w, h, 0, 0, self.cw, self.ch)


    def update(self):
        self.window_left = clamp(0, int((play_mode.player.x - play_mode.player.w / 2) * play_mode.camera_scale) - self.cw // 2, self.cw * play_mode.camera_scale - self.cw - 1)
        self.window_bottom = clamp(0, int((play_mode.player.y - play_mode.player.h / 2) * play_mode.camera_scale) - self.ch // 2, self.ch * play_mode.camera_scale - self.ch - 1)


    def handle_event(self, event):
        pass