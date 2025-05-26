# 🧀 **Lab-Rat**

Lab Rat Escape es un juego donde un ratón debe encontrar varios quesos escondidos en un mapa, mientras escapa de un robot que lo persigue. El desafío consiste en encontrar la ruta más óptima usando el algoritmo A* para moverse en un mapa generado aleatoriamente.

## 🎮 _Objetivo del Juego_

Controlas al ratón y debes recolectar todos los quesos antes de que el robot te atrape. El robot utiliza el algoritmo A* en tiempo real para seguirte, y cada mapa ofrece múltiples rutas posibles, haciendo que cada partida sea distinta.

## 📍 _Algoritmo A*_

El robot y el sistema de validación de caminos utilizan el algoritmo A*, que encuentra la ruta más corta posible entre dos puntos. **La heurística utilizada es la distancia de Manhattan**:

```python
def heuristic(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])
```

Esto permite que el robot reaccione inteligentemente y que el mapa sea evaluado correctamente antes de iniciar el juego.

## 🧠 _¿Cómo funciona la generación del mapa?_

El mapa es una cuadrícula de celdas que pueden ser libres (0) u obstáculos (1). Se genera aleatoriamente con ciertas reglas para garantizar jugabilidad:

- El ratón comienza en la esquina superior izquierda.
- El queso aparece en la esquina inferior derecha.
- El robot aparece en el centro del mapa.
- Se libera el espacio alrededor del robot para evitar bloqueos inmediatos.
- Se exige que existan al menos dos caminos distintos entre el ratón y el queso, usando el algoritmo A*:

```python
def has_two_paths(start, goal, game_map):
    path1 = a_star(start, goal, game_map)
    alt_map = copy.deepcopy(game_map)
    for pos in path1[1:-1]: 
        alt_map[pos[0]][pos[1]] = 1
    path2 = a_star(start, goal, alt_map)
    return bool(path2)
```

Esto evita que el mapa tenga un único camino forzado y promueve decisiones estratégicas.

## 🛠 _Archivos principales_

- main.py: Lógica principal del juego.
- a_star.py: Implementación del algoritmo A*.
- map_generator.py: Crea mapas jugables con múltiples rutas.
- player.py, robot.py: Control de movimiento.
- images.py: Carga de imágenes del ratón, robot y queso.
