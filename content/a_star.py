# a_star.py 

from queue import PriorityQueue

def heuristic(a, b): # Heurística: distancia de Manhattan
    return abs(a[0] - b[0]) + abs(a[1] - b[1]) # |fila_actual - fila_objetivo| + |col_actual - col_objetivo|

def a_star(start, goal, maze):
    rows = len(maze)
    cols = len(maze[0]) if maze else 0

    open_set = PriorityQueue()
    open_set.put((0, start))
    came_from = {}
    g_score = {start: 0}

    while not open_set.empty():
        _, current = open_set.get()

        if current == goal:
            # Reconstruir camino
            path = []
            while current in came_from:
                path.append(current)
                current = came_from[current]
            path.reverse()
            return path

        # Vecinos (arriba, abajo, izquierda, derecha)
        for d in [(-1,0), (1,0), (0,-1), (0,1)]:
            neighbor = (current[0] + d[0], current[1] + d[1])

            if 0 <= neighbor[0] < rows and 0 <= neighbor[1] < cols:
                if maze[neighbor[0]][neighbor[1]] == 0:
                    temp_g = g_score[current] + 1
                    if neighbor not in g_score or temp_g < g_score[neighbor]:
                        g_score[neighbor] = temp_g
                        f_score = temp_g + heuristic(neighbor, goal)
                        open_set.put((f_score, neighbor))
                        came_from[neighbor] = current

    return []  # No hay camino
