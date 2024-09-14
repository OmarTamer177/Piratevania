import pygame
import sys
from os.path import join
from pygame.math import Vector2 as Vector
from pytmx.util_pygame import load_pygame
from random import randint

pygame.init()

# Window size
MY_SCREEN_SIZE = pygame.display.Info()
FULL_SCREEN_SIZE = (MY_SCREEN_SIZE.current_w, MY_SCREEN_SIZE.current_h)
WINDOWED_SIZE = (1280, 720)

# Constants
FPS = 60
TILE_SIZE = 64
