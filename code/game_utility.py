from pico2d import load_image as pico2d_load_image

SCREEN_X, SCREEN_Y = 960, 640

def load_image(name):
    add_path = "..\\res\\"
    return pico2d_load_image(add_path + name)