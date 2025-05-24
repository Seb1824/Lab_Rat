# main.py

import pygame
import random
from constants import *
from maze import generate_maze
from player import player_pos, player_dir, update_player_position
from robot import robot_pos, robot_dir
from a_star import a_star

pygame.init()
WIN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Lab Rat Escape")

from images import rat_images, robot_images, cheese_images

# Retardo en frames
robot_move_delay = 2  
robot_move_counter = 0

maze = generate_maze(GRID_HEIGHT, GRID_WIDTH)
goal_pos = (GRID_HEIGHT - 2, GRID_WIDTH - 2)

def draw_grid():
    for row in range(GRID_HEIGHT):
        for col in range(GRID_WIDTH):
            x = col * CELL_SIZE
            y = row * CELL_SIZE
            color = WHITE if maze[row][col] == 0 else BLACK
            pygame.draw.rect(WIN, color, (x, y, CELL_SIZE, CELL_SIZE))
            pygame.draw.rect(WIN, GRAY, (x, y, CELL_SIZE, CELL_SIZE), 1)

def draw_image(pos, image, offset=(0, 0)):
    x = pos[1] * CELL_SIZE + offset[0]
    y = pos[0] * CELL_SIZE + offset[1]
    WIN.blit(image, (x, y))


def main():
    global player_pos, player_dir, robot_pos, robot_dir
    clock = pygame.time.Clock()
    running = True
    global robot_move_counter
    cheese_shake_timer = 0
    cheese_shake_duration = 5      # duración de la sacudida 
    cheese_shake_cooldown = FPS * 2
    cheese_shaking = False
    cheese_offset = (0, 0)


    while running:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Moimiento del queso
        cheese_shake_timer += 1

        if cheese_shake_timer >= cheese_shake_cooldown:
            cheese_shaking = True
            cheese_shake_timer = 0

        if cheese_shaking:
            cheese_offset = (random.randint(-3, 3), random.randint(-3, 3))
            cheese_shake_duration -= 1
            if cheese_shake_duration <= 0:
                cheese_shaking = False
                cheese_shake_duration = 5
                cheese_offset = (0, 0)
        else:
            cheese_offset = (0, 0)


        # Movimiento del jugador
        keys = pygame.key.get_pressed()
        player_pos, player_dir = update_player_position(keys, player_pos, player_dir, maze)

        # Movimiento del robot con retardo
        robot_move_counter += 1
        if robot_move_counter >= robot_move_delay:
            path = a_star(robot_pos, player_pos, maze)
            if path:
                new_robot_pos = path[0]
                robot_dir = (new_robot_pos[0] - robot_pos[0], new_robot_pos[1] - robot_pos[1])
                robot_pos = new_robot_pos
            robot_move_counter = 0

        # Dibujar todo
        WIN.fill(WHITE)
        draw_grid()
        draw_image(goal_pos, cheese_images, offset=cheese_offset)
        draw_image(player_pos, rat_images.get(player_dir, rat_images[(0, 1)]))
        draw_image(robot_pos, robot_images.get(robot_dir, robot_images[(0, -1)]))

        pygame.display.update()

        # Condiciones de victoria o derrota
        if player_pos == goal_pos:
            print(MSG_WIN)
            running = False
        elif robot_pos == player_pos:
            print(MSG_LOSE)
            running = False

    pygame.quit()

if __name__ == "__main__":
    main()
