import random
import pygame

class Enemigo():
    def __init__(self):
        self.img = pygame.image.load("images/enemigo.png")
        self.x = random.randint(0, 736)
        self.y = random.randint(50, 150)
        self.x_cambio = 3
        self.y_cambio = 50
        self.velocidad = 6
        
    def print(self, pantalla):
        pantalla.blit(self.img, (self.x, self.y))
        