import pytmx
from settings import *
from sprites import Sprite
from player import Player


class Level:
    def __init__(self, tmx_map: pytmx.TiledMap):
        self.screen = pygame.display.get_surface()    # Gets the screen
        self.all_sprites = pygame.sprite.Group()
        self.setup(tmx_map)

    def setup(self, tmx_map: pytmx.TiledMap):
        for x, y, surf in tmx_map.get_layer_by_name('Terrain').tiles():
            Sprite((x * TILE_SIZE, y * TILE_SIZE), surf, self.all_sprites)

        for obj in tmx_map.get_layer_by_name('Objects'):
            if obj.name == 'player':
                Player((obj.x, obj.y), self.all_sprites)

    def run(self, dt):
        self.screen.fill('black')
        self.all_sprites.draw(self.screen)
        self.all_sprites.update(dt)
