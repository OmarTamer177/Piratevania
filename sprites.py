from settings import *


class Sprite(pygame.sprite.Sprite):
    def __init__(self, pos, surf, *groups):  # *groups allows multiple groups to be passed
        super().__init__(*groups)  # Pass groups correctly
        self.image = pygame.Surface((TILE_SIZE, TILE_SIZE))
        self.image.fill('white')
        self.rect = self.image.get_frect(topleft=pos)
