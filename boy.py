from pico2d import (load_image, get_time, SDL_KEYDOWN, SDL_KEYUP,
                    SDLK_SPACE, SDLK_LEFT, SDLK_RIGHT)

RUN_SPEED = 5
IDLE_TIMEOUT = 5.0


def key_down(e, key):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == key


def key_up(e, key):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == key


def arrow_down(boy, e):
    return key_down(e, SDLK_LEFT) or key_down(e, SDLK_RIGHT)


def run_key_up(boy, e):
    # only the key of the current running direction stops the boy
    return (key_up(e, SDLK_RIGHT) and boy.dir == 1) or \
           (key_up(e, SDLK_LEFT) and boy.dir == -1)


def space_down(boy, e):
    return key_down(e, SDLK_SPACE)


def time_out(boy, e):
    return e[0] == 'TIME_OUT'


class Idle:
    @staticmethod
    def enter(boy, e):
        boy.dir = 0
        boy.start_time = get_time()

    @staticmethod
    def exit(boy, e):
        pass

    @staticmethod
    def do(boy):
        boy.frame = (boy.frame + 1) % 8
        if get_time() - boy.start_time >= IDLE_TIMEOUT:
            boy.state_machine.handle_event(('TIME_OUT', 0))

    @staticmethod
    def draw(boy):
        row = 300 if boy.face_dir == 1 else 200
        boy.image.clip_draw(boy.frame * 100, row, 100, 100, boy.x, boy.y)


class Sleep:
    @staticmethod
    def enter(boy, e):
        pass

    @staticmethod
    def exit(boy, e):
        pass

    @staticmethod
    def do(boy):
        boy.frame = (boy.frame + 1) % 8

    @staticmethod
    def draw(boy):
        row = 300 if boy.face_dir == 1 else 200
        boy.image.clip_draw(boy.frame * 100, row, 100, 100, boy.x, boy.y)


class Run:
    @staticmethod
    def enter(boy, e):
        boy.dir = boy.face_dir = 1 if key_down(e, SDLK_RIGHT) else -1

    @staticmethod
    def exit(boy, e):
        pass

    @staticmethod
    def do(boy):
        boy.frame = (boy.frame + 1) % 8
        boy.x += boy.dir * RUN_SPEED

    @staticmethod
    def draw(boy):
        row = 100 if boy.face_dir == 1 else 0
        boy.image.clip_draw(boy.frame * 100, row, 100, 100, boy.x, boy.y)


class StateMachine:
    def __init__(self, boy):
        self.boy = boy
        self.cur_state = Idle
        self.transitions = {
            Idle: [(time_out, Sleep), (arrow_down, Run)],
            Sleep: [(space_down, Idle), (arrow_down, Run)],
            Run: [(run_key_up, Idle), (arrow_down, Run)],
        }

    def start(self):
        self.cur_state.enter(self.boy, ('START', 0))

    def handle_event(self, e):
        for check, next_state in self.transitions[self.cur_state]:
            if check(self.boy, e):
                self.cur_state.exit(self.boy, e)
                self.cur_state = next_state
                self.cur_state.enter(self.boy, e)
                return True
        return False

    def update(self):
        self.cur_state.do(self.boy)

    def draw(self):
        self.cur_state.draw(self.boy)


class Boy:
    def __init__(self):
        self.x, self.y = 400, 90
        self.frame = 0
        self.face_dir = 1
        self.dir = 0
        self.start_time = 0
        self.image = load_image('animation_sheet.png')
        self.state_machine = StateMachine(self)
        self.state_machine.start()

    def handle_event(self, event):
        self.state_machine.handle_event(('INPUT', event))

    def update(self):
        self.state_machine.update()

    def draw(self):
        self.state_machine.draw()
