"""
En este archivo se implementa la heuristica que se utiliza en el algoritmo A*
Esta sirve para estimar que tán lejos se encuentra un estado actual del objetivo
final, ayudando al algoritmo a decidir que nodos va a explorar primero. 

Relación con otros módulos:
- tablero.py: Recibe el estado del tablero para Calcular heurísticas
- astar.py: Utiliza estas funciones para calcular f(n) = g(n) + h(n)
- main.py: Selecciona qué heurística usar para ejecutar A*
"""

import math

def heuristica_contar_fichas(tablero):
    """
    Esta heurística cuenta cuántas fichas faltan por eliminar
    para llegar al objetivo de dejar solo una en el tablero.
    Se calcula como fichas_restantes - 1.
    """
    return tablero.contar_fichas() - 1