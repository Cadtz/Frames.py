import numpy as np
from beam.beamDirCosines import beam_dir_cosines
from beam.beamStiffness import beam_stiffness

def stiffness(frame):
    """
    Calcula la matriz de rigidez global para un marco 2D.

    Parámetros:
    - frame: Objeto que contiene nodos (frame.n) y vigas (frame.b).

    Retorna:
    - k: Matriz de rigidez global del sistema.
    """
    nodos = frame.n
    vigas = frame.b

    nx = len(nodos)  # Número de nodos
    ndof = 3 * nx  # Grados de libertad (3 por nodo en 2D)
    k = np.zeros((ndof, ndof))  # Inicializar la matriz de rigidez global

    # Ensamblar la matriz de rigidez global
    for viga in vigas:
        # Obtener la matriz de cosenos directores (transformación de coordenadas)
        T = beam_dir_cosines(viga, nodos)

        # Obtener la matriz de rigidez local de la viga
        kl = beam_stiffness(viga)

        # Transformar la matriz de rigidez local a global
        kg = T.T @ kl @ T

        # Definir los índices de los grados de libertad
        ni = viga['ni'] - 1  # Índice del nodo inicial (ajustado para índice 0 en Python)
        nj = viga['nj'] - 1  # Índice del nodo final (ajustado para índice 0 en Python)

        idofs = list(range(ni * 3, ni * 3 + 3))  # Grados de libertad del nodo inicial
        jdofs = list(range(nj * 3, nj * 3 + 3))  # Grados de libertad del nodo final
        dofs = idofs + jdofs  # Grados de libertad combinados

        # Ensamblar la matriz global
        for i in range(6):
            for j in range(6):
                k[dofs[i], dofs[j]] += kg[i, j]

    return k