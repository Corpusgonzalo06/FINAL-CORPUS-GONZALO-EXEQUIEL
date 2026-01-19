import pygame
import sys

from usuarios import cargar_usuarios, guardar_usuarios
from estadisticas import inicializar_estadisticas
from pygame_estadisticas import mostrar_estadisticas
from palabras import PALABRAS

from pygame_controlador import *
from pygame_pantalla import dibujar_juego

# ==========================
# CONFIGURACIÓN GENERAL
# ==========================
pygame.init()

ANCHO, ALTO = 1600, 900
pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Pop A Word")

reloj = pygame.time.Clock()
FUENTE = pygame.font.SysFont("Brodway", 28)

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
FONDO_MENU = pygame.image.load("fondomenu.jpg")

def dibujar_fondo_menu():
    fondo = pygame.transform.scale(FONDO_MENU, (ANCHO, ALTO))
    pantalla.blit(fondo, (0, 0))
    overlay = pygame.Surface((ANCHO, ALTO), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 140))
    pantalla.blit(overlay, (0, 0))

def dibujar_texto(texto, x, y, color=BLANCO):
    render = FUENTE.render(texto, True, color)
    pantalla.blit(render, (x, y))

# ==========================
# USUARIOS
# ==========================
usuarios = cargar_usuarios("usuarios.json")

