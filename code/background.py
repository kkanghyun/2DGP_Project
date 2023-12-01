from pico2d import get_canvas_width, get_canvas_height, clamp
from game_utility import load_image, load_mp3, load_wav, SCREEN_W, SCREEN_H

import play_mode


class Background:
    def __init__(self):
        self.image = load_image('background.jpg')
        self.w = SCREEN_W
        self.h = SCREEN_H
        self.bgm = None
        self.bgm_enable = False


    def draw(self):
        self.image.draw(SCREEN_W // 2, SCREEN_H // 2, self.w, self.h)


    def update(self):
        pass


    def set_image(self, name):
        self.image = load_image(name)


    def set_size(self, w, h):
        self.w, self.h = w, h


    def set_bgm(self, name):
        self.bgm = load_mp3(name)


    def set_volume(self, val):
        self.bgm.set_volume(val)

        
    def play_sound(self):
        if self.bgm_enable == False:
            self.bgm.play()
            self.bgm_enable = True


    def play_sound_repeat(self):
        self.bgm.repeat_play()



class FixedBackground:
    goal_line = 190

    def __init__(self):
        self.image = load_image('background.jpg')
        self.cw = get_canvas_width()
        self.ch = get_canvas_height()
        self.w = self.image.w
        self.h = self.image.h
        self.bgm = None
        self.bgm_wav = None
        self.bgm_enable = False


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


    def set_bgm(self, name):
        self.bgm = load_mp3(name)
        

    def set_bgm_wav(self, name):
        self.bgm_wav = load_wav(name)


    def set_volume(self, val):
        self.bgm.set_volume(val)


    def play_sound(self):
        if self.bgm_enable == False:
            self.bgm.play()
            self.bgm_enable = True