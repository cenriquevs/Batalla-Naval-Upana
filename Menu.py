import pygame, sys
from pygame import *
import sys
import os

pygame.init()

ancho,alto = 1000,500 
pantalla = pygame.display.set_mode((ancho,alto))
pygame.display.set_caption("Batalla Naval Upana")

intoF = image.load('img/creditos.png')
intoF = transform.scale(intoF,(120,110))

goJ = image.load('img/go.png')
goJ = transform.scale(goJ,(120,100))

onmouse= (247, 244, 116)
hover= (73, 198, 214)

def fuction_boton(pantalla,boton,texto):
        if boton.collidepoint(mouse.get_pos()):
            pygame.draw.rect(pantalla,hover,(boton))
       
        else:
            pygame.draw.rect(pantalla,onmouse,(boton))
        texto=fuentesdeOrtiz.render(texto, True, (0,0,0))
        pantalla.blit(texto,(boton))

fondo=pygame.image.load("img/fondo2.jpg")
fondo = transform.scale(fondo,(1000,500))
pantalla.blit(fondo, (0,0)) 

Jugar = pygame.draw.rect(pantalla, onmouse,(360, 225, 140,90))
salir= pygame.draw.rect(pantalla, onmouse,(520, 225, 140,90))

fuentesdeOrtiz= font.SysFont("couriernew",25)
fuentesdeOrtiz.set_bold(True)
texto=fuentesdeOrtiz.render("Jugar", 0,(0,0,0))

icono=pygame.image.load("img/icono.png")
pygame.display.set_icon(icono)

while True:
    for event in pygame.event.get():
        if event.type == QUIT: sys.exit()
        if event.type== MOUSEBUTTONDOWN and event.button==1:
            if Jugar.collidepoint(mouse.get_pos()):                                       
                pygame.quit()
                os.system("python Mainjuego.py")                 
                 
            if salir.collidepoint(mouse.get_pos()): 
                pygame.quit()                  
                os.system("python creditos.py")                         
              
    fuction_boton(pantalla,Jugar,None)
    pantalla.blit(goJ,(370,215))
    fuction_boton(pantalla,salir,None)
    pantalla.blit(intoF,(530,215))
    display.flip()   

    pygame.display.update()

#Derechos reservados por: @Cevs