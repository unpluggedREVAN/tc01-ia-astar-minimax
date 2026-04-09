"""
En este arhivo se desarrolla como se implementa el algoritmo. Se controla el
proceso de búsqueda, manejando la cantidad limite de estados que se van a 
explorar, el costo acumulado, y la selección del nodo que sea mejor según
nuestra heuristica. 

Relación con otros módulos:
- tablero.py: Trabaja con objetos Tablero y verifica estado objetivo
- movimientos.py: Obtiene movimientos válidos para explorar sucessores
- heuristica.py: Utiliza la función heurística para calcular f(n)
- main.py: Es llamado por main para encontrar la solución

"""

import heapq
from typing import Tuple, List, Dict, Optional
from tablero import Tablero
from movimientos import obtener_movimientos_validos, aplicar_movimiento


class NodoAStar:
    """
    Representa un nodo en la búsqueda A*.
    
    Atributos:
        tablero (Tablero): Estado del tablero en este nodo
        g (float): Costo real desde el inicio hasta este nodo
        h (float): Estimación heurística desde este nodo al objetivo
        f (float): f(n) = g(n) + h(n), usado para ordenar en la cola
        padre (NodoAStar): Nodo anterior en el camino 
        movimiento (tuple): Movimiento que llevó a este nodo desde su padre
        contador (int): Contador para desempates en la cola
    """
    
    def __init__(self, tablero, g=0, h=0, padre=None, movimiento=None, contador=0):
        """
        Inicializa un nodo A*.
        
        Args:
            tablero (Tablero): Estado del tablero
            g (float): Costo acumulado desde el inicio
            h (float): Heurística estimada al objetivo
            padre (NodoAStar): Nodo padre (None si es raíz)
            movimiento (tuple): Movimiento desde el padre a este nodo
            contador (int): Para desempates entre nodos con igual f
        """
        self.tablero = tablero
        self.g = g
        self.h = h
        self.f = g + h  # f(n) = g(n) + h(n)
        self.padre = padre
        self.movimiento = movimiento
        self.contador = contador
    
    def __menorQue__(self, otro):
        """
        Operador para comparación.
        
        Permite usar NodoAStar en heapq.
        Primero compara por f, luego por contador y se usa FIFO para desempates.
        
        Args:
            otro (NodoAStar): Otro nodo para comparar
            
        Returns:
            bool: True si este nodo tiene menor prioridad
        """
        if self.f != otro.f:
            return self.f < otro.f
        return self.contador < otro.contador


def reconstruir_camino(nodo_objetivo):
    """
    Reconstruye el camino desde el nodo inicial hasta el nodo objetivo.
    
    Sigue la cadena de padres hacia atrás para construir la solución.
    
    Args:
        nodo_objetivo (NodoAStar): Nodo que alcanzó el objetivo
        
    Returns:
        list: Lista de NodoAStar desde el inicio al objetivo
    """
    camino = []
    nodo_actual = nodo_objetivo
    
    # Seguir la cadena de padres hacia atrás
    while nodo_actual is not None:
        camino.append(nodo_actual)
        nodo_actual = nodo_actual.padre
    
    # Invertir para tener el camino desde inicio a objetivo
    camino.reverse()
    return camino

def astar(tablero_inicial, heuristica_fn, max_nodos=100000):
    """
    Implementa el algoritmo A* para Peg Solitaire.

    Como funciona:
    1. Comienza con el tablero inicial en una cola de prioridad
    2. Extrae el nodo con menor f(n) de la cola
    3. Si es el objetivo, retorna la solución
    4. Si no, genera todos sus sucesores aplicando movimientos válidos
    5. Añade sucesores no visitados a la cola
    6. Repite hasta encontrar solución o agotarse los recursos

    Returns:
        tuple: (camino, costo, nodos_expandidos, nodos_generados)
    """
    # Inicialización
    cola_abierta = []
    conjunto_cerrado = set()
    mejor_g = {}

    contador_nodos = 0
    nodos_expandidos = 0
    nodos_generados = 0

    # Crear nodo inicial
    h_inicial = heuristica_fn(tablero_inicial)
    nodo_inicial = NodoAStar(
        tablero=tablero_inicial,
        g=0,
        h=h_inicial,
        padre=None,
        movimiento=None,
        contador=contador_nodos
    )

    contador_nodos += 1
    nodos_generados += 1

    # Añadir nodo inicial a la cola
    heapq.heappush(cola_abierta, (nodo_inicial.f, nodo_inicial.contador, nodo_inicial))

    # Guardar el mejor costo conocido para el estado inicial
    estado_inicial = tablero_inicial.a_tupla()
    mejor_g[estado_inicial] = 0

    print(f"  [Inicio] f(0) = 0 + {h_inicial:.1f} = {nodo_inicial.f:.1f}")
    print(f"  Fichas: {tablero_inicial.contar_fichas()}")

    while cola_abierta and nodos_expandidos < max_nodos:
        _, _, nodo_actual = heapq.heappop(cola_abierta)

        estado_actual = nodo_actual.tablero.a_tupla()

        if estado_actual in conjunto_cerrado:
            continue

        # Marcar como visitado
        conjunto_cerrado.add(estado_actual)
        nodos_expandidos += 1

        # Verificar si es objetivo
        if nodo_actual.tablero.es_objetivo():
            print(f"\n  [OBJETIVO ALCANZADO]")
            print(f"  Nodo en posición: expansión #{nodos_expandidos}")
            print(f"  g(n) = {nodo_actual.g} (costo real)")
            print(f"  h(n) = {nodo_actual.h:.1f} (heurística)")
            print(f"  f(n) = {nodo_actual.f:.1f}")

            camino = reconstruir_camino(nodo_actual)
            return camino, nodo_actual.g, nodos_expandidos, nodos_generados

        if nodos_expandidos % 1000 == 1:
            print(f"  Expandidos: {nodos_expandidos}, Cola abierta: {len(cola_abierta)}, "
                  f"f(n)={nodo_actual.f:.1f}, fichas={nodo_actual.tablero.contar_fichas()}")

        # Expandir sucesores
        movimientos_validos = obtener_movimientos_validos(nodo_actual.tablero)

        for movimiento in movimientos_validos:
            # Generar el nuevo tablero después del movimiento
            tablero_sucesor = aplicar_movimiento(nodo_actual.tablero, movimiento)
            estado_sucesor = tablero_sucesor.a_tupla()

            if estado_sucesor in conjunto_cerrado:
                continue

            g_sucesor = nodo_actual.g + 1
            h_sucesor = heuristica_fn(tablero_sucesor)

            # Solo guardar este sucesor si es la primera vez que aparece
            # o si encontramos un camino mejor hacia ese mismo estado
            if estado_sucesor not in mejor_g or g_sucesor < mejor_g[estado_sucesor]:
                mejor_g[estado_sucesor] = g_sucesor

                nodo_sucesor = NodoAStar(
                    tablero=tablero_sucesor,
                    g=g_sucesor,
                    h=h_sucesor,
                    padre=nodo_actual,
                    movimiento=movimiento,
                    contador=contador_nodos
                )

                contador_nodos += 1
                nodos_generados += 1

                heapq.heappush(cola_abierta, (nodo_sucesor.f, nodo_sucesor.contador, nodo_sucesor))

    print(f"\n  No se encontró solución en {nodos_expandidos} expansiones")
    return None, None, nodos_expandidos, nodos_generados