""" # Ejemplo Celigueta
# Definir las coordenadas de los nodos separados por ","
x = [0, 0, 4, 6] #Distancias en M
y = [0, 4, 4, 0] #Distancias en M

# Definir las conectividades de las vigas (nodos que une cada viga)
node_ids = [[1, 2], [2, 3], [3, 4]]

# Definir los grados de libertad restringidos para los nodos
# Formato: {nodo_id: [dx, dy, rotacion]}
# 1 = restringido, 0 = libre
grados_libertad = {
    1: [1, 1, 1],  # Nodo 1 restringido completamente
    4: [1, 1, 1]   # Nodo 2 Empotrado tambien
}

# Definir la carga puntual
# Formato: [(nodo_id, [fuerza_x, fuerza_y, momento])]
cargas_puntuales = [(2, [5, 0, 0])]

# Definir la carga distribuida
cargas_distribuidas = [
    (2, (-3, 1)),  # Carga distribuida para la viga 2 (magnitud, caso)
]
# Definir propiedades de las vigas
E=200e6
area = [0.01, 0.008, 0.01]
elastic_mod = [E]*3 # Módulo de elasticidad (Kn/mm2) de cada viga
inertia = [0.0001, 0.00015, 0.0001]  # Momento de inercia (mm^4) de cada viga

#Funcion para definir que elementos mostrar: elementos_a_mostrar
#Opciones: "matriz de rigidez global", "Matriz de rigidez local de la viga {id}"
elementos_a_mostrar = ["Matriz de rigidez global",
                       "Matriz de rigidez local de la viga 1",
                       "Matriz transformada a coordenadas globales de la viga 1",
                       "Fuerzas en coordenadas globales de la viga 1"]

#Funcion para mostrar graficos graficos_a_mostrar.
#Opciones: "plot_frame", "plot_nodes", "plot_beam", "plot_pload"

graficos_a_mostrar = ["plot_frame","plot_deformed_frame", "plot_nodes", "plot_pload"]

# Ejecutar el análisis estructural importando y llamando a main
if __name__ == "__main__":
    import Main   """
    
""" #Ejemplo Voladizo Aereo Carga Puntual
#Ejemplo portico L
x = [0, 0, 0, 0, 0, 0.25, 0.5, 0.75, 1]
y = [0, 0.25, 0.5, 0.75, 1, 1, 1, 1, 1]

grados_libertad = {
    1: [1, 1, 1],  # Nodo 1 restringido completamente
}

node_ids = [[i, i+1] for i in range (1,9)]

cargas_puntuales = [(9, [0, -1, 0])]

graficos_a_mostrar = ["plot_frame","plot_pload"]

if __name__ == "__main__":
    import Main  """

""" # Ejemplo 1 Python emp emp y voladizo

# Definir las coordenadas de los nodos
x = [0, 2.5, 5]
y = [0, 0, 0]

# Definir las conectividades de las vigas (nodos que une cada viga)
node_ids = [[1, 2], [2, 3]]

# Definir los grados de libertad restringidos para los nodos
# Formato: {nodo_id: [dx, dy, rotacion]}
# 1 = restringido, 0 = libre
grados_libertad = {
    1: [1, 1, 1],  # Nodo 1 restringido completamente
}

# Definir la carga distribuida
cargas_distribuidas = [
    (1, (-1, 1)), # Carga distribuida para la viga 1 (magnitud, caso)
    (2, (-1, 2))  # Carga distribuida para la viga 2 (magnitud, caso)
]
graficos_a_mostrar = ["plot_beam"]

# Ejecutar el análisis estructural importando y llamando a main
if __name__ == "__main__":
    import Main """

""" #Ejemplo Voladizo Puntual MATLAB
x = [0, 0.83333333, 1.66666667, 2.5, 3.33333333, 4.16666667, 5]
y = [0]*7
node_ids = [
    [1, 2],
    [2, 3],
    [3, 4],
    [4, 5],
    [5, 6],
    [6, 7]
]
grados_libertad = {
    1: [1, 1, 1]  # Nodo 1 restringido completamente
}
cargas_puntuales = [(7, [0, -1, 0])]
graficos_a_mostrar = ["plot_frame","plot_pload"]
if __name__ == "__main__":
    import Main """

""" #Ejemplo 1 rotado
import numpy as np

cx = np.cos(30*np.pi/180); sx = np.sin(30*np.pi/180)
x = [1, 3.1651, 5.3331]
y = [0, 1.25, 2.5]
grados_libertad = {
    1: [1, 1, 1]  # Nodo 1 restringido completamente
}
node_ids = [[1,2],[2,3]]
cargas_distribuidas = [
    (1, (-1, 1)),
    (2, (-1, 2))# Carga distribuida para la viga 2 (magnitud, caso)
]
graficos_a_mostrar = ["plot_frame","plot_deformed_frame"]
if __name__ == "__main__":
    import Main """