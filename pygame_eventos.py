import pygame
import sys

from estadisticas import inicializar_estadisticas
from usuarios import guardar_usuarios
from pygame_estadisticas import mostrar_estadisticas
from palabras import PALABRAS
from manejo_aleatoriedad import seleccionar_palabras_nivel
from pygame_botones import ver_boton_fue_clickeado
from pygame_sonidos import reproducir_sonido, detener_musica
from pygame_controlador import borrar_palabra,procesar_intento,agregar_letra,mezclar_letras,usar_comodin,actualizar_tiempo
from pygame_estado_juego import crear_estado_inicial


def iniciar_informacion_juego():
    estado = {
        "pantalla_actual": "inicio",
        "usuario_input": "",
        "contrasena_input": "",
        "mensaje": "",
        "usuario_actual": None,
        "clave_usuario": None,
        "input_activo": "usuario",
        "estado_juego": None,
        "tdah_activo": False
    }
    return estado

def salir_del_juego(usuarios):
    guardar_usuarios(usuarios, "usuarios.json")
    detener_musica()
    pygame.quit()
    sys.exit()

def limpiar_inputs(estado, pantalla_destino):
    estado["usuario_input"] = ""
    estado["contrasena_input"] = ""
    estado["mensaje"] = ""
    estado["pantalla_actual"] = pantalla_destino

def eventos_inicio(evento, estado,botones,usuarios):
    if evento.type == pygame.MOUSEBUTTONDOWN:
        if botones["btn_login"].collidepoint(evento.pos):
         limpiar_inputs(estado, "login")

        elif botones["btn_registro"].collidepoint(evento.pos):
         limpiar_inputs(estado, "registro")


        elif botones["btn_salir_juego"].collidepoint(evento.pos):
            salir_del_juego(usuarios)

            
    return estado

def mostrar_error(estado, sonidos, mensaje):
    estado["mensaje"] = mensaje
    reproducir_sonido(sonidos, "mal")

def manejar_teclado_login(evento, estado):
    campo = estado["input_activo"] + "_input"

    if evento.key == pygame.K_BACKSPACE:
        estado[campo] = estado[campo][:-1]
    else:
        estado[campo] += evento.unicode


def procesar_login(estado, usuarios, sonidos):

    usuario_input = estado["usuario_input"]
    contrasena_input = estado["contrasena_input"]

    if usuario_input in usuarios and usuarios[usuario_input]["contraseña"] == contrasena_input:

        estado["clave_usuario"] = usuario_input
        estado["usuario_actual"] = usuarios[usuario_input]
        inicializar_estadisticas(estado["usuario_actual"])
        estado["pantalla_actual"] = "menu"
        estado["mensaje"] = ""

    else:
        mostrar_error(estado, sonidos, "Usuario o contraseña incorrectos")

def procesar_registro(estado, usuarios, sonidos):

    usuario_input = estado["usuario_input"]
    contrasena_input = estado["contrasena_input"]

    if usuario_input in usuarios:
        mostrar_error(estado, sonidos, "Ese usuario ya existe")

    elif usuario_input == "" or contrasena_input == "":
        mostrar_error(estado, sonidos, "Campos incompletos")

    else:
        usuarios[usuario_input] = {"contraseña": contrasena_input}

        inicializar_estadisticas(usuarios[usuario_input])
        guardar_usuarios(usuarios, "usuarios.json")

        estado["pantalla_actual"] = "login"
        estado["mensaje"] = "Usuario creado ✔"
        reproducir_sonido(sonidos, "bien")

def eventos_login_registro(evento, estado, usuarios, sonidos, botones):

    if evento.type == pygame.MOUSEBUTTONDOWN:

        if botones["btn_atras"].collidepoint(evento.pos):
            estado["pantalla_actual"] = "inicio"
            estado["mensaje"] = ""

        elif botones["rect_usuario"].collidepoint(evento.pos):
            estado["input_activo"] = "usuario"

        elif botones["rect_contrasena"].collidepoint(evento.pos):
            estado["input_activo"] = "contrasena"

        elif botones["btn_submit"].collidepoint(evento.pos):

            if estado["pantalla_actual"] == "login":
                procesar_login(estado, usuarios, sonidos)
            else:
                procesar_registro(estado, usuarios, sonidos)

    elif evento.type == pygame.KEYDOWN:
        manejar_teclado_login(evento, estado)

    return estado

