import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np
import matplotlib.pyplot as plt

def plot_frame(nodos, vigas):
    """
    Función para graficar el marco estructural con nodos y vigas.
    """
    fig, ax = plt.subplots()

    # Graficar nodos
    x = [nodo.x for nodo in nodos]
    y = [nodo.y for nodo in nodos]
    ax.scatter(x, y, c='black')  # Nodos

    # Graficar vigas
    for viga in vigas:
        nodo_inicial = nodos[viga['ni'] - 1]
        nodo_final = nodos[viga['nj'] - 1]
        x_coords = [nodo_inicial.x, nodo_final.x]
        y_coords = [nodo_inicial.y, nodo_final.y]
        ax.plot(x_coords, y_coords, 'k-', linewidth=2)  # Dibujar vigas en negro
    plt.title("Marco Inicial")   
    ax.set_xlabel("X")
    ax.set_ylabel("Y")
    ax.grid(True)
   
    return fig, ax


def plot_nodes(nodos):
    # Graficar nodos
    x = [nodo.x for nodo in nodos]
    y = [nodo.y for nodo in nodos]
    plt.scatter(x, y, c='red')
    
    # Añadir etiquetas a los nodos
    for nodo in nodos:
        plt.text(nodo.x, nodo.y, f'N{nodo.id}', fontsize=9, ha='left')
    plt.title("Gráfico de Nodos")
    plt.xlabel("X")
    plt.ylabel("Y")

def plot_beam(nodos, vigas):
    # Graficar nodos
    x = [nodo.x for nodo in nodos]
    y = [nodo.y for nodo in nodos]
    plt.scatter(x, y, c='red')
    
    # Añadir etiquetas a los nodos
    for nodo in nodos:
        plt.text(nodo.x, nodo.y, f'N{nodo.id}', fontsize=9, ha='left')
    # Graficar vigas
    for viga in vigas:
        nodo_inicial = nodos[viga['ni'] - 1]
        nodo_final = nodos[viga['nj'] - 1]
        x_coords = [nodo_inicial.x, nodo_final.x]
        y_coords = [nodo_inicial.y, nodo_final.y]
        plt.plot(x_coords, y_coords, 'blue')
        
        # Añadir etiquetas a las vigas
        mid_x = (nodo_inicial.x + nodo_final.x) / 2
        mid_y = (nodo_inicial.y + nodo_final.y) / 2
        plt.text(mid_x, mid_y, f'V{viga["id"]}', fontsize=9, ha='center')
    plt.grid(True)
    plt.title("Gráfico de Nodos y Vigas")
    plt.show(block=True)
    plt.xlabel("X")
    plt.ylabel("Y")

def plot_pload(nodos, vigas, cargas_puntuales_obj):
    """
    Función para graficar el marco estructural y las cargas puntuales en los nodos.
    """
    # Llamar a plot_frame para crear el marco estructural
    fig, ax = plot_frame(nodos, vigas)
    
    # Calcular dimensiones para el ajuste de escala
    max_coord = max(max(nodo.x for nodo in nodos), max(nodo.y for nodo in nodos))
    max_carga = max(
        max(abs(carga_info['valor'][0]), abs(carga_info['valor'][1]), abs(carga_info['valor'][2]) if len(carga_info['valor']) > 2 else 0)
        for carga in cargas_puntuales_obj
        for carga_info in carga.cargas
    )
    escala = (0.1 * max_coord) / max_carga

    # Añadir las cargas puntuales a la figura
    for carga in cargas_puntuales_obj:
        for carga_info in carga.cargas:
            nodo_id = carga_info['nodo']
            valores = carga_info['valor']
            
            # Desempaquetar con valores predeterminados
            px = valores[0] if len(valores) > 0 else 0
            py = valores[1] if len(valores) > 1 else 0
            mz = valores[2] if len(valores) > 2 else 0

            nodo = next(n for n in nodos if n.id == nodo_id)  # Nodo donde se aplica la carga
            
            # Dibujar flecha para carga en X
            if px != 0:
                x_offset = 0.1 * np.sign(px)
                plt.arrow(nodo.x - x_offset, nodo.y, px * escala, 0, head_width=0.05 * max_coord, head_length=0.05 * max_coord, color='blue')
                plt.text(nodo.x - x_offset, nodo.y - 0.1 * max_coord, f'{px:.2f}', color='blue', ha='center')
            
            # Dibujar flecha para carga en Y
            if py != 0:
                y_offset = 0.1 * np.sign(py)
                plt.arrow(nodo.x, nodo.y - y_offset, 0, py * escala, head_width=0.05 * max_coord, head_length=0.05 * max_coord, color='red')
                plt.text(nodo.x, nodo.y - y_offset - 0.2 * max_coord, f'{py:.2f}', color='red', ha='center')

            # Dibujar momento como arco
            if mz != 0:
                arc_direction = -1 if mz < 0 else 1
                arc = patches.Arc((nodo.x, nodo.y), 0.2 * max_coord, 0.2 * max_coord, angle=0, theta1=0, theta2=180 * arc_direction, color='purple', lw=2)
                ax.add_patch(arc)
                ax.text(nodo.x, nodo.y + 0 * arc_direction * max_coord, f'{mz:.2f}', color='purple', ha='center')
    
    plt.title("Carga Puntual")
    plt.grid(True)

