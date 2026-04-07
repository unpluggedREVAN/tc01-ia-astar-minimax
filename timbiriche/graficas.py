# =============================================================
# graficas.py — Visualización del desempeño del algoritmo
# =============================================================
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches


def grafica_desempeno(registro, stats, titulo='Desempeño Minimax'):
    """
    Genera 3 gráficas sobre la partida jugada:

      1. Tiempo de búsqueda por turno (barras por jugador)
      2. Nodos explorados por turno (escala logarítmica)
      3. Evolución del marcador a lo largo de la partida

    registro : lista de (jugador, movimiento, cajas_cerradas)
    stats    : {1: {'tiempo': [...], 'nodos': [...]}, 2: {...}}
    """
    if not registro:
        print('No hay datos para graficar.')
        return

    C1, C2 = '#4A90D9', '#E05A5A'

    fig, axes = plt.subplots(1, 3, figsize=(15, 4))
    fig.suptitle(titulo, fontweight='bold', fontsize=13)

    # ── 1. Tiempo por turno ──────────────────────────────────
    ax = axes[0]
    for j, color in [(1, C1), (2, C2)]:
        ts = stats[j]['tiempo']
        if ts:
            xs = [i for i, (jug, _, _) in enumerate(registro) if jug == j]
            ax.bar(xs, ts, color=color, edgecolor='white', linewidth=0.5,
                   label=f'J{j}')
    todos_tiempos = stats[1]['tiempo'] + stats[2]['tiempo']
    if todos_tiempos:
        prom = sum(todos_tiempos) / len(todos_tiempos)
        ax.axhline(prom, color='black', linestyle='--', linewidth=1.2,
                   label=f'Promedio: {prom:.3f}s')
    ax.set_title('Tiempo por turno')
    ax.set_xlabel('Turno')
    ax.set_ylabel('Segundos')
    ax.legend(fontsize=8)
    ax.grid(axis='y', alpha=0.3)

    # ── 2. Nodos explorados ──────────────────────────────────
    ax = axes[1]
    for j, color in [(1, C1), (2, C2)]:
        ns = stats[j]['nodos']
        if ns:
            xs = [i for i, (jug, _, _) in enumerate(registro) if jug == j]
            ax.plot(xs, ns, 'o-', color=color, linewidth=2,
                    markersize=4, label=f'J{j}')
    ax.set_title('Nodos explorados por turno')
    ax.set_xlabel('Turno')
    ax.set_ylabel('Nodos (escala log)')
    ax.set_yscale('log')
    ax.legend(fontsize=8)
    ax.grid(alpha=0.3)

    # ── 3. Evolución del marcador ────────────────────────────
    ax = axes[2]
    p1, p2 = [0], [0]
    for jugador, _, cerradas in registro:
        if jugador == 1:
            p1.append(p1[-1] + cerradas)
            p2.append(p2[-1])
        else:
            p1.append(p1[-1])
            p2.append(p2[-1] + cerradas)
    xs = list(range(len(p1)))
    ax.step(xs, p1, where='post', color=C1, linewidth=2.5, label='J1')
    ax.step(xs, p2, where='post', color=C2, linewidth=2.5, label='J2')
    ax.set_title('Evolución del marcador')
    ax.set_xlabel('Movimiento')
    ax.set_ylabel('Cajas cerradas')
    ax.legend(fontsize=8)
    ax.grid(alpha=0.3)

    plt.tight_layout()
    plt.show()


def grafica_benchmark(profundidades, tiempos, nodos, n_tablero):
    """
    Muestra cómo crecen el tiempo y los nodos al aumentar la profundidad.
    Útil para analizar la complejidad del algoritmo.

    profundidades : lista de enteros [1, 2, 3, ...]
    tiempos       : tiempo de búsqueda para cada profundidad
    nodos         : nodos explorados para cada profundidad
    n_tablero     : tamaño del tablero usado en el benchmark
    """
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11, 4))
    fig.suptitle(f'Escalabilidad Minimax — Tablero {n_tablero}×{n_tablero}',
                 fontweight='bold')

    ax1.plot(profundidades, tiempos, 'o-', color='#4A90D9', linewidth=2)
    ax1.set_title('Tiempo de búsqueda')
    ax1.set_xlabel('Profundidad')
    ax1.set_ylabel('Segundos')
    ax1.grid(alpha=0.3)

    ax2.plot(profundidades, nodos, 's-', color='#E05A5A', linewidth=2)
    ax2.set_title('Nodos explorados')
    ax2.set_xlabel('Profundidad')
    ax2.set_ylabel('Nodos')
    ax2.set_yscale('log')
    ax2.grid(alpha=0.3)

    plt.tight_layout()
    plt.show()


def benchmark(n_tablero=2, profundidades=None):
    """
    Mide tiempo y nodos para el primer movimiento desde el tablero vacío
    con distintas profundidades. Imprime tabla y genera gráfica.
    """
    from tablero import Tablero
    from minimax import mejor_movimiento

    if profundidades is None:
        profundidades = [1, 2, 3, 4, 5, 6, 7]

    t = Tablero(n_tablero)
    tiempos, nodos = [], []

    print(f'\nBenchmark — tablero {n_tablero}×{n_tablero}')
    print(f'  {"Prof":>5}  {"Tiempo (s)":>12}  {"Nodos":>12}')
    print('  ' + '─' * 35)

    for p in profundidades:
        _, _, dur, n = mejor_movimiento(t, p)
        tiempos.append(dur)
        nodos.append(n)
        print(f'  {p:>5}  {dur:>12.4f}  {n:>12,}')

    grafica_benchmark(profundidades, tiempos, nodos, n_tablero)
    return profundidades, tiempos, nodos