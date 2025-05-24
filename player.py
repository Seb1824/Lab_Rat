# player.py

import pygame

class Player:
    def __init__(self, pos):
        self.pos = pos

    def handle_input(self, keys, maze):
        dx, dy = 0, 0
        if keys[pygame.K_UP]: dx = -1
        if keys[pygame.K_DOWN]: dx = 1
        if keys[pygame.K_LEFT]: dy = -1
        if keys[pygame.K_RIGHT]: dy = 1

        new_x = self.pos[0] + dx
        new_y = self.pos[1] + dy

        if 0 <= new_x < len(maze) and 0 <= new_y < len(maze[0]):
            if maze[new_x][new_y] == 0:
                self.pos = (new_x, new_y)
