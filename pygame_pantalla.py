# pygame_pantalla.py
import pygame
from pygame_botones import (
    crear_botones_juego,
    crear_botones_comodines,
    crear_botones_fin_juego
)

# ==========================
# COLORES
# ==========================
BLANCO = (255, 255, 255)
NEGRO = (20, 20, 20)
GRIS = (35, 35, 35)
GRIS_PANEL = (28, 28, 28)
AZUL = (70, 130, 180)
VERDE = (60, 180, 90)
ROJO = (180, 60, 60)

# ==========================
# FUENTES
# ==========================
pygame.font.init()
FUENTE = pygame.font.SysFont("arial", 24)
FUENTE_MEDIANA = pygame.font.SysFont("arial", 28)
FUENTE_GRANDE = pygame.font.SysFont("arial", 36)


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
    pantalla.fill(GRIS)

    # ==========================
    # HEADER
    # ==========================
    pygame.draw.rect(pantalla, NEGRO, (0, 0, ancho, 90))

    dibujar_texto(
        pantalla,
        "POP A WORD",
        ancho // 2 - 90,
        25,
        BLANCO,
        FUENTE_GRANDE
    )

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
    # MENSAJE
    # ==========================
    if estado["mensaje"]:
        color = VERDE if estado["estado"] == "ganado" else ROJO
        dibujar_texto(
            pantalla,
            estado["mensaje"],
            centro_x,
            330,
            color,
            FUENTE_MEDIANA
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
    # FIN DE JUEGO
    # ==========================
    if estado["estado"] in ("ganado", "perdido"):

        if "botones_fin" not in estado:
            estado["botones_fin"] = crear_botones_fin_juego()

        texto = "🎉 NIVEL COMPLETADO" if estado["estado"] == "ganado" else "😢 GAME OVER"
        color = VERDE if estado["estado"] == "ganado" else ROJO

        dibujar_texto(
            pantalla,
            texto,
            centro_x,
            480,
            color,
            FUENTE_GRANDE
        )

        fin_y = 540
        fin_x = centro_x

        # BOTÓN VOLVER AL MENÚ
        boton_menu = estado["botones_fin"]["menu"]
        boton_menu.rect.topleft = (fin_x, fin_y)
        boton_menu.dibujar(pantalla, FUENTE)

        # BOTÓN SIGUIENTE NIVEL (solo si ganó)
        if estado["estado"] == "ganado":
            boton_sig = estado["botones_fin"]["siguiente"]
            boton_sig.rect.topleft = (fin_x + 240, fin_y)
            boton_sig.dibujar(pantalla, FUENTE)