def iniciar_partida(estado, lista_bases):
    palabra_random = seleccionar_palabras_nivel(lista_bases, 1)
    base = palabra_random[0]

    # SIN .get()
    if "accesibilidad" in estado["usuario_actual"]:
        accesibilidad = estado["usuario_actual"]["accesibilidad"]
    else:
        accesibilidad = {}

    accesibilidad["tdah"] = estado["tdah_activo"]
    estado["usuario_actual"]["accesibilidad"] = accesibilidad

    estado["estado_juego"] = crear_estado_inicial(
        base,
        PALABRAS[base],
        nivel=1,
        accesibilidad=accesibilidad
    )

    estado["estado_juego"]["usuario"] = estado["clave_usuario"]
    estado["pantalla_actual"] = "jugando"

    return estado
def eventos_menu(evento, estado, botones, lista_bases, pantalla):
    if evento.type == pygame.MOUSEBUTTONDOWN:

        if botones["btn_tdah"].collidepoint(evento.pos):
            estado["tdah_activo"] = not estado["tdah_activo"]

        elif botones["btn_jugar"].collidepoint(evento.pos):
            estado = iniciar_partida(estado, lista_bases)

        elif botones["btn_stats"].collidepoint(evento.pos):
            estado["pantalla_actual"] = mostrar_estadisticas(
                pantalla, estado["usuario_actual"]
            )

        elif botones["btn_cerrar_sesion"].collidepoint(evento.pos):
            estado["usuario_actual"] = None
            estado["clave_usuario"] = None
            estado["pantalla_actual"] = "inicio"

    return estado

def cerrar_partida(estado_juego, usuarios, clave_usuario):
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

def eventos_jugando(evento, estado, usuarios, sonidos):

    estado_juego = estado["estado_juego"]
    clave_usuario = estado["clave_usuario"]

    if estado_juego is None:
        return estado

    actualizar_tiempo(estado_juego)

    # ================= CIERRE DE PARTIDA =================
    if (estado_juego["estado"] in ["ganado", "perdido"] and ("partida_cerrada" not in estado_juego or estado_juego["partida_cerrada"] == False)):
        cerrar_partida(estado_juego, usuarios, clave_usuario)

    # ================= TECLADO =================
    if evento.type == pygame.KEYDOWN:

        if evento.key == pygame.K_BACKSPACE:
            borrar_palabra(estado_juego)

        elif evento.key == pygame.K_RETURN:
            procesar_intento(estado_juego)

            if estado_juego["ultimo_feedback"] == "bien":
                reproducir_sonido(sonidos, "bien")
            elif estado_juego["ultimo_feedback"] == "mal":
                reproducir_sonido(sonidos, "mal")

        elif evento.unicode.isalpha():
            agregar_letra(estado_juego, evento.unicode.lower())

    # ================= BOTONES NORMALES =================
    for boton in estado_juego["botones"].values():
        if ver_boton_fue_clickeado(boton, evento):

            if boton["texto"] == "SHUFFLE":
                mezclar_letras(estado_juego)

            elif boton["texto"] == "CLEAR":
                borrar_palabra(estado_juego)

            elif boton["texto"] == "SUBMIT":
                procesar_intento(estado_juego)

    # ================= COMODINES =================
    for nombre, boton in estado_juego["botones_comodines"].items():
        if ver_boton_fue_clickeado(boton, evento):
            usar_comodin(estado_juego, nombre)

    # ================= BOTONES FIN =================
    if (estado_juego["estado"] in ["ganado", "perdido"] and "botones_fin" in estado_juego):
        for boton in estado_juego["botones_fin"].values():
            if ver_boton_fue_clickeado(boton, evento):
                estado["pantalla_actual"] = "menu"
                estado["estado_juego"] = None

    return estado


def manejar_eventos(estado, usuarios, sonidos, botones, lista_bases, pantalla):
    for evento in pygame.event.get():

        if evento.type == pygame.QUIT:
            salir_del_juego(usuarios)

        if estado["pantalla_actual"] == "inicio":
            estado = eventos_inicio(evento, estado, botones, usuarios)

        elif estado["pantalla_actual"] in ["login", "registro"]:
            estado = eventos_login_registro(evento, estado, usuarios, sonidos, botones)

        elif estado["pantalla_actual"] == "menu":
            estado = eventos_menu(evento, estado, botones, lista_bases, pantalla)

        elif estado["pantalla_actual"] == "jugando":
            estado = eventos_jugando(evento, estado, usuarios, sonidos)

    return estado
