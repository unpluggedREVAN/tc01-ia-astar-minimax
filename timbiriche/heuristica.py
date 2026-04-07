# =============================================================
# heuristica.py — Función de evaluación para Timbiriche
# =============================================================


def evaluar(tablero, jugador_max):
    """
    Estima qué tan buena es la posición para jugador_max.

    Criterios:
      1. Diferencia de puntos actual (×3)
      2. Cajas capturables ahora por mí, tienen 3 lados (+2)
      3. Cajas capturables ahora por el rival, tienen 3 lados (-2)
      4. Cajas con 2 lados, peligrosas (-0.5)

    Regla estratégica: nunca pongas el tercer lado si no vas
    a cerrar la caja tú mismo.
    """
    rival = 2 if jugador_max == 1 else 1

    diff_puntos = (tablero.puntos[jugador_max - 1] - tablero.puntos[rival - 1]) * 3

    capturo_yo = 0
    captura_el = 0
    peligrosas = 0

    for f in range(tablero.n):
        for c in range(tablero.n):
            if tablero.cajas[f][c] == 0:
                lados = tablero.lados_de_caja(f, c)
                if lados == 3:
                    if tablero.turno == jugador_max:
                        capturo_yo += 1
                    else:
                        captura_el += 1
                elif lados == 2:
                    peligrosas += 1

    return (
        diff_puntos
        + capturo_yo * 2
        - captura_el * 2
        - peligrosas * 0.5
    )