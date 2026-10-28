from pico2d import (load_image, get_time, SDL_KEYDOWN, SDL_KEYUP,
                    SDLK_SPACE, SDLK_LEFT, SDLK_RIGHT, SDLK_a)
from transitions import Machine


class Boy:
    states = ['IDLE', 'SLEEP', 'RUN', 'AUTORUN']

    def __init__(self):
        self.x, self.y = 400, 90
        self.frame = 0
        self.face_dir = 1
        self.dir = 0
        self.image = load_image('animation_sheet.png')
        self.machine = Machine(model=self, states=Boy.states, initial='IDLE',
                               auto_transitions=False)
        self.machine.add_transition('time_out', 'IDLE', 'SLEEP')
        self.machine.add_transition('space_down', 'SLEEP', 'IDLE')
        self.machine.add_transition('run', ['IDLE', 'SLEEP', 'AUTORUN'], 'RUN')
        self.machine.add_transition('stop', 'RUN', 'IDLE')
        self.machine.add_transition('auto_run', ['IDLE', 'SLEEP'], 'AUTORUN')
        self.machine.add_transition('auto_run_end', 'AUTORUN', 'IDLE')
        self.idle_start_time = get_time()
        self.auto_run_start_time = get_time()

    def on_enter_IDLE(self):
        self.idle_start_time = get_time()

    def on_enter_AUTORUN(self):
        self.dir = self.face_dir
        self.auto_run_start_time = get_time()

    def handle_event(self, event):
        if event.type == SDL_KEYDOWN:
            if self.state == 'SLEEP' and event.key == SDLK_SPACE:
                self.space_down()
            elif self.state in ('IDLE', 'SLEEP') and event.key == SDLK_a:
                self.auto_run()
            elif event.key in (SDLK_LEFT, SDLK_RIGHT):
                self.dir = self.face_dir = 1 if event.key == SDLK_RIGHT else -1
                if self.state != 'RUN':
                    self.run()
        elif event.type == SDL_KEYUP and self.state == 'RUN':
            if (event.key == SDLK_RIGHT and self.dir == 1) or \
                    (event.key == SDLK_LEFT and self.dir == -1):
                self.dir = 0
                self.stop()

    def update(self):
        if self.state == 'IDLE':
            self.frame = (self.frame + 1) % 8
            if get_time() - self.idle_start_time >= 5.0:
                self.time_out()
        elif self.state == 'RUN':
            self.frame = (self.frame + 1) % 8
            self.x += self.dir * 5
        elif self.state == 'AUTORUN':
            self.frame = (self.frame + 1) % 8
            self.x += self.dir * 5
            if get_time() - self.auto_run_start_time >= 5.0:
                self.dir = 0
                self.auto_run_end()

    def draw(self):
        if self.state in ('RUN', 'AUTORUN'):
            row = 100 if self.face_dir == 1 else 0
        else:
            row = 300 if self.face_dir == 1 else 200
        self.image.clip_draw(self.frame * 100, row, 100, 100, self.x, self.y)
