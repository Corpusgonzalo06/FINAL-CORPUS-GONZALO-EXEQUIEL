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
# MEDIDAS UI (reales)
# ==========================
HEADER_ALTO = 100
PANEL_ANCHO = 360

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
FONDO_IMG = pygame.image.load("fondo_juego.jpg")

# ==========================
# AUXILIAR
# ==========================
def dibujar_texto(pantalla, texto, x, y, color=BLANCO, fuente=FUENTE):
    render = fuente.render(texto, True, color)
    pantalla.blit(render, (x, y))


# ==========================
# SECCIONES DE DIBUJO
# ==========================
def dibujar_fondo(pantalla):
    ancho, alto = pantalla.get_size()
    fondo = pygame.transform.scale(FONDO_IMG, (ancho, alto))
    pantalla.blit(fondo, (0, 0))
    


def dibujar_header(pantalla, estado):
    ancho, _ = pantalla.get_size()
    pygame.draw.rect(pantalla, NEGRO, (0, 0, ancho, HEADER_ALTO))

    dibujar_texto(pantalla, "MAR DE PALABRAS", ancho // 2 - 140, 15, BLANCO, FUENTE_GRANDE)
    dibujar_texto(pantalla, f"NIVEL {estado['nivel']}", ancho // 2 - 60, 58, AZUL, FUENTE_NIVEL)

    dibujar_texto(pantalla, f"Puntaje: {estado['puntaje']}", 30, 20)
    dibujar_texto(pantalla, f"Vidas: {estado['vidas']}", 30, 55)


def dibujar_tiempo(pantalla, estado):
    ancho, _ = pantalla.get_size()
    tiempo = estado["tiempo_restante"]

    if tiempo > 20:
        color = VERDE
    elif tiempo > 10:
        color = AMARILLO
    else:
        color = ROJO

    dibujar_texto(pantalla, f"{tiempo}s", ancho - 150, 30, color, FUENTE_TIMER)


def dibujar_panel_derecho(pantalla, estado):
    ancho, alto = pantalla.get_size()
    panel_x = ancho - PANEL_ANCHO

    pygame.draw.rect(pantalla, GRIS_PANEL, (panel_x, HEADER_ALTO, PANEL_ANCHO, alto - HEADER_ALTO))
    dibujar_texto(pantalla, "PALABRAS", panel_x + 30, 120, AZUL, FUENTE_MEDIANA)

    y = 160
    for pista in estado["pistas"]:
        dibujar_texto(pantalla, pista, panel_x + 30, y)
        y += 30

    dibujar_texto(pantalla, "COMODINES", panel_x + 30, y + 20, AZUL, FUENTE_MEDIANA)

    if "botones_comodines" not in estado:
        estado["botones_comodines"] = crear_botones_comodines()

    comodin_y = y + 70
    for nombre, boton in estado["botones_comodines"].items():
        boton["rect"].topleft = (panel_x + 30, comodin_y)
        boton["activo"] = estado["comodines"].get(nombre, False)
        dibujar_boton(pantalla, boton, FUENTE)
        comodin_y += 55


def dibujar_zona_central(pantalla, estado):
    ancho, _ = pantalla.get_size()
    centro_x = ancho // 2 - 200

    pygame.draw.rect(pantalla, BLANCO, (centro_x, 180, 400, 52), 2)
    dibujar_texto(pantalla, estado["palabra_actual"].upper(), centro_x + 15, 192, BLANCO, FUENTE_MEDIANA)

    letras = estado["letras"]
    inicio_x = centro_x + 200 - (len(letras) * 60) // 2

    for i, letra in enumerate(letras):
        x = inicio_x + i * 60
        pygame.draw.circle(pantalla, AZUL, (x, 280), 26)
        dibujar_texto(pantalla, letra.upper(), x - 9, 267)


def dibujar_mensaje(pantalla, estado):
    if not estado["mensaje"]:
        return

    ancho, _ = pantalla.get_size()
    centro_x = ancho // 2 - 200

    if estado["estado"] == "ganado":
        color = VERDE
    elif estado["estado"] == "perdido":
        color = ROJO
    else:
        color = AMARILLO

    dibujar_texto(pantalla, estado["mensaje"], centro_x, 350, color, FUENTE_MEDIANA)


def dibujar_botones_juego(pantalla, estado_juego):
    # Solo dibujamos botones cuando el juego está activo o terminó
    if estado_juego["estado"] not in ("jugando", "ganado", "perdido"):
        return

    if "botones" not in estado_juego:
        estado_juego["botones"] = crear_botones_juego()

    ancho, _ = pantalla.get_size()
    x = ancho // 2 - 200

    for boton in estado_juego["botones"].values():
        boton["rect"].topleft = (x, 430)
        dibujar_boton(pantalla, boton, FUENTE)
        x += 150


def dibujar_fin_partida(pantalla, estado):
    ancho, alto = pantalla.get_size()
    centro_x = ancho // 2 - 200

    overlay = pygame.Surface((ancho, alto), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 230))
    pantalla.blit(overlay, (0, 0))

    pygame.draw.rect(pantalla, AZUL, (centro_x - 20, 190, 520, 420), 2)

    y = 220
    dibujar_texto(pantalla, "RESUMEN DE LA PARTIDA", centro_x, y, AZUL, FUENTE_GRANDE)
    y += 60

    dibujar_texto(pantalla, f"Nivel alcanzado: {estado['nivel']}", centro_x, y, BLANCO, FUENTE_MEDIANA)
    y += 40
    dibujar_texto(pantalla, f"Puntaje final: {estado['puntaje']}", centro_x, y, BLANCO, FUENTE_MEDIANA)
    y += 40
    dibujar_texto(pantalla, f"Tiempo jugado: {estado['tiempo_jugado']} s", centro_x, y, BLANCO, FUENTE_MEDIANA)

    usuarios = cargar_usuarios("usuarios.json")
    ranking = sorted(usuarios.items(), key=lambda x: x[1].get("puntos", 0), reverse=True)

    y += 60
    dibujar_texto(pantalla, "🏆 TOP 3", centro_x, y, AMARILLO, FUENTE_MEDIANA)
    y += 40

    for i, (nombre, datos) in enumerate(ranking[:3], start=1):
        dibujar_texto(pantalla, f"{i}. {nombre} - {datos.get('puntos', 0)} pts", centro_x, y)
        y += 28

    if "botones_fin" not in estado:
        estado["botones_fin"] = crear_botones_fin_juego()

    boton_menu = estado["botones_fin"]["menu"]
    boton_menu["rect"].topleft = (centro_x + 60, 560)
    dibujar_boton(pantalla, boton_menu, FUENTE)

    if estado["estado"] == "ganado":
        boton_sig = estado["botones_fin"]["siguiente"]
        boton_sig["rect"].topleft = (centro_x + 260, 560)
        dibujar_boton(pantalla, boton_sig, FUENTE)


# ==========================
# DIBUJO PRINCIPAL
# ==========================
def dibujar_juego(pantalla, estado):
    dibujar_fondo(pantalla)
    dibujar_header(pantalla, estado)
    dibujar_tiempo(pantalla, estado)
    dibujar_panel_derecho(pantalla, estado)
    dibujar_zona_central(pantalla, estado)
    dibujar_mensaje(pantalla, estado)
    dibujar_botones_juego(pantalla, estado)

    if estado["estado"] in ("ganado", "perdido"):
        dibujar_fin_partida(pantalla, estado)


