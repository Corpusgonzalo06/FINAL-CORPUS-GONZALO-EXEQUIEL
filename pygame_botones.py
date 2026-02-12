import pygame

# ==========================
# COLORES
# ==========================
AZUL = (70, 130, 180)
AZUL_HOVER = (100, 160, 220)
GRIS_OSCURO = (50, 50, 50)
BLANCO = (255, 255, 255)

# ==========================
# CREAR BOTÓN
# ==========================
def crear_boton(x=0, y=0, ancho=150, alto=50, texto=""):
    boton = {}
    boton["rect"] = pygame.Rect(x, y, ancho, alto)
    boton["texto"] = texto
    boton["activo"] = True

    return boton

# ==========================
# DIBUJAR BOTÓN
# ==========================
def dibujar_boton(pantalla, boton, fuente):
    mouse_pos = pygame.mouse.get_pos()

    esta_hover = False
    if boton["rect"].collidepoint(mouse_pos):
        esta_hover = True

    color = AZUL

    if boton["activo"] == False:
        color = GRIS_OSCURO
    else:
        if esta_hover:
            color = AZUL_HOVER

    pygame.draw.rect(
        pantalla,
        color,
        boton["rect"],
        border_radius=10
    )

    pygame.draw.rect(
        pantalla,
        BLANCO,
        boton["rect"],
        2,
        border_radius=10
    )

    texto_render = fuente.render(boton["texto"], True, BLANCO)

    x_texto = boton["rect"].centerx - texto_render.get_width() // 2
    y_texto = boton["rect"].centery - texto_render.get_height() // 2

    pantalla.blit(texto_render, (x_texto, y_texto))

# ==========================
# CLICK BOTÓN
# ==========================
def ver_boton_fue_clickeado(boton, evento):
    fue_clic = False

    if boton["activo"] == True:
        if evento.type == pygame.MOUSEBUTTONDOWN:
            if evento.button == 1:
                if boton["rect"].collidepoint(evento.pos):
                    fue_clic = True

    return fue_clic

# ==========================
# BOTONES PRINCIPALES
# ==========================
def crear_botones_juego():
    botones = {}

    boton_shuffle = crear_boton(texto="SHUFFLE")
    boton_clear = crear_boton(texto="CLEAR")
    boton_submit = crear_boton(texto="SUBMIT")

    botones["shuffle"] = boton_shuffle
    botones["clear"] = boton_clear
    botones["submit"] = boton_submit

    return botones

# ==========================
# BOTONES FINALES
# ==========================
def crear_botones_fin_juego():
    botones = {}

    boton_menu = crear_boton(texto="VOLVER AL MENÚ")
    boton_siguiente = crear_boton(texto="SIGUIENTE NIVEL")

    botones["menu"] = boton_menu
    botones["siguiente"] = boton_siguiente

    return botones

# ==========================
# BOTONES COMODINES
# ==========================
def crear_botones_comodines():
    botones = {}

    boton_base = crear_boton(texto="🔍 Revelar base")
    boton_sin_vida = crear_boton(texto="🚀 Sin perder vida")
    boton_pista = crear_boton(texto="🧠 Pista")

    botones["revelar_palabra_base"] = boton_base
    botones["eliminar_restricciones"] = boton_sin_vida
    botones["pista_extra"] = boton_pista

    return botones