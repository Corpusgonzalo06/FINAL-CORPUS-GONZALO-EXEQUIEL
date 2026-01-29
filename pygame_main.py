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

# ==========================
# SONIDOS
# ==========================
from pygame_sonidos import *

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


def dibujar_fondo_menu():
    """Dibuja el fondo del menú con un overlay oscuro."""
    fondo = pygame.transform.scale(FONDO_MENU, (ANCHO, ALTO))
    pantalla.blit(fondo, (0, 0))

    overlay = pygame.Surface((ANCHO, ALTO), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 120))
    pantalla.blit(overlay, (0, 0))


def dibujar_texto(texto, x, y, color=BLANCO):
    """Renderiza texto en pantalla."""
    render = FUENTE.render(texto, True, color)
    pantalla.blit(render, (x, y))

# ==========================
# USUARIOS
# ==========================
usuarios = cargar_usuarios("usuarios.json")

# ==========================
# ESTADOS GENERALES
# ==========================
pantalla_actual = "inicio"

usuario_input = ""
contrasena_input = ""
mensaje = ""

usuario_actual = None
clave_usuario = None
input_activo = "usuario"

estado_juego = None
indice_palabra = 0
lista_bases = list(PALABRAS.keys())

# ==========================
# RECTÁNGULOS (BOTONES / INPUTS)
# ==========================
btn_tdah = pygame.Rect(700, 560, 200, 55)
tdah_activo = False

rect_usuario = pygame.Rect(650, 270, 300, 40)
rect_contrasena = pygame.Rect(650, 360, 300, 40)

btn_login = pygame.Rect(700, 350, 200, 55)
btn_registro = pygame.Rect(700, 430, 200, 55)
btn_salir_juego = pygame.Rect(700, 550, 200, 55)

btn_submit = pygame.Rect(650, 430, 300, 50)

btn_jugar = pygame.Rect(700, 320, 200, 55)
btn_stats = pygame.Rect(700, 400, 200, 55)
btn_cerrar_sesion = pygame.Rect(700, 480, 200, 55)

btn_atras = pygame.Rect(30, 30, 140, 45)

