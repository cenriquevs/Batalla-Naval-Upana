
from Player import Player
from Tablon import Tablon

"""
Las estadísticas de la clase se utilizan para mostrar las 
estadísticas del juego. Muestra el número total de
acorazados, el número total de acorazados restantes en el 
juego y la puntuación del jugador.
"""
class Estadísticas():
    def __init__(self):
        """
        Inicializa la clase Stats.
        """
        self.score = 0
        self.number_of_ships = 0
        self.remaining_ships = 0

    def score(self):
        """
        Establece la puntuación a la puntuación del jugador
        """
        self.score = Player.get_total_score()
        return self.score

    def number_of_ships(self):
        """
        Establece number_of_ships en el número total de barcos 
        en el juego que el jugador tiene que adivinar
        """
        self.number_of_ships = Tablon.number_of_ships
        return self.number_of_ships

    def remaining_ships(self):
        """
        Establece los remaining_ships en el número total de
        barcos que quedan en el juego para que el jugador adivine
        """
        self.remaining_ships = Tablon.number_of_ships
        if Tablon.all_ships_sunk():
            self.remaining_ships = self.remaining_ships - 1
        return self.remaining_ships


        
        

    

    
        
        
