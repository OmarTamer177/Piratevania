import pygame
import sys
from os.path import join
from os import walk
from pygame.math import Vector2 as Vector
from pytmx.util_pygame import load_pygame
from random import randint
from utils import *

pygame.init()

# Window size
MY_SCREEN_SIZE = pygame.display.Info()
FULL_SCREEN_SIZE = (MY_SCREEN_SIZE.current_w, MY_SCREEN_SIZE.current_h)
WINDOWED_SIZE = (1280, 720)

# Constants
FPS = 60
TILE_SIZE = 64

# Layers
LAYERS = {
    'bg': 0,
    'clouds': 1,
    'bg tiles': 2,
    'path': 3,
    'bg details': 4,
    'main': 5,
    'water': 6,
    'fg': 7,
}
