import pygame

class Bala():
    def __init__(self):
        self.img = pygame.image.load("images/bala.png")
        self.x = 2000
        self.y = 2000
        self.x_cambio = 0
        self.y_cambio = 20
        global bala_visible
        self.bala_visible = False
        
    def disparar(self, pantalla):
        global bala_visible 
        self.bala_visible = True
        pantalla.blit(self.img, (self.x + 16, self.y + 10))
        
    def print(self, pantalla, jugador_x):
        if self.y <= -64:
            self.y = 530
            self.x = jugador_x
            self.bala_visible = False
        if self.bala_visible:
            self.disparar(pantalla)
            self.y -= self.y_cambio