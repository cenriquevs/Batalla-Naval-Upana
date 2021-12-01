import pygame
from pygame import transform
from AutomaticPlayer import*
from VisibleBoard import*
from PersonPlayer import*
from Stats import*
import time
import random

scrren = pygame.display.set_mode([1000, 500])
fondo = pygame.display.set_mode([0,0])

bg = pygame.image.load("img/fondop.jpg")
bg = transform.scale(bg,(1000,500))
bg2 = pygame.image.load("img/pixel.png")
bg2 = transform.scale(bg2,(1000,500))

FPS = 30
HEIGHT = 1000
WIDTH = 500
P_SHIPS = []
BORDER_WIDTH = 235
BORDER_HEIGHT = 35
REQ_SHIP_SIZE = 40
MAX_SCORE = 5
MOUSE_POS_X = 430
MOUSE_POS_Y = 130
RESTRICT_X = 775
RESTRICT_Y = 475
MARGIN = 5
SIZE = 30


class Start(pygame.sprite.Sprite):
    """
    Start (controller) utiliza todos los \
     clases de objetos del juego.
     NOTA: Esto sigue los protocolos de diseño de la arquitectura MVC.
     ya que esta clase también representa la parte de la vista y el controlador de MVC.
    
    """

    def __init__(self, auto, person, stats, vboard, vb_auto, vb_player, p_ships):
        """
        Inicializa la clase de inicio con.
         auto: representa el aspecto informático (ai) del juego.
         person: representa el aspecto de jugador humano del juego.
         stats: representa el estado del juego.
         vboard: representa el tablero visual que se muestra en la pantalla.
         vb_auto: representa la placa de las computadoras (ai).
         vb_player: representa el bpoard del jugador humano.
         p_ships: una lista de las coordenadas de los barcos para que la computadora adivine.
        """

        logo = pygame.image.load("img/Battleship.png")
        logo = transform.scale(logo,[450, 70]) 
        scrren.blit(logo,[200, 15]) 

        super(Start, self).__init__()
        self.auto = auto
        self.stats = stats
        self.person = person
        self.vboard = vboard
        self.vb_auto = vb_auto
        self.vb_player = vb_player
        self.win = (False, "")
        self.player1_score = 0 #El jugador humano es el jugador 1
        self.player2_score = 0 #la computadora es el jugador 2
        self.turns = 0 #0 significa que el jugador humano es el turno de jugar, 1 significa que es el turno de las computadoras.
        self.p_ships = p_ships #una lista de barcos
        self.guesses = 0
        

    def set_auto_ships(self):
        """ Coloca las naves en coordenadas válidas 
        para que el jugador humano las adivine.
        """
        ships = self.auto.set_battleships()
        for enemy_ships in ships:
                self.vb_auto.add_ship(enemy_ships[0], enemy_ships[1],\
                                     enemy_ships[2], enemy_ships[3], enemy_ships[4])

    def set_person_ships(self):
        """ Coloca las naves en coordenadas válidas para 
        que el jugador de la computadora las adivine.
        NOTE: Esto se basa en la lista de barcos P_SHIPS 
        que eligió el jugador humano.
        """
        ships = self.p_ships
        for person_ships in ships:
                self.vb_player.add_ship(person_ships[0], person_ships[1],\
                                     person_ships[2], person_ships[3], person_ships[4])
          
                
    def play_ai(self):
        """Permita que el jugador de la computadora pueda adivinar 
        la nave del jugador humano en posiciones válidas, 
        asegurándose de que las mismas coordenadas se elijan 
        solo una vez.
        """
        #time.sleep(0.5)
        pos = self.auto.guess_location()
        no_go = self.update(self.vb_player, pos[0], pos[1])
        if no_go == None:
            no_go = []
        if no_go != []:
            self.player2_score = self.player2_score + 1
        self.auto.avoid_plots(no_go)
        
    def update(self, obj, coord_x, coord_y):
        """actualiza la pantalla basándose en conjeturas hechas 
        por el jugador humano o el jugador de la computadora

         -obj: representa un objeto que puede ser un jugador humano 
         o el jugador de la computadora.
         -coord_x: coordenada de la fila
         -coor_y: coordenada de la columna

         devuelve los movimientos realizados.
        """
        no_go = obj.viewable_move(coord_x, coord_y)
        return no_go
                
        
    def display_score(self):
        """Muestra la puntuación del jugador humano y 
        del jugador de la computadora.
        """
        font = pygame.font.SysFont(""'couriernew'"", 19) #mensajero nuevo
        #font.set_bold(True)
        mess_1 = "Puntuación del jugador: {}".format(self.player1_score)#Puntuación del jugador
        mess_2 = "Puntuacion computadora: {}".format(self.player2_score)#Puntaje de computadora
        txt1 = font.render(mess_1, True, (0,0,0))
        txt2 = font.render(mess_2, True, (0, 0, 0)) 
        self.vboard.blit(txt1, (38, 100))
        self.vboard.blit(txt2, (430, 100))

