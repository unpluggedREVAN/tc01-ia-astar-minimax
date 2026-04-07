# =============================================================
# interfaz.py — Visualización ASCII e interacción
# =============================================================
from tablero import Tablero

RAYA_H = {0: '─ ─ ─', 1: '─────', 2: '═════'}
RAYA_V = {0: ':',     1: '│',     2: '║'    }

RESET    = '\033[0m'
AZUL     = '\033[94m'
ROJO     = '\033[91m'
VERDE    = '\033[92m'
GRIS     = '\033[90m'
AMARILLO = '\033[93m'

COLOR_JUGADOR = {1: AZUL,               2: ROJO              }
COLOR_CAJA    = {1: '\033[44m\033[97m', 2: '\033[41m\033[97m'}


def dibujar_tablero(tablero, ultimo_mov=None):
    n      = tablero.n
    lineas = []

    for f in range(n + 1):
        fila_h = '  '
        for c in range(n):
            dueno     = tablero.rayas_h[f][c]
            es_ultimo = (ultimo_mov == ('h', f, c))
            if dueno != 0:
                color  = VERDE if es_ultimo else COLOR_JUGADOR[dueno]
                fila_h += '●' + color + RAYA_H[dueno] + RESET
            else:
                fila_h += '●' + GRIS + f'─h{f}{c}─' + RESET
        fila_h += '●'
        lineas.append(fila_h)

        if f < n:
            fila_v = '  '
            for c in range(n + 1):
                dueno_v   = tablero.rayas_v[f][c]
                es_ultimo = (ultimo_mov == ('v', f, c))
                if dueno_v != 0:
                    color  = VERDE if es_ultimo else COLOR_JUGADOR[dueno_v]
                    fila_v += color + RAYA_V[dueno_v] + RESET
                else:
                    fila_v += GRIS + ':' + RESET
                if c < n:
                    dueno_c = tablero.cajas[f][c]
                    if dueno_c != 0:
                        fila_v += COLOR_CAJA[dueno_c] + f'  {dueno_c}  ' + RESET
                    else:
                        fila_v += '     '
            lineas.append(fila_v)

    lineas.append('')
    estado = (f'  {AZUL}■ J1: {tablero.puntos[0]} pts{RESET}   '
              f'{ROJO}■ J2: {tablero.puntos[1]} pts{RESET}')
    if tablero.es_terminal():
        g = tablero.ganador()
        resultado = 'EMPATE' if g == 0 else f'Ganó J{g}'
        estado += f'   {AMARILLO}★ {resultado} ★{RESET}'
    else:
        color_t = COLOR_JUGADOR[tablero.turno]
        estado += f'   → Turno: {color_t}J{tablero.turno}{RESET}'
    lineas.append(estado)

    print('\n'.join(lineas))


def leyenda():
    print()
    print('  Leyenda:')
    print(f'    {AZUL}─────{RESET}  raya del Jugador 1')
    print(f'    {ROJO}═════{RESET}  raya del Jugador 2')
    print(f'    {GRIS}─h00─{RESET}  raya disponible  (código: h 0 0)')
    print(f'    {GRIS}:{RESET}      raya vertical disponible')
    print(f'    \033[44m\033[97m  1  \033[0m  caja cerrada por J1')
    print(f'    \033[41m\033[97m  2  \033[0m  caja cerrada por J2')
    print()
    print('  Comandos:')
    print('    h f c  →  raya horizontal, fila f, columna c')
    print('    v f c  →  raya vertical,   fila f, columna c')
    print('    ayuda  →  ver rayas disponibles')
    print('    salir  →  terminar la partida')
    print()


