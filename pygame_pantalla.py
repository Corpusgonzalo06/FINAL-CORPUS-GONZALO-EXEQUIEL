import pygame
from pygame_botones import (
    crear_botones_juego,
    crear_botones_comodines,
    crear_botones_fin_juego,
    dibujar_boton
)
from usuarios import cargar_usuarios

# ==========================
# COLORES
# ==========================
BLANCO = (255, 255, 255)
NEGRO = (20, 20, 20)
GRIS_PANEL = (28, 28, 28)
AZUL = (70, 130, 180)
VERDE = (60, 180, 90)
ROJO = (180, 60, 60)
AMARILLO = (230, 200, 60)

# ==========================
# FUENTES
# ==========================
pygame.font.init()
FUENTE = pygame.font.SysFont("arial", 24)
FUENTE_MEDIANA = pygame.font.SysFont("arial", 28)
FUENTE_GRANDE = pygame.font.SysFont("arial", 38, bold=True)
FUENTE_TIMER = pygame.font.SysFont("arial", 48, bold=True)
FUENTE_NIVEL = pygame.font.SysFont("arial", 30, bold=True)

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

    # ---------- FONDO ----------
    fondo = pygame.transform.scale(FONDO_IMG, (ancho, alto))
    pantalla.blit(fondo, (0, 0))

    # ---------- HEADER ----------
    pygame.draw.rect(pantalla, NEGRO, (0, 0, ancho, 100))

    dibujar_texto(pantalla, "POP A WORD", ancho // 2 - 140, 15, BLANCO, FUENTE_GRANDE)
    dibujar_texto(pantalla, f"NIVEL {estado['nivel']}", ancho // 2 - 60, 58, AZUL, FUENTE_NIVEL)

    dibujar_texto(pantalla, f"Puntaje: {estado['puntaje']}", 30, 20)
    dibujar_texto(pantalla, f"Vidas: {estado['vidas']}", 30, 55)

    # ---------- TIEMPO ----------
    tiempo = estado["tiempo_restante"]
    color_tiempo = VERDE if tiempo > 20 else AMARILLO if tiempo > 10 else ROJO
    dibujar_texto(pantalla, f"{tiempo}s", ancho - 150, 30, color_tiempo, FUENTE_TIMER)

    # ---------- PANEL DERECHO ----------
    panel_x = ancho - 360
    pygame.draw.rect(pantalla, GRIS_PANEL, (panel_x, 100, 360, alto - 100))

    dibujar_texto(pantalla, "PALABRAS", panel_x + 30, 120, AZUL, FUENTE_MEDIANA)

    y = 160
    for pista in estado["pistas"]:
        dibujar_texto(pantalla, pista, panel_x + 30, y)
        y += 30

    # ---------- COMODINES ----------
    dibujar_texto(pantalla, "COMODINES", panel_x + 30, y + 20, AZUL, FUENTE_MEDIANA)

    if "botones_comodines" not in estado:
        estado["botones_comodines"] = crear_botones_comodines()

    comodin_y = y + 70
    for nombre, boton in estado["botones_comodines"].items():
        boton["rect"].topleft = (panel_x + 30, comodin_y)
        boton["activo"] = estado["comodines"].get(nombre, False)
        dibujar_boton(pantalla, boton, FUENTE)
        comodin_y += 55

    # ---------- ZONA CENTRAL ----------
    centro_x = ancho // 2 - 200



    pygame.draw.rect(pantalla, BLANCO, (centro_x, 180, 400, 52), 2)
    dibujar_texto(
        pantalla,
        estado["palabra_actual"].upper(),
        centro_x + 15,
        192,
        BLANCO,
        FUENTE_MEDIANA
    )

    # ---------- LETRAS ----------
    letras = estado["letras"]
    total_ancho = len(letras) * 60
    inicio_x = centro_x + 200 - total_ancho // 2
    y_letras = 280

    for i, letra in enumerate(letras):
        x = inicio_x + i * 60
        pygame.draw.circle(pantalla, AZUL, (x, y_letras), 26)
        dibujar_texto(pantalla, letra.upper(), x - 9, y_letras - 13)

    # ---------- MENSAJE ----------
    if estado["mensaje"]:
        color = VERDE if estado["estado"] == "ganado" else ROJO if estado["estado"] == "perdido" else AMARILLO
        dibujar_texto(pantalla, estado["mensaje"], centro_x, 350, color, FUENTE_MEDIANA)

    # ---------- BOTONES DE JUEGO ----------
    if estado["estado"] == "jugando":
        if "botones" not in estado:
            estado["botones"] = crear_botones_juego()

        x_btn = centro_x
        for boton in estado["botones"].values():
            boton["rect"].topleft = (x_btn, 430)
            dibujar_boton(pantalla, boton, FUENTE)
            x_btn += 150

    # ---------- FIN DE PARTIDA ----------
    if estado["estado"] in ("ganado", "perdido"):

        overlay = pygame.Surface((ancho, alto), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 230))
        pantalla.blit(overlay, (0, 0))

        card = pygame.Surface((520, 420), pygame.SRCALPHA)
        card.fill((15, 30, 50, 230))
        pantalla.blit(card, (centro_x - 20, 190))
        pygame.draw.rect(pantalla, AZUL, (centro_x - 20, 190, 520, 420), 2)

        y = 220

        dibujar_texto(pantalla, "RESUMEN DE LA PARTIDA", centro_x, y, AZUL, FUENTE_GRANDE)
        y += 60

        dibujar_texto(pantalla, f"Nivel máximo alcanzado: {estado['nivel']}", centro_x, y, BLANCO, FUENTE_MEDIANA)
        y += 40
        dibujar_texto(pantalla, f"Puntaje final: {estado['puntaje']}", centro_x, y, BLANCO, FUENTE_MEDIANA)
        y += 40
        dibujar_texto(
            pantalla,
            f"Tiempo restante: {estado['tiempo_restante']} segundos",
            centro_x,
            y,
            BLANCO,
            FUENTE_MEDIANA
        )

        # ---------- TOP 3 ----------
        usuarios = cargar_usuarios("usuarios.json")
        ranking = sorted(
            usuarios.items(),
            key=lambda item: item[1].get("puntos", 0),
            reverse=True
        )

        y += 60
        dibujar_texto(pantalla, "🏆 TOP 3", centro_x, y, AMARILLO, FUENTE_MEDIANA)
        y += 40

        for i, (nombre, datos) in enumerate(ranking[:3], start=1):
            dibujar_texto(
                pantalla,
                f"{i}. {nombre} - {datos.get('puntos', 0)} pts",
                centro_x,
                y,
                BLANCO
            )
            y += 28

        # ---------- BOTONES FINALES ----------
        if "botones_fin" not in estado:
            estado["botones_fin"] = crear_botones_fin_juego()

        boton_menu = estado["botones_fin"]["menu"]
        boton_menu["rect"].topleft = (centro_x + 60, 560)
        dibujar_boton(pantalla, boton_menu, FUENTE)

        if estado["estado"] == "ganado":
            boton_sig = estado["botones_fin"]["siguiente"]
            boton_sig["rect"].topleft = (centro_x + 260, 560)
            dibujar_boton(pantalla, boton_sig, FUENTE)
