# 이것은 각 상태들을 객체로 구현한 것임.

import game_engine
from pico2d import draw_rectangle, SDL_KEYDOWN, SDL_KEYUP, SDLK_SPACE, SDLK_LEFT, SDLK_RIGHT
from game_utility import load_image, load_font, cal_speed_pps, SCREEN_W, SCREEN_H, GRAVITY, FRICTION_COEF

FRAMES_PER_ACTION = 8

# animation frame per time
TIME_PER_ACTION = 0.6
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION

# animation frame per velocity
ACTION_PER_VELOCITY = 50


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
        if player.is_jump == False:
            player.action = player.dir + '_' + 'idle'
            player.frame = 0
        
        if space_down(e):
            player.jump_init()


    @staticmethod
    def exit(player, e):
        pass


    @staticmethod
    def update(player):
        player.frame = (player.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_engine.delta_time) % FRAMES_PER_ACTION
        player.cal_pos()


    @staticmethod
    def draw(player):
        if player.is_jump:
            action = player.dir + '_run'
            player.images.clip_draw_to_origin(1 * player.image_w, player.animations.index(action) * player.image_h, player.image_w, player.image_h, player.x, player.y, player.w, player.h)
        else:
            player.images.clip_draw_to_origin(int(player.frame) * player.image_w, player.animations.index(player.action) * player.image_h, player.image_w, player.image_h, player.x, player.y, player.w, player.h)




class Run:

    @staticmethod
    def enter(player, e):
        if right_down(e) or left_up(e): # 오른쪽으로 RUN
            player.dir, player.action = 'right', 'right_run'
        elif left_down(e) or right_up(e): # 왼쪽으로 RUN
            player.dir, player.action = 'left', 'left_run'
        elif space_down(e):
            player.jump_init()

  
    @staticmethod
    def exit(player, e):
        pass


    @staticmethod
    def update(player):
        action_per_velocity = player.velocity / ACTION_PER_VELOCITY
        player.frame = (player.frame + FRAMES_PER_ACTION * action_per_velocity * game_engine.delta_time) % FRAMES_PER_ACTION
        player.cal_velocity()
        player.cal_pos()


    @staticmethod
    def draw(player):
        if player.is_jump:
            player.images.clip_draw_to_origin(1 * player.image_w, player.animations.index(player.action) * player.image_h, player.image_w, player.image_h, player.x, player.y, player.w, player.h)
        else:
            player.images.clip_draw_to_origin(int(player.frame) * player.image_w, player.animations.index(player.action) * player.image_h, player.image_w, player.image_h, player.x, player.y, player.w, player.h)




class StateMachine:
    def __init__(self, player):
        self.player = player
        self.cur_state = Idle
        self.transitions = {
            Idle: {right_down: Run, left_down: Run, left_up: Run, right_up: Run, space_down: Idle},
            Run: {right_down: Idle, left_down: Idle, right_up: Idle, left_up: Idle, space_down: Run},
        }


    def start(self):
        self.cur_state.enter(self.player, ('NONE', 0))


    def update(self):
        if self.player.is_jump == True:
            self.player.jump_update()
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
    font = None
    animations = ('left_run', 'right_run', 'left_idle', 'right_idle')

    def __init__(self, pos_x = SCREEN_W // 2, pos_y = SCREEN_H // 2):
        self.start_x, self.start_y = pos_x, pos_y
        self.x, self.y = pos_x, pos_y
        self.w, self.h = 100, 100
        self.frame = 0
        self.dir = 'right'
        self.action = 'right_idle'
        self.force = 300.0
        self.mass = 1.0
        self.accel = self.force / self.mass
        # self.velocity = cal_speed_pps(self.accel)
        self.velocity = 0.0 # m/s
        self.velocity_max = 200.0
        self.is_jump = False
        self.jump_force = 1.8
        self.jump_velocity = 0.0
        if Player.images == None:
            Player.images = load_image('player.png')
        if Player.font == None:
            Player.font = load_font('ENCR10B.TTF', 10)
            self.font_color = (0, 0, 255)
            self.font_x, self.font_y = -10, 30
        self.image_w, self.image_h = 100, 100
        self.state_machine = StateMachine(self)
        self.state_machine.start()
        self.collision_bb = []


    def update(self):
        self.state_machine.update()


    def handle_event(self, event):
        self.state_machine.handle_event(('INPUT', event))


    def draw(self):
        self.font.draw(self.x + self.w / 2 + self.font_x, self.y + self.h / 2 + self.font_y, f'{abs(self.velocity / 10):.2f}', self.font_color)
        self.state_machine.draw()
        draw_rectangle(*self.get_bb())


    def handle_collision(self, group, other):
        pass


    def set_size(self, w, h):
        self.w, self.h = w, h
            

    def set_velocity(self, velocity):
        self.velocity = velocity

        
    def set_bb(self, left, bottom, right, top):
        self.collision_bb = {'left' : left, 'bottom' : bottom, 'right' : right, 'top' : top}


    def set_font(self, name, size):
        Player.font = load_font(name, size)


    def get_scale(self):
        return self.w, self.h


    def get_velocity(self):
        return self.velocity

        
    def get_bb(self):
        return [self.x - self.collision_bb['left'] + self.w / 2, self.y - self.collision_bb['bottom'] + self.h / 2, 
                self.x + self.collision_bb['right'] + self.w / 2, self.y + self.collision_bb['top'] + self.h / 2]


    def cal_velocity(self):
        match self.dir:
            case 'right':
                self.accel = self.force / self.mass
            case 'left':
                self.accel = -self.force / self.mass

        self.velocity = self.velocity + self.accel * game_engine.delta_time
        if self.velocity >= self.velocity_max:
            self.velocity = self.velocity_max
        elif self.velocity <= -self.velocity_max:
            self.velocity = -self.velocity_max


    def cal_pos(self):
        normal_force = self.mass * GRAVITY

        friction = FRICTION_COEF * normal_force

        friction_dir_x = -self.velocity

        mag = abs(friction_dir_x)

        # 마찰력만큼 속력 감소
        if mag > 0.0:
            friction_dir_x = friction_dir_x / mag
            friction_force_x = friction_dir_x * friction
            friction_accel_x = friction_force_x / self.mass

            if self.state_machine.cur_state == Idle:
                if friction_dir_x >= 0.0:
                    self.accel = self.force / self.mass
                else:
                    self.accel = -self.force / self.mass

                self.velocity = self.velocity + self.accel * game_engine.delta_time

            velocity = self.velocity + friction_accel_x * game_engine.delta_time
            if velocity * self.velocity < 0.0:
                self.velocity = 0.0
            else:
                self.velocity = velocity

        self.x = self.x + self.velocity * game_engine.delta_time


    def jump_init(self):
        if self.is_jump == True: return

        self.is_jump = True
        self.jump_velocity = self.jump_force


    def jump_update(self):
        self.jump_velocity -= GRAVITY * game_engine.delta_time
        self.y += self.jump_velocity
        if self.y <= self.start_y:
            self.y = self.start_y
            self.is_jump = False

            if self.state_machine.cur_state == Idle:
                self.action = self.dir + '_' + 'idle'
                self.frame = 0
