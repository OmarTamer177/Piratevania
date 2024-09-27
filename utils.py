from os.path import join
from os import walk
from typing import Dict, List

import pygame
from pygame import Surface, SurfaceType


def load_image(*path, file_type='png') -> pygame.Surface:
    full_path = join(*path) + f'.{file_type}'
    image = pygame.image.load(full_path).convert_alpha()
    return image


def load_animation(*path) -> list[pygame.Surface]:
    images = []

    for folder, _, frames_names in walk(str(join(*path))):
        for frame_name in sorted(frames_names, key=lambda name: int(name.split('.')[0])):
            image_path = join(folder, frame_name)
            image = pygame.image.load(image_path).convert_alpha()
            images.append(image)

    return images


def load_folder(*path) -> dict[str, pygame.Surface]:
    images = {}

    for folder, _, frames_names in walk(str(join(*path))):
        for frame_name in frames_names:
            image_path = join(folder, frame_name)
            image = pygame.image.load(image_path).convert_alpha()
            images[frame_name.split('.')[0]] = image

    return images


def load_animations(*path) -> dict[str, list[Surface]]:
    animations = {}

    for folder, sub_folders, __ in walk(str(join(*path))):
        for sub_folder in sub_folders:
            animations[sub_folder] = load_animation(folder, sub_folder)

    return animations
