import pygame
import sys

# ==========================
# IMPORTS DEL PROYECTO
# ==========================
from usuarios import cargar_usuarios, guardar_usuarios
from estadisticas import inicializar_estadisticas
from pygame_estadisticas import mostrar_estadisticas
from palabras import PALABRAS

from pygame_controlador import *
from pygame_pantalla import dibujar_juego
from manejo_aleatoriedad import seleccionar_palabras_nivel
from pygame_botones import ver_boton_fue_clickeado
# ==========================
# SONIDOS
# ==========================
from pygame_sonidos import *
from pygame_ui import crear_botones
from pygame_eventos import *


# ==========================
# CONFIGURACIÓN GENERAL
# ==========================
pygame.init()

ANCHO, ALTO = 1700, 900
pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Mar de Palabras")

reloj = pygame.time.Clock()
FUENTE = pygame.font.SysFont("Brodway", 28)

# ==========================
# INICIALIZACIÓN DE SONIDOS
# ==========================
sonidos = inicializar_sonidos()
reproducir_musica_fondo()

# ==========================
# CONFIG PARTIDA
# ==========================
NIVEL_MAXIMO = 5

# ==========================
# COLORES
# ==========================
BLANCO = (255, 255, 255)
AZUL = (70, 130, 180)
ROJO = (180, 60, 60)

# ==========================
# FONDO
# ==========================
FONDO_MENU = pygame.image.load("menu_imagen.jpg")
botones = crear_botones()


def dibujar_fondo_menu():
    fondo = pygame.transform.scale(FONDO_MENU, (ANCHO, ALTO))
    pantalla.blit(fondo, (0, 0))

    overlay = pygame.Surface((ANCHO, ALTO), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 120))
    pantalla.blit(overlay, (0, 0))


def dibujar_texto(texto, x, y, color=BLANCO):
    render = FUENTE.render(texto, True, color)
    pantalla.blit(render, (x, y))


# ==========================
# USUARIOS
# ==========================
usuarios = cargar_usuarios("usuarios.json")

lista_bases = list(PALABRAS.keys())

# ==========================
# RECTÁNGULOS
# ==========================


# ==========================
# FUNCIONES DE EVENTOS
# ==========================


# ==========================
# FUNCIONES DE DIBUJO
# ==========================
def dibujar_inicio(botones):
    pygame.draw.rect(pantalla, AZUL, botones["btn_login"])
    pygame.draw.rect(pantalla, AZUL, botones["btn_registro"])
    pygame.draw.rect(pantalla, ROJO, botones["btn_salir_juego"])

    dibujar_texto("INICIAR SESIÓN", botones["btn_login"].x + 20, botones["btn_login"].y + 15)
    dibujar_texto("REGISTRARSE", botones["btn_registro"].x + 25, botones["btn_registro"].y + 15)
    dibujar_texto("SALIR", botones["btn_salir_juego"].x + 75, botones["btn_salir_juego"].y + 15)


def dibujar_login_registro(estado, botones):
    pygame.draw.rect(pantalla, BLANCO, botones["rect_usuario"], 2)
    pygame.draw.rect(pantalla, BLANCO, botones["rect_contrasena"], 2)
    pygame.draw.rect(pantalla, AZUL, botones["btn_submit"])
    pygame.draw.rect(pantalla, AZUL, botones["btn_atras"])

    dibujar_texto("Usuario:", botones["rect_usuario"].x, botones["rect_usuario"].y - 30)
    dibujar_texto(estado["usuario_input"], botones["rect_usuario"].x + 10, botones["rect_usuario"].y + 5)

    dibujar_texto("Contraseña:", botones["rect_contrasena"].x, botones["rect_contrasena"].y - 30)
    dibujar_texto("*" * len(estado["contrasena_input"]), botones["rect_contrasena"].x + 10, botones["rect_contrasena"].y + 5)

    dibujar_texto("CONFIRMAR", botones["btn_submit"].x + 80, botones["btn_submit"].y + 12)
    dibujar_texto("ATRÁS", botones["btn_atras"].x + 30, botones["btn_atras"].y + 10)
    dibujar_texto(estado["mensaje"], 650, 500, ROJO)



def dibujar_menu(estado, botones):
    pygame.draw.rect(
        pantalla,
        AZUL if not estado["tdah_activo"] else (60, 180, 90),
        botones["btn_tdah"]
    )
    dibujar_texto("MODO-TDAH", botones["btn_tdah"].x + 60, botones["btn_tdah"].y + 15)

    pygame.draw.rect(pantalla, AZUL, botones["btn_jugar"])
    pygame.draw.rect(pantalla, AZUL, botones["btn_stats"])
    pygame.draw.rect(pantalla, ROJO, botones["btn_cerrar_sesion"])

    dibujar_texto("JUGAR", botones["btn_jugar"].x + 70, botones["btn_jugar"].y + 15)
    dibujar_texto("ESTADÍSTICAS", botones["btn_stats"].x + 30, botones["btn_stats"].y + 15)
    dibujar_texto("CERRAR SESIÓN", botones["btn_cerrar_sesion"].x + 20, botones["btn_cerrar_sesion"].y + 15)


def dibujar_pantalla(estado, botones):
    pantalla.fill((0, 0, 0))
    dibujar_fondo_menu()

    if estado["pantalla_actual"] == "inicio":
        dibujar_inicio(botones)

    elif estado["pantalla_actual"] in ["login", "registro"]:
        dibujar_login_registro(estado, botones)

    elif estado["pantalla_actual"] == "menu":
        dibujar_menu(estado, botones)

    elif estado["pantalla_actual"] == "jugando" and estado["estado_juego"] is not None:
        dibujar_juego(pantalla, estado["estado_juego"])


 
# ==========================
# LOOP PRINCIPAL
# ==========================
estado = crear_estado_app()

while True:
    estado = manejar_eventos(estado, usuarios, sonidos, botones, lista_bases, pantalla)

    dibujar_pantalla(estado, botones)

    pygame.display.update()
    reloj.tick(60)
