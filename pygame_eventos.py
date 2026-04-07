import pygame
import sys

from estadisticas import inicializar_estadisticas
from usuarios_datos import guardar_usuarios
from pygame_estadisticas import mostrar_estadisticas
from palabras import PALABRAS
from manejo_aleatoriedad import seleccionar_palabras_nivel
from pygame_botones import ver_boton_fue_clickeado
from pygame_sonidos import reproducir_sonido, detener_musica
from pygame_controlador import borrar_palabra,procesar_intento,agregar_letra,mezclar_letras,usar_comodin,actualizar_tiempo
from pygame_estado_juego import crear_estado_inicial


def iniciar_informacion_juego():
    estado_interfaz = {
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
    return estado_interfaz

def salir_del_juego(usuarios):
    guardar_usuarios(usuarios, "usuarios.json")
    detener_musica()
    pygame.quit()
    sys.exit()

def limpiar_inputs(estado_interfaz, pantalla_destino):
    estado_interfaz["usuario_input"] = ""
    estado_interfaz["contrasena_input"] = ""
    estado_interfaz["mensaje"] = ""
    estado_interfaz["pantalla_actual"] = pantalla_destino

def eventos_inicio(evento, estado_interfaz,botones,usuarios):
    if evento.type == pygame.MOUSEBUTTONDOWN:
        if botones["btn_login"].collidepoint(evento.pos):
         limpiar_inputs(estado_interfaz, "login")

        elif botones["btn_registro"].collidepoint(evento.pos):
         limpiar_inputs(estado_interfaz, "registro")


        elif botones["btn_salir_juego"].collidepoint(evento.pos):
            salir_del_juego(usuarios)

            
    return estado_interfaz

def mostrar_error(estado_interfaz, sonidos, mensaje):
    estado_interfaz["mensaje"] = mensaje
    reproducir_sonido(sonidos, "mal")

def manejar_teclado_login(evento, estado):
    campo = estado["input_activo"] + "_input"

    if evento.key == pygame.K_BACKSPACE:
        estado[campo] = estado[campo][:-1]
    else:
        estado[campo] += evento.unicode


def procesar_login(estado_interfaz, usuarios, sonidos):

    usuario_input = estado_interfaz["usuario_input"]
    contrasena_input = estado_interfaz["contrasena_input"]

    if usuario_input in usuarios and usuarios[usuario_input]["contraseña"] == contrasena_input:

        estado_interfaz["clave_usuario"] = usuario_input
        estado_interfaz["usuario_actual"] = usuarios[usuario_input]
        inicializar_estadisticas(estado_interfaz["usuario_actual"])
        estado_interfaz["pantalla_actual"] = "menu"
        estado_interfaz["mensaje"] = ""

    else:
        mostrar_error(estado_interfaz, sonidos, "Usuario o contraseña incorrectos")

def procesar_registro(estado_interfaz, usuarios, sonidos):

    usuario_input = estado_interfaz["usuario_input"]
    contrasena_input = estado_interfaz["contrasena_input"]

    if usuario_input in usuarios:
        mostrar_error(estado_interfaz, sonidos, "Ese usuario ya existe")

    elif usuario_input == "" or contrasena_input == "":
        mostrar_error(estado_interfaz, sonidos, "Campos incompletos")

    else:
        usuarios[usuario_input] = {"contraseña": contrasena_input}

        inicializar_estadisticas(usuarios[usuario_input])
        guardar_usuarios(usuarios, "usuarios.json")

        estado_interfaz["pantalla_actual"] = "login"
        estado_interfaz["mensaje"] = "Usuario creado ✔"
        reproducir_sonido(sonidos, "bien")

def eventos_login_registro(evento, estado_interfaz, usuarios, sonidos, botones):

    if evento.type == pygame.MOUSEBUTTONDOWN:

        if botones["btn_atras"].collidepoint(evento.pos):
            estado_interfaz["pantalla_actual"] = "inicio"
            estado_interfaz["mensaje"] = ""

        elif botones["rect_usuario"].collidepoint(evento.pos):
            estado_interfaz["input_activo"] = "usuario"

        elif botones["rect_contrasena"].collidepoint(evento.pos):
            estado_interfaz["input_activo"] = "contrasena"

        elif botones["btn_submit"].collidepoint(evento.pos):

            if estado_interfaz["pantalla_actual"] == "login":
                procesar_login(estado_interfaz, usuarios, sonidos)
            else:
                procesar_registro(estado_interfaz, usuarios, sonidos)

    elif evento.type == pygame.KEYDOWN:
        manejar_teclado_login(evento, estado_interfaz)

    return estado_interfaz

def iniciar_partida(estado_interfaz, lista_bases):
    palabra_random = seleccionar_palabras_nivel(lista_bases, 1)
    base = palabra_random[0]

    # SIN .get()
    if "accesibilidad" in estado_interfaz["usuario_actual"]:
        accesibilidad = estado_interfaz["usuario_actual"]["accesibilidad"]
    else:
        accesibilidad = {}

    accesibilidad["tdah"] = estado_interfaz["tdah_activo"]
    estado_interfaz["usuario_actual"]["accesibilidad"] = accesibilidad

    estado_interfaz["estado_juego"] = crear_estado_inicial(
        base,
        PALABRAS[base],
        nivel=1,
        accesibilidad=accesibilidad
    )

    estado_interfaz["estado_juego"]["usuario"] = estado_interfaz["clave_usuario"]
    estado_interfaz["pantalla_actual"] = "jugando"

    return estado_interfaz

def eventos_menu(evento, estado_interfaz, botones, lista_bases, pantalla):
    if evento.type == pygame.MOUSEBUTTONDOWN:

        if botones["btn_tdah"].collidepoint(evento.pos):
            estado_interfaz["tdah_activo"] = not estado_interfaz["tdah_activo"]

        elif botones["btn_jugar"].collidepoint(evento.pos):
            estado_interfaz = iniciar_partida(estado_interfaz, lista_bases)

        elif botones["btn_stats"].collidepoint(evento.pos):
            estado_interfaz["pantalla_actual"] = mostrar_estadisticas(
                pantalla, estado_interfaz["usuario_actual"]
            )

        elif botones["btn_cerrar_sesion"].collidepoint(evento.pos):
            estado_interfaz["usuario_actual"] = None
            estado_interfaz["clave_usuario"] = None
            estado_interfaz["pantalla_actual"] = "inicio"

    return estado_interfaz

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

def eventos_jugando(evento, estado_interfaz, usuarios, sonidos):

    estado_juego = estado_interfaz["estado_juego"]
    clave_usuario = estado_interfaz["clave_usuario"]

    if estado_juego is None:
        return estado_interfaz

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
                estado_interfaz["pantalla_actual"] = "menu"
                estado_interfaz["estado_juego"] = None

    return estado_interfaz


def manejar_eventos(estado_interfaz, usuarios, sonidos, botones, lista_bases, pantalla):
    for evento in pygame.event.get():

        if evento.type == pygame.QUIT:
            salir_del_juego(usuarios)

        if estado_interfaz["pantalla_actual"] == "inicio":
            estado_interfaz = eventos_inicio(evento, estado_interfaz, botones, usuarios)

        elif estado_interfaz["pantalla_actual"] in ["login", "registro"]:
            estado_interfaz = eventos_login_registro(evento, estado_interfaz, usuarios, sonidos, botones)

        elif estado_interfaz["pantalla_actual"] == "menu":
            estado_interfaz = eventos_menu(evento, estado_interfaz, botones, lista_bases, pantalla)

        elif estado_interfaz["pantalla_actual"] == "jugando":
            estado_interfaz = eventos_jugando(evento, estado_interfaz, usuarios, sonidos)

    return estado_interfaz
