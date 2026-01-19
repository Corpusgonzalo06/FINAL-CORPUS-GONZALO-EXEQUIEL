import random
import time
from comodines import crear_comodines_iniciales


# ==========================
# CREAR ESTADO INICIAL
# ==========================
def crear_estado_desde_palabras(palabra_base, lista_palabras, nivel=1, puntaje=0, vidas=3):
    pistas = []
    for palabra in lista_palabras:
        pistas.append("_ " * len(palabra))

    TIEMPO_POR_NIVEL = 180

    return {
        "nivel": nivel,
        "palabra_base": palabra_base,
        "letras": list(palabra_base),
        "pistas": pistas,
        "palabras_validas": lista_palabras,
        "palabras_encontradas": [],
        "palabra_actual": "",
        "puntaje": puntaje,
        "vidas": vidas,

        # estados: jugando | ganado | perdido
        "estado": "jugando",

        # comodines
        "comodines": crear_comodines_iniciales(),
        "intento_libre": False,

        # feedback visual
        "mensaje": "",
        "ultimo_feedback": "",

        # tiempo
        "tiempo_inicio": time.time(),
        "tiempo_limite": TIEMPO_POR_NIVEL,
        "tiempo_restante": TIEMPO_POR_NIVEL,

        # resumen final (se completa al terminar la partida)
        "nivel_maximo": None,
        "puntaje_final": None,
        "tiempo_final": None
    }


# ==========================
# ACCIONES BÁSICAS
# ==========================
def agregar_letra(estado, letra):
    if estado["estado"] == "jugando":
        estado["palabra_actual"] += letra.lower()


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
        return

    if estado["comodines"].get(nombre_comodin) is False:
        estado["mensaje"] = "⚠️ Comodín no disponible"
        return

    if nombre_comodin == "revelar_palabra_base":
        estado["mensaje"] = f"💡 Palabra base: {estado['palabra_base']}"

    elif nombre_comodin == "eliminar_restricciones":
        estado["intento_libre"] = True
        estado["mensaje"] = "🚀 Tenés un intento libre"

    elif nombre_comodin == "pista_extra":
        letra = estado["palabra_base"][0].lower()
        estado["mensaje"] = f"🕵️ Empieza con '{letra}'"

    estado["comodines"][nombre_comodin] = False


# ==========================
# ENVIAR PALABRA
# ==========================
def submit_palabra(estado):
    if estado["estado"] != "jugando":
        return

    palabra = estado["palabra_actual"]

    # PALABRA CORRECTA
    if palabra in estado["palabras_validas"]:
        if palabra not in estado["palabras_encontradas"]:
            estado["palabras_encontradas"].append(palabra)

            puntos = len(palabra)
            estado["puntaje"] += puntos

            estado["mensaje"] = f"🔥 +{puntos} puntos!"
            estado["ultimo_feedback"] = "bien"

            indice = estado["palabras_validas"].index(palabra)
            estado["pistas"][indice] = " ".join(palabra.upper())

            # NIVEL COMPLETADO
            if all("_" not in pista for pista in estado["pistas"]):
                estado["estado"] = "ganado"
                estado["mensaje"] = "🎉 ¡NIVEL COMPLETADO!"

                # resumen final
                estado["nivel_maximo"] = estado["nivel"]
                estado["puntaje_final"] = estado["puntaje"]
                estado["tiempo_final"] = estado["tiempo_restante"]

        else:
            estado["mensaje"] = "⚠️ Ya la encontraste"
            estado["ultimo_feedback"] = "neutral"

    # PALABRA INCORRECTA
    else:
        if estado["intento_libre"]:
            estado["mensaje"] = "🚀 Intento libre usado"
            estado["intento_libre"] = False
        else:
            estado["vidas"] -= 1
            estado["mensaje"] = "❌ Ups, probá otra"
            estado["ultimo_feedback"] = "mal"

        # SIN VIDAS
        if estado["vidas"] <= 0:
            estado["estado"] = "perdido"
            estado["mensaje"] = "💀 Te quedaste sin vidas"

            # resumen final
            estado["nivel_maximo"] = estado["nivel"]
            estado["puntaje_final"] = estado["puntaje"]
            estado["tiempo_final"] = estado["tiempo_restante"]

    estado["palabra_actual"] = ""


# ==========================
# TIEMPO
# ==========================
def actualizar_tiempo(estado):
    if estado["estado"] != "jugando":
        return

    transcurrido = time.time() - estado["tiempo_inicio"]
    restante = estado["tiempo_limite"] - int(transcurrido)
    estado["tiempo_restante"] = max(0, restante)

    if estado["tiempo_restante"] == 0:
        estado["estado"] = "perdido"
        estado["mensaje"] = "⏰ Tiempo agotado"

        # resumen final
        estado["nivel_maximo"] = estado["nivel"]
        estado["puntaje_final"] = estado["puntaje"]
        estado["tiempo_final"] = 0


# ==========================
# SIGUIENTE NIVEL (opcional)
# ==========================
def crear_siguiente_nivel(estado_actual, palabra_base, lista_palabras):
    nuevo_estado = crear_estado_desde_palabras(
        palabra_base,
        lista_palabras,
        estado_actual["nivel"] + 1,
        estado_actual["puntaje"],
        estado_actual["vidas"]
    )

    return nuevo_estado
