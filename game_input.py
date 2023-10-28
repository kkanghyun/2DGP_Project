from pico2d import *

def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            exit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            exit()