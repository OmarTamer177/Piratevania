import pygame.sprite
import pytmx
from settings import *
from sprites import Sprite
from player import Player


# Level class holds the tiled map and sprites needed for the level
class Level:
    def __init__(self, tmx_map: pytmx.TiledMap):
        self.screen = pygame.display.get_surface()    # Gets the screen

        # Sprite groups
        self.all_sprites = pygame.sprite.Group()      # Create a sprite group to handle the sprites
        self.collision_group = pygame.sprite.Group()  # Create a group to check collisions between sprites

        self.setup(tmx_map)                           # Set up the tiled map

    # Method used to load the tiles and objects in the tiled map to all_sprites group
    def setup(self, tmx_map: pytmx.TiledMap):
        # For each tile we need to multiply the position with the tile size,
        # as the position is its arrangement not the absolute position,
        # and Instantiate a new sprite object
        for x, y, surf in tmx_map.get_layer_by_name('Terrain').tiles():
            Sprite((x * TILE_SIZE, y * TILE_SIZE), surf, (self.all_sprites, self.collision_group))

        # For the objects, their position is the absolute position unlike regular tiles
        for obj in tmx_map.get_layer_by_name('Objects'):
            # Instantiate a player object if the current object in tiled map objects is a player
            if obj.name == 'player':
                Player((obj.x, obj.y), self.all_sprites, self.collision_group)

        # Moving objects
        for obj in tmx_map.get_layer_by_name('Moving Objects'):
            if obj.name == 'helicopter':
                print("pp")

    # Load background, draw sprites and update them
    def run(self, dt):
        self.screen.fill('black')
        self.all_sprites.draw(self.screen)
        self.all_sprites.update(dt)
