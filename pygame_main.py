import pygame
import sys
from usuarios import cargar_usuarios, guardar_usuarios
from estadisticas import inicializar_estadisticas
from pygame_estadisticas import mostrar_estadisticas
from palabras import PALABRAS
from pygame_controlador import *
from pygame_dibujos import dibujar_juego
from manejo_aleatoriedad import seleccionar_palabras_nivel
from pygame_botones import ver_boton_fue_clickeado
from pygame_sonidos import *
from pygame_ui import crear_botones_disponibles
from pygame_eventos import *
from pygame_renderizacion import mostrar_vista_actual


pygame.init()

ANCHO, ALTO = 1700, 900
pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Mar de Palabras")

reloj = pygame.time.Clock()
FUENTE = pygame.font.SysFont("Brodway", 28)


sonidos = inicializar_sonidos()
reproducir_musica_fondo()


NIVEL_MAXIMO = 5

BLANCO = (255, 255, 255)
AZUL = (70, 130, 180)
ROJO = (180, 60, 60)

FONDO_MENU = pygame.image.load("menu_imagen.jpg")
botones = crear_botones_disponibles()

usuarios = cargar_usuarios("usuarios.json")

lista_bases = list(PALABRAS.keys())

estado = iniciar_informacion_juego()

while True:
    estado = manejar_eventos(estado, usuarios, sonidos, botones, lista_bases, pantalla)

    mostrar_vista_actual(
    pantalla,
    FUENTE,
    FONDO_MENU,
    ANCHO,
    ALTO,
    estado,
    botones,
    dibujar_juego
)


    pygame.display.update()
    reloj.tick(60)