# ==========================
# ESTADOS
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
# RECTÁNGULOS
# ==========================
rect_usuario = pygame.Rect(650, 250, 300, 40)
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
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            guardar_usuarios(usuarios, "usuarios.json")
            pygame.quit()
            sys.exit()

        # -------- INICIO --------
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
                    pygame.quit()
                    sys.exit()

        # -------- LOGIN / REGISTRO --------
        elif pantalla_actual in ("login", "registro"):
            if evento.type == pygame.MOUSEBUTTONDOWN:
                if btn_atras.collidepoint(evento.pos):
                    pantalla_actual = "inicio"
                    mensaje = ""

                elif rect_usuario.collidepoint(evento.pos):
                    input_activo = "usuario"

                elif rect_contrasena.collidepoint(evento.pos):
                    input_activo = "contrasena"

                elif btn_submit.collidepoint(evento.pos):
                    if pantalla_actual == "login":
                        if usuario_input in usuarios and usuarios[usuario_input]["contraseña"] == contrasena_input:
                            clave_usuario = usuario_input
                            usuario_actual = usuarios[usuario_input]
                            inicializar_estadisticas(usuario_actual)
                            pantalla_actual = "menu"
                            mensaje = ""
                        else:
                            mensaje = "Usuario o contraseña incorrectos"
                    else:
                        if usuario_input in usuarios:
                            mensaje = "Ese usuario ya existe"
                        elif not usuario_input or not contrasena_input:
                            mensaje = "Campos incompletos"
                        else:
                            usuarios[usuario_input] = {"contraseña": contrasena_input}
                            inicializar_estadisticas(usuarios[usuario_input])
                            guardar_usuarios(usuarios, "usuarios.json")
                            pantalla_actual = "login"
                            mensaje = "Usuario creado ✔"

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

        # -------- MENU --------
        elif pantalla_actual == "menu":
            if evento.type == pygame.MOUSEBUTTONDOWN:
                if btn_jugar.collidepoint(evento.pos):
                    indice_palabra = 0
                    base = lista_bases[indice_palabra]

                    estado_juego = crear_estado_desde_palabras(
                        base,
                        PALABRAS[base],
                        nivel=1
                    )

                    estado_juego["usuario"] = clave_usuario
                    pantalla_actual = "jugando"

                elif btn_stats.collidepoint(evento.pos):
                    pantalla_actual = mostrar_estadisticas(pantalla, usuario_actual)

                elif btn_cerrar_sesion.collidepoint(evento.pos):
                    usuario_actual = None
                    clave_usuario = None
                    pantalla_actual = "inicio"

        # -------- JUGANDO --------
        elif pantalla_actual == "jugando" and estado_juego:
            actualizar_tiempo(estado_juego)

            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_BACKSPACE:
                    borrar_palabra(estado_juego)
                elif evento.key == pygame.K_RETURN:
                    submit_palabra(estado_juego)
                elif evento.unicode.isalpha():
                    agregar_letra(estado_juego, evento.unicode.lower())

            if evento.type == pygame.MOUSEBUTTONDOWN:
                for boton in estado_juego.get("botones", {}).values():
                    if boton.fue_clickeado(evento):
                        if boton.texto == "SHUFFLE":
                            mezclar_letras(estado_juego)
                        elif boton.texto == "CLEAR":
                            borrar_palabra(estado_juego)
                        elif boton.texto == "SUBMIT":
                            submit_palabra(estado_juego)

                for nombre, boton in estado_juego.get("botones_comodines", {}).items():
                    if boton.fue_clickeado(evento):
                        usar_comodin(estado_juego, nombre)

                if estado_juego["estado"] in ("ganado", "perdido"):
                    for boton in estado_juego.get("botones_fin", {}).values():
                        if boton.fue_clickeado(evento):

                            usuarios[clave_usuario]["puntos"] = estado_juego["puntaje"]
                            guardar_usuarios(usuarios, "usuarios.json")

                            if estado_juego["estado"] == "ganado" and estado_juego["nivel"] < NIVEL_MAXIMO:
                                indice_palabra += 1
                                base = lista_bases[indice_palabra]
                                estado_juego = crear_estado_desde_palabras(
                                    base,
                                    PALABRAS[base],
                                    nivel=estado_juego["nivel"] + 1,
                                    puntaje=estado_juego["puntaje"],
                                    vidas=estado_juego["vidas"]
                                )
                                estado_juego["usuario"] = clave_usuario
                            else:
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

    elif pantalla_actual in ("login", "registro"):
        titulo = "INICIAR SESIÓN" if pantalla_actual == "login" else "REGISTRO"

        pygame.draw.rect(pantalla, BLANCO, rect_usuario, 2)
        pygame.draw.rect(pantalla, BLANCO, rect_contrasena, 2)
        pygame.draw.rect(pantalla, AZUL, btn_submit)
        pygame.draw.rect(pantalla, AZUL, btn_atras)

        dibujar_texto(titulo, 680, 200)
        dibujar_texto("Usuario:", rect_usuario.x, rect_usuario.y - 30)
        dibujar_texto(usuario_input, rect_usuario.x + 10, rect_usuario.y + 5)

        dibujar_texto("Contraseña:", rect_contrasena.x, rect_contrasena.y - 30)
        dibujar_texto("*" * len(contrasena_input), rect_contrasena.x + 10, rect_contrasena.y + 5)

        dibujar_texto("CONFIRMAR", btn_submit.x + 80, btn_submit.y + 12)
        dibujar_texto("ATRÁS", btn_atras.x + 30, btn_atras.y + 10)
        dibujar_texto(mensaje, 650, 500, ROJO)

    elif pantalla_actual == "menu":
        if clave_usuario:
            texto = FUENTE.render(f"👋 Bienvenido, {clave_usuario}", True, BLANCO)
            rect = texto.get_rect(center=(ANCHO // 2, 80))
            pantalla.blit(texto, rect)

        pygame.draw.rect(pantalla, AZUL, btn_jugar)
        pygame.draw.rect(pantalla, AZUL, btn_stats)
        pygame.draw.rect(pantalla, ROJO, btn_cerrar_sesion)

        dibujar_texto("JUGAR", btn_jugar.x + 70, btn_jugar.y + 15)
        dibujar_texto("ESTADÍSTICAS", btn_stats.x + 30, btn_stats.y + 15)
        dibujar_texto("CERRAR SESIÓN", btn_cerrar_sesion.x + 20, btn_cerrar_sesion.y + 15)

    elif pantalla_actual == "jugando" and estado_juego:
        dibujar_juego(pantalla, estado_juego)

    pygame.display.update()
    reloj.tick(60)
