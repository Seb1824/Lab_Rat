import pygame
import random
from constants import *
from maze import generate_map
from player import player_pos, player_dir, update_player_position
from robot import robot_pos, robot_dir
from a_star import a_star

pygame.init()
WIN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Lab Rat Escape")

from images import rat_images, robot_images, cheese_images, start_bg, win_bg, button_play, lose_overlay

# Retardo en frames
robot_move_delay = 2.5  
robot_move_counter = 0

# Ya no inicializamos maze aquí porque se genera dentro de main()

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

def distance(p1, p2):
    return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])  # distancia Manhattan

def generate_cheese_positions(maze, player_pos, count=4, min_distance_player=6, min_distance_cheese=4):
    free_cells = []
    height = len(maze)
    width = len(maze[0])
    
    for r in range(height):
        for c in range(width):
            if maze[r][c] == 0:
                free_cells.append((r, c))
                
    cheese_positions = []
    attempts = 0
    max_attempts = 1000
    
    while len(cheese_positions) < count and attempts < max_attempts:
        candidate = random.choice(free_cells)
        if distance(candidate, player_pos) < min_distance_player:
            attempts += 1
            continue
        
        too_close = False
        for ch in cheese_positions:
            if distance(candidate, ch) < min_distance_cheese:
                too_close = True
                break
        if too_close:
            attempts += 1
            continue
        
        cheese_positions.append(candidate)
        
    if len(cheese_positions) < count:
        print("Advertencia: no se pudieron generar todas las posiciones de queso con las restricciones dadas.")
    return cheese_positions

def main():
    global player_pos, player_dir, robot_pos, robot_dir

    while True:
        start_screen()

        maze = generate_map(GRID_HEIGHT, GRID_WIDTH, density=0.3, min_distance=5)
        player_pos = (1, 1)
        robot_pos = (GRID_HEIGHT // 2, GRID_WIDTH // 2)

        player_dir = (0, 1)
        robot_dir = (0, -1)

        cheese_positions = generate_cheese_positions(maze, player_pos, count=4)
        cheeses_collected = 0

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

            # Sacudida del queso (puedes hacer que uno se sacuda aleatoriamente)
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

            # Comprobar si el jugador está sobre un queso
            if player_pos in cheese_positions:
                cheese_positions.remove(player_pos)
                cheeses_collected += 1

            WIN.fill(WHITE)
            draw_grid(maze)

            # Dibujar quesos restantes
            for cheese_pos in cheese_positions:
                draw_image(cheese_pos, cheese_images, offset=cheese_offset)

            draw_image(player_pos, rat_images.get(player_dir, rat_images[(0, 1)]))
            draw_image(robot_pos, robot_images.get(robot_dir, robot_images[(0, -1)]))
            pygame.display.update()

            if cheeses_collected == 4:
                end_screen(won=True)
                break
            elif robot_pos == player_pos:
                end_screen(won=False, maze=maze)
                break

if __name__ == "__main__":
    main()
