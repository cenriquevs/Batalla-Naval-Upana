import random


class Player:
    """Representa a cualquier jugador que pueda jugar."""
    def __init__(self):
        """ Inicializa la clase Player.
        """
        self.score = []  # Realiza un seguimiento de los acorazados que han sido alcanzados.
        self.placements = [[], [], [], [], [], [], [], [], [], []]  # [x] [y] Acorazado de la computadora en formato de cuadrícula
        for i in range(10):
            for j in range(10):
                self.placements[i].append(0)
        self.battleship_set = []  # El acorazado de la computadora en formato (start_x, start_y, end_x, end_y, length)
        self.selection_history = []  # Realiza un seguimiento de la selección de la computadora para evitar repeticiones.

    def get_total_score(self):        
        """
        Suma la puntuación total obtenida por el Jugador.
         Input variables:
             self: el objeto Player
         Returns:
             total (entero): suma de la puntuación
        """
        total = 0
        for ship_length in range(len(self.score)):
            total += ship_length

        return total

    def avoid_plots(self, plot_list):
        """
        Agrega una trama al historial de selección del jugador para evitar adivinar en ubicaciones no válidas.
         Esta función se llama cuando se golpea un acorazado. plot_list constará de la
         parcelas restantes del acorazado.
         Input variables:
             plot_list: una lista de tuplas en formato (x, y) que representan gráficos que deben evitarse.
         Returns:
             Ninguno
        """
        for plot in plot_list:
            self.selection_history.append(plot)

    def valid_location(self, grid, x, y, ship_len, ship_orientation):
        """
        Determina si el barco con longitud ship_len y orientación ship_orientation se puede colocar en la cuadrícula en x, y.
         Input variables:
             grid: una matriz doble que representa el tablero
             x: número entero que representa x la ubicación de la cabeza del acorazado
             y: número entero que representa la ubicación y de la cabeza del acorazado
             ship_len: la longitud del acorazado
             ship_orientation: será 0 si es horizontal, 1 si es vertical
         Returns:
             Bool: 1 si es válido, 0 si no es válido
        """
        if ship_orientation == 0:  # Nave horizontal
            for column in grid[x: x + ship_len]:
                if column[y] == 1:
                    return 0
        else:  # Nave vertical, x es constante
            for row in range(y-ship_len + 1, y+1):
                if grid[x][row] == 1:
                    return 0
        return 1

    def update_internal_board(self, grid, x, y, ship_len, ship_orientation):
        """
        Una vez que se determine que la ubicación es válida, actualizaremos la cuadrícula para que contenga el acorazado recién colocado.
         Input variable:
             grid: una matriz doble que representa el tablero
             x: número entero que representa x la ubicación de la cabeza del acorazado
             y: número entero que representa la ubicación y de la cabeza del acorazado
             ship_len: la longitud del acorazado
             ship_orientation: será 0 si es horizontal, 1 si es vertical
         Returns:
             nulo(null)
        """
        if ship_orientation == 0:  # Nave horizontal
            for column in grid[x: x + ship_len]:
                column[y] = 1
        else:  # Nave vertical, x es constante
            for row in range(y-ship_len + 1, y + 1):
                grid[x][row] = 1

