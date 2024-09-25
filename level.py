import pytmx

from settings import *
from input import InputSystem
from sprites import Sprite, MovingSprite
from player import Player
from groups import CameraGroup


# Level class holds the tiled map and sprites needed for the level
class Level:
    def __init__(self, tmx_map: pytmx.TiledMap, input_system: InputSystem):
        self.player = None
        self.screen = pygame.display.get_surface()    # Gets the screen

        # Sprite groups
        self.all_sprites = CameraGroup()              # Create a sprite group to handle the sprites
        self.collision_group = pygame.sprite.Group()  # Create a group to check collisions between sprites
        self.semi_collision_group = pygame.sprite.Group()  # Create a group to check collisions for semi-collidable sprites

        # Input system
        self.input_system = input_system

        # Set up the tiled map
        self.setup(tmx_map)

    # Method used to load the tiles and objects in the tiled map to all_sprites group
    def setup(self, tmx_map: pytmx.TiledMap):
        # For each tile in each layer we need to multiply the position with the tile size,
        # as the position is its arrangement not the absolute position,
        # and specify its type according to its layer
        # and Instantiate a new sprite object
        for layer in ['BG', 'Terrain', 'Platforms', 'FG']:
            for x, y, surf in tmx_map.get_layer_by_name(layer).tiles():
                # Add tiles to their suitable collision group, and add all to all_sprites camera group
                groups = [self.all_sprites]
                z = LAYERS['bg tiles']
                if layer == 'Terrain':
                    groups.append(self.collision_group)
                if layer == 'Platforms':
                    groups.append(self.semi_collision_group)
                if layer == 'FG':
                    z = LAYERS['fg']
                if layer == 'BG':
                    z = LAYERS['bg']
                Sprite(z, (x * TILE_SIZE, y * TILE_SIZE), surf, groups)

        # For the objects, their position is the absolute position unlike regular tiles
        for obj in tmx_map.get_layer_by_name('Objects'):
            # Instantiate a player object if the current object in tiled map objects is a player
            if obj.name == 'player':
                self.player = Player(self.input_system, (obj.x, obj.y), self.all_sprites, self.collision_group,
                                     self.semi_collision_group, LAYERS['main'])

        # Moving objects
        for obj in tmx_map.get_layer_by_name('Moving Objects'):
            if obj.name == 'helicopter':
                # Horizontal platform
                if obj.width > obj.height:
                    # obj.x and obj.y are the top-left point of the object
                    direction = 'x'
                    start_point = (obj.x, obj.y + obj.height/2)
                    end_point = (obj.x + obj.width, obj.y + obj.height/2)
                # Vertical platform
                else:
                    direction = 'y'
                    start_point = (obj.x + obj.width/2, obj.y)
                    end_point = (obj.x + obj.width/2, obj.y + obj.height)
                speed = obj.properties['speed']
                MovingSprite((self.all_sprites, self.semi_collision_group), start_point, end_point, direction, speed, LAYERS['main'])

    # Load background, draw sprites and update them
    def run(self, dt):
        self.screen.fill('black')
        self.all_sprites.draw(dt)
        self.all_sprites.update(dt)
        self.all_sprites.start_slide(self.player.rect.topleft)
