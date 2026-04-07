 # =============================================================
# pruebas.py — Pruebas unitarias y de integración
# =============================================================
from tablero  import Tablero
from minimax  import mejor_movimiento


def prueba(nombre, condicion):
    estado = 'OK  ' if condicion else 'FALLO'
    print(f'  {estado}  {nombre}')
    return condicion


def test_movimientos_iniciales():
    t = Tablero(2)
    return prueba('Tablero 2×2: 12 movimientos legales iniciales',
                  len(t.movimientos_legales()) == 12)


def test_aplicar_reduce_movimientos():
    t = Tablero(2)
    t2, _ = t.aplicar_movimiento(('h', 0, 0))
    return prueba('Aplicar movimiento: quedan 11 disponibles',
                  len(t2.movimientos_legales()) == 11)


def test_clonacion_independiente():
    t = Tablero(2)
    t2, _ = t.aplicar_movimiento(('h', 0, 0))
    return prueba('Clonación: el original no se modifica',
                  t.rayas_h[0][0] == 0)


def test_cerrar_caja():
    t = Tablero(2)
    t, _ = t.aplicar_movimiento(('h', 0, 0))
    t, _ = t.aplicar_movimiento(('h', 1, 0))
    t, _ = t.aplicar_movimiento(('v', 0, 0))
    t, cerradas = t.aplicar_movimiento(('v', 0, 1))
    r1 = prueba('Cerrar caja: 1 caja cerrada',
                cerradas == 1)
    r2 = prueba('Cerrar caja: punto asignado al Jugador 2',
                t.puntos[1] == 1 and t.cajas[0][0] == 2)
    r3 = prueba('Cerrar caja: J2 mantiene el turno',
                t.turno == 2)
    return r1 and r2 and r3


def test_estado_terminal():
    t = Tablero(2)
    while not t.es_terminal():
        t, _ = t.aplicar_movimiento(t.movimientos_legales()[0])
    return prueba('Estado terminal: todas las cajas cerradas, 4 puntos totales',
                  t.es_terminal() and sum(t.puntos) == 4)


def test_minimax_captura_obvia():
    t = Tablero(2)
    t.rayas_h[0][0] = 1
    t.rayas_h[1][0] = 1
    t.rayas_v[0][0] = 1
    t.turno = 1
    mov, _, _, _ = mejor_movimiento(t, profundidad=3)
    return prueba('Minimax captura la caja obvia: elige v 0 1',
                  mov == ('v', 0, 1))


def test_partida_completa_2x2():
    t = Tablero(2)
    pasos = 0
    while not t.es_terminal():
        mov, _, _, _ = mejor_movimiento(t, profundidad=3)
        t, _ = t.aplicar_movimiento(mov)
        pasos += 1
        if pasos > 50:
            break
    return prueba('Partida 2×2 completa: termina correctamente',
                  t.es_terminal() and sum(t.puntos) == 4)


def correr_todas():
    print('\n' + '─' * 50)
    print('  PRUEBAS — Timbiriche')
    print('─' * 50)

    resultados = [
        test_movimientos_iniciales(),
        test_aplicar_reduce_movimientos(),
        test_clonacion_independiente(),
        test_cerrar_caja(),
        test_estado_terminal(),
        test_minimax_captura_obvia(),
        test_partida_completa_2x2(),
    ]

    ok = sum(resultados)
    print('─' * 50)
    print(f'  {ok}/{len(resultados)} pruebas pasaron')
    print('─' * 50)
    return ok == len(resultados)


if __name__ == '__main__':
    correr_todas()