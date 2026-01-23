import pygame

pygame.font.init()

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
# INICIALIZAR ESTADÍSTICAS
# ==========================
def inicializar_estadisticas(usuario):
    """
    Inicializa las estadísticas del usuario si no existen.
    Se usa al registrarse o al iniciar sesión.
    """
    usuario.setdefault("partidas_jugadas", 0)
    usuario.setdefault("palabras_completadas", 0)
    usuario.setdefault("palabras_incompletas", 0)
    usuario.setdefault("puntos", 0)
    usuario.setdefault("errores_totales_juego", 0)
    usuario.setdefault("tiempo_total", 0)


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
    inicializar_estadisticas(usuario_actual)
    reloj = pygame.time.Clock()
    boton_volver = pygame.Rect(300, 420, 200, 45)

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
        pantalla.fill(GRIS)

        dibujar_texto(
            pantalla,
            "ESTADÍSTICAS DEL JUGADOR",
            180,
            30,
            FUENTE_TITULO
        )

        dibujar_texto(
            pantalla,
            f"Partidas jugadas: {usuario_actual['partidas_jugadas']}",
            200,
            100
        )

        dibujar_texto(
            pantalla,
            f"Palabras completadas: {usuario_actual['palabras_completadas']}",
            200,
            140
        )

        dibujar_texto(
            pantalla,
            f"Palabras incompletas: {usuario_actual['palabras_incompletas']}",
            200,
            180
        )

        dibujar_texto(
            pantalla,
            f"Puntos totales: {usuario_actual['puntos']}",
            200,
            220
        )

        dibujar_texto(
            pantalla,
            f"Errores totales: {usuario_actual['errores_totales_juego']}",
            200,
            260
        )

        tiempo_total = round(usuario_actual["tiempo_total"], 2)
        dibujar_texto(
            pantalla,
            f"Tiempo total jugado: {tiempo_total} segundos",
            200,
            300
        )

        # -------- BOTÓN VOLVER --------
        pygame.draw.rect(pantalla, AZUL, boton_volver)
        dibujar_texto(pantalla, "VOLVER", 360, 432)

        pygame.display.update()
        reloj.tick(60)

    return resultado
