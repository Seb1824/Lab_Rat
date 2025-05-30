# images.py

import pygame
from content.constants import CELL_SIZE

def load_scaled_image(path, target_size=None):
    image = pygame.image.load(path).convert_alpha()
    if target_size:
        image = pygame.transform.scale(image, target_size)
    return image


# Fondo
start_bg = load_scaled_image("assets/start_bg.png", (600, 600))
win_bg = load_scaled_image("assets/win_bg.png", (600, 600))
lose_overlay = load_scaled_image("assets/lose_overlay.png", (600, 600))

# Botones
button_play = load_scaled_image("assets/button_play.png", (230, 100))
#button_retry = load_scaled_image("assets/button_retry.png", size=(200, 80))

# Imágenes base
rat_images = load_scaled_image("assets/rat.png", (CELL_SIZE, CELL_SIZE))
robot_images = load_scaled_image("assets/robot.png", (CELL_SIZE, CELL_SIZE))
cheese_images = load_scaled_image("assets/cheese.png", (CELL_SIZE, CELL_SIZE))

# Diccionarios de imágenes rotadas según dirección
def get_rotated_images(base_image):
    return {
        (0, -1): pygame.transform.rotate(base_image, -90),  # izquierda
        (0, 1): pygame.transform.rotate(base_image, 90),    # derecha
        (-1, 0): pygame.transform.rotate(base_image, 180),  # arriba
        (1, 0): base_image                                  # abajo
    }

rat_images = get_rotated_images(rat_images)
robot_images = get_rotated_images(robot_images)
