from settings import *


class CameraGroup(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.screen = pygame.display.get_surface()
        self.offset = Vector(0, 0)
        self.target_offset = Vector(0, 0)
        self.transition_speed = 5  # Controls how fast the camera slides

        # Fade effect
        self.fade_surface = pygame.Surface(self.screen.get_size())
        self.fade_surface.fill((0, 0, 0))
        self.fade_alpha = 0
        self.is_fading = False
        self.fade_in = True
        self.fade_duration = 1000  # Duration in milliseconds
        self.fade_start_time = None

        # screen shake
        self.shake_pos = Vector(0, 0)
        self.shake_power = 0

    def start_slide(self, player_pos):
        """Start sliding the camera to the target position and trigger fade."""
        self.target_offset = Vector(
            player_pos[0] - self.screen.get_width() // 2,
            player_pos[1] - self.screen.get_height() // 2
        )
        self.is_fading = True
        self.fade_in = True
        self.fade_start_time = pygame.time.get_ticks()

    def update_camera(self, dt):
        """Slide the camera towards the target offset smoothly."""
        direction = self.target_offset - self.offset
        if direction.length() > 1:
            self.offset += direction * self.transition_speed * dt

    def handle_fade(self):
        """Handle the fade in and fade out effect."""
        if self.is_fading:
            current_time = pygame.time.get_ticks()
            elapsed_time = current_time - self.fade_start_time
            fade_progress = elapsed_time / self.fade_duration

            if self.fade_in:
                self.fade_alpha = min(255, fade_progress * 255)
                if self.fade_alpha >= 255:
                    self.fade_in = False
                    self.fade_start_time = pygame.time.get_ticks()  # Restart timer for fade out
            else:
                self.fade_alpha = max(0, 255 - fade_progress * 255)
                if self.fade_alpha <= 0:
                    self.is_fading = False  # End fading

            self.fade_surface.set_alpha(self.fade_alpha)
            self.screen.blit(self.fade_surface, (0, 0))

    def draw(self, dt):
        # Update camera position
        self.update_camera(dt)

        # Draw all sprites with the updated offset
        self.shake_pos = Vector(randint(-self.shake_power, self.shake_power),
                                randint(-self.shake_power, self.shake_power))
        for sprite in self:
            pos = sprite.rect.topleft - self.offset + self.shake_pos
            self.screen.blit(sprite.image, pos)

        # Handle the fade effect
        if self.is_fading:
            self.handle_fade()
