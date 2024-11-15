class Nodo:
    def __init__(self, x, y, nodo_id):
        """
        Constructor para definir uno o varios nodos en un espacio euclidiano 2D.

        Parámetros:
        - x: coordenada X del nodo (puede ser un escalar o una lista de coordenadas).
        - y: coordenada Y del nodo (debe coincidir en longitud con x).
        - nodo_id: ID único del nodo o lista de IDs; si no se proporciona, se asignan automáticamente.
        """

        self.id = nodo_id 
        self.x = x         # Coordenada x
        self.y = y         # Coordenada y
        self.rdofs = [0, 0, 0]  # Grados de libertad restringidos [x, y, z]
        self.disp = [0, 0, 0]   # Desplazamientos [ux, uy, rz]
        self.nload = [0, 0, 0]  # Cargas nodales [px, py, mz]
        self.react = [0, 0, 0]  # Reacciones [Rx, Ry, Mz]

    def set_grados_libertad(self, grados_libertad):
        """
        Establece los grados de libertad restringidos de un nodo.

        Parámetros:
        - grados_libertad: lista [x, y, z] que define los grados de libertad restringidos.
        """
        self.rdofs = grados_libertad

    def set_carga(self, carga):
        """
        Establece la carga aplicada en un nodo.

        Parámetros:
        - carga: lista [px, py, mz] que representa las fuerzas y momento aplicados en el nodo.
        """
        self.nload = carga

    def set_desplazamiento(self, desplazamiento):
        """
        Establece el desplazamiento en un nodo.

        Parámetros:
        - desplazamiento: lista [ux, uy, rz] que representa los desplazamientos en el nodo.
        """
        self.disp = desplazamiento

    def set_reaccion(self, reaccion):
        """
        Establece las reacciones en un nodo.

        Parámetros:
        - reaccion: lista [Rx, Ry, Mz] que representa las reacciones en el nodo.
        """
        self.react = reaccion

    def __str__(self):
        """
        Representación en string del nodo.
        """
        if self.nodes:
            return "\n".join([str(node) for node in self.nodes])
        return (f"Nodo {self.id}: ({self.x}, {self.y})\n"
                f"  Grados de libertad restringidos: {self.rdofs}\n"
                f"  Desplazamientos: {self.disp}\n"
                f"  Cargas nodales: {self.nload}\n"
                f"  Reacciones: {self.react}\n")