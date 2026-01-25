import pygame

pygame.font.init()
FONDO_STATS = pygame.image.load("fondo_juego.jpg")

# ==========================
# COLORES
# ==========================
BLANCO = (255, 255, 255)
GRIS = (40, 40, 40)
AZUL = (70, 130, 180)

# ==========================
# FUENTES
# ==========================
FUENTE_TITULO = pygame.font.SysFont("arial", 32)
FUENTE = pygame.font.SysFont("arial", 22)


# ==========================
# DIBUJAR TEXTO
# ==========================
def dibujar_texto(pantalla, texto, x, y, fuente=FUENTE, color=BLANCO):
    texto_render = fuente.render(texto, True, color)
    pantalla.blit(texto_render, (x, y))


# ==========================
# MOSTRAR ESTADÍSTICAS
# ==========================
def mostrar_estadisticas(pantalla, usuario_actual):
    """ 
    Muestra las estadísticas del usuario en pantalla.
    Devuelve 'menu' cuando el usuario presiona volver.
    """

    reloj = pygame.time.Clock()
    boton_volver = pygame.Rect(720, 520, 200, 50)

    corriendo = True
    resultado = None

    while corriendo:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                exit()

            if evento.type == pygame.MOUSEBUTTONDOWN:
                if boton_volver.collidepoint(evento.pos):
                    resultado = "menu"
                    corriendo = False

        # -------- DIBUJO --------
        fondo = pygame.transform.scale(FONDO_STATS, pantalla.get_size())
        pantalla.blit(fondo, (0, 0))
        overlay = pygame.Surface(pantalla.get_size(), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 190))
        pantalla.blit(overlay, (0, 0))


        dibujar_texto(
            pantalla,
            "ESTADÍSTICAS DEL JUGADOR",
            740,
            60,
            FUENTE_TITULO
        )

        dibujar_texto(
            pantalla,
            f"Partidas jugadas: {usuario_actual['partidas_jugadas']}",
            740,
            180
        )

        dibujar_texto(
            pantalla,
            f"Palabras completadas: {usuario_actual['palabras_completadas']}",
            740,
            220
        )

        dibujar_texto(
            pantalla,
            f"Palabras incompletas: {usuario_actual['palabras_incompletas']}",
            740,
            260
        )

        dibujar_texto(
            pantalla,
            f"Puntos totales: {usuario_actual['puntos']}",
            740,
            300
        )

        dibujar_texto(
            pantalla,
            f"Errores totales: {usuario_actual['errores_totales_juego']}",
            740,
            340
        )

        tiempo_total = round(usuario_actual["tiempo_total"], 2)
        dibujar_texto(
            pantalla,
            f"Tiempo total jugado: {tiempo_total} segundos",
            740,
            380
        )

        # -------- BOTÓN VOLVER --------
        pygame.draw.rect(pantalla, AZUL, boton_volver)
        dibujar_texto(pantalla, "VOLVER", 785, 535)


        pygame.display.update()
        reloj.tick(60)

    return resultado
