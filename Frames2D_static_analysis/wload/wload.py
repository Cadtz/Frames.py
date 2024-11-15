class CargaDistribuida:
    def __init__(self, vigas_cargadas, valores_carga, caso=1):
        """
        Constructor para definir una carga distribuida aplicada a una viga.

        Parámetros:
        - vigas_cargadas: lista de objetos viga en las que se aplicará la carga distribuida.
        - valores_carga: lista con los valores de la carga distribuida.
        - caso: tipo de carga distribuida (1: empotrado-empotrado, 2: voladizo).
        """
        if not isinstance(vigas_cargadas, list):
            raise TypeError("Se esperaba una lista de vigas.")

        if len(vigas_cargadas) != len(valores_carga):
            raise ValueError("El número de vigas no coincide con el número de valores de carga.")

        self.vigas = vigas_cargadas
        self.valores_carga = valores_carga
        self.caso = caso

        # Crear un atributo beamId que corresponda al ID de cada viga
        self.beamId = [viga['id'] for viga in vigas_cargadas]

    def __str__(self):
        """
        Representación en string de las cargas distribuidas.
        """
        resultado = f"Carga distribuida (caso {self.caso}):\n"
        for i, viga in enumerate(self.vigas):
            resultado += f"Viga {viga['tag']}: Carga = {self.valores_carga[i]}\n"
        return resultado