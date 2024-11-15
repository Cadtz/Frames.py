import numpy as np

class Viga:
    def __init__(self, nodos, node_ids, *args):
        """
        Constructor para definir una viga en un espacio Euclidiano 2D.

        Parámetros:
        - nodos: lista de objetos Nodo generados a partir de las coordenadas x e y.
        - node_ids: matriz Nx2 con los pares de nodos [nodo inicial, nodo final] que definen las vigas.
        - *args: parámetros opcionales para definir el área, módulo de elasticidad, e inercia.
        """
        self.vigas = []  # Lista para almacenar todas las vigas

        area = None
        elasticMod = None
        inertia = None

        # Procesar los argumentos adicionales
        if len(args) > 0:
            area = args[0]
        if len(args) > 1:
            elasticMod = args[1]
        if len(args) > 2:
            inertia = args[2]

        # Crear vigas para cada par de nodos en node_ids
        for i, (ni, nj) in enumerate(node_ids):
            viga = {
                'id': i + 1,
                'ni': ni,
                'nj': nj,
                'tag': f"{ni}-{nj}",  # Etiqueta de la viga
                'area': 1 if area is None else (area[i] if isinstance(area, list) else area),
                'elasticMod': 1 if elasticMod is None else (elasticMod[i] if isinstance(elasticMod, list) else elasticMod),
                'inertia': 1 if inertia is None else (inertia[i] if isinstance(inertia, list) else inertia)
            }

            # Calcular propiedades geométricas (longitud, vector unitario, punto medio)
            viga['len'], viga['uv'], viga['mp'] = self.calcular_geometria_viga(viga, nodos)
            viga['axialLoad'] = 0  # Inicialización
            viga['shearLoad'] = [0, 0]  # Inicialización
            viga['bendingMoment'] = [0, 0]  # Inicialización
            self.vigas.append(viga)

    def calcular_geometria_viga(self, viga, nodos):
        """
        Calcula las propiedades geométricas de la viga: longitud, vector unitario y punto medio.

        Parámetros:
        - viga: diccionario con la información de la viga.
        - nodos: lista de diccionarios que representan las coordenadas de los nodos.

        Retorna:
        - len: longitud de la viga.
        - uv: vector unitario de la viga.
        - mp: coordenadas del punto medio de la viga.
        """
        nodo_inicial = nodos[viga['ni'] - 1]
        nodo_final = nodos[viga['nj'] - 1]

        dx = nodo_final.x - nodo_inicial.x
        dy = nodo_final.y - nodo_inicial.y

        # Longitud de la viga
        longitud = np.sqrt(dx**2 + dy**2)

        # Vector unitario
        vector_unitario = [dx / longitud, dy / longitud]

        # Punto medio
        punto_medio = [(nodo_inicial.x + nodo_final.x) / 2, (nodo_inicial.y + nodo_final.y) / 2]

        return longitud, vector_unitario, punto_medio

    def __str__(self):
        """
        Representación en string de todas las vigas.
        """
        resultado = "Lista de vigas:\n"
        for viga in self.vigas:
            resultado += f"Viga {viga['tag']}: Longitud = {viga['len']:.2f}, Area = {viga['area']}, E = {viga['elasticMod']}, Inercia = {viga['inertia']}\n"
        return resultado