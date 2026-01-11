import pygame
import sys
from usuarios import cargar_usuarios, guardar_usuarios
from estadisticas import inicializar_estadisticas
from palabras import PALABRAS
from pygame_controlador import *
from pygame_pantalla import dibujar_juego
from pygame_botones import crear_botones_fin_juego  # <- necesario para fin de juego

# ==========================
# CONFIGURACIÓN GENERAL
# ==========================
pygame.init()

ANCHO, ALTO = 1600, 900
pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Pop A Word")

reloj = pygame.time.Clock()
FUENTE = pygame.font.SysFont("arial", 28)

BLANCO = (255, 255, 255)
GRIS = (40, 40, 40)
AZUL = (70, 130, 180)
ROJO = (180, 60, 60)

# ==========================
# CARGA DE USUARIOS
# ==========================
usuarios = cargar_usuarios("usuarios.json")

# ==========================
# ESTADO GENERAL
# ==========================
pantalla_actual = "inicio"

usuario_input = ""
contrasena_input = ""
mensaje = ""

usuario_actual = None
clave_usuario = None
input_activo = "usuario"

# ==========================
# ESTADO DEL JUEGO
# ==========================
estado_juego = None
indice_palabra = 0
lista_bases = list(PALABRAS.keys())

# ==========================
# RECTÁNGULOS
# ==========================
rect_usuario = pygame.Rect(650, 300, 300, 40)
rect_contrasena = pygame.Rect(650, 360, 300, 40)

btn_login = pygame.Rect(700, 350, 200, 55)
btn_registro = pygame.Rect(700, 430, 200, 55)
btn_salir_juego = pygame.Rect(700, 550, 200, 55)  # nuevo botón salir desde inicio

btn_submit = pygame.Rect(650, 430, 300, 50)

btn_jugar = pygame.Rect(700, 320, 200, 55)
btn_stats = pygame.Rect(700, 400, 200, 55)
btn_cerrar_sesion = pygame.Rect(700, 480, 200, 55)  # reemplaza salir en menú
btn_volver = pygame.Rect(700, 650, 240, 50)

btn_atras = pygame.Rect(30, 30, 140, 45)

# ==========================
# FUNCIONES DE DIBUJO
# ==========================
def dibujar_texto(texto, x, y, color=BLANCO):
    render = FUENTE.render(texto, True, color)
    pantalla.blit(render, (x, y))


def dibujar_inicio():
    pantalla.fill(GRIS)
    dibujar_texto("POP A WORD", 720, 200)

    pygame.draw.rect(pantalla, AZUL, btn_login)
    pygame.draw.rect(pantalla, AZUL, btn_registro)
    pygame.draw.rect(pantalla, ROJO, btn_salir_juego)

    dibujar_texto("INICIAR SESIÓN", 720, 365)
    dibujar_texto("REGISTRARSE", 720, 445)
    dibujar_texto("SALIR DEL JUEGO", 700, 555)


def dibujar_login():
    pantalla.fill(GRIS)
    dibujar_texto("LOGIN", 760, 200)
    dibujar_texto("Usuario:", 550, 310)
    dibujar_texto("Contraseña:", 520, 370)

    pygame.draw.rect(pantalla, BLANCO, rect_usuario, 2)
    pygame.draw.rect(pantalla, BLANCO, rect_contrasena, 2)
    pygame.draw.rect(pantalla, AZUL, btn_submit)

    dibujar_texto(usuario_input, 660, 308)
    dibujar_texto("*" * len(contrasena_input), 660, 368)
    dibujar_texto("INGRESAR", 740, 445)

    dibujar_texto(mensaje, 650, 500)

    pygame.draw.rect(pantalla, ROJO, btn_atras)
    dibujar_texto("VOLVER", 60, 42)


def dibujar_registro():
    pantalla.fill(GRIS)
    dibujar_texto("REGISTRO", 740, 200)
    dibujar_texto("Nuevo usuario:", 490, 310)
    dibujar_texto("Contraseña:", 520, 370)

    pygame.draw.rect(pantalla, BLANCO, rect_usuario, 2)
    pygame.draw.rect(pantalla, BLANCO, rect_contrasena, 2)
    pygame.draw.rect(pantalla, AZUL, btn_submit)

    dibujar_texto(usuario_input, 660, 308)
    dibujar_texto("*" * len(contrasena_input), 660, 368)
    dibujar_texto("CREAR CUENTA", 715, 445)

    dibujar_texto(mensaje, 650, 500)

    pygame.draw.rect(pantalla, ROJO, btn_atras)
    dibujar_texto("VOLVER", 60, 42)


def dibujar_menu():
    pantalla.fill(GRIS)
    dibujar_texto(f"Bienvenido {clave_usuario}", 680, 200)

    pygame.draw.rect(pantalla, AZUL, btn_jugar)
    pygame.draw.rect(pantalla, AZUL, btn_stats)
    pygame.draw.rect(pantalla, ROJO, btn_cerrar_sesion)

    dibujar_texto("NUEVA PARTIDA", 720, 335)
    dibujar_texto("ESTADÍSTICAS", 720, 415)
    dibujar_texto("CERRAR SESIÓN", 710, 495)


