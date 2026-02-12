import random
import time

from mis_funciones import convertir_a_minusculas, agregar_elemento
from comodines import crear_comodines_iniciales


# ==========================
# CREAR ESTADO DEL JUEGO
# ==========================
def crear_estado_inicial(
    palabra_base,
    lista_palabras,
    nivel=1,
    puntaje=0,
    vidas=3,
    accesibilidad=None
):
    pistas = []
    for palabra in lista_palabras:
        pistas = agregar_elemento(pistas, "_ " * len(palabra))

    letras = []
    for letra in palabra_base:
        letras = agregar_elemento(letras, letra)

    random.shuffle(letras)

    tiempo_por_nivel = 180

    tdah = False
    mensaje_inicial = ""

    if accesibilidad is not None:
        tdah = accesibilidad.get("tdah", False)
        if tdah:
            tiempo_por_nivel = 90
            mensaje_inicial = "⚡ Modo rápido activado"

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
        "tiempo_limite": tiempo_por_nivel,
        "tiempo_restante": tiempo_por_nivel,
        "tiempo_jugado": 0,

        "comodines": crear_comodines_iniciales(),
        "intento_libre": False,

        "mensaje": mensaje_inicial,
        "ultimo_feedback": "",

        "tdah": tdah,

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

    palabra_correcta = es_palabra_valida(estado, palabra)
    palabra_repetida = ya_fue_encontrada(estado, palabra)

    if palabra_correcta and not palabra_repetida:
        manejar_palabra_correcta(estado, palabra)

    elif palabra_correcta and palabra_repetida:
        estado["mensaje"] = "⚠️ Ya la encontraste"
        estado["ultimo_feedback"] = "neutral"

    else:
        manejar_error(estado)

    estado["palabra_actual"] = ""


# ==========================
# FUNCIONES AUXILIARES
# ==========================
def es_palabra_valida(estado, palabra):
    valida = False
    for palabra_valida in estado["palabras_validas"]:
        if palabra == palabra_valida:
            valida = True
    return valida


def ya_fue_encontrada(estado, palabra):
    repetida = False
    for encontrada in estado["palabras_encontradas"]:
        if palabra == encontrada:
            repetida = True
    return repetida


def manejar_palabra_correcta(estado, palabra):
    estado["palabras_encontradas"] = agregar_elemento(
        estado["palabras_encontradas"],
        palabra
    )

    puntos = len(palabra)
    estado["puntaje"] = estado["puntaje"] + puntos
    estado["mensaje"] = f"🔥 +{puntos} puntos!"
    estado["ultimo_feedback"] = "bien"

    actualizar_pistas(estado, palabra)
    verificar_nivel_completo(estado)


def manejar_error(estado):
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


def actualizar_pistas(estado, palabra):
    for i in range(len(estado["palabras_validas"])):
        if estado["palabras_validas"][i] == palabra:
            letras = ""
            for letra in palabra:
                letras = letras + chr(ord(letra) - 32) + " "
            estado["pistas"][i] = letras


def verificar_nivel_completo(estado):
    nivel_completado = True
    for pista in estado["pistas"]:
        if "_" in pista:
            nivel_completado = False

    if nivel_completado:
        estado["estado"] = "ganado"
        estado["mensaje"] = "🎉 ¡NIVEL COMPLETADO!"
        estado["nivel_maximo"] = estado["nivel"]
        estado["puntaje_final"] = estado["puntaje"]
        estado["tiempo_final"] = estado["tiempo_restante"]


# ==========================
# TIEMPO
# ==========================
def actualizar_tiempo(estado):
    if estado["estado"] == "jugando":
        transcurrido = int(time.time() - estado["tiempo_inicio"])

        estado["tiempo_jugado"] = transcurrido

        restante = estado["tiempo_limite"] - transcurrido
        if restante < 0:
            restante = 0

        estado["tiempo_restante"] = restante

        if restante == 0:
            estado["estado"] = "perdido"
            estado["mensaje"] = "⏰ Tiempo agotado"
            estado["nivel_maximo"] = estado["nivel"]
            estado["puntaje_final"] = estado["puntaje"]
            estado["tiempo_final"] = estado["tiempo_jugado"]
