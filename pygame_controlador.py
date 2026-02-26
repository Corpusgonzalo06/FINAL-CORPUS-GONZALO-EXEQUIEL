import random
import time
from manejo_mis_funciones import convertir_a_minusculas, agregar_elemento
from manejo_validaciones import limpiar_palabra, verificar_si_palabra_es_permitida ,verificar_palabra_usada


def ver_si_esta_jugando(estado):
    jugando = False
    if estado["estado"] == "jugando":
        jugando = True
    return jugando


def agregar_letra(estado, letra):
    if ver_si_esta_jugando(estado):
        letra_min = convertir_a_minusculas(letra)
        estado["palabra_actual"] = estado["palabra_actual"] + letra_min


def borrar_palabra(estado):
    if ver_si_esta_jugando(estado):
        estado["palabra_actual"] = ""


def mezclar_letras(estado):
    if ver_si_esta_jugando(estado):
        random.shuffle(estado["letras"])


def usar_comodin(estado, nombre_comodin):

    accion_valida = True

    if not ver_si_esta_jugando(estado):
        estado["mensaje"] = "⚠️ Acción inválida"
        accion_valida = False

    elif estado["comodines"][nombre_comodin] == False:
        estado["mensaje"] = "⚠️ Comodín no disponible"
        accion_valida = False

    if accion_valida:

        if nombre_comodin == "revelar_palabra_base":
            estado["mensaje"] = "💡 Palabra base: " + estado["palabra_base"]

        elif nombre_comodin == "eliminar_restricciones":
            estado["intento_libre"] = True
            estado["mensaje"] = "🚀 Tenés un intento libre"

        elif nombre_comodin == "pista_extra":
            letra = convertir_a_minusculas(estado["palabra_base"][0])
            estado["mensaje"] = "🕵️ Empieza con '" + letra + "'"

        estado["comodines"][nombre_comodin] = False



def procesar_intento(estado):

    if ver_si_esta_jugando(estado):

        palabra = estado["palabra_actual"]
        palabra_limpia = limpiar_palabra(palabra)

        palabra_correcta = verificar_si_palabra_es_permitida(
            palabra_limpia,
            estado["palabras_validas"]
        )

        palabra_repetida = verificar_palabra_usada(
            palabra_limpia,
            estado["palabras_encontradas"]
        )

        if palabra_correcta and not palabra_repetida:
            manejar_palabra_correcta(estado, palabra_limpia)

        elif palabra_correcta and palabra_repetida:
            estado["mensaje"] = " Ya la encontraste"
            estado["ultimo_feedback"] = "neutral"

        else:
            manejar_error(estado)

        estado["palabra_actual"] = ""


def manejar_palabra_correcta(estado, palabra):

    estado["palabras_encontradas"] = agregar_elemento(
        estado["palabras_encontradas"],
        palabra
    )

    puntos = len(palabra)
    estado["puntaje"] = estado["puntaje"] + puntos
    estado["mensaje"] = str(puntos) + " puntos!"
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
                letras = letras + letra + " "

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


def actualizar_tiempo(estado):

    if ver_si_esta_jugando(estado):

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
