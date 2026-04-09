"""
Aquí definimos los movimientos legales que se pueden hacer en el peg solitaire, 
cómo se aplican esos movimientos al tablero y cómo verificar si un 
movimiento es válido. Más que todo lo que se hace es revisar el estado del tablero, 
y generar los movimientos válidos. 

RELACIÓN CON OTROS MÓDULOS:
- tablero.py: Modifica el estado del tablero después de aplicar movimientos
- astar.py: Obtiene movimientos válidos para explorar sucessores
- main.py: Utiliza estos movimientos para mostrar la solución
"""

def obtener_movimientos_validos(tablero):
    """
    Aquí se buscan todos los movimientos que sí se pueden hacer
    en el estado actual del tablero.
    """
    movimientos = []

    # Estas son las 4 direcciones permitidas en el juego:
    # arriba, abajo, izquierda y derecha
    direcciones = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    # Se recorre todo el tablero para buscar fichas que se puedan mover
    for fila in range(tablero.tamaño):
        for col in range(tablero.tamaño):

            # Solo tiene sentido revisar posiciones donde sí hay ficha
            if tablero.estado[fila][col] == 1:

                for df, dc in direcciones:
                    fila_intermedia = fila + df
                    col_intermedia = col + dc

                    fila_destino = fila + 2 * df
                    col_destino = col + 2 * dc

                    # Aquí revisamos que las posiciones no se salgan del tablero
                    if (0 <= fila_intermedia < tablero.tamaño and
                        0 <= col_intermedia < tablero.tamaño and
                        0 <= fila_destino < tablero.tamaño and
                        0 <= col_destino < tablero.tamaño):

                        # Para que el movimiento sea válido:
                        # - debe haber una ficha en medio
                        # - y el destino debe estar vacío
                        if (tablero.estado[fila_intermedia][col_intermedia] == 1 and
                            tablero.estado[fila_destino][col_destino] == 0):

                            # Si cumple todo, entonces sí se puede hacer ese movimiento
                            movimientos.append(((fila, col), (fila_destino, col_destino)))

    return movimientos


def aplicar_movimiento(tablero, movimiento):
    """
    Esta función aplica un movimiento y devuelve un tablero nuevo.
    No modifica el tablero original.
    """
    nuevo_tablero = tablero.copiar()

    (fila_origen, col_origen), (fila_destino, col_destino) = movimiento

    # La ficha sale de la posición inicial
    nuevo_tablero.estado[fila_origen][col_origen] = 0

    # La ficha llega a la posición final
    nuevo_tablero.estado[fila_destino][col_destino] = 1

    # Se calcula la posición de la ficha que fue saltada
    fila_intermedia = (fila_origen + fila_destino) // 2
    col_intermedia = (col_origen + col_destino) // 2

    # Esa ficha se elimina
    nuevo_tablero.estado[fila_intermedia][col_intermedia] = 0

    return nuevo_tablero


def es_movimiento_valido(tablero, movimiento):
    """
    Aquí solo se revisa si un movimiento está dentro
    de los movimientos válidos del tablero actual.
    """
    return movimiento in obtener_movimientos_validos(tablero)


def costo_movimiento(movimiento):
    """
    En este problema todos los movimientos cuestan lo mismo,
    entonces siempre se devuelve 1.
    """
    return 1