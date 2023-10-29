from pico2d import load_image
from constant_value import SCREEN_W, SCREEN_H
from state_machine import StateMachine


class Player:
    image = None

    def __init__(self):
        self.x, self.y = SCREEN_W / 2, SCREEN_H // 2
        self.frame = 0
        self.action = 3
        self.dir = 0
        self.face_dir = 1
        self.state_machine = StateMachine(self)
        self.state_machine.start()
        if Player.image == None:
            Player.image = load_image('res\\player.png')

    def update(self):
        self.state_machine.update()

    def handle_event(self, event):
        self.state_machine.handle_event(('INPUT', event))

    def draw(self):
        self.state_machine.draw()
    