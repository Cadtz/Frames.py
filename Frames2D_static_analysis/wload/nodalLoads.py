import numpy as np

def nodal_loads(cargas_distribuidas, vigas):
    """
    Calcula las cargas nodales equivalentes a partir de las cargas distribuidas sobre vigas.

    Parámetros:
    - cargas_distribuidas: Lista o un único objeto CargaDistribuida que aplica cargas sobre las vigas.
    - vigas: Lista de objetos que representan las vigas.

    Retorna:
    - p: Matriz 3x2xn con las cargas nodales en coordenadas locales, donde n es el número de cargas distribuidas.
    - p0: Matriz 3x2xn con las cargas nodales en coordenadas locales para un caso genérico empotrado-empotrado.
    """
    if not isinstance(cargas_distribuidas, list):
        # Si no es una lista, lo convertimos en una lista de un solo elemento
        cargas_distribuidas = [cargas_distribuidas]

    nw = len(cargas_distribuidas)
    p = np.zeros((nw, 3, 2))   # Inicializar matriz de cargas nodales equivalentes
    p0 = np.zeros((nw, 3, 2))  # Inicializar matriz de cargas nodales genéricas (caso empotrado-empotrado)

    for i in range(nw):
        q, q0 = loading_cases(cargas_distribuidas[i], vigas)
        p[i, :, :] = q
        p0[i, :, :] = q0

    return p, p0

def loading_cases(carga_distribuida, vigas):
    """
    Calcula las cargas nodales equivalentes para un caso de carga específico en una viga,
    y también genera una carga genérica para el caso empotrado-empotrado.

    Parámetros:
    - carga_distribuida: Objeto que representa la carga distribuida en una viga específica.
    - vigas: Lista de objetos viga que representan las vigas.

    Retorna:
    - q: Matriz 3x2 con las cargas nodales equivalentes en coordenadas locales para el caso específico.
    - q0: Matriz 3x2 con las cargas nodales equivalentes en coordenadas locales para el caso empotrado-empotrado.
    """
    fid = carga_distribuida.beamId[0]  # ID de la viga (ajusta si se espera una lista)
    L = vigas[fid - 1]['len']  # Longitud de la viga
    caso = carga_distribuida.caso
    w = carga_distribuida.valores_carga[0]  # Valor de la carga

    # Inicializar matrices de carga
    q = np.zeros((3, 2))
    q0 = np.zeros((3, 2))

    # Calculo para el caso genérico empotrado-empotrado
    q0[1, :] = -w * L / 2  # Fuerzas en y
    q0[2, :] = -w * L**2 / 12 * np.array([1, -1])  # Momentos en z

    # Calculo para el caso específico según el tipo de conectividad
    if caso == 1:
        # Carga distribuida en toda la longitud de la viga (empotrado-empotrado o viga continua)
        q = q0
    elif caso == 2:
        # Carga distribuida en toda la longitud de la viga (voladizo)
        q[1, 0] = -w * L  # Fuerza en y en el nodo inicial
        q[2, 0] = -w * L**2 / 2  # Momento en z en el nodo inicial

    return q, q0
