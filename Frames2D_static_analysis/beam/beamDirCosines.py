import numpy as np

def beam_dir_cosines(viga, nodos):
    """
    Calcula la matriz de cosenos directores para una viga en un sistema 2D.

    Parámetros:
    - viga: Diccionario que representa una viga, con sus propiedades (ni, nj, len).
    - nodos: Lista de diccionarios que representan los nodos, cada uno con coordenadas x e y.

    Retorna:
    - T: Matriz de transformación de coordenadas de 6x6.
    """
    # Obtener los nodos inicial y final de la viga
    ni = viga['ni'] - 1  # Índice del nodo inicial
    nj = viga['nj'] - 1  # Índice del nodo final

    # Coordenadas de los nodos
    xi = nodos[ni].x
    xj = nodos[nj].x
    yi = nodos[ni].y
    yj = nodos[nj].y

    # Diferencias en coordenadas
    dx = xj - xi
    dy = yj - yi

    # Longitud de la viga
    len_viga = viga['len']

    # Cálculo del coseno y seno del ángulo (theta)
    cx = dx / len_viga  # cos(theta)
    sx = dy / len_viga  # sin(theta)

    # Definir los vectores unitarios Vx y Vz
    Vx = [cx, sx, 0]
    Vz = [0, 0, 1]

    # Si la diferencia en x es negativa, invertir el signo de Vz
    if dx < 0:
        Vz = [0, 0, -1]

    # Calcular el vector Vy como el producto cruz de Vz y Vx
    Vy = np.cross(Vz, Vx)

    # Construir la matriz L de 3x3 con los vectores unitarios
    L = np.array([Vx, Vy, Vz])

    # Construir la matriz de transformación de coordenadas T de 6x6
    T = np.zeros((6, 6))
    T[0:3, 0:3] = L
    T[3:6, 3:6] = L

    return T