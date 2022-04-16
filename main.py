import pygame
import random
import math
from pygame import mixer

def start_game():

    # Inicializar PyGame
    pygame.init()

    # Crear la pantala
    pantalla = pygame.display.set_mode((800, 600))

    # Titulo & Icono
    pygame.display.set_caption("Invasión espacial")
    icon = pygame.image.load("images/icon.png")
    pygame.display.set_icon(icon)
    fondo = pygame.image.load("images/fondo.jpg")

    # Agregar musica
    mixer.music.load("sounds/MusicaFondo.mp3")
    mixer.music.set_volume(0.3)
    mixer.music.play(-1)

    # Puntaje
    puntaje = 0
    fuente = pygame.font.Font("freesansbold.ttf", 28)
    puntaje_x = 10
    puntaje_y = 10

    # Jugador
    jugador_img = pygame.image.load("images/cohete.png")
    jugador_x = 368
    jugador_y = 530
    jugador_x_cambio = 0
    jugador_velocidad = 7

    # Enemigo
    enemigo_img = []
    enemigo_x = []
    enemigo_y = []
    enemigo_x_cambio = []
    enemigo_y_cambio = []
    enemigo_velocidad = []
    cantidad_enemigos = 6

    for i in range(cantidad_enemigos):
        enemigo_img.append(pygame.image.load("images/enemigo.png"))
        enemigo_x.append(random.randint(0, 736))
        enemigo_y.append(random.randint(50, 150))
        enemigo_x_cambio.append(3)
        enemigo_y_cambio.append(50)
        enemigo_velocidad.append(6)

    # Bala
    bala_img = pygame.image.load("images/bala.png")
    bala_x = 0
    bala_y = 530
    bala_x_cambio = 0
    bala_y_cambio = 20
    global bala_visible
    bala_visible = False

    # Mensaje final
    fuente_final = pygame.font.Font("freesansbold.ttf", 60)
    fuente_final_help = pygame.font.Font("freesansbold.ttf", 24)

    def texto_final():
        mi_fuente_final = fuente_final.render("JUEGO TERMINADO", True, (255, 255, 255))
        pantalla.blit(mi_fuente_final, (110, 250))
        mi_fuente_final_help = fuente_final_help.render("ENTER PARA COMENZAR DE NUEVO", True, (255, 255, 255))
        pantalla.blit(mi_fuente_final_help, (190, 330))

    # Mostrar puntaje
    def mostrar_puntaje(x, y):
        texto = fuente.render(f"Puntaje: {str(puntaje)}", True, (255, 255, 255))
        pantalla.blit(texto, (x, y))

    # Imprime en pantalla el jugador
    def jugador(x, y):
        pantalla.blit(jugador_img, (x, y))
        
    # Imprime en pantalla el enemigo
    def enemigo(x, y, enemigo_numero):
        pantalla.blit(enemigo_img[enemigo_numero], (x, y))
        
    # Imprime en pantalla la bala
    def disparar_bala(x, y):
        global bala_visible 
        bala_visible = True
        pantalla.blit(bala_img, (x + 16, y + 10))
        
    # Detectar colisiones
    def hay_colision(x1, y1, x2, y2):
        distancia = math.sqrt(math.pow(x2 - x1, 2) + math.pow(y2 - y1, 2))
        if distancia < 27:
            return True
        else:
            return False

    # Loop principal
    playing = True
    while playing:
        pantalla.blit(fondo, (0, 0))
            
        # Evento cerrar ventana
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                playing = False
                pygame.quit()
                
            # Evento presionar teclas
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    jugador_x_cambio = -jugador_velocidad
                if event.key == pygame.K_RIGHT:
                    jugador_x_cambio = jugador_velocidad
                if event.key == pygame.K_SPACE:
                    sonido_bala = mixer.Sound("sounds/disparo.mp3")
                    if bala_visible == False:
                        sonido_bala.play()
                    if not bala_visible:
                        bala_x = jugador_x
                        disparar_bala(bala_x, bala_y)
                if event.key == pygame.K_RETURN:
                    start_game()
                    
            # Evento soltar teclas        
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    jugador_x_cambio = 0

        # Movimiento jugador
        jugador_x += jugador_x_cambio
        
        # Mantener al jugador en el rango de la pantalla
        if jugador_x <= 0:
            jugador_x = 0
        elif jugador_x >= 736:
            jugador_x = 736
            
        # Movimiento de la bala
        if bala_y <= -64:
            bala_y = 530
            bala_x = jugador_x
            bala_visible = False
        if bala_visible:
            disparar_bala(bala_x, bala_y)
            bala_y -= bala_y_cambio
            
        # Movimiento enemigo
        for e in range(cantidad_enemigos):
            
            # Fin del juego
            if enemigo_y[e] > 470:
                for x in range(cantidad_enemigos):
                    enemigo_y[x] = 2000
                texto_final()
                break
            
            enemigo_x[e] += enemigo_x_cambio[e]
            
            # Mantener al enemigo en el rango de la pantalla
            if enemigo_x[e] <= 0:
                enemigo_x_cambio[e] = enemigo_velocidad[e]
                enemigo_y[e] += enemigo_y_cambio[e]
            elif enemigo_x[e] >= 736:
                enemigo_x_cambio[e] = -enemigo_velocidad[e]
                enemigo_y[e] += enemigo_y_cambio[e]
                
            # Verifico colision
            colision = hay_colision(enemigo_x[e], enemigo_y[e], bala_x, bala_y)
            if colision:
                sonido_colision = mixer.Sound("sounds/golpe.mp3")
                sonido_colision.play()
                bala_y = 530
                bala_visible = False
                puntaje += 1
                enemigo_x[e] = random.randint(0, 736)
                enemigo_y[e] = random.randint(50, 150) 
                
            enemigo(enemigo_x[e], enemigo_y[e], e)
            
        jugador(jugador_x, jugador_y)
        mostrar_puntaje(puntaje_x, puntaje_y)
                
        pygame.display.update()
        
start_game()