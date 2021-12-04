from pygame import *
import sys
import pygame
from pygame.locals import*

init()
pantalla = display.set_mode((1000,500))
pestañol = image.load("img/creditos.jpg")
pestañol = transform.scale(pestañol,(1000,500))

#Musicon Perez
pygame.mixer.music.load('audios/output.wav')
pygame.mixer.music.play()

#Fuentes de letra
font2 = pygame.font.SysFont(""'Georgia'"",25)
font = pygame.font.SysFont(""'System'"", 35)
font.set_bold(True)

txt1 = font.render("Logic Developers", True, (255,255,255),(0,0,0))
txt2 = font.render("Design Developers", True, (255,255,255),(0,0,0))

name1 = font2.render("Carlos Velásquez",True,(0,0,0),(219, 182, 127))
name2 = font2.render("Jeremy García",True,(0,0,0),(219, 182, 127))
name3 = font2.render("Jesús López",True,(0,0,0),(219, 182, 127))
name4 = font2.render("Ana Chang",True,(0,0,0),(219, 182, 127))
name5 = font2.render("Kendy Mora ",True,(0,0,0),(219, 182, 127))

#skins
skin_cevs = image.load('img/skin_cevs.jpg')
skin_cevs = transform.scale(skin_cevs,(90,90))

skin_jeremy = image.load('img/skin_jeremy.jpg')
skin_jeremy = transform.scale(skin_jeremy,(90,90))

skin_chuz = image.load('img/skin_chuz.jpg')
skin_chuz = transform.scale(skin_chuz,(90,90))

skin_anita = image.load('img/skin_ana.jpg')
skin_anita = transform.scale(skin_anita,(90,90))

skin_kendy = image.load('img/skin_kendy.jpg')
skin_kendy = transform.scale(skin_kendy,(90,90))

icono=pygame.image.load("img/icono.png")
pygame.display.set_icon(icono)

def setTitle(title):
    pygame.display.set_caption(title)
setTitle("Creditos")

while True:
    pantalla.fill((255,255,255))
    for e in event.get():
        if e.type == QUIT: sys.exit()
    pantalla.blit(pestañol,(0,0))
    #titulos
    pantalla.blit(txt1, (75, 110))
    pantalla.blit(txt2, (675, 150))

    #nombres
    pantalla.blit(name1,(130,190))
    pantalla.blit(name2,(130,300))
    pantalla.blit(name3,(130,410))
    pantalla.blit(name4,(665,230))
    pantalla.blit(name5,(665,360))

    pantalla.blit(skin_cevs,(25,160))
    pantalla.blit(skin_jeremy,(25,270))
    pantalla.blit(skin_chuz,(25,380))
    pantalla.blit(skin_anita,(560,200))
    pantalla.blit(skin_kendy,(560,330))
    display.flip()

#Derechos reservados por: @Cevs
