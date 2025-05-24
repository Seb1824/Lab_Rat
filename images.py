# images.py

import pygame
from constants import CELL_SIZE

def load_scaled_image(path):
    image = pygame.image.load(path).convert_alpha()
    return pygame.transform.scale(image, (CELL_SIZE, CELL_SIZE))

# Carga las imágenes base
rat_images = load_scaled_image("assets/rat.png")
robot_images = load_scaled_image("assets/robot.png")
cheese_images = load_scaled_image("assets/cheese.png")

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
