import numpy as np

def beam_stiffness(viga):
    """
    Calcula la matriz de rigidez de una viga en un sistema 2D.

    Parámetros:
    - viga: Diccionario que representa una viga, con sus propiedades (elasticMod, area, inertia, len).

    Retorna:
    - k: Matriz de rigidez de 6x6.
    """
    e = viga['elasticMod']
    a = viga['area']
    inertia = viga['inertia']
    L = viga['len']

    # Inicializar la matriz de rigidez de 6x6
    k = np.zeros((6, 6))

    # Componentes de la matriz de rigidez
    Ao = e * a / L
    Vo = 12 * e * inertia / (L ** 3)
    V1 = 6 * e * inertia / (L ** 2)
    Mo = 4 * e * inertia / L
    M1 = 2 * e * inertia / L

    # Asignar valores a la matriz de rigidez
    k[0, 0] = Ao
    k[1, 1] = Vo
    k[1, 2] = V1
    k[2, 1] = V1
    k[2, 2] = Mo
    k[0, 3] = -Ao
    k[1, 4] = -Vo
    k[1, 5] = V1
    k[2, 4] = -V1
    k[2, 5] = M1
    k[3, 0] = -Ao
    k[4, 1] = -Vo
    k[4, 2] = -V1
    k[5, 1] = V1
    k[5, 2] = M1
    k[3, 3] = Ao
    k[4, 4] = Vo
    k[4, 5] = -V1
    k[5, 4] = -V1
    k[5, 5] = Mo

    return k

