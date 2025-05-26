# robot.py

from constants import GRID_HEIGHT

robot_pos = (GRID_HEIGHT - 2, 1)
robot_dir = (0, 1)

def update_robot_position(path):
    global robot_pos, robot_dir
    if path:
        next_pos = path[0]  # Siguiente punto del camino
        robot_dir = (next_pos[0] - robot_pos[0], next_pos[1] - robot_pos[1])
        # Actualiza pos
        robot_pos = next_pos
