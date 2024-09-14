from pygame.time import get_ticks


class Timer:
    def __init__(self, duration, function=None, auto_activate=False, loop=False):
        self.duration = duration
        self.start_time = 0
        self.function = function
        self.active = False
        self.loop = loop

        if auto_activate:
            self.activate()

    def activate(self):
        self.start_time = get_ticks()
        self.active = True

    def deactivate(self):
        self.start_time = 0
        self.active = False

    def update(self):
        if self.active:
            if get_ticks() - self.start_time >= self.duration:
                if self.function:
                    self.function()

                if self.loop:
                    self.activate()
                else:
                    self.deactivate()