def dibujar_estadisticas():
    pantalla.fill(GRIS)
    dibujar_texto("ESTADÍSTICAS", 720, 200)

    y = 260
    for clave, valor in usuario_actual.items():
        if clave != "contraseña":
            dibujar_texto(f"{clave}: {valor}", 600, y)
            y += 35

    pygame.draw.rect(pantalla, AZUL, btn_volver)
    dibujar_texto("VOLVER AL MENÚ", 715, 665)


# ==========================
# LOOP PRINCIPAL
# ==========================
while True:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            guardar_usuarios("usuarios.json", usuarios)
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
                    guardar_usuarios("usuarios.json", usuarios)
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
                        if (
                            usuario_input in usuarios and
                            usuarios[usuario_input]["contraseña"] == contrasena_input
                        ):
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
                        elif usuario_input == "" or contrasena_input == "":
                            mensaje = "Campos incompletos"
                        else:
                            usuarios[usuario_input] = {"contraseña": contrasena_input}
                            inicializar_estadisticas(usuarios[usuario_input])
                            guardar_usuarios("usuarios.json", usuarios)
                            pantalla_actual = "login"
                            mensaje = "Usuario creado ✔"

            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_BACKSPACE:
                    if input_activo == "usuario":
                        usuario_input = usuario_input[:-1]
                    else:
                        contrasena_input = contrasena_input[:-1]

                elif evento.key == pygame.K_RETURN:
                    pygame.event.post(
                        pygame.event.Event(pygame.MOUSEBUTTONDOWN, pos=btn_submit.center)
                    )

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
                    estado_juego = crear_estado_desde_palabras(base, PALABRAS[base])
                    pantalla_actual = "jugando"

                elif btn_stats.collidepoint(evento.pos):
                    pantalla_actual = "estadisticas"

                elif btn_cerrar_sesion.collidepoint(evento.pos):
                    usuario_actual = None
                    clave_usuario = None
                    pantalla_actual = "inicio"

        # -------- JUGANDO --------
        elif pantalla_actual == "jugando" and estado_juego:
            actualizar_tiempo(estado_juego)

            # ---- TECLADO ----
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_BACKSPACE:
                    borrar_palabra(estado_juego)
                elif evento.key == pygame.K_RETURN:
                    submit_palabra(estado_juego)
                else:
                    letra = evento.unicode.lower()
                    if letra.isalpha():
                        agregar_letra(estado_juego, letra)

            # ---- MOUSE CLICK ----
            if evento.type == pygame.MOUSEBUTTONDOWN:
                # ---- BOTONES PRINCIPALES ----
                for nombre, boton in estado_juego["botones"].items():
                    if boton.fue_clickeado(evento):
                        if nombre == "shuffle":
                            mezclar_letras(estado_juego)
                        elif nombre == "clear":
                            borrar_palabra(estado_juego)
                        elif nombre == "submit":
                            submit_palabra(estado_juego)

                # ---- BOTONES DE COMODINES ----
                for nombre, boton in estado_juego["botones_comodines"].items():
                    if boton.fue_clickeado(evento):
                        usar_comodin(estado_juego, nombre)

                # ---- BOTONES DE FIN DE JUEGO ----
                if estado_juego["estado"] in ("ganado", "perdido"):
                    if "botones_fin" not in estado_juego:
                        estado_juego["botones_fin"] = crear_botones_fin_juego()

                    for nombre, boton in estado_juego["botones_fin"].items():
                        if boton.fue_clickeado(evento):
                            if nombre == "siguiente" and estado_juego["estado"] == "ganado":
                                indice_palabra += 1
                                if indice_palabra < len(lista_bases):
                                    base = lista_bases[indice_palabra]
                                    estado_juego = crear_estado_desde_palabras(base, PALABRAS[base])
                                else:
                                    pantalla_actual = "menu"
                            elif nombre == "menu":
                                pantalla_actual = "menu"

        # -------- ESTADÍSTICAS --------
        elif pantalla_actual == "estadisticas":
            if evento.type == pygame.MOUSEBUTTONDOWN:
                if btn_volver.collidepoint(evento.pos):
                    pantalla_actual = "menu"

    # ==========================
    # DIBUJO GENERAL
    # ==========================
    if pantalla_actual == "inicio":
        dibujar_inicio()
    elif pantalla_actual == "login":
        dibujar_login()
    elif pantalla_actual == "registro":
        dibujar_registro()
    elif pantalla_actual == "menu":
        dibujar_menu()
    elif pantalla_actual == "jugando" and estado_juego:
        dibujar_juego(pantalla, estado_juego)
    elif pantalla_actual == "estadisticas":
        dibujar_estadisticas()

    pygame.display.update()
    reloj.tick(60)
