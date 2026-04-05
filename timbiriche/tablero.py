# =============================================================
# tablero.py — Representación del estado del juego Timbiriche
# =============================================================
import copy


class Tablero:
    """
    Estado completo del juego Dots and Boxes (Timbiriche).

    Para un tablero de n×n cajas (con (n+1)×(n+1) puntos):

      rayas_h[fila][col]  → quién puso la raya horizontal
                            índices: (n+1) filas × n columnas
      rayas_v[fila][col]  → quién puso la raya vertical
                            índices: n filas × (n+1) columnas
      cajas[fila][col]    → quién cerró esa caja
                            0 = abierta, 1 = J1, 2 = J2
      puntos              → [puntos_J1, puntos_J2]
      turno               → jugador que mueve ahora (1 o 2)

    Una caja (f, c) está cerrada cuando tiene sus 4 lados:
      arriba    → rayas_h[f][c]
      abajo     → rayas_h[f+1][c]
      izquierda → rayas_v[f][c]
      derecha   → rayas_v[f][c+1]
    """

    def __init__(self, n=3):
        self.n = n
        self.rayas_h = [[0] * n       for _ in range(n + 1)]
        self.rayas_v = [[0] * (n + 1) for _ in range(n)]
        self.cajas   = [[0] * n       for _ in range(n)]
        self.puntos  = [0, 0]
        self.turno   = 1

    # ── Copia ────────────────────────────────────────────────

    def clonar(self):
        """Retorna una copia profunda. El original nunca se modifica."""
        return copy.deepcopy(self)

    # ── Movimientos ──────────────────────────────────────────

    def movimientos_legales(self):
        """
        Lista de todos los movimientos posibles desde este estado.
        Cada movimiento es una tupla ('h', fila, col) o ('v', fila, col).
        """
        movs = []
        for f in range(self.n + 1):
            for c in range(self.n):
                if self.rayas_h[f][c] == 0:
                    movs.append(('h', f, c))
        for f in range(self.n):
            for c in range(self.n + 1):
                if self.rayas_v[f][c] == 0:
                    movs.append(('v', f, c))
        return movs

    def aplicar_movimiento(self, mov):
        """
        Aplica el movimiento sobre una copia y retorna (nuevo_tablero, cajas_cerradas).

        Si se cierran cajas, el turno NO cambia: el mismo jugador vuelve a mover.
        Si no se cierra ninguna, el turno pasa al otro jugador.
        """
        nuevo = self.clonar()
        tipo, f, c = mov

        if tipo == 'h':
            nuevo.rayas_h[f][c] = self.turno
        else:
            nuevo.rayas_v[f][c] = self.turno

        cerradas = nuevo._marcar_cajas_nuevas(tipo, f, c)
        nuevo.puntos[self.turno - 1] += cerradas

        if cerradas == 0:
            nuevo.turno = 2 if self.turno == 1 else 1

        return nuevo, cerradas

    def _marcar_cajas_nuevas(self, tipo, f, c):
        """
        Revisa las cajas adyacentes a la raya recién puesta.
        Marca las que quedaron completas y retorna cuántas fueron.
        """
        cerradas = 0
        # Una raya horizontal (f,c) es el techo de la caja (f,c)
        # y el piso de la caja (f-1,c).
        # Una raya vertical (f,c) es el lado izquierdo de (f,c)
        # y el lado derecho de (f,c-1).
        vecinos = [(f, c), (f-1, c)] if tipo == 'h' else [(f, c), (f, c-1)]

        for (bf, bc) in vecinos:
            if 0 <= bf < self.n and 0 <= bc < self.n:
                if self.cajas[bf][bc] == 0 and self._caja_completa(bf, bc):
                    self.cajas[bf][bc] = self.turno
                    cerradas += 1
        return cerradas

    def _caja_completa(self, f, c):
        """True si los 4 lados de la caja (f, c) están puestos."""
        return (
            self.rayas_h[f][c]     and
            self.rayas_h[f + 1][c] and
            self.rayas_v[f][c]     and
            self.rayas_v[f][c + 1]
        )

    # ── Consultas ────────────────────────────────────────────

    def es_terminal(self):
        """True cuando todas las cajas están cerradas (juego terminado)."""
        return all(
            self.cajas[f][c] != 0
            for f in range(self.n)
            for c in range(self.n)
        )

    def lados_de_caja(self, f, c):
        """Cuántos de los 4 lados de la caja (f, c) ya están puestos."""
        return sum([
            bool(self.rayas_h[f][c]),
            bool(self.rayas_h[f + 1][c]),
            bool(self.rayas_v[f][c]),
            bool(self.rayas_v[f][c + 1])
        ])

    def ganador(self):
        """Retorna 1, 2, o 0 si hay empate."""
        if self.puntos[0] > self.puntos[1]:
            return 1
        if self.puntos[1] > self.puntos[0]:
            return 2
        return 0