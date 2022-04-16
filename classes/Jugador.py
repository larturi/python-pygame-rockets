import pygame

class Jugador():
    def __init__(self):
        self.img = pygame.image.load("images/cohete.png")
        self.x = 368
        self.y = 530
        self.x_cambio = 0
        self.velocidad = 7
        
    def print(self, pantalla):
        pantalla.blit(self.img, (self.x, self.y))

