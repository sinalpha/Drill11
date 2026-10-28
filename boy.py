from pico2d import (load_image, SDL_KEYDOWN, SDL_KEYUP,
                    SDLK_LEFT, SDLK_RIGHT)
from transitions import Machine


class Boy:
    states = ['IDLE', 'RUN']

    def __init__(self):
        self.x, self.y = 400, 90
        self.frame = 0
        self.face_dir = 1
        self.dir = 0
        self.image = load_image('animation_sheet.png')
        self.machine = Machine(model=self, states=Boy.states, initial='IDLE',
                               auto_transitions=False)
        self.machine.add_transition('run', 'IDLE', 'RUN')
        self.machine.add_transition('stop', 'RUN', 'IDLE')

    def handle_event(self, event):
        if event.type == SDL_KEYDOWN:
            if event.key in (SDLK_LEFT, SDLK_RIGHT):
                self.dir = self.face_dir = 1 if event.key == SDLK_RIGHT else -1
                if self.state != 'RUN':
                    self.run()
        elif event.type == SDL_KEYUP and self.state == 'RUN':
            if event.key in (SDLK_LEFT, SDLK_RIGHT):
                self.dir = 0
                self.stop()

    def update(self):
        if self.state == 'IDLE':
            self.frame = (self.frame + 1) % 8
        elif self.state == 'RUN':
            self.frame = (self.frame + 1) % 8
            self.x += self.dir * 5

    def draw(self):
        if self.state == 'RUN':
            row = 100 if self.face_dir == 1 else 0
        else:
            row = 300 if self.face_dir == 1 else 200
        self.image.clip_draw(self.frame * 100, row, 100, 100, self.x, self.y)
