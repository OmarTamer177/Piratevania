import pygame.display

from settings import *
from timer import Timer
from input import InputSystem, Input


class Player(pygame.sprite.Sprite):
    def __init__(self, input_system, pos, group, collision_sprites, semi_collision_sprites):
        super().__init__(group)

        # Load the character's input system
        self.input_system = input_system

        # Add the character's inputs to the input system
        inputs = {
            pygame.K_SPACE: Input(lambda: print("jump")),
        }
        for key, value in inputs.items():
            self.input_system.add_input(key, value)

        # Load surface and rect
        self.image = pygame.Surface((45, 54))
        self.image.fill('red')

        self.rect = self.image.get_frect(topleft=pos)

        # Copy of previous position
        self.prev_rect = self.rect.copy()

        # Movement of the player
        self.velocity = Vector(0, 0)
        self.speed = 300
        self.gravity = 2000
        self.jump = False
        self.jump_force = -800
        self.dash = False
        self.dash_speed = 1700

        # Collisions
        self.collision_sprites = collision_sprites
        self.semi_collision_sprites = semi_collision_sprites
        self.on_surface = {'floor': False, 'left': False, 'right': False}
        self.platform = None

        # Timers
        self.timers = {
            'wall jump': Timer(200),
            'wall slide block': Timer(300),
            'dash': Timer(100, lambda: self.deactivate_dash()),
            'dash delay': Timer(700),
            'platform skip': Timer(200),
        }

    def input(self):
        keys = pygame.key.get_pressed()

        # input vector used to get player input on the axis
        # and to stop the player if both directions are pressed at the same time
        input_vector = Vector(0, 0)
        if not self.timers['wall jump'].active and not self.dash:
            if keys[pygame.K_d]:
                input_vector.x += 1
            if keys[pygame.K_a]:
                input_vector.x -= 1
            if keys[pygame.K_s]:
                self.timers['platform skip'].activate()

            # Dash on left shift
            if keys[pygame.K_LSHIFT] and input_vector.x:
                if not self.dash and not self.timers['dash delay'].active:
                    self.dash = True
                    self.velocity.x = input_vector.x  # Lock in the direction
                    self.timers['dash'].activate()

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
        if self.dash and not self.timers['dash delay'].active:
            self.rect.x += self.velocity.x * self.dash_speed * dt
            self.velocity.y = 0
        else:
            self.rect.x += self.velocity.x * self.speed * dt
        self.check_collisions_x()

        # Vertical movement
        # Move the player in the vertical direction then check vertical collisions.

        # Player can wall slide only if he is not touching the ground and touching a wall
        # and has been airborne for some time, else: fall with gravity
        if (not self.timers['wall slide block'].active and not self.on_surface['floor']
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

        # Jump only if the player in on ground or touching a wall and player is not dashing
        if self.jump and not self.dash:
            if self.on_surface['floor']:
                self.velocity.y = self.jump_force
                self.timers['wall slide block'].activate()
            elif not self.timers['wall slide block'].active and (self.on_surface['left'] or self.on_surface['right']):
                self.timers['wall jump'].activate()
                self.velocity.y = -600
                self.velocity.x = 1 if self.on_surface['left'] else -1
            self.jump = False

    def deactivate_dash(self):
        self.dash = False
        self.timers['dash delay'].activate()

    def move_platform(self, dt):
        if self.platform:
            self.rect.topleft += self.platform.direction * self.platform.speed * dt

    # Create rects under the player, to his left and to his right to check for contacts with other sprites
    def check_contact(self):
        # Place rectangles on the bottom, right and left of player
        floor_rect = pygame.Rect(self.rect.bottomleft, (self.rect.width, 2))
        left_rect = pygame.Rect((self.rect.topleft + Vector(-2, self.rect.height / 4)), (2, self.rect.height / 2))
        right_rect = pygame.Rect((self.rect.topright + Vector(0, self.rect.height / 4)), (2, self.rect.height / 2))

        # Place sprite rects in a list
        collidable_contacts = [sprite.rect for sprite in self.collision_sprites]
        semi_collidable_contacts = [sprite.rect for sprite in self.semi_collision_sprites]

        # And check for contact of that list with the player
        self.on_surface['floor'] = True if (floor_rect.collidelist(collidable_contacts + semi_collidable_contacts) >= 0
                                            and self.velocity.y >= 0) else False
        self.on_surface['left'] = True if left_rect.collidelist(collidable_contacts) >= 0 else False
        self.on_surface['right'] = True if right_rect.collidelist(collidable_contacts) >= 0 else False

        # Check for contacts with moving platforms
        self.platform = None
        sprites = self.collision_sprites.sprites() + self.semi_collision_sprites.sprites()
        for sprite in [sprite for sprite in sprites if hasattr(sprite, 'moving')]:
            if sprite.rect.colliderect(floor_rect):
                self.platform = sprite

    def check_collisions_x(self):
        for sprite in self.collision_sprites:
            if self.rect.colliderect(sprite.rect):
                # Check Left collision
                if self.rect.left <= sprite.rect.right and int(self.prev_rect.left) >= int(sprite.prev_rect.right):
                    self.rect.left = sprite.rect.right

                # Check Right collision
                if self.rect.right >= sprite.rect.left and int(self.prev_rect.right) <= int(sprite.prev_rect.left):
                    self.rect.right = sprite.rect.left

    def check_collisions_y(self):
        for sprite in self.collision_sprites:
            if self.rect.colliderect(sprite.rect):

                # Check Bottom collision
                if self.rect.bottom >= sprite.rect.top and int(self.prev_rect.bottom) <= int(sprite.prev_rect.top):
                    self.rect.bottom = sprite.rect.top

                # Check Top collision
                if self.rect.top <= sprite.rect.bottom and int(self.prev_rect.top) >= int(sprite.prev_rect.bottom):
                    self.rect.top = sprite.rect.bottom
                    if hasattr(sprite, 'moving'):
                        self.rect.top += 5
                    self.jump = False

                self.velocity.y = 0

        # Check collisions with semi-collidable platforms
        for sprite in self.semi_collision_sprites:
            # Check Bottom collision
            if not self.timers['platform skip'].active:
                if self.rect.colliderect(sprite.rect):
                    if self.rect.bottom >= sprite.rect.top and int(self.prev_rect.bottom) <= int(sprite.prev_rect.top):
                        self.rect.bottom = sprite.rect.top
                        if self.velocity.y >= 0:
                            self.velocity.y = 0

    def update_timers(self):
        for timer in self.timers.values():
            timer.update()

    def update(self, dt):
        self.prev_rect = self.rect.copy()
        self.update_timers()
        self.move_platform(dt)
        self.input()
        self.move(dt)
        self.check_contact()
