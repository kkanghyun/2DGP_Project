from game_utility import load_image

class Background:
    def __init__(self):
        self.image = load_image('background.png')

    def draw(self):
        self.image.draw(400, 300)

    def update(self):
        pass
