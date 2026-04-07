# =============================================================
# minimax.py — Algoritmo Minimax con poda Alpha-Beta
# =============================================================
import math
import time

from heuristica import evaluar


nodos_visitados = 0  # se reinicia en cada llamada a mejor_movimiento


def minimax(tablero, profundidad, alpha, beta, jugador_max):
    """
    Minimax con poda Alpha-Beta.

    El turno en Timbiriche NO alterna siempre: quien cierra una caja
    vuelve a jugar. Por eso determinamos MAX o MIN mirando tablero.turno,
    no la paridad de la profundidad.

    alpha : mejor valor garantizado para MAX hasta ahora
    beta  : mejor valor garantizado para MIN hasta ahora
    """
    global nodos_visitados
    nodos_visitados += 1

    if tablero.es_terminal():
        diff = tablero.puntos[jugador_max - 1] - tablero.puntos[2 - jugador_max]
        return diff * 100

    if profundidad == 0:
        return evaluar(tablero, jugador_max)

    movimientos = tablero.movimientos_legales()

    # Ordenar: primero los movimientos que cierran cajas.
    # Hace que alpha suba rápido y mejora la poda.
    def ganancia_inmediata(m):
        hijo, _ = tablero.aplicar_movimiento(m)
        return -(hijo.puntos[jugador_max - 1] - tablero.puntos[jugador_max - 1])

    movimientos.sort(key=ganancia_inmediata)

    es_max = (tablero.turno == jugador_max)

    if es_max:
        mejor = -math.inf
        for mov in movimientos:
            hijo, _ = tablero.aplicar_movimiento(mov)
            valor = minimax(hijo, profundidad - 1, alpha, beta, jugador_max)
            mejor = max(mejor, valor)
            alpha = max(alpha, mejor)
            if beta <= alpha:
                break  # poda beta
        return mejor
    else:
        mejor = math.inf
        for mov in movimientos:
            hijo, _ = tablero.aplicar_movimiento(mov)
            valor = minimax(hijo, profundidad - 1, alpha, beta, jugador_max)
            mejor = min(mejor, valor)
            beta = min(beta, mejor)
            if beta <= alpha:
                break  # poda alpha
        return mejor


def mejor_movimiento(tablero, profundidad=5):
    """
    Encuentra el mejor movimiento para el jugador en turno.
    Retorna (movimiento, valor, tiempo_segundos, nodos_visitados).
    """
    global nodos_visitados
    nodos_visitados = 0

    jugador_max = tablero.turno
    mejor_mov   = None
    mejor_val   = -math.inf

    t0 = time.time()

    for mov in tablero.movimientos_legales():
        hijo, _ = tablero.aplicar_movimiento(mov)
        val = minimax(hijo, profundidad - 1, -math.inf, math.inf, jugador_max)
        if val > mejor_val:
            mejor_val = val
            mejor_mov = mov

    duracion = time.time() - t0
    return mejor_mov, mejor_val, duracion, nodos_visitados