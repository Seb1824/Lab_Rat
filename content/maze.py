import random
from constants import GRID_HEIGHT, GRID_WIDTH
from a_star import a_star
import copy

def has_two_paths(start, goal, game_map):
    path1 = a_star(start, goal, game_map)
    if not path1:
        return False

    # Clonar mapa y bloquear el primer camino (excepto inicio y fin)
    alt_map = copy.deepcopy(game_map)
    for pos in path1[1:-1]: 
        alt_map[pos[0]][pos[1]] = 1 # Bloqueo (pared)

    path2 = a_star(start, goal, alt_map)
    return bool(path2)


def generate_map(height=GRID_HEIGHT, width=GRID_WIDTH, density=0.3, min_distance=5):
    while True:
        game_map = []
        for i in range(height):
            row = []
            for j in range(width):
                if random.random() < density:
                    row.append(1)  # Obstáculo
                else:
                    row.append(0)
            game_map.append(row)

        player = (1, 1)
        goal = (height - 2, width - 2)
        robot = (height // 2, width // 2)

        # Liberar zonas clave
        game_map[player[0]][player[1]] = 0
        game_map[goal[0]][goal[1]] = 0
        game_map[robot[0]][robot[1]] = 0

        # Liberar alrededores del robot
        for dx, dy in [(-1,0), (1,0), (0,-1), (0,1)]:
            x, y = robot[0] + dx, robot[1] + dy
            if 0 <= x < height and 0 <= y < width:
                game_map[x][y] = 0

        # Verifica caminos
        path_to_goal = a_star(player, goal, game_map)
        path_robot_to_player = a_star(robot, player, game_map)

        # Distancia mínima entre bot y rat
        dx = abs(player[0] - robot[0])
        dy = abs(player[1] - robot[1])
        dist = dx + dy

        if path_to_goal and path_robot_to_player and dist >= min_distance:
            if has_two_paths(player, goal, game_map):
                return game_map