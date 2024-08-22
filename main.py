from settings import *

# Start in windowed mode
screen = pygame.display.set_mode(WINDOWED_SIZE, pygame.SCALED)
clock = pygame.time.Clock()
pygame.display.set_caption('PirateVania')

while True:
    screen.fill((0, 0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()

    pygame.display.flip()
    clock.tick(60)
