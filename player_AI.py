from pico2d import draw_rectangle, SDL_KEYDOWN, SDL_KEYUP, SDLK_SPACE, SDLK_LEFT, SDLK_RIGHT
from game_utility import load_image, load_font, cal_speed_pps, SCREEN_W, SCREEN_H, GRAVITY, FRICTION_COEF
from behavior_tree import BehaviorTree, Action, Sequence, Condition, Selector

import game_engine
import play_mode
import background

FRAMES_PER_ACTION = 8

# animation frame per time
TIME_PER_ACTION = 0.6
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION

# animation frame per velocity
ACTION_PER_VELOCITY = 50




class AI_State:

    @staticmethod
    def idle(player):
        if play_mode.game_start == False or player.x >= play_mode.background.cw - 100:
            if player.state != 'idle':
                if player.is_jump == False:
                    player.action = player.dir + '_' + 'idle'
                    player.frame = 0
                player.state = 'idle'
            return BehaviorTree.SUCCESS
        else:
            return BehaviorTree.FAIL


    @staticmethod
    def run(player):
        if player.state != 'run':
            player.dir, player.action = 'right', 'right_run'
            player.state = 'run'
        player.cal_velocity()
        player.state = 'run'
        return BehaviorTree.SUCCESS


    @staticmethod
    def jump(player):
        player.jump_init()
        return BehaviorTree.SUCCESS
    

    @staticmethod
    def is_hurdles_nearby(player):
        for hurdle in play_mode.hurdles_list[player.id]:
            if hurdle.x < player.x:
                continue
            else:
                if hurdle.x - player.x < 60:
                    return BehaviorTree.SUCCESS
                else:
                    return BehaviorTree.FAIL
        
        return BehaviorTree.FAIL




class Player_AI:
    animations = ('left_run', 'right_run', 'left_idle', 'right_idle')

    def __init__(self, id, pos_x = SCREEN_W // 2, pos_y = SCREEN_H // 2):
        self.id = id
        self.goal = False
        self.record = 0.0
        self.rank = ""
        self.start_x, self.start_y = pos_x, pos_y
        self.x, self.y = pos_x, pos_y
        self.w, self.h = 100, 100
        self.frame = 0
        self.dir = 'right'
        self.action = 'right_idle'
        self.force = 350.0
        self.mass = 1.0
        self.accel = self.force / self.mass
        self.velocity = 0.0 # km/s
        self.velocity_max = 200.0
        self.is_jump = False
        self.jump_force = 1.4
        self.jump_velocity = 0.0
        self.images = load_image('player.png')
        self.font = load_font('ENCR10B.TTF', 10 * play_mode.camera_scale)
        self.font_color = (0, 0, 255)
        self.font_x, self.font_y = -10, 30
        self.image_w, self.image_h = 100, 100
        self.collision_bb = []

        self.state = 'idle'
        self.build_behavior_tree()


    def update(self):
        if self.x >= SCREEN_W - background.FixedBackground.goal_line:
            if self.record <= 1.0:
                self.goal = True
                self.record = play_mode.real_time
        if self.is_jump == True:
            self.jump_update()
        self.cal_pos()
        self.frame_update()
        self.bt.run()


    def draw(self):
        sx = self.x * play_mode.camera_scale - play_mode.background.window_left
        sy = self.y * play_mode.camera_scale - play_mode.background.window_bottom
        sw = self.w * play_mode.camera_scale
        sh = self.h * play_mode.camera_scale

        self.font.draw(sx + sw / 2 + self.font_x * play_mode.camera_scale, sy + sh / 2 + self.font_y * play_mode.camera_scale, f'{abs(self.velocity / 10):.2f}km/s', self.font_color)
        self.draw_player()
        draw_rectangle(*self.get_bb())


    def handle_event(self, event):
        pass


    def handle_collision(self, group, other):
        pass


    def set_size(self, w, h):
        self.w, self.h = w, h
            

    def set_velocity(self, velocity):
        self.velocity = velocity

        
    def set_bb(self, left, bottom, right, top):
        self.collision_bb = {'left' : left, 'bottom' : bottom, 'right' : right, 'top' : top}


    def set_images(self, name):
        self.images = load_image(name)


    def set_font(self, name, size):
        self.font = load_font(name, size * play_mode.camera_scale)


    def get_scale(self):
        return self.w, self.h


    def get_velocity(self):
        return self.velocity

        
    def get_bb(self):
        sx = self.x * play_mode.camera_scale - play_mode.background.window_left
        sy = self.y * play_mode.camera_scale - play_mode.background.window_bottom
        sw = self.w * play_mode.camera_scale
        sh = self.h * play_mode.camera_scale

        return [sx - self.collision_bb['left'] * play_mode.camera_scale + sw / 2, sy - self.collision_bb['bottom'] * play_mode.camera_scale + sh / 2, 
                sx + self.collision_bb['right'] * play_mode.camera_scale + sw / 2, sy + self.collision_bb['top'] * play_mode.camera_scale + sh / 2]


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

            if self.state == 'idle':
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

            if self.state == 'idle':
                self.action = self.dir + '_' + 'idle'
                self.frame = 0


    def frame_update(self):
        match self.state:
            case 'idle':
                self.frame = (self.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_engine.delta_time) % FRAMES_PER_ACTION
            case 'run':
                action_per_velocity = self.velocity / ACTION_PER_VELOCITY
                self.frame = (self.frame + FRAMES_PER_ACTION * action_per_velocity * game_engine.delta_time) % FRAMES_PER_ACTION

                
    def draw_player(self):
        sx = self.x * play_mode.camera_scale - play_mode.background.window_left
        sy = self.y * play_mode.camera_scale - play_mode.background.window_bottom
        sw = self.w * play_mode.camera_scale
        sh = self.h * play_mode.camera_scale

        if self.is_jump:
            self.images.clip_draw_to_origin(1 * self.image_w, self.animations.index(self.action) * self.image_h, self.image_w, self.image_h, sx, sy, sw, sh)
        else:
            self.images.clip_draw_to_origin(int(self.frame) * self.image_w, self.animations.index(self.action) * self.image_h, self.image_w, self.image_h, sx, sy, sw, sh)
            

    def build_behavior_tree(self):
        a1 = Action('Idle', AI_State.idle, self)
        a2 = Action('Run', AI_State.run, self)
        a3 = Action('Jump', AI_State.jump, self)
        c1 = Condition('Are there any hurdles ahead?', AI_State.is_hurdles_nearby, self)

        SEQ_Jump_and_Run = Sequence('Jump', c1, a3, a2)
        SEL_Jump_or_Run = Selector('Jump or Run', SEQ_Jump_and_Run, a2)

        SEQ_Idle = Sequence('Idle', a1)
        SEQ_Run = Sequence('Run', SEL_Jump_or_Run)

        root = SEL_Idle_or_Run = Selector('Idle or Run', SEQ_Idle, SEQ_Run)

        self.bt = BehaviorTree(root)