#ESTADISTICAS DEL 2DO ESCENARIO

    def display_stats(self):
        """Muestre la información importante sobre ambos jugadores:
         1) Barcos restantes
         2) Número de conjeturas
         4) Puntajes de ambos jugadores cuando un barco es impactado.
        """
        font = pygame.font.SysFont("agencyfb", 25)
        mess_1 = "Barcos restantes: "
        mess_2 = "Número de intentos: {}".format(self.guesses)
        txt1 = font.render(mess_1, True, (255, 197, 8))
        txt2 = font.render(mess_2, True, (0,0,0))
        play_score_msg2 = font.render("Jugador: {}  Computadora: {}".format(MAX_SCORE - self.player1_score, MAX_SCORE - self.player2_score), True, (0,0,0))
        self.vboard.blit(txt1, (810, 240))
        self.vboard.blit(txt2, (780, 315))
        self.vboard.blit(play_score_msg2, (780, 265))

    def quit(self):
        """Para salir del juego.
        """
        pygame.quit()
        sys.exit()

class Begin:
    """ Begin representa la pantalla de bienvenida, 
    donde el jugador humano puede esconder barcos 
    del jugador de la computadora.
    """

    def __init__(self, player_board, user_board, person):
        """ Initializes the begin class with:
        player_board: represents the visual part from Start class.
        person: represents the human player from Start class.
        user_board: represents the visual board from Start class.
        """
        self.player_board = player_board
        self.user_board = user_board
        self.person = person
        self.required_ships = [5, 4, 3, 2, 1] #numbers of ships(5 ships) needed to play the game.
        self.num_set_ships = 0

    def show_required(self, color, index):
        """
         Muestra las naves necesarias para que el jugador humano 
         las oculte.
         color: para resaltar qué barco se está utilizando. En este caso
         el color es rojo.
         index: el conjunto de barcos necesarios.
        """
        x = 5
        for row in range(5):
            for column in range(x):
                if index == x:
                    pygame.draw.rect(self.player_board,
                                 color,
                                 pygame.Rect(800+(REQ_SHIP_SIZE * column), 200+(REQ_SHIP_SIZE * row), 30, 30))
                else:
                    pygame.draw.rect(self.player_board,
                                     WHITE,
                                     pygame.Rect(800+(REQ_SHIP_SIZE * column), 200+(REQ_SHIP_SIZE * row), 30, 30))
            x -= 1
            
    def set_player_ships(self, x_head, y_head, battleship_length):
        """ Configure los barcos del jugador en coordenadas válidas 
        para que el jugador de la computadora adivine.
         x_head: posición de la columna
         y_head: posición de la fila
         battleship_length: eslora del barco. por ejemplo, 5
                            si el barco tiene una eslora de 5.
        """
        person = self.person.set_battleship(x_head, y_head, battleship_length)
        if(len(person) > 0):
            person_ships = person[-1]
            self.user_board.add_ship(person_ships[0], person_ships[1],\
                                         person_ships[2], person_ships[3], person_ships[4])
            P_SHIPS.append((person_ships[0], person_ships[1],\
                                         person_ships[2], person_ships[3], person_ships[4]))

    
    def display_info(self):
        """ Muestre lo que debe hacer el jugador humano.
        """
        title = pygame.font.SysFont("ocraextended", 40)
        font = pygame.font.SysFont("'couriernew'", 19)
        font.set_bold(True)
        main_title = title.render("", True, (BLUE),)
        #COLOCAMOS LA IMAGEN 
        logo = pygame.image.load("img/Battleship.png")
        instruc = font.render("Instrucciones", True, (50, 21, 153))
        #AJUSTAMOS MARGENES
        logo = transform.scale(logo,[450, 100]) 
        instruc = transform.scale(instruc,[230, 80]) 
        scrren.blit(logo,[370, 20]) 
        scrren.blit(instruc,[100,120])

        self.player_board.blit(main_title, (450, 20))
        txt1 = font.render("1. Elige la posición del barco", True, (0,0,0))
        txt2 = font.render("  (pon el cursor encima de un ", True, (0,0,0))
        txt3 = font.render("   cuadro y presiona cualquier", True, (0,0,0))
        txt4 = font.render("   tecla para selecionarlo)", True, (0,0,0))
        txt5 = font.render("2. Presiona enter para iniciar ", True, (0,0,0))

        self.player_board.blit(txt1, (20, 220))
        self.player_board.blit(txt2, (25, 237))
        self.player_board.blit(txt3, (25, 256))
        self.player_board.blit(txt4, (25, 278))
        self.player_board.blit(txt5, (20, 320))
        font = pygame.font.SysFont("couriernew", 17)
        mess_1 = "Barcos requeridos"
        font.set_bold(True)
        txt1 = font.render(mess_1, True, (0, 0, 0))
        self.player_board.blit(txt1, (805, 162))
        
        

    def update(self, human_player, coord_x, coord_y):
        """
        actualiza la pantalla basándose únicamente en 
        adivinanzas realizadas por el jugador humano.

        human_player: representa el objeto del jugador humano.
         coord_x: coordenada de la fila
         coor_y: coordenada de la columna
        """
        human_player.viewable_move(coord_x, coord_y)

