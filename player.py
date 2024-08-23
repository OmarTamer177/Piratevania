from settings import *


class Player(pygame.sprite.Sprite):
    def __init__(self, pos, *groups):
        super().__init__(*groups)
        self.image = pygame.Surface((48, 56))
        self.image.fill('red')
        self.rect = self.image.get_frect(topleft=pos)

        # Movement
        self.direction = Vector(0, 0)
        self.speed = 200

    def input(self):
        keys = pygame.key.get_pressed()

        input_vector = Vector(0, 0)
        if keys[pygame.K_d]:
            input_vector.x += 1
        if keys[pygame.K_a]:
            input_vector.x -= 1

        if input_vector:
            self.direction = input_vector.normalize()
        else:
            self.direction = input_vector

    def move(self, dt):
        self.rect.topleft += self.direction * self.speed * dt

    def update(self, dt):
        self.input()
        self.move(dt)
