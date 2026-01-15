import pygame

# ==========================
# COLORES
# ==========================
AZUL = (70, 130, 180)
AZUL_HOVER = (100, 160, 220)
GRIS = (90, 90, 90)
GRIS_OSCURO = (50, 50, 50)
BLANCO = (255, 255, 255)

# ==========================
# CLASE BOTÓN
# ==========================
class Boton:
    def __init__(self, x=0, y=0, ancho=150, alto=50, texto=""):
        self.rect = pygame.Rect(x, y, ancho, alto)
        self.texto = texto
        self.activo = True

    def dibujar(self, pantalla, fuente):
        mouse_pos = pygame.mouse.get_pos()
        hover = self.rect.collidepoint(mouse_pos)

        # COLOR SEGÚN ESTADO
        if not self.activo:
            color = GRIS_OSCURO
        elif hover:
            color = AZUL_HOVER
        else:
            color = AZUL

        # BOTÓN
        pygame.draw.rect(
            pantalla,
            color,
            self.rect,
            border_radius=10
        )

        # BORDE
        pygame.draw.rect(
            pantalla,
            BLANCO,
            self.rect,
            2,
            border_radius=10
        )

        # TEXTO
        texto_render = fuente.render(self.texto, True, BLANCO)
        pantalla.blit(
            texto_render,
            (
                self.rect.centerx - texto_render.get_width() // 2,
                self.rect.centery - texto_render.get_height() // 2
            )
        )

    def fue_clickeado(self, evento):
        return (
            self.activo
            and evento.type == pygame.MOUSEBUTTONDOWN
            and evento.button == 1
            and self.rect.collidepoint(evento.pos)
        )

# ==========================
# BOTONES PRINCIPALES DEL JUEGO
# ==========================
def crear_botones_juego():
    return {
        "shuffle": Boton(texto="SHUFFLE"),
        "clear": Boton(texto="CLEAR"),
        "submit": Boton(texto="SUBMIT"),
    }

# ==========================
# BOTONES FINALES (WIN / LOSE)
# ==========================
def crear_botones_fin_juego():
    # Devuelve siempre las claves "menu" y "siguiente"
    return {
        "menu": Boton(texto="VOLVER AL MENÚ"),
        "siguiente": Boton(texto="SIGUIENTE NIVEL"),
    }

# ==========================
# BOTONES DE COMODINES
# ==========================
def crear_botones_comodines():
    return {
        "revelar_palabra_base": Boton(texto="🔍 Revelar base"),
        "eliminar_restricciones": Boton(texto="🚀 Sin perder vida"),
        "pista_extra": Boton(texto="🧠 Pista"),
    }
