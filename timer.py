from pygame.time import get_ticks


class Timer:
    def __init__(self, duration, function=None, activate=False, loop=False):
        self.duration = duration
        self.start_time = 0
        self.function = function
        self.active = activate
        self.loop = loop

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
