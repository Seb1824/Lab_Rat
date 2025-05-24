import pygame
from a_star import a_star
from constants import WIDTH, ROWS, CELL_SIZE, WHITE, BLACK, GRAY, BLUE, RED, YELLOW, FPS, DIRECTIONS, MSG_WIN, MSG_LOSE
import random


pygame.init()
WIN = pygame.display.set_mode((WIDTH, WIDTH))
pygame.display.set_caption("Lab Rat Escape")

def generate_maze(rows):
    maze = [[1 for _ in range(rows)] for _ in range(rows)]

    def carve_passages_from(cx, cy):
        directions = [(0,1),(1,0),(0,-1),(-1,0)]
        random.shuffle(directions)
        for dx, dy in directions:
            nx, ny = cx + dx*2, cy + dy*2
            if 0 <= nx < rows and 0 <= ny < rows and maze[nx][ny] == 1:
                maze[cx + dx][cy + dy] = 0  # romper muro intermedio
                maze[nx][ny] = 0            # marcar celda destino
                carve_passages_from(nx, ny)

    maze[1][1] = 0
    carve_passages_from(1,1)
    return maze

ROWS = 21  # debe ser impar para el algoritmo
maze = generate_maze(ROWS)
start_pos = (1, 1)
goal_pos = (ROWS - 2, ROWS - 2)
robot_pos = (ROWS - 2, 1)

def draw_grid():
    for row in range(ROWS):
        for col in range(ROWS):
            x = col * CELL_SIZE
            y = row * CELL_SIZE
            color = WHITE
            if maze[row][col] == 1:
                color = BLACK
            pygame.draw.rect(WIN, color, (x, y, CELL_SIZE, CELL_SIZE))
            pygame.draw.rect(WIN, GRAY, (x, y, CELL_SIZE, CELL_SIZE), 1)

def draw_entity(pos, color):
    x = pos[1] * CELL_SIZE
    y = pos[0] * CELL_SIZE
    pygame.draw.rect(WIN, color, (x, y, CELL_SIZE, CELL_SIZE))



def main():
    global start_pos, robot_pos
    clock = pygame.time.Clock()
    running = True

    while running:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Movimiento del jugador
        keys = pygame.key.get_pressed()
        dx, dy = 0, 0
        if keys[pygame.K_UP]: dx = -1
        if keys[pygame.K_DOWN]: dx = 1
        if keys[pygame.K_LEFT]: dy = -1
        if keys[pygame.K_RIGHT]: dy = 1
        new_pos = (start_pos[0] + dx, start_pos[1] + dy)
        if 0 <= new_pos[0] < ROWS and 0 <= new_pos[1] < ROWS and maze[new_pos[0]][new_pos[1]] == 0:
            start_pos = new_pos

        # A* para mover al robot
        path = a_star(robot_pos, start_pos, maze)
        if path:
            robot_pos = path[0]  # mueve 1 paso

        WIN.fill(WHITE)
        draw_grid()
        draw_entity(start_pos, BLUE)     # jugador
        draw_entity(goal_pos, YELLOW)    # queso
        draw_entity(robot_pos, RED)      # robot
        pygame.display.update()

        if start_pos == goal_pos:
            print(MSG_WIN)
            running = False
        elif robot_pos == start_pos:
            print(MSG_LOSE)
            running = False

    pygame.quit()

if __name__ == "__main__":
    main()
