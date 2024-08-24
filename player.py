from settings import *
from timer import Timer


class Player(pygame.sprite.Sprite):
    def __init__(self, pos, group, collision_sprites):
        super().__init__(group)
        self.image = pygame.Surface((48, 56))
        self.image.fill('red')
        self.rect = self.image.get_frect(topleft=pos)

        # Copy of previous position
        self.prev_rect = self.rect.copy()

        # Movement of the player
        self.velocity = Vector(0, 0)
        self.speed = 300
        self.gravity = 1300
        self.jump = False
        self.jump_force = -900

        # Collisions
        self.collision_sprites = collision_sprites
        self.on_surface = {'floor': False, 'left': False, 'right': False}

        # Timers
        self.timers = {
            'wall jump': Timer(200),
            'wall slide block': Timer(250),
        }

    def input(self):
        keys = pygame.key.get_pressed()

        # input vector used to get player input on the axis
        # and to stop the player if both directions are pressed at the same time
        input_vector = Vector(0, 0)
        if not self.timers['wall jump'].active:
            if keys[pygame.K_d]:
                input_vector.x += 1
            if keys[pygame.K_a]:
                input_vector.x -= 1

            # Normalize the input vector to ensure the direction vector is always a unit vector
            if input_vector.x:
                self.velocity.x = input_vector.normalize().x
            else:
                self.velocity.x = input_vector.x

        # Press space to jump
        if keys[pygame.K_SPACE]:
            self.jump = True

    # Move the player according to its direction and speed
    def move(self, dt):
        # Horizontal movement
        # Move the player in the horizontal direction then check horizontal collisions
        self.rect.x += self.velocity.x * self.speed * dt
        self.check_collisions_x()

        # Vertical movement
        # Move the player in the vertical direction then check vertical collisions.

        # Player can wall slide only if he is not touching the ground and touching a wall
        # and has been airborne for some time, else: fall with gravity
        if (not not self.timers['wall slide block'].active and not self.on_surface['floor']
                and (self.on_surface['right'] or self.on_surface['left'])):
            # Give The player a constant falling speed on wall slide
            self.velocity.y = self.gravity / 10 * dt
            self.rect.y += self.velocity.y
        else:
            # Add vertical acceleration(aka gravity) to the vertical velocity
            self.velocity.y += self.gravity / 2 * dt
            self.rect.y += self.velocity.y * dt
            self.velocity.y += self.gravity / 2 * dt

        self.check_collisions_y()

        # Jump only if the player in on ground or touching a wall
        if self.jump:
            if self.on_surface['floor']:
                self.timers['wall slide block'].activate()
                self.velocity.y = self.jump_force
            elif not self.timers['wall slide block'].active and (self.on_surface['left'] or self.on_surface['right']):
                self.timers['wall jump'].activate()
                self.velocity.y = self.jump_force
                self.velocity.x = 1 if self.on_surface['left'] else -1
            self.jump = False

    # Create rects under the player, to his left and to his right to check for contacts with other sprites
    def check_contact(self):
        # Place rectangles on the bottom, right and left of player
        floor_rect = pygame.Rect(self.rect.bottomleft, (self.rect.width, 2))
        left_rect = pygame.Rect((self.rect.topleft + Vector(-2, self.rect.height / 4)), (2, self.rect.height / 2))
        right_rect = pygame.Rect((self.rect.topright + Vector(0, self.rect.height / 4)), (2, self.rect.height / 2))

        # Debug
        pygame.draw.rect(pygame.display.get_surface(), 'yellow', floor_rect)
        pygame.draw.rect(pygame.display.get_surface(), 'yellow', left_rect)
        pygame.draw.rect(pygame.display.get_surface(), 'yellow', right_rect)

        # Place sprite rects in a list
        contacts = [sprite.rect for sprite in self.collision_sprites]

        # And check for contact of that list with the player
        self.on_surface['floor'] = True if floor_rect.collidelist(contacts) >= 0 else False
        self.on_surface['left'] = True if left_rect.collidelist(contacts) >= 0 else False
        self.on_surface['right'] = True if right_rect.collidelist(contacts) >= 0 else False

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

                # Check Bottom collision
                if self.rect.bottom >= sprite.rect.top and self.prev_rect.bottom <= sprite.prev_rect.top:
                    self.rect.bottom = sprite.rect.top

                # Check Top collision
                if self.rect.top <= sprite.rect.bottom and self.prev_rect.top >= sprite.prev_rect.bottom:
                    self.rect.top = sprite.rect.bottom
                    self.jump = False

                self.velocity.y = 0

    def update_timers(self):
        for timer in self.timers.values():
            timer.update()

    def update(self, dt):
        self.prev_rect = self.rect.copy()
        self.update_timers()
        self.check_contact()
        self.input()
        self.move(dt)
