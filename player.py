from settings import *
from timer import Timer
from input import Input


class Player(pygame.sprite.Sprite):
    def __init__(self, input_system, pos, group, collision_sprites, semi_collision_sprites):
        super().__init__(group)

        # Load the character's input system
        self.input_system = input_system

        # Add the character's inputs to the input system
        inputs = {
            pygame.K_a: Input(self.left_pressed, self.left_released),
            pygame.K_d: Input(self.right_pressed, self.right_released),
            pygame.K_s: Input(self.down_pressed),
            pygame.K_SPACE: Input(self.jump_pressed),
            pygame.K_LSHIFT: Input(self.dash_pressed),
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
        self.input_vector = Vector(0, 0)   # Used to capture the direction of the player input in the x-axis
        self.velocity = Vector(0, 0)
        self.speed = 300
        self.gravity = 2000
        self.jump_force = -830
        self.wall_jump_force = -600
        self.dash = False
        self.dash_speed = 1700

        # Collision groups with the player
        self.collision_sprites = collision_sprites
        self.semi_collision_sprites = semi_collision_sprites
        self.on_surface = {'floor': False, 'left': False, 'right': False}
        self.platform = None

        # Timers
        self.timers = {
            'wall jump': Timer(200),
            'wall slide block': Timer(300),
            'dash': Timer(100, self.deactivate_dash),
            'dash delay': Timer(700),
            'platform skip': Timer(200),
        }

    def left_pressed(self):
        self.input_vector.x -= 1

    def left_released(self):
        self.input_vector.x += 1

    def right_pressed(self):
        self.input_vector.x += 1

    def right_released(self):
        self.input_vector.x -= 1

    def down_pressed(self):
        self.timers['platform skip'].activate()

    def jump_pressed(self):
        # Jump only if the player in on ground or touching a wall and player is not dashing
        if not self.dash:
            # Normal Jump, if on floor
            if self.on_surface['floor']:
                self.velocity.y = self.jump_force
                # player can't wall slide until he has been airborne for some time,
                # to execute the jump properly if player is beside a wall
                self.timers['wall slide block'].activate()
            # Wall jump, if touching either wall and sliding
            elif not self.timers['wall slide block'].active and (self.on_surface['left'] or self.on_surface['right']):
                # Activate a timer to block movement when wall jumping
                self.timers['wall jump'].activate()
                self.velocity.y = self.wall_jump_force
                # Give a slight push outside the wall, needed because of the movement block
                if self.on_surface['left']:
                    self.velocity.x = 1
                elif self.on_surface['right']:
                    self.velocity.x = -1

    def dash_pressed(self):
        if self.input_vector.x and not self.dash and not self.timers['dash delay'].active:
            self.dash = True
            self.timers['dash'].activate()

    # Move the player according to its direction and speed
    def move(self, dt):
        # Assign the velocity according to the player's input,
        # if movement isn't locked by wall jumping or player dashing
        if not self.timers['wall jump'].active and not self.dash:
            # Normalize the input vector to ensure the direction vector is always a unit vector
            if self.input_vector.x:
                self.velocity.x = self.input_vector.normalize().x
            else:
                self.velocity.x = 0

        # Horizontal movement
        # Move the player in the horizontal direction then check horizontal collisions...

        # Player moves with the dash speed if he is dashing, and normal speed if not dashing
        if self.dash:
            # Note: Fetch the direction of dashing from the input vector, not the velocity vector
            # as it doesn't allow choosing dashing direction when blocking the movement when wall jumping
            dash_direction = self.input_vector.normalize().x if self.input_vector.x else 0
            self.rect.x += dash_direction * self.dash_speed * dt
            self.velocity.y = 0   # stop falling while dashing
        else:
            self.rect.x += self.velocity.x * self.speed * dt

        self.check_collisions_x()

        # Vertical movement
        # Move the player in the vertical direction then check vertical collisions...

        # Player can wall slide only if he is not touching the ground and touching a wall
        # and has been airborne for some time, else: fall with gravity
        if (not self.timers['wall slide block'].active and not self.on_surface['floor']
                and (self.on_surface['right'] or self.on_surface['left'])):
            # Give The player a constant falling speed on wall slide
            self.rect.y += self.gravity / 10 * dt
        else:
            # Add vertical acceleration(aka gravity) to the vertical velocity
            # vf = vi + a.t,
            # df = di + v.t
            self.velocity.y += self.gravity * dt
            self.rect.y += self.velocity.y * dt

        self.check_collisions_y()

    def move_platform(self, dt):
        # If the player is in contact with the platform, move with it
        if self.platform:
            self.rect.topleft += self.platform.direction * self.platform.speed * dt

    def deactivate_dash(self):
        self.dash = False
        self.timers['dash delay'].activate()

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

                self.velocity.y = 0

        # Check collisions with semi-collidable platforms if player is not skipping platforms
        if not self.timers['platform skip'].active:
            for sprite in self.semi_collision_sprites:
                # Check Bottom collision
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
        self.move(dt)
        self.check_contact()