def parsear_movimiento(texto, tablero):
    texto  = texto.strip().lower().replace(',', ' ')
    partes = texto.split()

    if len(partes) == 3:
        tipo = partes[0]
        try:
            f, c = int(partes[1]), int(partes[2])
        except ValueError:
            return None
    elif len(partes) == 1 and len(texto) >= 3:
        tipo    = texto[0]
        digitos = texto[1:].replace(' ', '')
        try:
            f, c = int(digitos[0]), int(digitos[1])
        except (ValueError, IndexError):
            return None
    else:
        return None

    if tipo not in ('h', 'v'):
        return None

    mov = (tipo, f, c)
    return mov if mov in tablero.movimientos_legales() else None


def mostrar_movimientos_disponibles(tablero):
    movs  = tablero.movimientos_legales()
    horiz = [f'h {f} {c}' for (t, f, c) in movs if t == 'h']
    verti = [f'v {f} {c}' for (t, f, c) in movs if t == 'v']
    print()
    print('  Rayas disponibles:')
    print(f'    Horizontales: {", ".join(horiz)}')
    print(f'    Verticales  : {", ".join(verti)}')
    print()


def mostrar_resultado(tablero, humano=None, ia=None):
    print()
    print('═' * 50)
    print('  RESULTADO FINAL')
    print(f'  Jugador 1: {tablero.puntos[0]} cajas')
    print(f'  Jugador 2: {tablero.puntos[1]} cajas')
    g = tablero.ganador()
    if g == 0:
        print(f'  {AMARILLO}¡EMPATE!{RESET}')
    elif humano and g == humano:
        print(f'  {AMARILLO}¡Ganaste! (Jugador {g}){RESET}')
    elif ia and g == ia:
        print(f'  {AMARILLO}Ganó la IA (Jugador {g}){RESET}')
    else:
        print(f'  {AMARILLO}¡Ganó el Jugador {g}!{RESET}')
    print('═' * 50)


def imprimir_camino(registro, n, mostrar_tablero_cada=5):
    print()
    print('═' * 55)
    print('  CAMINO: ESTADO INICIAL → ESTADO OBJETIVO')
    print('═' * 55)

    estado = Tablero(n)
    print('\n  ESTADO INICIAL:')
    dibujar_tablero(estado)

    for i, (jugador, mov, cerradas) in enumerate(registro, 1):
        tipo, f, c = mov
        estado, _ = estado.aplicar_movimiento(mov)
        direccion = 'horizontal' if tipo == 'h' else 'vertical  '
        cierre    = f'→ cerró {cerradas} caja(s)!' if cerradas else ''
        print(f'\n  #{i:2}  J{jugador}  |  {tipo} {f} {c} ({direccion})  {cierre}')
        print(f'       Marcador: J1={estado.puntos[0]}  J2={estado.puntos[1]}')
        if mostrar_tablero_cada > 0 and (i % mostrar_tablero_cada == 0 or cerradas):
            dibujar_tablero(estado, mov)

    print()
    print('  ESTADO FINAL:')
    dibujar_tablero(estado)
    g = estado.ganador()
    print(f'\n  Total movimientos : {len(registro)}')
    print(f'  Resultado         : ' + ('EMPATE' if g == 0 else f'Ganó J{g}'))
    print('═' * 55)


def resumen_tiempo(registro, stats):
    print()
    print('─' * 50)
    print('  TIEMPO DE EJECUCIÓN DEL ALGORITMO')
    print('─' * 50)
    print(f'  Movimientos totales: {len(registro)}')
    for j in [1, 2]:
        ts = stats[j]['tiempo']
        ns = stats[j]['nodos']
        if ts:
            print(f'\n  Jugador {j} (Minimax):')
            print(f'    Turnos jugados  : {len(ts)}')
            print(f'    Tiempo total    : {sum(ts):.3f} s')
            print(f'    Tiempo promedio : {sum(ts)/len(ts):.4f} s')
            print(f'    Tiempo máximo   : {max(ts):.4f} s')
            print(f'    Nodos totales   : {sum(ns):,}')
            print(f'    Nodos promedio  : {sum(ns)//len(ns):,}')
    print('─' * 50)