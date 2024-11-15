import pandas as pd
import numpy as np
from frame.stiffness import stiffness
from wload.nodalLoads import nodal_loads
from beam.beamDirCosines import beam_dir_cosines
from beam.beamStiffness import beam_stiffness

try:
    from ejemplo import elementos_a_mostrar
except ImportError:
    elementos_a_mostrar = []

def mostrar_elemento(nombre, valor, formato_tabla=False):
    """Función para mostrar elementos específicos si están en la lista de elementos_a_mostrar."""
    if nombre in elementos_a_mostrar:
        print(f"\n{nombre}:")
        if formato_tabla:
            print(pd.DataFrame(valor))
        else:
            print(valor)
        print("\n")

def solve_static(frame, print_output=False):
    """
    Resuelve el problema estático para el marco, calculando los desplazamientos, reacciones
    y cargas internas de las vigas.

    Parámetros:
    - frame: Diccionario que contiene los nodos (frame['n']), las vigas (frame['b']),
             y las cargas (frame['p'] y frame['w']).
    - print_output: Booleano para decidir si se imprimen los resultados (desactivado por defecto).

    Retorna:
    - frame: El mismo marco con los resultados (desplazamientos, reacciones y cargas internas actualizados).
    """
    # Cargar nodos y grados de libertad
    nodos = frame.n
    nx = len(nodos)
    rdofs = np.array([nodo.rdofs for nodo in nodos], dtype=bool).flatten()  # Grados de libertad restringidos
    adofs = ~rdofs  # Grados de libertad activos (no restringidos)

    # Ensamblar los vectores de cargas nodales pn, p0, y el vector de carga total p
    pn = np.zeros(len(rdofs))  # Cargas nodales equivalentes específicas
    p0 = np.zeros(len(rdofs))  # Cargas nodales equivalentes genéricas

    # ENSAMBLA LAS CARGAS PUNTUALES DEFINIDAS POR EL USUARIO
    ploads = frame.p
    for carga_puntual in ploads:  # 'carga_puntual' es una instancia de CargaPuntual
        for pload in carga_puntual.cargas:  # 'pload' es un diccionario con las claves 'nodo' y 'valor'
            ni = pload['nodo'] - 1  # Índice del nodo (ajustado a 0 para Python)
            idofs = range(ni * 3, ni * 3 + 3)  # Grados de libertad del nodo en p
            if isinstance(pload['valor'], (list, np.ndarray)) and len(pload['valor']) == 3:
                pn[idofs] += np.array(pload['valor'])
            else:
                raise ValueError(f"La carga puntual en el nodo {ni+1} debe tener 3 componentes.")
    
    wloads = frame.w
    q = np.zeros((len(frame.b), 3, 2))  # Matriz de cargas nodales para cada viga
    q0 = np.zeros((len(frame.b), 3, 2))  # Matriz de cargas nodales genéricas para cada viga
    if wloads:
        for wload in wloads:
            # Calcula qi y q0i, las cargas nodales equivalentes específicas y genéricas
            qi, q0i = nodal_loads(wload, frame.b)
            beam_indices = np.array(wload.beamId) - 1  # Convertimos a índice 0-based para Python
        
                # Asignar qi y q0i a cada índice de viga específico
            for i, beam_index in enumerate(beam_indices):
                #print(f"Asignando carga a beam_index {beam_index} (debe ser único para cada viga)") # Print de verificacion.
            
                # Asignar solo si la viga tiene una carga distribuida
                if beam_index < len(q) and np.all(q[beam_index, :, :] == 0) and np.all(q0[beam_index, :, :] == 0):
                    q[beam_index, :, :] = qi[i]
                    q0[beam_index, :, :] = q0i[i]
                else:
                    print(f"Advertencia: `beam_index {beam_index}` ya tiene valores asignados o no es válido.")

            # Imprimir para verificar el estado de `q` y `q0` después de cada asignación
            #print(f"Después de asignar, q para beam_index {beam_index}:") # Print de verificacion.
            #print(q) # Print de verificacion.
            #print(f"Después de asignar, q0 para beam_index {beam_index}:") # Print de verificacion.
            #print(q0) # Print de verificacion.
            for beam_id in wload.beamId:
                beam = frame.b[beam_id - 1]
                T = beam_dir_cosines(beam, nodos)
                ni = beam['ni'] - 1
                nj = beam['nj'] - 1
                idofs = list(range(ni * 3, ni * 3 + 3))
                jdofs = list(range(nj * 3, nj * 3 + 3))
                dofs = idofs + jdofs
                T_t = np.transpose(T)
        
                # Contribuciones de cargas nodales equivalentes específicas (pn) y genéricas (p0)
                qqq_i = qi.flatten(order='F')
                pn[np.ix_(dofs)] -= T_t @ qqq_i  # Cambiar a resta para alinearlo con MATLAB

                qqq_0 = q0i.flatten(order='F')
                p0[np.ix_(dofs)] -= T_t @ qqq_0  # Cambiar a resta para alinearlo con MATLAB

   # Inicializar nuevamente el vector `p` y otros vectores después del cálculo de desplazamientos
    p = np.zeros(len(rdofs))  # Vector de carga total para acumular fuerzas internas
    r = np.zeros(len(rdofs))
    d = np.zeros(len(rdofs))
    # Inicializar Pi para almacenar las cargas internas de cada viga
    Pi = np.zeros((3, 2, len(frame.b)))  # Dimensiones: (fuerzas internas, 2 puntos, número de vigas)
    # Resolver los desplazamientos {d} si hay cargas
    if np.any(np.abs(pn) > 0):  # Cambiado a pn para que sea equivalente a MATLAB
        k_global = stiffness(frame)
        mostrar_elemento("Matriz de rigidez global", k_global, formato_tabla=True)
        active_dof_stiffness = k_global[np.ix_(adofs, adofs)]
        active_dof_forces = pn[adofs]  # Usamos pn como en MATLAB
        d[adofs] = np.linalg.solve(active_dof_stiffness, active_dof_forces)
        r[rdofs] = k_global[np.ix_(rdofs, adofs)] @ d[adofs] - pn[rdofs]

        # Calcular las cargas internas en las vigas
        for i, viga in enumerate(frame.b):
            ni = viga['ni'] - 1
            nj = viga['nj'] - 1
            idofs = range(ni * 3, ni * 3 + 3)
            jdofs = range(nj * 3, nj * 3 + 3)
            dofs = list(idofs) + list(jdofs)
            T = beam_dir_cosines(viga, nodos)
            # Mostrar la matriz de transformación a coordenadas globales
            mostrar_elemento(f"Matriz transformada a coordenadas globales de la viga {viga['id']}", np.array2string(T, precision=2, suppress_small=True))
            di = T @ d[np.ix_(dofs)]
            kl = beam_stiffness(viga)
            mostrar_elemento(f"Matriz de rigidez local de la viga {viga['id']}", np.array2string(kl, precision=2, suppress_small=True))

            # Uso de q (específico) y q0 (genérico) en el cálculo de fuerzas internas
            pn_local = q[i, :, :]
            p0_local = q0[i, :, :]
            pi = kl @ di + p0_local.flatten(order='F')  # Cambio a suma para reflejar MATLAB
            pi = pi.reshape((3, 2), order='F')
            pi = np.round(pi, decimals=10)

            # Guardar `pi` en `Pi` para esta viga
            Pi[:, :, i] = pi

            # Actualización de las cargas globales en `p`
            p[np.ix_(dofs)] += T.T @ pi.flatten(order='F')
            mostrar_elemento(f"Fuerzas en coordenadas globales de la viga {viga['id']}", np.array2string(p, precision=2, suppress_small=True))
 
    # Asignar los resultados de `Pi` a las propiedades de las vigas
    for i, viga in enumerate(frame.b):
        viga['axialLoad'] = Pi[0, :, i]
        viga['shearLoad'] = Pi[1, :, i]
        viga['bendingMoment'] = Pi[2, :, i]

    # Actualizar desplazamientos, cargas nodales y reacciones en los nodos
    # Actualizar desplazamientos, cargas nodales y reacciones en los nodos
    d = d.reshape((nx, 3))
    p = p.reshape((nx, 3))
    r = r.reshape((nx, 3))
    nodos_deformados = []

    for i, nodo in enumerate(nodos):
        nodo.nload = np.array([p[i][0], p[i][1], p[i][2]])
        nodo.disp = d[i]
        nodo.react = r[i]  # Asignar directamente el valor calculado en `r`
    
        # Crear nodo deformado sumando desplazamientos a coordenadas originales
        x_deformado = nodo.x + nodo.disp[0]
        y_deformado = nodo.y + nodo.disp[1]
        nodos_deformados.append({'id': nodo.id, 'x': x_deformado, 'y': y_deformado})

    # Almacenar nodos deformados en el marco
    frame.nodos_deformados = nodos_deformados

    # Imprimir los resultados si es necesario
    if print_output:
        print_static_data(frame)

    return frame

def print_static_data(frame):
    """
    Imprime los resultados de las cargas internas, reacciones y desplazamientos en el marco.
    """
    print("\nCargas internas en las vigas:")
    for viga in frame.b:
        print(f"Viga {viga['id']}:\tAxial = {viga['axialLoad']}\tShear = {viga['shearLoad']}\tBending = {viga['bendingMoment']}")

    print("\nReacciones en los nodos:")
    for nodo in frame.n:
        if any(nodo.rdofs):
            print(f"Nodo {nodo.id}:\trx = {nodo.react[0]:.6f}, ry = {nodo.react[1]:.6f}, rz = {nodo.react[2]:.6f}")

    print("\nDesplazamientos en los nodos:")
    for nodo in frame.n:
        print(f"Nodo {nodo.id}:\tux = {nodo.disp[0]:.6f}, uy = {nodo.disp[1]:.6f}, rz = {nodo.disp[2]:.6f}")
    
    print("\nPropiedades de las vigas:")
    for viga in frame.b:
        print(f"Viga {viga['id']} - Área: {viga['area']}, Módulo de Elasticidad: {viga['elasticMod']}, Inercia: {viga['inertia']}")
