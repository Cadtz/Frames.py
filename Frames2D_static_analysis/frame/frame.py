from pload.pload import CargaPuntual
from wload.wload import CargaDistribuida

class Marco:
    def __init__(self, nodos, vigas, *args):
        """
        Constructor para definir un marco estructural.

        Parámetros:
        - nodos: Lista de objetos que representan los nodos del marco.
        - vigas: Lista de objetos que representan las vigas del marco.
        - *args: Parámetros opcionales para incorporar cargas puntuales y distribuidas.

        """
        self.n = nodos  # Nodos del marco
        self.b = vigas  # Vigas del marco

        # Inicializar cargas
        self.p = []  # Cargas puntuales
        self.w = []  # Cargas distribuidas

        # Incorporar cargas, si se proporcionan
        for arg in args:
            if isinstance(arg, list):
                if len(arg) > 0 and isinstance(arg[0], CargaPuntual):
                    self.p = arg  # Cargas puntuales
                elif len(arg) > 0 and isinstance(arg[0], CargaDistribuida):
                    self.w = arg  # Cargas distribuidas
                else:
                    raise ValueError("Tipo de carga desconocido")

    def __str__(self):
        """
        Representación en string del marco estructural.
        """
        resultado = "Marco estructural:\n"
        resultado += f"Nodos: {len(self.n)}\n"
        resultado += f"Vigas: {len(self.b)}\n"
        resultado += f"Nodos con cargas Puntuales: {len(self.p)}\n"
        resultado += f"Cargas distribuidas: {len(self.w)}\n"
        return resultado