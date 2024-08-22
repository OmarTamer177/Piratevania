import pygame
import sys
pygame.init()

# Window size
MY_SCREEN_SIZE = pygame.display.Info()
FULL_SCREEN_SIZE = (MY_SCREEN_SIZE.current_w, MY_SCREEN_SIZE.current_h)
WINDOWED_SIZE = (1280, 720)

# Frames Per Second
FPS = 60

# Flags
fullscreen = False
