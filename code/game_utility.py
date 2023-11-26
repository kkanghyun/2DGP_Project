from pico2d import load_image as pico2d_load_image
from pico2d import load_font as pico2d_load_font


SCREEN_W, SCREEN_H = 1280, 720
PIXEL_PER_METER = (10.0 / 0.3)  # 10 pixel 30 cm, canvas 1 block is 10 pixel
GRAVITY = 5.5

FRICTION_COEF = 30.0


def load_image(name):
    add_path = ".\\res\\"
    image = pico2d_load_image(add_path + name)
    return image


def load_font(name, size):
    add_path = ".\\res\\"
    image = pico2d_load_font(add_path + name, size)
    return image


# speed is km/h
def cal_speed_pps(speed):
    mpm = speed * 1000.0 / 60.0
    mps = mpm / 60.0
    pps = mps * PIXEL_PER_METER
    return pps