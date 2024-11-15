from ejemplo import x, y, node_ids
try:
    from ejemplo import grados_libertad
except ImportError:
    grados_libertad = {}  # Valor por defecto si no se define en el archivo ejemplo
try:
    from ejemplo import cargas_distribuidas
except ImportError:
    cargas_distribuidas = []  # Valor por defecto si no se define en el archivo ejemplo
try:
    from ejemplo import cargas_puntuales
except ImportError:
    cargas_puntuales = []  # Valor por defecto si no se define en el archivo ejemplo
from node.node import Nodo
from beam.beam import Viga
from wload.wload import CargaDistribuida
from pload.pload import CargaPuntual
from wload.nodalLoads import nodal_loads
from frame.frame import Marco
from frame.solveStatic import solve_static
from plot import plot_beam, plot_frame, plot_nodes, plot_pload, plot_deformed_frame_scaled
import matplotlib.pyplot as plt
# Crear nodos usando la clase Nodo
nodos = []
for i in range(len(x)):
    nodos.append(Nodo(x[i], y[i], i + 1))  # Nodo recibe x, y, y un ID
# Aplicar grados de libertad definidos en el archivo ejemplo
if grados_libertad:
    for i, grados in grados_libertad.items():
        nodos[i - 1].set_grados_libertad(grados)  # Los IDs de los nodos empiezan desde 1
# Crear vigas usando la clase Viga
try:
    from ejemplo import area, elastic_mod, inertia
except ImportError:
    area, elastic_mod, inertia = None, None, None  # Valores por defecto si no se definen en ejemplo

if area is None and elastic_mod is None and inertia is None:
    vigas_obj = Viga(nodos, node_ids)
elif area is not None and elastic_mod is None and inertia is None:
    vigas_obj = Viga(nodos, node_ids, area)
elif area is not None and elastic_mod is not None and inertia is None:
    vigas_obj = Viga(nodos, node_ids, area, elastic_mod)
else:
    vigas_obj = Viga(nodos, node_ids, area, elastic_mod, inertia)
#Acceder a las vigas generadas
vigas = vigas_obj.vigas
# Generar la carga distribuida usando la clase CargaDistribuida para cada tramo si existen cargas distribuidas
cargas_distribuidas_obj = []
if cargas_distribuidas:
    for beam_id, (magnitud, caso) in cargas_distribuidas:
        viga_obj = next((v for v in vigas if v['id'] == beam_id), None)
        if viga_obj:
            cargas_distribuidas_obj.append(CargaDistribuida([viga_obj], [magnitud], caso))
        # Generar las cargas nodales a partir de la carga distribuida
        q_nodal = nodal_loads(cargas_distribuidas_obj, vigas)
# Generar la carga puntual usando la clase CargaPuntual si existen cargas puntuales
cargas_puntuales_obj = []
if cargas_puntuales:
    cargas_puntuales_obj = [
        CargaPuntual(nodos, [carga[0]], [carga[1]]) for carga in cargas_puntuales
    ]
# Crear el marco estructural usando la clase Marco
if not cargas_puntuales_obj and not cargas_distribuidas_obj:
    marco = Marco(nodos, vigas)
elif not cargas_puntuales_obj:
    marco = Marco(nodos, vigas, cargas_distribuidas_obj)
elif not cargas_distribuidas_obj:
    marco = Marco(nodos, vigas, cargas_puntuales_obj)
else:
    marco = Marco(nodos, vigas, cargas_puntuales_obj, cargas_distribuidas_obj)
# Resolver el problema estático
marco_resuelto = solve_static(marco, print_output=True)
# Imprimir los resultados
print("\nResultados finales del análisis estructural:")
print(marco_resuelto)

# Crear nodos deformados usando los datos en marco_resuelto
nodos_deformados = []
for nodo_info in marco_resuelto.nodos_deformados:
    # Crear un objeto Nodo para cada nodo deformado
    nodos_deformados.append(Nodo(nodo_info['x'], nodo_info['y'], nodo_info['id']))

try:
    from ejemplo import graficos_a_mostrar
except ImportError:
    graficos_a_mostrar = []  # Si no está definido, se establece como lista vacía


def mostrar_grafico(nombre, func, *args):
    if nombre in graficos_a_mostrar:
        func(*args)
        plt.grid(True)
        plt.show(block=True)
# Llamadas condicionales para cada gráfico
mostrar_grafico("plot_frame", plot_frame, nodos, vigas)
mostrar_grafico("plot_nodes", plot_nodes, nodos)
mostrar_grafico("plot_beam", plot_beam, nodos, vigas)
mostrar_grafico("plot_deformed_frame", plot_deformed_frame_scaled, nodos, vigas, nodos_deformados)
mostrar_grafico("plot_pload", plot_pload, nodos, vigas, cargas_puntuales_obj)