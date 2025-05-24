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
BLUE = (0, 0, 255)      # jugador (lab rat)
RED = (255, 0, 0)       # robot perseguidor
YELLOW = (255, 255, 0)  # objetivo (queso)

# FPS del juego (velocidad de actualización)
FPS = 10

# Direcciones de movimiento: arriba, abajo, izquierda, derecha
DIRECTIONS = [(-1, 0), (1, 0), (0, -1), (0, 1)]

# Opcional: Mensajes o textos comunes
MSG_WIN = "¡Ganaste!"
MSG_LOSE = "¡Te atraparon!"