# ==========================
# LOOP PRINCIPAL
# ==========================
while True:

    # ======================
    # EVENTOS
    # ======================
    for evento in pygame.event.get():

        # Salida del juego
        if evento.type == pygame.QUIT:
            guardar_usuarios(usuarios, "usuarios.json")
            detener_musica()
            pygame.quit()
            sys.exit()

        # ======================
        # PANTALLA INICIO
        # ======================
        if pantalla_actual == "inicio":
            if evento.type == pygame.MOUSEBUTTONDOWN:

                if btn_login.collidepoint(evento.pos):
                    usuario_input = ""
                    contrasena_input = ""
                    mensaje = ""
                    pantalla_actual = "login"

                elif btn_registro.collidepoint(evento.pos):
                    usuario_input = ""
                    contrasena_input = ""
                    mensaje = ""
                    pantalla_actual = "registro"

                elif btn_salir_juego.collidepoint(evento.pos):
                    guardar_usuarios(usuarios, "usuarios.json")
                    detener_musica()
                    pygame.quit()
                    sys.exit()

        # ======================
        # LOGIN / REGISTRO
        # ======================
        elif pantalla_actual in ["login", "registro"]:

            if evento.type == pygame.MOUSEBUTTONDOWN:

                if btn_atras.collidepoint(evento.pos):
                    pantalla_actual = "inicio"
                    mensaje = ""

                elif rect_usuario.collidepoint(evento.pos):
                    input_activo = "usuario"

                elif rect_contrasena.collidepoint(evento.pos):
                    input_activo = "contrasena"

                elif btn_submit.collidepoint(evento.pos):

                    # ----- LOGIN -----
                    if pantalla_actual == "login":
                        if (
                            usuario_input in usuarios
                            and usuarios[usuario_input]["contraseña"] == contrasena_input
                        ):
                            clave_usuario = usuario_input
                            usuario_actual = usuarios[usuario_input]
                            inicializar_estadisticas(usuario_actual)
                            pantalla_actual = "menu"
                            mensaje = ""
                        else:
                            mensaje = "Usuario o contraseña incorrectos"
                            reproducir_sonido(sonidos, "mal")

                    # ----- REGISTRO -----
                    else:
                        if usuario_input in usuarios:
                            mensaje = "Ese usuario ya existe"
                            reproducir_sonido(sonidos, "mal")

                        elif usuario_input == "" or contrasena_input == "":
                            mensaje = "Campos incompletos"
                            reproducir_sonido(sonidos, "mal")

                        else:
                            usuarios[usuario_input] = {"contraseña": contrasena_input}
                            inicializar_estadisticas(usuarios[usuario_input])
                            guardar_usuarios(usuarios, "usuarios.json")
                            pantalla_actual = "login"
                            mensaje = "Usuario creado ✔"
                            reproducir_sonido(sonidos, "bien")

            elif evento.type == pygame.KEYDOWN:

                if evento.key == pygame.K_BACKSPACE:
                    if input_activo == "usuario":
                        usuario_input = usuario_input[:-1]
                    else:
                        contrasena_input = contrasena_input[:-1]

                else:
                    if input_activo == "usuario":
                        usuario_input += evento.unicode
                    else:
                        contrasena_input += evento.unicode

        # ======================
        # MENU PRINCIPAL
        # ======================
        elif pantalla_actual == "menu":

            if evento.type == pygame.MOUSEBUTTONDOWN:

                if btn_tdah.collidepoint(evento.pos):
                    tdah_activo = not tdah_activo

                elif btn_jugar.collidepoint(evento.pos):
                    palabra_random = seleccionar_palabras_nivel(lista_bases, 1)
                    base = palabra_random[0]

                    accesibilidad_usuario = usuario_actual.get("accesibilidad", {})
                    accesibilidad_usuario["tdah"] = tdah_activo

                    estado_juego = crear_estado_desde_palabras(
                        base,
                        PALABRAS[base],
                        nivel=1,
                        accesibilidad=accesibilidad_usuario
                    )

                    estado_juego["usuario"] = clave_usuario
                    pantalla_actual = "jugando"

                elif btn_stats.collidepoint(evento.pos):
                    pantalla_actual = mostrar_estadisticas(pantalla, usuario_actual)

                elif btn_cerrar_sesion.collidepoint(evento.pos):
                    usuario_actual = None
                    clave_usuario = None
                    pantalla_actual = "inicio"

        # ======================
        # JUGANDO
        # ======================
        elif pantalla_actual == "jugando" and estado_juego is not None:

            actualizar_tiempo(estado_juego)

            # Cierre de partida
            if (
                estado_juego["estado"] in ["ganado", "perdido"]
                and not estado_juego.get("partida_cerrada", False)
            ):
                usuario = usuarios[clave_usuario]

                usuario["partidas_jugadas"] += 1
                usuario["puntos"] += estado_juego["puntaje_final"]

                completadas = len(estado_juego["palabras_encontradas"])
                total = len(estado_juego["palabras_validas"])

                usuario["palabras_completadas"] += completadas
                usuario["palabras_incompletas"] += total - completadas
                usuario["errores_totales_juego"] += estado_juego["errores_nivel"]

                tiempo_jugado = (
                    estado_juego["tiempo_limite"]
                    - estado_juego["tiempo_restante"]
                )
                usuario["tiempo_total"] += tiempo_jugado

                guardar_usuarios(usuarios, "usuarios.json")
                estado_juego["partida_cerrada"] = True

            # Entrada por teclado
            if evento.type == pygame.KEYDOWN:

                if evento.key == pygame.K_BACKSPACE:
                    borrar_palabra(estado_juego)

                elif evento.key == pygame.K_RETURN:
                    submit_palabra(estado_juego)

                    if estado_juego["ultimo_feedback"] == "bien":
                        reproducir_sonido(sonidos, "bien")
                    elif estado_juego["ultimo_feedback"] == "mal":
                        reproducir_sonido(sonidos, "mal")

                elif evento.unicode.isalpha():
                    agregar_letra(estado_juego, evento.unicode.lower())

            # Entrada por mouse
            if evento.type == pygame.MOUSEBUTTONDOWN:

                for boton in estado_juego["botones"].values():
                    if boton["rect"].collidepoint(evento.pos):

                        if boton["texto"] == "SHUFFLE":
                            mezclar_letras(estado_juego)
                        elif boton["texto"] == "CLEAR":
                            borrar_palabra(estado_juego)
                        elif boton["texto"] == "SUBMIT":
                            submit_palabra(estado_juego)

                for nombre, boton in estado_juego["botones_comodines"].items():
                    if boton["rect"].collidepoint(evento.pos):
                        usar_comodin(estado_juego, nombre)

                if estado_juego["estado"] in ["ganado", "perdido"]:
                    if "botones_fin" in estado_juego:
                        for boton in estado_juego["botones_fin"].values():
                            if boton["rect"].collidepoint(evento.pos):
                                pantalla_actual = "menu"
                                estado_juego = None

    # ==========================
    # DIBUJO
    # ==========================
    pantalla.fill((0, 0, 0))
    dibujar_fondo_menu()

    if pantalla_actual == "inicio":
        pygame.draw.rect(pantalla, AZUL, btn_login)
        pygame.draw.rect(pantalla, AZUL, btn_registro)
        pygame.draw.rect(pantalla, ROJO, btn_salir_juego)

        dibujar_texto("INICIAR SESIÓN", btn_login.x + 20, btn_login.y + 15)
        dibujar_texto("REGISTRARSE", btn_registro.x + 25, btn_registro.y + 15)
        dibujar_texto("SALIR", btn_salir_juego.x + 75, btn_salir_juego.y + 15)

    elif pantalla_actual in ["login", "registro"]:
        pygame.draw.rect(pantalla, BLANCO, rect_usuario, 2)
        pygame.draw.rect(pantalla, BLANCO, rect_contrasena, 2)
        pygame.draw.rect(pantalla, AZUL, btn_submit)
        pygame.draw.rect(pantalla, AZUL, btn_atras)

        dibujar_texto("Usuario:", rect_usuario.x, rect_usuario.y - 30)
        dibujar_texto(usuario_input, rect_usuario.x + 10, rect_usuario.y + 5)

        dibujar_texto("Contraseña:", rect_contrasena.x, rect_contrasena.y - 30)
        dibujar_texto("*" * len(contrasena_input), rect_contrasena.x + 10, rect_contrasena.y + 5)

        dibujar_texto("CONFIRMAR", btn_submit.x + 80, btn_submit.y + 12)
        dibujar_texto("ATRÁS", btn_atras.x + 30, btn_atras.y + 10)
        dibujar_texto(mensaje, 650, 500, ROJO)

    elif pantalla_actual == "menu":
        pygame.draw.rect(
            pantalla,
            AZUL if not tdah_activo else (60, 180, 90),
            btn_tdah
        )
        dibujar_texto("MODO-TDAH", btn_tdah.x + 60, btn_tdah.y + 15)

        pygame.draw.rect(pantalla, AZUL, btn_jugar)
        pygame.draw.rect(pantalla, AZUL, btn_stats)
        pygame.draw.rect(pantalla, ROJO, btn_cerrar_sesion)

        dibujar_texto("JUGAR", btn_jugar.x + 70, btn_jugar.y + 15)
        dibujar_texto("ESTADÍSTICAS", btn_stats.x + 30, btn_stats.y + 15)
        dibujar_texto("CERRAR SESIÓN", btn_cerrar_sesion.x + 20, btn_cerrar_sesion.y + 15)

    elif pantalla_actual == "jugando" and estado_juego is not None:
        dibujar_juego(pantalla, estado_juego)

    pygame.display.update()
    reloj.tick(60)
