'''
En este tablero, lo que hace es definir como se va a representar el tablero en el peg 
solitaire, como el enunciado nos pide representar la estrutura del tablero, aquí es donde 
se hará. 
También se modela el estado del juego, indicando cuales celdas tienen una ficha, cuales están
vacías y cuales no son parte del tablero. 

Relación con otros módulos:
- movimientos.py: Utiliza el estado del tablero para calcular movimientos válidos
- heuristica.py: Utiliza el estado del tablero para calcular heurísticas
- astar.py: El algoritmo A* trabaja con instancias de tablero
- main.py: Crea el tablero inicial y lo pasa al algoritmo
'''


class Tablero:
    """
    Clase que representa el tablero del juego .
    
    El tablero es de 7x7 con forma de cruz. Las celdas pueden ser:
    - 1: Posición con ficha
    - 0: Posición vacía
    - -1: Posición que no es parte del tablero (fuera de la forma de cruz)
    
    Atributos:
        tamaño (int): Dimensión del tablero 7x7
        estado (list): Matriz que representa el estado del tablero
    """
    
    def __init__(self, tamaño=7):
        """
        Inicializa el tablero.
        
        Args:
            tamaño (int): Tamaño del tablero
        """
        self.tamaño = tamaño
        self.estado = []
        self.inicializar()
    
    def _es_posicion_valida(self, fila, col):
        """
        Verifica si una posición es parte del tablero.
        
        Según lo que se buscó en internet, el tablero clasico de Peg Solitaire tiene esta forma de cruz:
        ```
              O  O  O         
              O  O  O         
        O  O  O  O  O  O  O   
        O  O  O  -  O  O  O   
        O  O  O  O  O  O  O 
              O  O  O          
              O  O  O         
        ```
        
        Parametros:
            fila (int): Fila de la posición
            col (int): Columna de la posición
            
        Retorna:
            bool: True si la posición es parte del tablero, False sino
        """
        # Primero se calcula dónde está el centro del tablero.
        # Como el tablero es de 7x7, el centro queda en la posición 3.
        centro = self.tamaño // 2

        # En las primeras filas de arriba (0 y 1), no toda la fila pertenece al tablero.
        # Solo se usan las columnas del centro, para formar la parte superior de la cruz.
        if fila < centro - 1:
            return col >= centro - 1 and col <= centro + 1

        # Esta fila ya forma parte del ancho completo de la cruz,
        # por eso cualquier columna en esta fila es válida.
        if fila == centro - 1:
            return True

        # Estas son las filas centrales del tablero,
        # entonces aquí también todas las columnas son válidas.
        if fila == centro or fila == centro + 1:
            return True

        # Ya en la parte de abajo, la cruz se vuelve a cerrar,
        # así que solo se permiten las columnas del centro.
        if fila == centro + 2:
            return col >= centro - 1 and col <= centro + 1

        # Última fila de abajo: igual que arriba,
        # solo se usan las columnas del centro para mantener la forma de cruz.
        if fila == centro + 3:
            return col >= centro - 1 and col <= centro + 1

        # Si no cumple ninguno de los casos anteriores,
        # significa que esa posición no pertenece al tablero.
        return False
    
    def inicializar(self):
        """
        Inicializa el tablero con la configuración inicial del juego.
        - Todas las posiciones válidas tienen fichas (1)
        - La posición central está vacía (0)
        - Las posiciones inválidas están marcadas como -1
        """
        self.estado = []
        for fila in range(self.tamaño):
            fila_datos = []
            for col in range(self.tamaño):
                if not self._es_posicion_valida(fila, col):
                    # Posición no válida (fuera de la cruz)
                    fila_datos.append(-1)
                else:
                    # Posición válida
                    centro = self.tamaño // 2
                    if fila == centro and col == centro:
                        # Centro vacío al inicio
                        fila_datos.append(0)
                    else:
                        # Posición con ficha
                        fila_datos.append(1)
            self.estado.append(fila_datos)
    
    def copiar(self):
        """
        Retorna una copia del tablero actual.
        
        Esto es importante para que movimientos.py pueda crear nuevos estados
        sin modificar el original.
        
        """
        nuevo_tablero = Tablero(self.tamaño)
        nuevo_tablero.estado = [fila[:] for fila in self.estado]
        return nuevo_tablero
    
    def es_objetivo(self):
        """
        El objetivo correcto es:
        - que quede exactamente 1 ficha
        - y que esté en el centro del tablero
        """
        centro = self.tamaño // 2
        return self.contar_fichas() == 1 and self.estado[centro][centro] == 1
    
    def contar_fichas(self):
        """
        Cuenta el número total de fichas en el tablero.
        Utilizado por heuristica.py para calcular heurísticas.
        
        Retorna:
            int: Número de fichas en el tablero
        """
        return sum(row.count(1) for row in self.estado)
    
    def __str__(self):
        """
        Representación en string del tablero para mostrar en consola.
        
        Símbolos:
        - "O": Posición con ficha
        - "-": Posición vacía
        - " ": Posición no válida 
        
        """
        lineas = []
        for fila in self.estado:
            linea = ""
            for celda in fila:
                if celda == -1:
                    linea += "   "  # Espacio para posiciones inválidas
                elif celda == 1:
                    linea += " O "  # Ficha
                else:
                    linea += " - "  # Posición vacía
            lineas.append(linea)
        return "\n".join(lineas)
    
    def __eq__(self, otro):
        """
        Compara dos tableros para verificar si son idénticos.
        Utilizado por astar.py para evitar explorar estados duplicados.
        
        Args:
            otro (Tablero): Otro tablero a comparar
            
        Retorna:
            bool: True si ambos tableros son idénticos
        """
        if not isinstance(otro, Tablero):
            return False
        return self.estado == otro.estado

    def a_tupla(self):
        """
        Convierte el tablero a una tupla de tuplas para que sea hashable.
        """
        return tuple(tuple(fila) for fila in self.estado)
    
    def __hash__(self):
        """
        Retorna un hash del estado del tablero.
        Permite usar el tablero como clave en diccionarios (conjunto cerrado en astar.py).
        
        Returns:
            int: Hash del estado actual del tablero
        """
        return hash(self.a_tupla())