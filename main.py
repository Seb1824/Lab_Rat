import pygame
from constants import *
from maze import generate_maze
from player import Player
from robot import Robot

pygame.init()
WIN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Lab Rat Escape")

def draw_grid(maze):
    for row in range(GRID_HEIGHT):
        for col in range(GRID_WIDTH):
            x = col * CELL_SIZE
            y = row * CELL_SIZE
            color = WHITE if maze[row][col] == 0 else BLACK
            pygame.draw.rect(WIN, color, (x, y, CELL_SIZE, CELL_SIZE))
            pygame.draw.rect(WIN, GRAY, (x, y, CELL_SIZE, CELL_SIZE), 1)

def draw_entity(pos, color):
    x = pos[1] * CELL_SIZE
    y = pos[0] * CELL_SIZE
    pygame.draw.rect(WIN, color, (x, y, CELL_SIZE, CELL_SIZE))

def main():
    clock = pygame.time.Clock()
    maze = generate_maze()
    player = Player((1, 1))
    robot = Robot((GRID_HEIGHT - 2, 1))
    goal = (GRID_HEIGHT - 2, GRID_WIDTH - 2)
    running = True

    while running:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        keys = pygame.key.get_pressed()
        player.handle_input(keys, maze)
        robot.update(maze, player.pos)

        WIN.fill(WHITE)
        draw_grid(maze)
        draw_entity(player.pos, BLUE)
        draw_entity(goal, YELLOW)
        draw_entity(robot.pos, RED)
        pygame.display.update()

        if player.pos == goal:
            print(MSG_WIN)
            running = False
        elif player.pos == robot.pos:
            print(MSG_LOSE)
            running = False

    pygame.quit()

if __name__ == "__main__":
    main()
