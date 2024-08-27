import pygame

from settings import *


# Sprite class is responsible for loading a sprite objects and adding them to different groups
class Sprite(pygame.sprite.Sprite):
    def __init__(self, pos, surf=pygame.Surface((TILE_SIZE, TILE_SIZE)), group=None):
        super().__init__(group)  # Pass groups correctly
        self.image = surf
        self.image.fill('white')
        self.rect = self.image.get_frect(topleft=pos)

        # Copy of previous position
        self.prev_rect = self.rect.copy()


class MovingSprite(Sprite):
    def __init__(self, group, start_point, end_point, move_dir, speed):
        super().__init__(start_point, pygame.Surface((200, 50)), group=group)
        self.rect.center = start_point

        self.start_point = start_point
        self.end_point = end_point
        self.speed = speed
        self.move_dir = move_dir

        self.direction = Vector(1, 0) if move_dir == 'x' else Vector(0, 1)
        self.moving = True

    def update(self, dt):
        self.prev_rect = self.rect.copy()
        self.rect.topleft += self.direction * self.speed * dt

        if self.move_dir == 'x':
            if self.direction == Vector(1, 0) and self.rect.right >= self.end_point[0]:
                self.direction = Vector(-1, 0)
            elif self.direction == Vector(-1, 0) and self.rect.left <= self.start_point[0]:
                self.direction = Vector(1, 0)
        elif self.move_dir == 'y':
            if self.direction == Vector(0, 1) and self.rect.bottom >= self.end_point[1]:
                self.direction = Vector(0, -1)
            elif self.direction == Vector(0, -1) and self.rect.top <= self.start_point[1]:
                self.direction = Vector(0, 1)

