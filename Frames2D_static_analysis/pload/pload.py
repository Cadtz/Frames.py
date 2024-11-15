class CargaPuntual:
    def __init__(self, nodos, nodos_con_carga, valores_carga):
        """
        Constructor para definir cargas puntuales en nodos específicos.

        Parámetros:
        - nodos: Lista de objetos Nodo.
        - nodos_con_carga: Lista de IDs de los nodos donde se aplicarán las cargas.
        - valores_carga: Lista de listas [px, py, mz] que define los valores de carga aplicados a los nodos correspondientes.
        """
        if len(nodos_con_carga) != len(valores_carga):
            raise ValueError(f"El número de nodos con carga ({len(nodos_con_carga)}) debe ser igual al número de valores de carga ({len(valores_carga)}).")

        self.cargas = []  # Lista para almacenar las cargas

        # Asignar las cargas a los nodos específicos
        for i in range(len(nodos_con_carga)):
            nodo_id = nodos_con_carga[i]

            # Verificar si el nodo existe en la lista de nodos
            nodo_existente = next((nodo for nodo in nodos if nodo.id == nodo_id), None)
            if nodo_existente is None:
                raise ValueError(f"Nodo con ID {nodo_id} no existe en el sistema.")

            # Verificar el formato de la carga y añadir un valor por defecto para el momento si es necesario
            carga_valores = valores_carga[i]
            if len(carga_valores) == 2:
                carga_valores.append(0)  # Añadir mz = 0 si solo se proporcionan px y py

            # Asignar carga al nodo
            carga = {
                'nodo': nodo_id,  # ID del nodo
                'valor': carga_valores  # Valores de carga [px, py, mz]
            }
            self.cargas.append(carga)

    def __str__(self):
        """
        Representación en string de todas las cargas puntuales.
        """
        resultado = "Cargas puntuales aplicadas:\n"
        for carga in self.cargas:
            resultado += f"Nodo {carga['nodo']}: Carga = {carga['valor']}\n"
        return resultado
