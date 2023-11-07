# 이것은 각 상태들을 객체로 구현한 것임.

import game_engine
from pico2d import draw_rectangle, SDL_KEYDOWN, SDL_KEYUP, SDLK_SPACE, SDLK_LEFT, SDLK_RIGHT
from game_utility import load_image, cal_speed_pps, SCREEN_X, SCREEN_Y


# animation frame velocity
TIME_PER_ACTION = 0.5
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 8


# state event check
# ( state event type, event value )

def right_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_RIGHT


def right_up(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_RIGHT


def left_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_LEFT


def left_up(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_LEFT


def space_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_SPACE


def time_out(e):
    return e[0] == 'TIME_OUT'

# time_out = lambda e : e[0] == 'TIME_OUT'


class Idle:

    @staticmethod
    def enter(player, e):
        if player.face_dir == -1:
            player.action = 2
        elif player.face_dir == 1:
            player.action = 3
        player.dir = 0
        player.frame = 0
        pass


    @staticmethod
    def exit(player, e):
        pass


    @staticmethod
    def update(player):
        player.frame = (player.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_engine.delta_time) % FRAMES_PER_ACTION


    @staticmethod
    def draw(player):
        player.image.clip_draw(int(player.frame) * 100, player.action * 100, player.w, player.h, player.x, player.y)


class Run:

    @staticmethod
    def enter(player, e):
        if right_down(e) or left_up(e): # 오른쪽으로 RUN
            player.dir, player.action, player.face_dir = 1, 1, 1
        elif left_down(e) or right_up(e): # 왼쪽으로 RUN
            player.dir, player.action, player.face_dir = -1, 0, -1

  
    @staticmethod
    def exit(player, e):
        pass


    @staticmethod
    def update(player):
        player.frame = (player.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_engine.delta_time) % FRAMES_PER_ACTION
        player.x += player.dir * player.velocity * game_engine.delta_time


    @staticmethod
    def draw(player):
        player.image.clip_draw(int(player.frame) * 100, player.action * 100, player.w, player.h, player.x, player.y)


class StateMachine:
    def __init__(self, player):
        self.player = player
        self.cur_state = Idle
        self.transitions = {
            Idle: {right_down: Run, left_down: Run, left_up: Run, right_up: Run},
            Run: {right_down: Idle, left_down: Idle, right_up: Idle, left_up: Idle},
        }


    def start(self):
        self.cur_state.enter(self.player, ('NONE', 0))


    def update(self):
        self.cur_state.update(self.player)


    def handle_event(self, e):
        for check_event, next_state in self.transitions[self.cur_state].items():
            if check_event(e):
                self.cur_state.exit(self.player, e)
                self.cur_state = next_state
                self.cur_state.enter(self.player, e)
                return True

        return False


    def draw(self):
        self.cur_state.draw(self.player)


class Player:
    images = None

    def __init__(self):
        self.x, self.y = SCREEN_X // 2, SCREEN_Y // 2
        self.frame = 0
        self.action = 3
        self.face_dir = 1
        self.dir = 0
        self.velocity = cal_speed_pps(20.0)
        Player.image = load_image('player.png')
        self.w, self.h = 100, 100
        self.state_machine = StateMachine(self)
        self.state_machine.start()


    def update(self):
        self.state_machine.update()


    def handle_event(self, event):
        self.state_machine.handle_event(('INPUT', event))


    def draw(self):
        self.state_machine.draw()
        draw_rectangle(*self.get_bb())

        
    def get_bb(self):
        return self.x - 21, self.y - 36, self.x + 21, self.y + 46


    def handle_collision(self, group, other):
        pass
