# main.py

import pygame
import random
from constants import *
from maze import generate_maze
from player import update_player_position
from a_star import a_star

pygame.init()
WIN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Lab Rat Escape")

from images import rat_images, robot_images, cheese_images, start_bg, win_bg, button_play, lose_overlay

# Retardo en frames
robot_move_delay = 2  
robot_move_counter = 0

#maze = generate_maze(GRID_HEIGHT, GRID_WIDTH)
#goal_pos = (GRID_HEIGHT - 2, GRID_WIDTH - 2)

def draw_grid(maze):
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

def button_clicked(button_rect):
    return button_rect.collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0]

def start_screen():
    while True:
        WIN.blit(start_bg, (0, 0))
        btn_rect = WIN.blit(button_play, (SCREEN_WIDTH // 2 - 110, SCREEN_HEIGHT // 2 + 6))
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if button_clicked(btn_rect):
                    return

def end_screen(won, maze=None):
    while True:
        if won:
            WIN.blit(win_bg, (0, 0))
            btn_rect = WIN.blit(button_play, (SCREEN_WIDTH // 2 - 110, SCREEN_HEIGHT // 2 + 105))
        else:
            draw_grid(maze)

            s = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
            s.set_alpha(180)
            s.fill((0, 0, 0))
            WIN.blit(s, (0, 0))
            WIN.blit(lose_overlay, (0, 0))
            btn_rect = WIN.blit(button_play, (SCREEN_WIDTH // 2 - 110, SCREEN_HEIGHT // 2 + 125))

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if button_clicked(btn_rect):
                    return


def main():
    global player_pos, player_dir, robot_pos, robot_dir

    while True:
        start_screen()
        # Reset positions y laberinto
        maze = generate_maze(GRID_HEIGHT, GRID_WIDTH)
        goal_pos = (GRID_HEIGHT - 2, GRID_WIDTH - 2)
        player_pos = (1, 1)
        robot_pos = (GRID_HEIGHT - 2, 1)
        
        player_dir = (0, 1)
        robot_dir = (0, -1)
        

        cheese_shake_timer = 0
        cheese_shake_duration = 5
        cheese_shake_cooldown = FPS * 3
        cheese_shaking = False
        cheese_offset = (0, 0)

        robot_move_delay = 5
        robot_move_counter = 0

        clock = pygame.time.Clock()
        running = True
        while running:
            clock.tick(FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit(); exit()

            keys = pygame.key.get_pressed()
            player_pos, player_dir = update_player_position(keys, player_pos, player_dir, maze)

            # Movimiento robot más lento
            robot_move_counter += 1
            if robot_move_counter >= robot_move_delay:
                path = a_star(robot_pos, player_pos, maze)
                if path:
                    new_robot_pos = path[0]
                    robot_dir = (new_robot_pos[0] - robot_pos[0], new_robot_pos[1] - robot_pos[1])
                    robot_pos = new_robot_pos
                robot_move_counter = 0

            # Sacudida del queso
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

            WIN.fill(WHITE)
            draw_grid(maze)
            draw_image(goal_pos, cheese_images, offset=cheese_offset)
            draw_image(player_pos, rat_images.get(player_dir, rat_images[(0, 1)]))
            draw_image(robot_pos, robot_images.get(robot_dir, robot_images[(0, -1)]))
            pygame.display.update()

            if player_pos == goal_pos:
                end_screen(won=True)
                break
            elif robot_pos == player_pos:
                end_screen(won=False, maze=maze)
                break

if __name__ == "__main__":
    main()