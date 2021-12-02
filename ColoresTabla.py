import pygame, sys
from pygame.locals import *
import Tablon

#Colours
WHITE=(255,255,255)
BLUE=(0,0,255)
RED=(138,86,57)
BLACK=(253, 238, 32)
GREY=(128,128,128)


"Un rectángulo es un objeto con ancho(width), alto(height), coordenada-x & coordenada-y."
class Rectangle:
    
    def __init__(self,x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height


'''
Un VisibleBoard es una cuadrícula estándar de 10 * 10 Rectángulos(rectangles) donde el estado de
cada rectángulo(rectanle) tiene un color (por ejemplo, rojo para acertar y azul para fallar).
'''
class VisibleBoard(Tablon.Tablon):
    def __init__(self, startx, starty, display):
        Tablon.Tablon.__init__(self)
        self.rectangles = [[],[],[],[],[],[],[],[],[],[]]

        for i in range(10):
            for j in range(10):
                new_rect = Rectangle(startx + 35 * i,starty + 35 * j,30,30)
                self.rectangles[i].append(new_rect)
        self.display = display


    '''
    Comprueba el estado del rectángulo en (x, y) y cambia el color de forma adecuada.
    '''
    def viewable_move(self, x, y):
        move_return, ans = self.move(x, y)

        if (move_return, ans) == (None, []):
            return ans
        elif (move_return, ans) == (Tablon.MISS, []):
                self.miss(x, y)
                return ans
        else:
            for (xc, yc) in ans:
               self.hit(xc, yc)
            return ans

    '''
    Cambia el color del rectángulo en (x, y) a rojo.
    '''
    def hit(self, x, y):
        if (0 <= x <= 9) and (0 <= y <= 9):
            rect = self.rectangles[x][y]
            pygame.draw.rect(self.display, RED, (rect.x, rect.y, rect.width, rect.height))

    '''
    Cambia el color del rectángulo en (x, y) a azul.
    '''
    def miss(self, x, y):
        if (0 <= x <= 9) and (0 <= y <= 9):
            rect = self.rectangles[x][y]
            pygame.draw.rect(self.display, BLUE, (rect.x, rect.y, rect.width, rect.height))

    '''
    Agrega un barco al VisibleBoard y cambia el color de los 
    Rectángulos de ese barco de forma apropiada.
    '''
    def add_ship(self, startx, starty, endx, endy, size, colour):
        check = self.board_add_ship(startx, starty, endx, endy, size)
        if check != None:
            starting_point_x, ending_point_x, starting_point_y, ending_point_y = check
            for x in range(starting_point_x, ending_point_x + 1):
                for y in range(starting_point_y, ending_point_y + 1):
                    rect = self.rectangles[x][y]
                    pygame.draw.rect(self.display, colour, (rect.x, rect.y, rect.width, rect.height))


'''
Un VisibleEnemyBoard es un VisibleBoard donde los barcos 
se representan como rectángulos blancos.
'''
class VisibleEnemyBoard(VisibleBoard):

    def __init__(self, display):
        VisibleBoard.__init__(self, 40, 130, display)
        for row in self.rectangles:
            for rect in row:
                pygame.draw.rect(self.display, WHITE, (rect.x, rect.y, rect.width, rect.height))

    '''
Agregue un barco con las coordenadas proporcionadas al 
VisibleEnemyBoard. Cada coordenada del barco se representa 
como un Rectángulo blanco.
    '''
    def add_ship(self, startx, starty, endx, endy, size):
        VisibleBoard.add_ship(self, startx, starty, endx, endy, size, WHITE)


'''
Un VisibleUserBoard es un VisibleBoard donde los barcos se representan como rectángulos grises.
'''
class VisibleUserBoard(VisibleBoard):

    def __init__(self, display):
        VisibleBoard.__init__(self, 430, 130, display)
        for row in self.rectangles:
            for rect in row:
                pygame.draw.rect(self.display, WHITE, (rect.x, rect.y, rect.width, rect.height))

    '''
    Agregue un barco con las coordenadas proporcionadas a 
    VisibleUserBoard. Cada coordenada del barco se representa 
    como un Rectángulo gris.
    '''
    def add_ship(self, startx, starty, endx, endy, size):
        VisibleBoard.add_ship(self, startx, starty, endx, endy, size, GREY)
