import random
import pygame
import math
from pygame import mixer

from classes.Jugador import Jugador
from classes.Enemigo import Enemigo
from classes.Bala import Bala
from classes.Puntaje import Puntaje

class Game():
    def __init__(self):
            
        # Inicializar PyGame
        pygame.init()

        # Crear la pantala
        self.pantalla = pygame.display.set_mode((800, 600))

        # Titulo & Icono
        pygame.display.set_caption("Invasión espacial")
        icon = pygame.image.load("images/icon.png")
        pygame.display.set_icon(icon)
        self.fondo = pygame.image.load("images/fondo.jpg")

        # Musica
        mixer.music.load("sounds/MusicaFondo.mp3")
        mixer.music.set_volume(0.3)
        mixer.music.play(-1)
        
        # Puntaje
        self.puntaje = Puntaje()

        # Jugador
        self.jugador = Jugador()

        # Enemigos
        self.cantidad_enemigos = 6
        self.enemigos = []
        
        for i in range(self.cantidad_enemigos):
            self.enemigos.append(Enemigo())
            
        # Bala
        self.bala = Bala()

        # Mensaje final
        self.fuente_final = pygame.font.Font("freesansbold.ttf", 60)
        self.fuente_final_help = pygame.font.Font("freesansbold.ttf", 24)

        # Puntaje
        self.puntaje.mostrar_puntaje(self.pantalla)  
            
        # Loop principal
        self.loop()
        
        
    def texto_final(self):
        mi_fuente_final = self.fuente_final.render("JUEGO TERMINADO", True, (255, 255, 255))
        self.pantalla.blit(mi_fuente_final, (110, 250))
        mi_fuente_final_help = self.fuente_final_help.render("ENTER PARA COMENZAR DE NUEVO", True, (255, 255, 255))
        self.pantalla.blit(mi_fuente_final_help, (190, 330))
        
        
    def hay_colision(self, x1, y1, x2, y2):
        distancia = math.sqrt(math.pow(x2 - x1, 2) + math.pow(y2 - y1, 2))
        if distancia < 27:
            return True
        else:
            return False  
        
        
    def loop(self):
        playing = True
        terminado = False

        while playing:
            self.pantalla.blit(self.fondo, (0, 0))
                
            # Evento cerrar ventana
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    playing = False
                    pygame.quit()
                    
                 # Evento presionar teclas
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT and not terminado:
                        self.jugador.x_cambio = -self.jugador.velocidad
                    if event.key == pygame.K_RIGHT and not terminado:
                        self.jugador.x_cambio = self.jugador.velocidad
                    if event.key == pygame.K_SPACE and not terminado:
                        sonido_bala = mixer.Sound("sounds/disparo.mp3")
                        if self.bala.bala_visible == False:
                            sonido_bala.play()
                        if not self.bala.bala_visible:
                            self.bala.x = self.jugador.x
                            self.bala.disparar(self.pantalla)
                    if event.key == pygame.K_RETURN:
                        Game()
                        
                # Evento soltar teclas        
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                        self.jugador.x_cambio = 0
                        
            # Movimiento jugador
            self.jugador.x += self.jugador.x_cambio
            
            # Movimiento de la bala
            if self.bala.y <= -64:
                self.bala.y = 530
                self.bala.x = self.jugador.x
                self.bala.bala_visible = False
            if self.bala.bala_visible:
                self.bala.disparar(self.pantalla)
                self.bala.y -= self.bala.y_cambio
                
            # Movimiento enemigo
            for enemigo in self.enemigos:
                
                # Fin del juego
                if enemigo.y > 530 or self.hay_colision(enemigo.x, enemigo.y, self.jugador.x, self.jugador.y):
                    self.texto_final()
                    terminado = True
                    break
                else:
                
                    enemigo.x += enemigo.x_cambio
                    
                    # Mantener al enemigo en el rango de la pantalla
                    if enemigo.x <= 0:
                        enemigo.x_cambio = enemigo.velocidad
                        enemigo.y += enemigo.y_cambio
                    elif enemigo.x >= 736:
                        enemigo.x_cambio = -enemigo.velocidad
                        enemigo.y += enemigo.y_cambio
                        
                    # Verifico colision
                    colision = self.hay_colision(enemigo.x, enemigo.y, self.bala.x, self.bala.y)
                    if colision and not terminado:
                        sonido_colision = mixer.Sound("sounds/golpe.mp3")
                        sonido_colision.play()
                        self.bala.y = 530
                        self.bala.bala_visible = False
                        self.puntaje.puntos += 1
                        enemigo.x = random.randint(0, 736)
                        enemigo.y = random.randint(50, 150) 
                                        
            # Puntaje
            self.puntaje.mostrar_puntaje(self.pantalla)
            
            # Jugador
            self.jugador.print(self.pantalla)
            
            # Mantener al jugador en el rango de la pantalla
            if self.jugador.x <= 0:
                self.jugador.x = 0
            elif self.jugador.x >= 736:
                self.jugador.x = 736
            
            # Enemigos
            for enemigo in self.enemigos:
                if not terminado:
                    enemigo.print(self.pantalla)
                
            # Movimiento de la bala
            self.bala.print(self.pantalla, self.jugador.x)
            
            pygame.display.update()
            