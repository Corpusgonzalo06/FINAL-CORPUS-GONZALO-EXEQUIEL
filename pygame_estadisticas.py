import pygame
pygame.font.init()
# ==========================
# COLORES
# ==========================
BLANCO = (255, 255, 255)
GRIS = (40, 40, 40)
AZUL = (70, 130, 180)

FUENTE_TITULO = pygame.font.SysFont("arial", 32)
FUENTE = pygame.font.SysFont("arial", 22)


def dibujar_texto(pantalla, texto, x, y, fuente=FUENTE, color=BLANCO):
    render = fuente.render(texto, True, color)
    pantalla.blit(render, (x, y))


def mostrar_estadisticas(pantalla, usuario_actual):
    """
    Muestra las estadísticas del usuario en pantalla.
    Retorna 'menu' cuando se presiona el botón volver.
    """

    reloj = pygame.time.Clock()

    boton_volver = pygame.Rect(300, 420, 200, 45)

    corriendo = True
    while corriendo:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                exit()

            if evento.type == pygame.MOUSEBUTTONDOWN:
                if boton_volver.collidepoint(evento.pos):
                    return "menu"

        # -------- DIBUJO --------
        pantalla.fill(GRIS)

        dibujar_texto(pantalla, "ESTADÍSTICAS DEL JUGADOR", 180, 30, FUENTE_TITULO)

        dibujar_texto(pantalla, f"Partidas jugadas: {usuario_actual['partidas_jugadas']}", 200, 100)
        dibujar_texto(pantalla, f"Victorias: {usuario_actual['victorias']}", 200, 140)
        dibujar_texto(pantalla, f"Derrotas: {usuario_actual['derrotas']}", 200, 180)
        dibujar_texto(pantalla, f"Puntos totales: {usuario_actual['puntos']}", 200, 220)
        dibujar_texto(pantalla, f"Errores totales: {usuario_actual['errores_totales_juego']}", 200, 260)

        tiempo = round(usuario_actual["tiempo_total"], 2)
        dibujar_texto(pantalla, f"Tiempo total jugado: {tiempo} segundos", 200, 300)

        # Botón volver
        pygame.draw.rect(pantalla, AZUL, boton_volver)
        dibujar_texto(pantalla, "VOLVER", 360, 432)

        pygame.display.update()
        reloj.tick(60)
