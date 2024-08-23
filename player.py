from settings import *


class Player(pygame.sprite.Sprite):
    def __init__(self, pos, group, collision_sprites):
        super().__init__(group)
        self.image = pygame.Surface((48, 56))
        self.image.fill('red')
        self.rect = self.image.get_frect(topleft=pos)

        # Copy of previous position
        self.prev_rect = self.rect.copy()

        # Movement of the player
        self.direction = Vector(0, 0)
        self.speed = 300
        self.gravity = 2500

        # Collisions
        self.collision_sprites = collision_sprites

    def input(self):
        keys = pygame.key.get_pressed()

        # input vector used to get player input on the axis
        # and to stop the player if both directions are pressed at the same time
        input_vector = Vector(0, 0)
        if keys[pygame.K_d]:
            input_vector.x += 1
        if keys[pygame.K_a]:
            input_vector.x -= 1

        # Normalize the input vector to ensure the direction vector is always a unit vector
        if input_vector.x:
            self.direction.x = input_vector.normalize().x
        else:
            self.direction.x = input_vector.x

    def apply_gravity(self, dt):
        self.direction.y += self.gravity * dt

    # Move the player according to its direction and speed
    def move(self, dt):
        # Horizontal movement
        # Move the player in the horizontal direction then check horizontal collisions
        self.rect.x += self.direction.x * self.speed * dt
        self.check_collisions_x()

        # Vertical movement
        # Move the player in the vertical direction then check vertical collisions
        self.rect.y += self.direction.y * dt
        self.check_collisions_y()

    def check_collisions_x(self):
        for sprite in self.collision_sprites:
            if self.rect.colliderect(sprite.rect):
                # Check Left collision
                if self.rect.left <= sprite.rect.right and self.prev_rect.left >= sprite.prev_rect.right:
                    self.rect.left = sprite.rect.right

                # Check Right collision
                if self.rect.right >= sprite.rect.left and self.prev_rect.right <= sprite.prev_rect.left:
                    self.rect.right = sprite.rect.left

    def check_collisions_y(self):
        for sprite in self.collision_sprites:
            if self.rect.colliderect(sprite.rect):

                if self.rect.bottom >= sprite.rect.top and self.prev_rect.bottom <= sprite.prev_rect.top:
                    self.rect.bottom = sprite.rect.top

                if self.rect.top <= sprite.rect.bottom and self.prev_rect.top >= sprite.prev_rect.bottom:
                    self.rect.top = sprite.rect.bottom

                self.direction.y = 0

    def update(self, dt):
        self.prev_rect = self.rect.copy()
        self.input()
        self.apply_gravity(dt)
        self.move(dt)
