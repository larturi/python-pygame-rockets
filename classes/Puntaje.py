import pygame

class Puntaje():
    def __init__(self):
        self.puntos = 0
        self.fuente = pygame.font.Font("freesansbold.ttf", 28)
        self.x = 10
        self.y = 10
        
    def mostrar_puntaje(self, pantalla):
        texto = self.fuente.render(f"Puntaje: {str(self.puntos)}", True, (255, 255, 255))
        pantalla.blit(texto, (self.x, self.y))  