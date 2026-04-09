"""
PROGRAMA PRINCIPAL - PEG SOLITAIRE CON A*
Como funciona: 
- El juego comienza con 32 fichas (33 posiciones - 1 vacia en el centro)
- A* busca una secuencia de movimientos que deje solo 1 ficha
- Cada movimiento salta una ficha sobre otra y la elimina
- Se expande el nodo con menor f(n) = g(n) + h(n)
"""

from tablero import Tablero
from astar import astar
from heuristica import heuristica_contar_fichas
import time


def linea_separadora(titulo=""):
    """Muestra una linea de separacion"""
    if titulo:
        print("\n" + "="*70)
        print("  " + titulo)
        print("="*70 + "\n")
    else:
        print("="*70 + "\n")


def mostrar_tablero_info(tablero, titulo="Tablero"):
    """Muestra tablero con info"""
    print(titulo)
    print(tablero)
    fichas = tablero.contar_fichas()
    print(f"Fichas: {fichas}")
    if tablero.es_objetivo():
        print("Objetivo alcanzado - Solo 1 ficha en el centro")
    print()


def mostrar_solucion_pasos(camino):
    """Muestra la solucion paso a paso"""
    print(f"\nSolucion en {len(camino) - 1} movimientos:")
    print("-" * 70)
    
    for paso, nodo in enumerate(camino):
        print(f"\nPASO {paso}: ({nodo.tablero.contar_fichas()} fichas)")
        
        if nodo.movimiento:
            (f1, c1), (f2, c2) = nodo.movimiento
            print(f"Movimiento: ({f1},{c1}) -> ({f2},{c2})")
            print(f"Costo g(n): {nodo.g}")
        
        # Mostrar tablero
        print(nodo.tablero)


def principal():

    linea_separadora("PEG SOLITAIRE - SOLUCION CON A*")
    
    # PASO 1: CREAR TABLERO
    tablero = Tablero(tamaño=7)
    print("\nTABLERO INICIAL")
    mostrar_tablero_info(tablero, "Estado inicial del juego:")
    
    print("\nREGLAS DEL JUEGO:")
    print("- Salta una ficha sobre otra (ortogonalmente)")
    print("- La ficha saltada se elimina")
    print("- OBJETIVO: Dejar solo 1 ficha en el centro del tablero")
    print("- Total de movimientos posibles: ~5 millones")
    print("- Profundidad de solucion optima: ~31 movimientos")
    
    # PASO 2: BUSCAR SOLUCION CON A*
    linea_separadora("EJECUTANDO A*")
    
    print("Iniciando busqueda...")
    print("Heuristica usada:")
    print("  - Numero de fichas restantes - 1")
    print("  - Cada movimiento elimina exactamente una ficha\n")
    
    inicio = time.time()

    camino, costo, nodos_exp, nodos_gen = astar(
        tablero,
        heuristica_contar_fichas,
        max_nodos=100000
    )
    
    tiempo_ms = (time.time() - inicio) * 1000
    
    # PASO 3: MOSTRAR RESULTADOS
    linea_separadora("RESULTADOS")
    
    if camino:
        print("Se encontro solucion\n")
        print(f"Movimientos: {len(camino) - 1}")
        print(f"Costo total: {costo}")
        print(f"Nodos expandidos: {nodos_exp}")
        print(f"Nodos generados: {nodos_gen}")
        print(f"Tiempo: {tiempo_ms:.2f} ms")
        print(f"Fichas finales: 1")
        
        # Mostrar solucion detallada
        mostrar_solucion_pasos(camino)
        
        # Mostrar estado final
        linea_separadora("TABLERO FINAL")
        mostrar_tablero_info(camino[-1].tablero, "Estado final:")
        
    else:
        print("No se encontro solucion en {0} expansiones".format(nodos_exp))
        print("\nNota: Peg Solitaire es muy complejo")
        print("Se requiere:")
        print("- Mayor limite de nodos")
        print("- Mejor heuristica")
        print("- O un tablero mas pequeño (5x5)")
    
    print("\n" + "="*70)
    print("Programa finalizado")
    print("="*70 + "\n")

if __name__ == "__main__":
    principal()
