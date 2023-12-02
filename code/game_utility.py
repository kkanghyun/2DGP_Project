from pico2d import load_image as pico2d_load_image
from pico2d import load_font as pico2d_load_font
from pico2d import load_music as pico2d_load_music
from pico2d import load_wav as pico2d_load_wav

SCREEN_W, SCREEN_H = 1280, 720
PIXEL_PER_METER = (10.0 / 0.3)  # 10 pixel 30 cm, canvas 1 block is 10 pixel
GRAVITY = 5.5

FRICTION_COEF = 30.0


def load_image(name):
    add_path = '..\\res\\'
    image = pico2d_load_image(add_path + name)
    return image


def load_font(name, size):
    add_path = '..\\res\\'
    image = pico2d_load_font(add_path + name, int(size))
    return image


def load_mp3(name):
    add_path = '..\\res\\'
    mp3 = pico2d_load_music(add_path + name)
    return mp3


def load_wav(name):
    add_path = '..\\res\\'
    wav = pico2d_load_wav(add_path + name)
    return wav


# speed is km/h
def cal_speed_pps(speed):
    mpm = speed * 1000.0 / 60.0
    mps = mpm / 60.0
    pps = mps * PIXEL_PER_METER
    return pps