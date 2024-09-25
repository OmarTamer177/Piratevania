from settings import *


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