def plot_deformed_frame_scaled(nodos, vigas, nodos_deformados):
    """
    Función para graficar el marco estructural deformado con un factor de escala ajustado y etiquetas.
    """
    fig, ax = plt.subplots()

    # Coordenadas iniciales de las vigas
    xi = [nodos[viga['ni'] - 1].x for viga in vigas]
    xj = [nodos[viga['nj'] - 1].x for viga in vigas]
    yi = [nodos[viga['ni'] - 1].y for viga in vigas]
    yj = [nodos[viga['nj'] - 1].y for viga in vigas]

    # Calcular desplazamientos
    dx = np.array([nodo.disp for nodo in nodos])  # Matriz de desplazamientos (ux, uy)
    max_dx = np.max(np.abs(dx[:, :2]))  # Max desplazamiento en x o y
    ax_limits = ax.axis()  # Límites de los ejes del gráfico
    ref_dax = min(abs(ax_limits[1] - ax_limits[0]), abs(ax_limits[3] - ax_limits[2]))

    # Verificar que max_dx no sea cero para evitar el infinito en k
    if max_dx != 0:
        k = 0.10 * ref_dax / max_dx  # Escala para que el máximo desplazamiento sea 10% del eje
        kfactor = 10 ** round(np.log10(k))  # Factor de escala redondeado
    else:
        kfactor = 1  # Valor por defecto si no hay desplazamientos

    # Graficar marco deformado con el factor de escala ajustado
    for i, viga in enumerate(vigas):
        ni, nj = viga['ni'] - 1, viga['nj'] - 1  # Índices de nodos inicial y final

        # Aplicar deformación con factor de escala
        x_coords = [xi[i] + nodos[ni].disp[0] * kfactor, xj[i] + nodos[nj].disp[0] * kfactor]
        y_coords = [yi[i] + nodos[ni].disp[1] * kfactor, yj[i] + nodos[nj].disp[1] * kfactor]

        # Graficar viga deformada
        ax.plot(x_coords, y_coords, 'g--', linewidth=2, label="Viga deformada" if i == 0 else "")
        
        # Añadir etiqueta en el medio de la viga
        mid_x = (x_coords[0] + x_coords[1]) / 2
        mid_y = (y_coords[0] + y_coords[1]) / 2
        ax.text(mid_x, mid_y, f'V{viga["id"]}', fontsize=9, ha='center', color='green')

    # Graficar nodos deformados y añadir etiquetas en las posiciones exactas deformadas
    for i, nodo in enumerate(nodos):
        x_deformado = nodo.x + nodo.disp[0] * kfactor
        y_deformado = nodo.y + nodo.disp[1] * kfactor
        ax.scatter(x_deformado, y_deformado, c='green')
        ax.text(x_deformado + 0.02, y_deformado, f'N{nodo.id}', fontsize=9, ha='left', color='green')  # Ajuste de posición horizontal

    # Configuración final de la gráfica
    ax.set_xlabel("X")
    ax.set_ylabel("Y")
    ax.legend()
    ax.grid(True)
    plt.title(f"Marco Deformado (Factor de escala: {kfactor})")