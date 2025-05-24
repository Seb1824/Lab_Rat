import pygame
from queue import PriorityQueue

WIDTH = 600
ROWS = 20
CELL_SIZE = WIDTH // ROWS
FPS = 10

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

pygame.init()
WIN = pygame.display.set_mode((WIDTH, WIDTH))
pygame.display.set_caption("Lab Rat Escape")

# 0 = camino, 1 = muro
maze = [
    [0,1,0,0,0,0,0,1,0,0,0,1,0,1,0,1,0,0,0,0],
    [0,1,0,1,1,1,0,1,0,1,0,1,0,1,0,1,1,1,1,0],
    [0,0,0,0,0,1,0,0,0,1,0,0,0,0,0,0,0,0,1,0],
    [1,1,1,1,0,1,1,1,0,1,1,1,1,1,1,1,0,1,1,0],
    [0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,1,0,0,0,0],
    [0,1,1,1,1,1,0,1,1,1,1,1,1,1,0,1,1,1,1,0],
    [0,0,0,0,0,1,0,0,0,0,0,1,0,0,0,0,0,0,0,0],
    [1,1,1,1,0,1,1,1,1,1,0,1,1,1,1,1,1,1,1,0],
    [0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,1,0],
    [0,1,1,1,1,1,1,1,0,1,1,1,1,1,1,1,1,0,1,0],
    [0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,1,0,1,0],
    [1,1,1,1,1,1,0,1,1,1,1,1,1,1,1,0,1,0,1,0],
    [0,0,0,0,0,1,0,0,0,0,0,0,0,0,1,0,1,0,0,0],
    [0,1,1,1,0,1,1,1,1,1,1,1,1,0,1,1,1,1,1,1],
    [0,0,0,1,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0],
    [1,1,0,1,1,1,1,1,1,1,1,0,1,1,1,1,1,1,1,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0],
    [0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,1,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0]
]

start_pos = (0, 0)
goal_pos = (19, 19)
robot_pos = (19, 0)

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

def heuristic(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def a_star(start, goal):
    open_set = PriorityQueue()
    open_set.put((0, start))
    came_from = {}
    g_score = {start: 0}

    while not open_set.empty():
        _, current = open_set.get()

        if current == goal:
            path = []
            while current in came_from:
                path.append(current)
                current = came_from[current]
            path.reverse()
            return path

        for d in [(-1,0), (1,0), (0,-1), (0,1)]:
            neighbor = (current[0] + d[0], current[1] + d[1])

            if 0 <= neighbor[0] < ROWS and 0 <= neighbor[1] < ROWS and maze[neighbor[0]][neighbor[1]] == 0:
                temp_g = g_score[current] + 1
                if neighbor not in g_score or temp_g < g_score[neighbor]:
                    g_score[neighbor] = temp_g
                    f_score = temp_g + heuristic(neighbor, goal)
                    open_set.put((f_score, neighbor))
                    came_from[neighbor] = current
    return []

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
        path = a_star(robot_pos, start_pos)
        if path:
            robot_pos = path[0]  # mueve 1 paso

        WIN.fill(WHITE)
        draw_grid()
        draw_entity(start_pos, BLUE)     # jugador
        draw_entity(goal_pos, YELLOW)    # queso
        draw_entity(robot_pos, RED)      # robot
        pygame.display.update()

        if start_pos == goal_pos:
            print("¡Ganaste!")
            running = False
        elif robot_pos == start_pos:
            print("¡Te atraparon!")
            running = False

    pygame.quit()

if __name__ == "__main__":
    main()
