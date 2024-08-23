from settings import *


# Sprite class is responsible for loading a sprite objects and adding them to different groups
class Sprite(pygame.sprite.Sprite):
    def __init__(self, pos, surf, group):
        super().__init__(group)  # Pass groups correctly
        self.image = pygame.Surface((TILE_SIZE, TILE_SIZE))
        self.image.fill('white')
        self.rect = self.image.get_frect(topleft=pos)

        # Copy of previous position
        self.prev_rect = self.rect.copy()
