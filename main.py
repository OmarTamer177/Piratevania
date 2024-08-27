from settings import *
from level import Level


class Game:
    def __init__(self):
        # Create The Basic screen setup
        self.screen = pygame.display.set_mode(WINDOWED_SIZE, pygame.SCALED)
        self.clock = pygame.time.Clock()
        pygame.display.set_caption('PirateVania')

        # Importing tiled maps in a dictionary, and the current level is selected from it
        self.maps = {
            0: load_pygame(join('Assets', 'data', 'levels', 'omni.tmx')),
        }
        self.current_level = Level(self.maps[0])

    def run(self):
        # Basic Game-Loop
        while True:
            # Calculating delta-time and passing it to the level run method
            # Which passes it to all sprites
            dt = self.clock.tick(FPS) / 1000
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        sys.exit()

            # Run Level and handle the level's sprites
            self.current_level.run(dt)

            pygame.display.flip()


if __name__ == '__main__':
    game = Game()
    game.run()
