# constants.py

CELL_SIZE = 40
GRID_WIDTH = 15
GRID_HEIGHT = 15
SCREEN_WIDTH = GRID_WIDTH * CELL_SIZE
SCREEN_HEIGHT = GRID_HEIGHT * CELL_SIZE

# Colores RGB
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

FPS = 10

# Direcciones de movimiento
DIRECTIONS = [(-1, 0), (1, 0), (0, -1), (0, 1)]

MSG_WIN = "¡Ganaste!"
MSG_LOSE = "¡Te atraparon!"