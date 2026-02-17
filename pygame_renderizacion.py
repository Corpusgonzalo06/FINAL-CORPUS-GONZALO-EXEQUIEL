import pygame
from pygame_dibujos import oscurecer_pantalla

# ==========================
# COLORES (podés importarlos si los tenés en otro módulo)
# ==========================
BLANCO = (255, 255, 255)
AZUL = (70, 130, 180)
ROJO = (180, 60, 60)

def mostrar_fondo_menu(pantalla, fondo_menu, ancho, alto):
    fondo = pygame.transform.scale(fondo_menu, (ancho, alto))
    pantalla.blit(fondo, (0, 0))

    oscurecer_pantalla(pantalla, 120)


def mostrar_texto_en_la_interfaz(pantalla, fuente, texto, x, y, color=BLANCO):
    render = fuente.render(texto, True, color)
    pantalla.blit(render, (x, y))


def mostrar_inicio(pantalla, fuente, botones):
    pygame.draw.rect(pantalla, AZUL, botones["btn_login"])
    pygame.draw.rect(pantalla, AZUL, botones["btn_registro"])
    pygame.draw.rect(pantalla, ROJO, botones["btn_salir_juego"])

    mostrar_texto_en_la_interfaz(pantalla, fuente, "INICIAR SESIÓN", botones["btn_login"].x + 20, botones["btn_login"].y + 15)
    mostrar_texto_en_la_interfaz(pantalla, fuente, "REGISTRARSE", botones["btn_registro"].x + 25, botones["btn_registro"].y + 15)
    mostrar_texto_en_la_interfaz(pantalla, fuente, "SALIR", botones["btn_salir_juego"].x + 75, botones["btn_salir_juego"].y + 15)


def mostrar_login_registro(pantalla, fuente, estado, botones):
    pygame.draw.rect(pantalla, BLANCO, botones["rect_usuario"], 2)
    pygame.draw.rect(pantalla, BLANCO, botones["rect_contrasena"], 2)
    pygame.draw.rect(pantalla, AZUL, botones["btn_submit"])
    pygame.draw.rect(pantalla, AZUL, botones["btn_atras"])

    mostrar_texto_en_la_interfaz(pantalla, fuente, "Usuario:", botones["rect_usuario"].x, botones["rect_usuario"].y - 30)
    mostrar_texto_en_la_interfaz(pantalla, fuente, estado["usuario_input"], botones["rect_usuario"].x + 10, botones["rect_usuario"].y + 5)

    mostrar_texto_en_la_interfaz(pantalla, fuente, "Contraseña:", botones["rect_contrasena"].x, botones["rect_contrasena"].y - 30)
    mostrar_texto_en_la_interfaz(pantalla, fuente, "*" * len(estado["contrasena_input"]), botones["rect_contrasena"].x + 10, botones["rect_contrasena"].y + 5)

    mostrar_texto_en_la_interfaz(pantalla, fuente, "CONFIRMAR", botones["btn_submit"].x + 80, botones["btn_submit"].y + 12)
    mostrar_texto_en_la_interfaz(pantalla, fuente, "ATRÁS", botones["btn_atras"].x + 30, botones["btn_atras"].y + 10)
    mostrar_texto_en_la_interfaz(pantalla, fuente, estado["mensaje"], 650, 500, ROJO)


def mostrar_menu(pantalla, fuente, estado, botones):
    if estado["tdah_activo"]:
        color_tdah = (60, 180, 90)
    else:
        color_tdah = AZUL


    pygame.draw.rect(pantalla, color_tdah, botones["btn_tdah"])
    mostrar_texto_en_la_interfaz(pantalla, fuente, "MODO-TDAH", botones["btn_tdah"].x + 60, botones["btn_tdah"].y + 15)

    pygame.draw.rect(pantalla, AZUL, botones["btn_jugar"])
    pygame.draw.rect(pantalla, AZUL, botones["btn_stats"])
    pygame.draw.rect(pantalla, ROJO, botones["btn_cerrar_sesion"])

    mostrar_texto_en_la_interfaz(pantalla, fuente, "JUGAR", botones["btn_jugar"].x + 70, botones["btn_jugar"].y + 15)
    mostrar_texto_en_la_interfaz(pantalla, fuente, "ESTADÍSTICAS", botones["btn_stats"].x + 30, botones["btn_stats"].y + 15)
    mostrar_texto_en_la_interfaz(pantalla, fuente, "CERRAR SESIÓN", botones["btn_cerrar_sesion"].x + 20, botones["btn_cerrar_sesion"].y + 15)


def mostrar_vista_actual(pantalla, fuente, fondo_menu, ancho, alto, estado, botones, dibujar_juego):

    mostrar_fondo_menu(pantalla, fondo_menu, ancho, alto)

    if estado["pantalla_actual"] == "inicio":
        mostrar_inicio(pantalla, fuente, botones)

    elif estado["pantalla_actual"] in ["login", "registro"]:
        mostrar_login_registro(pantalla, fuente, estado, botones)

    elif estado["pantalla_actual"] == "menu":
        mostrar_menu(pantalla, fuente, estado, botones)

    elif estado["pantalla_actual"] == "jugando" and estado["estado_juego"] is not None:
        dibujar_juego(pantalla, estado["estado_juego"])
