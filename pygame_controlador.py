import random
import time

from comodines import crear_comodines_iniciales
from mis_funciones import (
    convertir_a_minusculas,
    agregar_elemento
)

# ==========================
# CREAR ESTADO INICIAL
# ==========================
def crear_estado_desde_palabras(palabra_base, lista_palabras, nivel=1, puntaje=0, vidas=3):
    pistas = []
    i = 0
    while i < len(lista_palabras):
        palabra = lista_palabras[i]
        pistas = agregar_elemento(pistas, "_ " * len(palabra))
        i += 1

    letras = []
    i = 0
    while i < len(palabra_base):
        letras = agregar_elemento(letras, palabra_base[i])
        i += 1

    TIEMPO_POR_NIVEL = 180

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

        # stats de la partida
        "errores_nivel": 0,
        "tiempo_inicio": time.time(),

        "comodines": crear_comodines_iniciales(),
        "intento_libre": False,
        "mensaje": "",
        "ultimo_feedback": "",

        "tiempo_limite": TIEMPO_POR_NIVEL,
        "tiempo_restante": TIEMPO_POR_NIVEL,

        # resumen final
        "nivel_maximo": None,
        "puntaje_final": None,
        "tiempo_final": None
    }

    return estado


# ==========================
# ACCIONES BÁSICAS
# ==========================
def agregar_letra(estado, letra):
    if estado["estado"] == "jugando":
        letra_min = convertir_a_minusculas(letra)
        estado["palabra_actual"] = estado["palabra_actual"] + letra_min


def borrar_palabra(estado):
    if estado["estado"] == "jugando":
        estado["palabra_actual"] = ""


def mezclar_letras(estado):
    if estado["estado"] == "jugando":
        random.shuffle(estado["letras"])


# ==========================
# COMODINES
# ==========================
def usar_comodin(estado, nombre_comodin):
    if estado["estado"] != "jugando":
        estado["mensaje"] = "⚠️ Acción inválida"
        return

    if estado["comodines"][nombre_comodin] == False:
        estado["mensaje"] = "⚠️ Comodín no disponible"
        return

    if nombre_comodin == "revelar_palabra_base":
        estado["mensaje"] = "💡 Palabra base: " + estado["palabra_base"]

    elif nombre_comodin == "eliminar_restricciones":
        estado["intento_libre"] = True
        estado["mensaje"] = "🚀 Tenés un intento libre"

    elif nombre_comodin == "pista_extra":
        letra = convertir_a_minusculas(estado["palabra_base"][0])
        estado["mensaje"] = "🕵️ Empieza con '" + letra + "'"

    estado["comodines"][nombre_comodin] = False


# ==========================
# ENVIAR PALABRA
# ==========================
def submit_palabra(estado):
    if estado["estado"] != "jugando":
        return

    palabra = estado["palabra_actual"]
    palabra_correcta = False
    palabra_repetida = False

    i = 0
    while i < len(estado["palabras_validas"]):
        if palabra == estado["palabras_validas"][i]:
            palabra_correcta = True
        i += 1

    i = 0
    while i < len(estado["palabras_encontradas"]):
        if palabra == estado["palabras_encontradas"][i]:
            palabra_repetida = True
        i += 1

    if palabra_correcta and not palabra_repetida:
        estado["palabras_encontradas"] = agregar_elemento(
            estado["palabras_encontradas"],
            palabra
        )

        puntos = len(palabra)
        estado["puntaje"] = estado["puntaje"] + puntos
        estado["mensaje"] = "🔥 +" + str(puntos) + " puntos!"
        estado["ultimo_feedback"] = "bien"

        indice = 0
        while indice < len(estado["palabras_validas"]):
            if estado["palabras_validas"][indice] == palabra:
                letras = ""
                j = 0
                while j < len(palabra):
                    codigo = ord(palabra[j])
                    letras = letras + chr(codigo - 32) + " "
                    j += 1
                estado["pistas"][indice] = letras
            indice += 1

        nivel_completado = True
        i = 0
        while i < len(estado["pistas"]):
            if "_" in estado["pistas"][i]:
                nivel_completado = False
            i += 1

        if nivel_completado:
            estado["estado"] = "ganado"
            estado["mensaje"] = "🎉 ¡NIVEL COMPLETADO!"
            estado["nivel_maximo"] = estado["nivel"]
            estado["puntaje_final"] = estado["puntaje"]
            estado["tiempo_final"] = estado["tiempo_restante"]

    elif palabra_correcta and palabra_repetida:
        estado["mensaje"] = "⚠️ Ya la encontraste"
        estado["ultimo_feedback"] = "neutral"

    else:
        if estado["intento_libre"]:
            estado["mensaje"] = "🚀 Intento libre usado"
            estado["intento_libre"] = False
        else:
            estado["vidas"] = estado["vidas"] - 1
            estado["errores_nivel"] = estado["errores_nivel"] + 1
            estado["mensaje"] = "❌ Ups, probá otra"
            estado["ultimo_feedback"] = "mal"

        if estado["vidas"] <= 0:
            estado["estado"] = "perdido"
            estado["mensaje"] = "💀 Te quedaste sin vidas"
            estado["nivel_maximo"] = estado["nivel"]
            estado["puntaje_final"] = estado["puntaje"]
            estado["tiempo_final"] = estado["tiempo_restante"]

    estado["palabra_actual"] = ""


# ==========================
# TIEMPO
# ==========================
def actualizar_tiempo(estado):
    if estado["estado"] == "jugando":
        transcurrido = time.time() - estado["tiempo_inicio"]
        restante = estado["tiempo_limite"] - int(transcurrido)

        if restante < 0:
            restante = 0

        estado["tiempo_restante"] = restante

        if restante == 0:
            estado["estado"] = "perdido"
            estado["mensaje"] = "⏰ Tiempo agotado"
            estado["nivel_maximo"] = estado["nivel"]
            estado["puntaje_final"] = estado["puntaje"]
            estado["tiempo_final"] = 0
