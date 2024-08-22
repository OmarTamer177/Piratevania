from settings import *

# Start in windowed mode
screen = pygame.display.set_mode(WINDOWED_SIZE, pygame.SCALED)
clock = pygame.time.Clock()
pygame.display.set_caption('PirateVania')

player_surf = pygame.Surface((50, 50))
player_surf.fill('blue')
player_rect = player_surf.get_rect(center=(100, 200))

direction = 0
speed = 600

gravity = 1000
vel_y = 0

platform_surf = pygame.Surface((400, 50))

while True:
    dt = clock.tick(240) / 1000  # Time in seconds
    screen.fill((0, 0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()
            elif event.key == pygame.K_LEFT:
                direction = -1
            elif event.key == pygame.K_RIGHT:
                direction = 1

            if event.key == pygame.K_f:
                fullscreen = not fullscreen
                # Pause briefly before switching to avoid flicker
                pygame.time.delay(100)
                if fullscreen:
                    screen = pygame.display.set_mode(FULL_SCREEN_SIZE, pygame.FULLSCREEN)
                else:
                    screen = pygame.display.set_mode(WINDOWED_SIZE)

        if event.type == pygame.KEYUP:
            if (event.key == pygame.K_LEFT and direction == -1) or (event.key == pygame.K_RIGHT and direction == 1):
                direction = 0

    # Update player position
    player_rect.x += direction * speed * dt
    vel_y += gravity * dt
    player_rect.y += vel_y * dt

    if player_rect.top > 720:
        player_rect.bottom = 0

    # Draw the updated scene
    screen.blit(player_surf, player_rect)
    pygame.display.flip()
