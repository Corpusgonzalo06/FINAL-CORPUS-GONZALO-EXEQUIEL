import pygame
from pygame_botones import (
    Boton,
    crear_botones_juego,
    crear_botones_comodines,
    crear_botones_fin_juego
)

# ==========================
# COLORES
# ==========================
BLANCO = (255, 255, 255)
NEGRO = (20, 20, 20)
GRIS_PANEL = (28, 28, 28)
AZUL = (70, 130, 180)
VERDE = (60, 180, 90)
ROJO = (180, 60, 60)
ROJO_OSCURO = (120, 30, 30)
VERDE_OSCURO = (30, 100, 60)

# ==========================
# FUENTES
# ==========================
pygame.font.init()
FUENTE = pygame.font.SysFont("arial", 24)
FUENTE_MEDIANA = pygame.font.SysFont("arial", 28)
FUENTE_GRANDE = pygame.font.SysFont("arial", 36)

# ==========================
# FONDO
# ==========================
FONDO_IMG = pygame.image.load("x2.jpg")

# ==========================
# AUXILIAR
# ==========================
def dibujar_texto(pantalla, texto, x, y, color=BLANCO, fuente=FUENTE):
    render = fuente.render(texto, True, color)
    pantalla.blit(render, (x, y))

# ==========================
# DIBUJO PRINCIPAL
# ==========================
def dibujar_juego(pantalla, estado):

    ancho, alto = pantalla.get_size()

    # 🔹 FONDO
    fondo_escalado = pygame.transform.scale(FONDO_IMG, (ancho, alto))
    pantalla.blit(fondo_escalado, (0, 0))

    # ==========================
    # HEADER
    # ==========================
    pygame.draw.rect(pantalla, NEGRO, (0, 0, ancho, 90))
    dibujar_texto(pantalla, "POP A WORD", ancho // 2 - 90, 25, BLANCO, FUENTE_GRANDE)

    info_x = 40
    dibujar_texto(pantalla, f"Nivel: {estado['nivel']}", info_x, 15)
    dibujar_texto(pantalla, f"Puntaje: {estado['puntaje']}", info_x, 45)
    dibujar_texto(pantalla, f"Vidas: {estado['vidas']}", info_x + 180, 15)

    color_tiempo = VERDE if estado["tiempo_restante"] > 10 else ROJO
    dibujar_texto(
        pantalla,
        f"⏱ {estado['tiempo_restante']}s",
        info_x + 180,
        45,
        color_tiempo
    )

    # ==========================
    # PANEL DERECHO
    # ==========================
    panel_x = ancho - 360
    pygame.draw.rect(pantalla, GRIS_PANEL, (panel_x, 90, 360, alto - 90))

    dibujar_texto(pantalla, "PALABRAS", panel_x + 30, 110, AZUL, FUENTE_MEDIANA)

    y = 150
    for pista in estado["pistas"]:
        dibujar_texto(pantalla, pista, panel_x + 30, y)
        y += 30

    # ==========================
    # COMODINES
    # ==========================
    dibujar_texto(pantalla, "COMODINES", panel_x + 30, y + 20, AZUL, FUENTE_MEDIANA)

    if "botones_comodines" not in estado:
        estado["botones_comodines"] = crear_botones_comodines()

    comodin_y = y + 70
    for nombre, boton in estado["botones_comodines"].items():
        boton.rect.topleft = (panel_x + 30, comodin_y)
        boton.activo = estado["comodines"].get(nombre, False)
        boton.dibujar(pantalla, FUENTE)
        comodin_y += 55

    # ==========================
    # ZONA CENTRAL
    # ==========================
    centro_x = ancho // 2 - 180

    dibujar_texto(
        pantalla,
        f"Palabra base: {estado['palabra_base'].upper()}",
        centro_x,
        120,
        BLANCO,
        FUENTE_MEDIANA
    )

    pygame.draw.rect(pantalla, BLANCO, (centro_x, 170, 360, 50), 2)
    dibujar_texto(
        pantalla,
        estado["palabra_actual"].upper(),
        centro_x + 15,
        183,
        BLANCO,
        FUENTE_MEDIANA
    )

    # ==========================
    # LETRAS
    # ==========================
    letras = estado["letras"]
    total_ancho = len(letras) * 55
    inicio_x = centro_x + 180 - total_ancho // 2
    y_letras = 260

    for i, letra in enumerate(letras):
        x = inicio_x + i * 55
        pygame.draw.circle(pantalla, AZUL, (x, y_letras), 25)
        dibujar_texto(pantalla, letra.upper(), x - 8, y_letras - 12)

    # ==========================
    # OVERLAY + MENSAJE DERROTA
    # ==========================
    if estado["estado"] == "perdido":

        overlay = pygame.Surface((ancho, alto), pygame.SRCALPHA)
        overlay.fill((120, 0, 0, 120))
        pantalla.blit(overlay, (0, 0))

        panel_rect = pygame.Rect(centro_x - 20, 300, 400, 90)
        pygame.draw.rect(pantalla, ROJO_OSCURO, panel_rect, border_radius=16)
        pygame.draw.rect(pantalla, BLANCO, panel_rect, 2, border_radius=16)

        dibujar_texto(
            pantalla,
            "💔 TE QUEDASTE SIN VIDAS",
            panel_rect.x + 40,
            panel_rect.y + 18,
            BLANCO,
            FUENTE_MEDIANA
        )

        dibujar_texto(
            pantalla,
            "GAME OVER",
            panel_rect.x + 140,
            panel_rect.y + 55,
            ROJO,
            FUENTE
        )

    # ==========================
    # BOTONES DE JUEGO
    # ==========================
    if estado["estado"] == "jugando":
        if "botones" not in estado:
            estado["botones"] = crear_botones_juego()

        botones_y = 400
        botones_x = centro_x

        for boton in estado["botones"].values():
            boton.rect.topleft = (botones_x, botones_y)
            boton.dibujar(pantalla, FUENTE)
            botones_x += 140

    # ==========================
    # FIN DE JUEGO (BOTONES)
    # ==========================
    if estado["estado"] in ("ganado", "perdido"):

        # Crear botones de fin si no existen
        if "botones_fin" not in estado or not isinstance(estado["botones_fin"], dict):
            estado["botones_fin"] = crear_botones_fin_juego()

        # ⚡ Asegurar que las claves existan
        if "menu" not in estado["botones_fin"]:
            estado["botones_fin"]["menu"] = Boton(0, 0, 220, 50, "VOLVER AL MENÚ")
        if "siguiente" not in estado["botones_fin"] and estado["estado"] == "ganado":
            estado["botones_fin"]["siguiente"] = Boton(0, 0, 220, 50, "SIGUIENTE NIVEL")

        fin_y = 540
        fin_x = centro_x

        # Dibujar botón "menu"
        boton_menu = estado["botones_fin"]["menu"]
        boton_menu.rect.topleft = (fin_x, fin_y)
        boton_menu.dibujar(pantalla, FUENTE)

        # Dibujar botón "siguiente" solo si ganó
        if estado["estado"] == "ganado":
            boton_sig = estado["botones_fin"]["siguiente"]
            boton_sig.rect.topleft = (fin_x + 240, fin_y)
            boton_sig.dibujar(pantalla, FUENTE)
