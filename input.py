from settings import *


class Input:
    def __init__(self, keydown=None, keyup=None):
        self.keyup = keyup
        self.keydown = keydown


class InputSystem:
    def __init__(self, inputs: dict[pygame.constants, Input]):
        self.inputs = inputs

    def add_input(self, key, new_input):
        self.inputs[key] = new_input

    def execute_keydown(self, key):
        if self.inputs[key].keydown:
            self.inputs[key].keydown()

    def execute_keyup(self, key):
        if self.inputs[key].keyup:
            self.inputs[key].keyup()