#PRIMER ESCENARIO


def main():      
    pygame.init() 
    DISPLAY=pygame.display.set_mode((1000,500),0,32)
    scrren.blit(bg,[0,0])
    pygame.display.set_caption("Batalla naval Upana")
    user_board = VisibleUserBoard(DISPLAY)
    person = PersonPlayer()

    begin = Begin(DISPLAY, user_board, person)
    begin.display_info()
    begin.show_required(WHITE, 0)

    begin.num_set_ships = 0 #numbers of battleship bricks can not be more than 15
    def mouse_event(event, start, size):
        """Maneja los eventos del mouse y garantiza que los clics 
        del mouse solo funcionen en las coordenadas de la cuadrícula.
         start: el objeto o la pantalla actual.
         size: tamaño de una sola coordenada de ladrillo.
        """

        if event.type == pygame.KEYDOWN:
            mouse_pos = pygame.mouse.get_pos()
            #Aca es donde se respeta el limite de seleccion del barco
            if MOUSE_POS_X <= mouse_pos[0] <= RESTRICT_X and MOUSE_POS_Y <= mouse_pos[1] <= RESTRICT_Y:
                col = mouse_pos[0] - MOUSE_POS_X
                rw = mouse_pos[1] - MOUSE_POS_Y
                column = col // (size + MARGIN)
                row = rw // (size + MARGIN)
                
                pygame.mixer.Channel(1).play(pygame.mixer.Sound('audios/mjm.wav'))
                if len(begin.required_ships) > 0:
                    #Muestra los barcos marcado
                    begin.set_player_ships(column, row, begin.required_ships[0])
                    popped_val = begin.required_ships.pop(0)
                    begin.show_required(RED, popped_val)
                    begin.num_set_ships += 1
                
    pygame.mixer.music.load('audios/look.wav')
    pygame.mixer.music.set_volume(0.10)
    pygame.mixer.music.play()
    
    #Aqui muestra la ventana
    run = True
    while run:
        for event in pygame.event.get():
            if event.type==QUIT:
                pygame.quit()
                sys.exit()
                #aca es donde se presiona la tecla y continua a otro escenario
            if event.type == pygame.KEYDOWN and begin.num_set_ships >= 5:
                run = False

            n_event = mouse_event(event, begin, 30) #Mandamos a llamar el evento
        pygame.display.update()
    
    

if __name__ == '__main__':
    def mouse_event(mouse_pos, start):
        """Maneja los eventos del mouse y garantiza que los 
        clics del mouse solo funcionen en las coordenadas 
        de la cuadrícula.
        start: el objeto o la pantalla actual.
        """

        if REQ_SHIP_SIZE <= mouse_pos[0] <= (RESTRICT_X - 390) and MOUSE_POS_Y <= mouse_pos[1] <= RESTRICT_Y:
            col = mouse_pos[0] - REQ_SHIP_SIZE
            rw = mouse_pos[1] - MOUSE_POS_Y
            column = col // (SIZE + MARGIN)
            row = rw // (SIZE + MARGIN)
            no_go = start.update(start.vb_auto, column, row)
            if no_go != None and no_go != []:
                start.player1_score = start.player1_score + 1
            pygame.mixer.Channel(1).play(pygame.mixer.Sound('audios/tiro.wav'))
            pygame.mixer.music.set_volume(0.10)#Aquí audio de vamooos sigue perro.
            start.guesses += 1
            start.turns = 1
            
    stats = Stats()
    auto = AutomaticPlayer()
    person = PersonPlayer()
    main()
    
    pygame.init()
    pygame.mixer.init()
    clock = pygame.time.Clock()
    DISPLAY=pygame.display
    main_board = DISPLAY.set_mode((HEIGHT, WIDTH),0,32)
