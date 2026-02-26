import random
import time
from manejo_mis_funciones import agregar_elemento
from consola_comodines import crear_comodines_iniciales


# ==========================
# CREACIÓN DE ESTRUCTURAS BASE
# ==========================

def crear_pistas(lista_palabras):
    pistas = []
    for palabra in lista_palabras:
        pistas = agregar_elemento(pistas, "_ " * len(palabra))
    return pistas


def crear_letras_mezcladas(palabra_base):
    letras = []
    for letra in palabra_base:
        letras = agregar_elemento(letras, letra)

    random.shuffle(letras)
    return letras


def configurar_accesibilidad(estado, accesibilidad):
    estado["tiempo_por_nivel"] = 180
    estado["tdah"] = False
    estado["mensaje_inicial"] = ""

    # SIN .get()
    if accesibilidad is not None:
        if "tdah" in accesibilidad:
            if accesibilidad["tdah"] == True:
                estado["tdah"] = True
                estado["tiempo_por_nivel"] = 90
                estado["mensaje_inicial"] = "⚡ Modo rápido activado"


# ==========================
# CREAR ESTADO PRINCIPAL
# ==========================

def crear_estado_inicial(palabra_base, lista_palabras, nivel=1, puntaje=0, vidas=3, accesibilidad=None):

    pistas = crear_pistas(lista_palabras)
    letras = crear_letras_mezcladas(palabra_base)

    estado = {
        "nivel": nivel,
        "palabra_base": palabra_base,
        "letras": letras,
        "pistas": pistas,
        "palabras_validas": lista_palabras,
        "palabras_encontradas": [],
        "palabra_actual": "",
        "puntaje": puntaje,
        "vidas": vidas,
        "estado": "jugando",
        "errores_nivel": 0,
        "tiempo_inicio": time.time(),
        "tiempo_limite": 180,  # valor por defecto
        "tiempo_restante": 180,
        "tiempo_jugado": 0,
        "comodines": crear_comodines_iniciales(),
        "intento_libre": False,
        "mensaje": "",
        "ultimo_feedback": "",
        "tdah": False,
        "nivel_maximo": None,
        "puntaje_final": None,
        "tiempo_final": None,
        "pantalla_actual": "inicio",
        "usuario_actual": None,
        "tiempo_por_nivel": 180,
        "mensaje_inicial": ""
    }

    # aplicamos accesibilidad
    configurar_accesibilidad(estado, accesibilidad)

    return estado