# robot.py

from a_star import a_star

class Robot:
    def __init__(self, pos):
        self.pos = pos

    def update(self, maze, target_pos):
        path = a_star(self.pos, target_pos, maze)
        if path:
            self.pos = path[0]