#escenario 2-----------*-*-*-*-*-*-*-*-*-*-*-**-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*



    scrren.blit(bg2,[0,0])
    DISPLAY.set_caption("Batalla Naval Upana")
    user_board = VisibleUserBoard(main_board)
    enemy_board = VisibleEnemyBoard(main_board)
    start = Start(auto, person, stats, main_board, enemy_board, user_board, P_SHIPS);
    start.set_auto_ships()
    start.set_person_ships()
    #ya en el tablero jajaja
    pygame.mixer.music.set_endevent(pygame.constants.USEREVENT)
    pygame.mixer.music.play()
    win = 0 #end game if equal to 1

    running = True
    while running:
        #events handler
        for event in pygame.event.get():
            start.display_score()
            start.display_stats()
            if event.type==QUIT:
                start.quit()
            if win == 0:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    if start.turns == 0:
                        m_event = mouse_event(mouse_pos, start)
                        if start.vb_auto.all_ships_sunk():
                            pygame.draw.rect(start.vboard,BLACK,
                            pygame.Rect(300, 98, 16, 20))

                            pygame.draw.rect(start.vboard,BLACK,
                            pygame.Rect(692, 98, 16, 20))

                            pygame.draw.rect(start.vboard, BLACK,
                            pygame.Rect(780, 270, 218, 27))
                        

                            start.display_score()
                            start.display_stats()
                            texto_intro = pygame.font.SysFont('console', 30, True)
                            reintentar = texto_intro.render('Presione R para volver al juego...', 1, (255,255,255))
                            title = pygame.font.SysFont("'couriernew'", 60)
                            title.set_bold(True)
                            main_title = title.render("¡GANASTE!", True, (181,230,29))
                            main_board.blit(main_title, (250, 250))
                            time.sleep(0.9)
                            pygame.mixer.Channel(1).play(pygame.mixer.Sound('audios/ganaste.wav'))
                            pygame.mixer.music.set_volume(0.1)
                            start.display_score()
                            start.display_stats()
                            win = 1
                            
                        pygame.draw.rect(start.vboard,BLACK,
                        pygame.Rect(937, 316, 29, 25))  

                    if True:
                        start.play_ai()
                        
                        if start.vb_player.all_ships_sunk():
                            #Igual aqui se delinean las estadisticas
                            pygame.draw.rect(start.vboard,BLACK,
                            pygame.Rect(300, 98, 16, 20))

                            pygame.draw.rect(start.vboard,BLACK,
                            pygame.Rect(692, 98, 16, 20))

                            pygame.draw.rect(start.vboard, BLACK,
                            pygame.Rect(780, 270, 218, 27))
                        
                            start.display_score()
                            start.display_stats()
                            title = pygame.font.SysFont("'couriernew'", 60)
                            title.set_bold(True)
                            main_title = title.render("¡PERDISTE!", True, (255,0,0))
                            main_board.blit(main_title, (250, 250))
                            time.sleep(0.9)
                            pygame.mixer.Channel(1).play(pygame.mixer.Sound('audios/perdiste.wav'))
                            pygame.mixer.music.set_volume(0.1)
                            start.display_score()
                            start.display_stats()
                            win = 1
                           
                        pygame.draw.rect(start.vboard,BLACK,
                            pygame.Rect(937, 316, 29, 25))
                        
                        start.turns = 0

                    if (win == 0):
                        '''#MI PANA FACHERITOOOO, PARA DIBUJAR UNA FIGURA
                        #LOS PARAMETROS SON LOS SIGUIENTES JEJEJE
                        #EJES X, Y (osea la posicion), seguido por el tamaño de la figura.

                        #Lo que hacemos aqui vos mano, es delinear asi como hacen las morras XD las
                        #estadisticas en tiempo real tanto como el jugador y la IA'''

                        pygame.draw.rect(start.vboard,BLACK,
                        pygame.Rect(300, 98, 16, 20))

                        pygame.draw.rect(start.vboard,BLACK,
                        pygame.Rect(692, 98, 16, 20))

                        pygame.draw.rect(start.vboard, BLACK,
                            pygame.Rect(780, 270, 218, 27))
                
        pygame.display.flip()
        clock.tick(FPS) #establecer el límite de fps en 30 fotogramas / seg.