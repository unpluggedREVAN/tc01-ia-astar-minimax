import time
import matplotlib.pyplot as plt
import pandas as pd

from tablero import Tablero
from astar import astar
from heuristica import heuristica_contar_fichas


# -----------------------------
# CASOS DE CORRECTITUD
# -----------------------------

def crear_tablero_caso_1():
    """
    Caso sencillo: queda a 1 movimiento de la meta.
    """
    tablero = Tablero(tamaño=7)

    # Limpiar todas las posiciones válidas
    for i in range(7):
        for j in range(7):
            if tablero.estado[i][j] != -1:
                tablero.estado[i][j] = 0

    # Dos fichas listas para saltar al centro
    tablero.estado[3][1] = 1
    tablero.estado[3][2] = 1
    tablero.estado[3][3] = 0

    return tablero


def crear_tablero_caso_2():
    """
    Caso sencillo: queda a 2 movimientos de la meta.
    """
    tablero = Tablero(tamaño=7)

    for i in range(7):
        for j in range(7):
            if tablero.estado[i][j] != -1:
                tablero.estado[i][j] = 0

    tablero.estado[1][2] = 1
    tablero.estado[2][2] = 1
    tablero.estado[3][1] = 1
    tablero.estado[3][2] = 0
    tablero.estado[3][3] = 0

    return tablero


def crear_tablero_caso_3():
    """
    Caso sencillo: queda a 3 movimientos de la meta.
    """
    tablero = Tablero(tamaño=7)

    for i in range(7):
        for j in range(7):
            if tablero.estado[i][j] != -1:
                tablero.estado[i][j] = 0

    tablero.estado[1][4] = 1
    tablero.estado[1][3] = 1
    tablero.estado[2][2] = 1
    tablero.estado[3][1] = 1

    tablero.estado[1][2] = 0
    tablero.estado[3][2] = 0
    tablero.estado[3][3] = 0

    return tablero


# -----------------------------
# FUNCIONES GENERALES
# -----------------------------

def ejecutar_caso(tablero, nombre_caso, max_nodos=1000, mostrar=False):
    """
    Ejecuta A* sobre un tablero dado y devuelve los resultados.
    """
    inicio = time.time()

    camino, costo, nodos_exp, nodos_gen = astar(
        tablero,
        heuristica_contar_fichas,
        max_nodos=max_nodos
    )

    fin = time.time()
    tiempo_ms = (fin - inicio) * 1000

    resultado = {
        "caso": nombre_caso,
        "solucion_encontrada": camino is not None,
        "movimientos": len(camino) - 1 if camino else None,
        "costo_total": costo,
        "nodos_expandidos": nodos_exp,
        "nodos_generados": nodos_gen,
        "tiempo_ms": tiempo_ms,
        "camino": camino
    }

    if mostrar:
        print("=" * 60)
        print(nombre_caso)
        print("=" * 60)
        print("Tablero inicial:")
        print(tablero)
        print()

        if camino is not None:
            print("Sí encontró solución")
            print("Movimientos:", resultado["movimientos"])
            print("Costo total:", resultado["costo_total"])
            print("Nodos expandidos:", resultado["nodos_expandidos"])
            print("Nodos generados:", resultado["nodos_generados"])
            print(f"Tiempo: {resultado['tiempo_ms']:.2f} ms")
            print("\nEstado final:")
            print(camino[-1].tablero)
            print("¿Es objetivo?:", camino[-1].tablero.es_objetivo())
        else:
            print("No encontró solución")
            print("Nodos expandidos:", resultado["nodos_expandidos"])
            print("Nodos generados:", resultado["nodos_generados"])
            print(f"Tiempo: {resultado['tiempo_ms']:.2f} ms")

        print()

    return resultado


# -----------------------------
# PRUEBAS DE CORRECTITUD
# -----------------------------

def correr_pruebas_correctitud(mostrar=True):
    """
    Ejecuta varios casos pequeños para verificar que A* sí resuelve
    estados cercanos al objetivo.
    """
    casos = [
        ("Caso 1: a 1 movimiento de la meta", crear_tablero_caso_1(), 100),
        ("Caso 2: a 2 movimientos de la meta", crear_tablero_caso_2(), 100),
        ("Caso 3: a 3 movimientos de la meta", crear_tablero_caso_3(), 200),
    ]

    resultados = []

    for nombre, tablero, limite in casos:
        resultado = ejecutar_caso(tablero, nombre, max_nodos=limite, mostrar=mostrar)
        resultados.append({
            "caso": resultado["caso"],
            "solucion_encontrada": resultado["solucion_encontrada"],
            "movimientos": resultado["movimientos"],
            "nodos_expandidos": resultado["nodos_expandidos"],
            "nodos_generados": resultado["nodos_generados"],
            "tiempo_ms": resultado["tiempo_ms"]
        })

    return pd.DataFrame(resultados)


# -----------------------------
# PRUEBAS DE DESEMPEÑO
# -----------------------------

def correr_pruebas_desempeno(limites=None):
    """
    Ejecuta el tablero clásico con distintos límites de nodos
    para observar tiempo, nodos expandidos y éxito.
    """
    if limites is None:
        limites = [1000, 5000, 10000, 50000, 100000]

    resultados = []

    for limite in limites:
        tablero = Tablero(tamaño=7)

        inicio = time.time()
        camino, costo, nodos_exp, nodos_gen = astar(
            tablero,
            heuristica_contar_fichas,
            max_nodos=limite
        )
        fin = time.time()

        resultados.append({
            "limite_nodos": limite,
            "solucion_encontrada": 1 if camino is not None else 0,
            "movimientos": len(camino) - 1 if camino else None,
            "nodos_expandidos": nodos_exp,
            "nodos_generados": nodos_gen,
            "tiempo_ms": (fin - inicio) * 1000
        })

    return pd.DataFrame(resultados)


# -----------------------------
# GRÁFICAS
# -----------------------------

def graficar_tiempo(df):
    plt.figure(figsize=(8, 5))
    plt.plot(df["limite_nodos"], df["tiempo_ms"], marker="o")
    plt.xlabel("Límite de nodos")
    plt.ylabel("Tiempo (ms)")
    plt.title("Tiempo de ejecución según el límite de nodos")
    plt.grid(True)
    plt.show()


def graficar_expandidos(df):
    plt.figure(figsize=(8, 5))
    plt.plot(df["limite_nodos"], df["nodos_expandidos"], marker="o")
    plt.xlabel("Límite de nodos")
    plt.ylabel("Nodos expandidos")
    plt.title("Nodos expandidos según el límite de nodos")
    plt.grid(True)
    plt.show()


def graficar_exito(df):
    plt.figure(figsize=(8, 5))
    plt.plot(df["limite_nodos"], df["solucion_encontrada"], marker="o")
    plt.xlabel("Límite de nodos")
    plt.ylabel("Éxito")
    plt.title("Éxito del algoritmo según el límite de nodos")
    plt.yticks([0, 1], ["No", "Sí"])
    plt.grid(True)
    plt.show()


# -----------------------------
# EJECUCIÓN DIRECTA
# -----------------------------

if __name__ == "__main__":
    print("\nPRUEBAS DE CORRECTITUD")
    df_correctitud = correr_pruebas_correctitud(mostrar=True)
    print(df_correctitud)

    print("\nPRUEBAS DE DESEMPEÑO")
    df_desempeno = correr_pruebas_desempeno()
    print(df_desempeno)

    graficar_tiempo(df_desempeno)
    graficar_expandidos(df_desempeno)
    graficar_exito(df_desempeno)