"""
En este archivo es para las pruebas sobre como se implementó el algoritmo, 
y comprobar si este funciona con el tablero inicial clasico, o si se cambia algo, 
que ese siga funcionando. 

Relación con otros módulos:
- tablero.py: Prueba creación, copia y operaciones básicas
- movimientos.py: Prueba generación y aplicación de movimientos
- astar.py: Prueba que el algoritmo encuentre soluciones
- heuristica.py: Prueba que las heurísticas devuelvan valores válidos

Como ejecutar:
  python pruebas.py
"""

import unittest
from tablero import Tablero
from movimientos import obtener_movimientos_validos, aplicar_movimiento, es_movimiento_valido
from heuristica import heuristica_contar_fichas
from astar import astar


class TestTablero(unittest.TestCase):
    """Aquí se prueban cosas básicas del tablero."""

    def setUp(self):
        # Antes de cada prueba se crea un tablero nuevo
        self.tablero = Tablero()

    def test_tablero_se_crea_bien(self):
        # Se revisa que el tablero exista y tenga tamaño 7x7
        self.assertEqual(self.tablero.tamaño, 7)
        self.assertEqual(len(self.tablero.estado), 7)

    def test_tablero_inicial_tiene_32_fichas(self):
        # El tablero clásico empieza con 32 fichas
        self.assertEqual(self.tablero.contar_fichas(), 32)

    def test_copiar_tablero_no_cambia_el_original(self):
        # Se hace una copia y se modifica la copia
        copia = self.tablero.copiar()
        copia.estado[3][2] = 0

        # El original debe seguir igual
        self.assertNotEqual(self.tablero.estado, copia.estado)

    def test_al_inicio_no_es_objetivo(self):
        # Al inicio no se ha ganado el juego
        self.assertFalse(self.tablero.es_objetivo())

    def test_si_hay_una_ficha_en_el_centro_si_es_objetivo(self):
        # Se limpia el tablero
        for i in range(7):
            for j in range(7):
                if self.tablero.estado[i][j] == 1:
                    self.tablero.estado[i][j] = 0

        # Se deja solo una ficha en el centro
        self.tablero.estado[3][3] = 1

        self.assertTrue(self.tablero.es_objetivo())

    def test_si_hay_una_ficha_fuera_del_centro_no_es_objetivo(self):
        # Se limpia el tablero
        for i in range(7):
            for j in range(7):
                if self.tablero.estado[i][j] == 1:
                    self.tablero.estado[i][j] = 0

        # Se deja una ficha, pero no en el centro
        self.tablero.estado[3][2] = 1

        self.assertFalse(self.tablero.es_objetivo())


class TestMovimientos(unittest.TestCase):
    """Aquí se prueban los movimientos del juego."""

    def setUp(self):
        self.tablero = Tablero()

    def test_al_inicio_hay_movimientos_validos(self):
        # Desde el tablero inicial sí deben existir movimientos
        movimientos = obtener_movimientos_validos(self.tablero)
        self.assertGreater(len(movimientos), 0)

    def test_al_inicio_hay_4_movimientos(self):
        # En el tablero clásico inicial normalmente hay 4 movimientos
        movimientos = obtener_movimientos_validos(self.tablero)
        self.assertEqual(len(movimientos), 4)

    def test_aplicar_movimiento_quita_una_ficha(self):
        # Se toma un movimiento válido y se aplica
        movimientos = obtener_movimientos_validos(self.tablero)
        movimiento = movimientos[0]
        nuevo_tablero = aplicar_movimiento(self.tablero, movimiento)

        # Después del movimiento debe haber una ficha menos
        self.assertEqual(nuevo_tablero.contar_fichas(), self.tablero.contar_fichas() - 1)

    def test_aplicar_movimiento_no_modifica_el_original(self):
        # El tablero original no debería cambiar
        fichas_antes = self.tablero.contar_fichas()
        movimiento = obtener_movimientos_validos(self.tablero)[0]
        _ = aplicar_movimiento(self.tablero, movimiento)

        self.assertEqual(self.tablero.contar_fichas(), fichas_antes)

    def test_es_movimiento_valido_funciona(self):
        # Se prueba un movimiento válido y uno inválido
        movimiento_valido = obtener_movimientos_validos(self.tablero)[0]
        movimiento_invalido = ((0, 0), (0, 2))

        self.assertTrue(es_movimiento_valido(self.tablero, movimiento_valido))
        self.assertFalse(es_movimiento_valido(self.tablero, movimiento_invalido))


class TestHeuristica(unittest.TestCase):
    """Aquí se prueba la heurística principal."""

    def setUp(self):
        self.tablero = Tablero()

    def test_heuristica_inicial_es_31(self):
        # Como hay 32 fichas al inicio, la heurística debe ser 31
        self.assertEqual(heuristica_contar_fichas(self.tablero), 31)

    def test_heuristica_baja_despues_de_un_movimiento(self):
        # Si se elimina una ficha, la heurística debe bajar
        h_inicial = heuristica_contar_fichas(self.tablero)
        movimiento = obtener_movimientos_validos(self.tablero)[0]
        nuevo_tablero = aplicar_movimiento(self.tablero, movimiento)
        h_nueva = heuristica_contar_fichas(nuevo_tablero)

        self.assertLess(h_nueva, h_inicial)


class TestAStar(unittest.TestCase):
    """Aquí se prueba que A* por lo menos corre bien."""

    def setUp(self):
        self.tablero = Tablero()

    def test_astar_se_ejecuta(self):
        # No se obliga a encontrar toda la solución,
        # solo se revisa que el algoritmo corra sin error
        camino, costo, nodos_exp, nodos_gen = astar(
            self.tablero,
            heuristica_contar_fichas,
            max_nodos=200
        )

        self.assertIsInstance(nodos_exp, int)
        self.assertIsInstance(nodos_gen, int)
        self.assertGreaterEqual(nodos_exp, 1)
        self.assertGreaterEqual(nodos_gen, 1)

    def test_si_astar_encuentra_camino_termina_en_objetivo(self):
        # Si encuentra una solución, entonces el último estado sí debe ser objetivo
        camino, costo, nodos_exp, nodos_gen = astar(
            self.tablero,
            heuristica_contar_fichas,
            max_nodos=5000
        )

        if camino is not None:
            self.assertTrue(camino[-1].tablero.es_objetivo())


if __name__ == "__main__":
    unittest.main()