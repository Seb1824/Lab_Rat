# player.py

import pygame

player_pos = (1, 1)
player_dir = (0, 1)


def update_player_position(keys, current_pos, current_dir, maze):
    dx, dy = 0, 0
    if keys[pygame.K_UP] or keys[pygame.K_w]:
        dx, dy = -1, 0
    elif keys[pygame.K_DOWN] or keys[pygame.K_s]:
        dx, dy = 1, 0
    elif keys[pygame.K_LEFT] or keys[pygame.K_a]:
        dx, dy = 0, -1
    elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
        dx, dy = 0, 1

    new_pos = (current_pos[0] + dx, current_pos[1] + dy)
    if 0 <= new_pos[0] < len(maze) and 0 <= new_pos[1] < len(maze[0]) and maze[new_pos[0]][new_pos[1]] == 0:
        return new_pos, (dx, dy)
    return current_pos, current_dir

