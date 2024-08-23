from settings import *
from level import Level


class Game:
    def __init__(self):
        # Start in windowed mode
        self.screen = pygame.display.set_mode(WINDOWED_SIZE, pygame.SCALED)
        self.clock = pygame.time.Clock()
        pygame.display.set_caption('PirateVania')

        self.maps = {0: load_pygame(join('Assets', 'data', 'levels', 'omni.tmx'))}

        self.current_level = Level(self.maps[0])

    def run(self):
        while True:
            dt = self.clock.tick(FPS) / 1000
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            self.current_level.run(dt)

            pygame.display.flip()


if __name__ == '__main__':
    game = Game()
    game.run()
