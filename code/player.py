# 이것은 각 상태들을 객체로 구현한 것임.

import game_engine
from pico2d import draw_rectangle, SDL_KEYDOWN, SDL_KEYUP, SDLK_SPACE, SDLK_LEFT, SDLK_RIGHT
from game_utility import load_image, cal_speed_pps, SCREEN_W, SCREEN_H, GRAVITY

FRAMES_PER_ACTION = 8

# animation frame from time
TIME_PER_ACTION = 0.5
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION

# animation frame from velocity
VELOCITY_PER_ACTION = 80


# state event check
# ( state event type, event value )
right_down = lambda e : e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_RIGHT
right_up = lambda e : e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_RIGHT
left_down = lambda e : e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_LEFT
left_up = lambda e : e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_LEFT
space_down = lambda e : e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_SPACE
time_out = lambda e : e[0] == 'TIME_OUT'


class Idle:

    @staticmethod
    def enter(player, e):
        player.action = player.dir + '_' + 'idle'
        player.frame = 0
        pass


    @staticmethod
    def exit(player, e):
        pass


    @staticmethod
    def update(player):
        player.frame = (player.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_engine.delta_time) % FRAMES_PER_ACTION
        player.cal_pos()


    @staticmethod
    def draw(player):
        player.images.clip_draw(int(player.frame) * player.w, player.animations.index(player.action) * player.h, player.w, player.h, player.x, player.y)


class Run:

    @staticmethod
    def enter(player, e):
        if right_down(e) or left_up(e): # 오른쪽으로 RUN
            player.dir, player.action = 'right', 'right_run'
        elif left_down(e) or right_up(e): # 왼쪽으로 RUN
            player.dir, player.action = 'left', 'left_run'

  
    @staticmethod
    def exit(player, e):
        pass


    @staticmethod
    def update(player):
        action_per_velocity = player.velocity / VELOCITY_PER_ACTION
        player.frame = (player.frame + FRAMES_PER_ACTION * action_per_velocity * game_engine.delta_time) % FRAMES_PER_ACTION
        player.cal_velocity()
        player.cal_pos()


    @staticmethod
    def draw(player):
        player.images.clip_draw(int(player.frame) * player.w, player.animations.index(player.action) * player.h, player.w, player.h, player.x, player.y)


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
    animations = ('left_run', 'right_run', 'left_idle', 'right_idle')

    def __init__(self, pos_x = SCREEN_W // 2, pos_y = SCREEN_H // 2):
        self.x, self.y = pos_x, pos_y
        self.frame = 0
        self.dir = 'right'
        self.action = 'right_idle'
        self.force = 200.0
        self.mass = 1.0
        self.accel = self.force / self.mass
        # self.velocity = cal_speed_pps(self.accel)
        self.velocity = 0.0
        if Player.images == None:
            Player.images = load_image('player.png')
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
            

    def set_velocity(self, velocity):
        self.velocity = velocity


    def get_velocity(self):
        return self.velocity


    def cal_velocity(self):
        match self.dir:
            case 'right':
                self.accel = self.force / self.mass
            case 'left':
                self.accel = -self.force / self.mass

        self.velocity = self.velocity + self.accel * game_engine.delta_time


    def cal_pos(self):
        normal_force = self.mass * GRAVITY

        friction_coef = 10.0

        friction = friction_coef * normal_force

        friction_dir_x = -self.velocity

        mag = abs(friction_dir_x)

        # 마찰력만큼 속력 감소
        if mag > 0.0:
            friction_dir_x = friction_dir_x / mag
            if self.state_machine.cur_state == Idle:
                friction_force_x = friction_dir_x * friction * 5
            else:
                friction_force_x = friction_dir_x * friction

            friction_accel_x = friction_force_x / self.mass

            velocity = self.velocity + friction_accel_x * game_engine.delta_time
            if velocity * self.velocity < 0.0:
                self.velocity = 0.0
            else:
                self.velocity = velocity

        self.x = self.x + self.velocity * game_engine.delta_time
