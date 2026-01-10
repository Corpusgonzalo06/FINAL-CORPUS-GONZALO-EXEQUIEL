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

    TIEMPO_POR_NIVEL = 60

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

        # estados posibles: jugando | ganado | perdido
        "estado": "jugando",

        "comodines": crear_comodines_iniciales(),
        "intento_libre": False,
        "mensaje": "",

        # ⏱️ TIEMPO
        "tiempo_inicio": time.time(),
        "tiempo_limite": TIEMPO_POR_NIVEL,
        "tiempo_restante": TIEMPO_POR_NIVEL
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
        estado["mensaje"] = f"🕵️ Una palabra empieza con '{letra}'"

    estado["comodines"][nombre_comodin] = False


# ==========================
# ENVIAR PALABRA
# ==========================
def submit_palabra(estado):
    if estado["estado"] != "jugando":
        return

    palabra = estado["palabra_actual"]

    if palabra in estado["palabras_validas"]:
        if palabra not in estado["palabras_encontradas"]:
            estado["palabras_encontradas"].append(palabra)
            estado["puntaje"] += len(palabra)
            estado["mensaje"] = "✔ Palabra correcta"

            indice = estado["palabras_validas"].index(palabra)
            estado["pistas"][indice] = " ".join(palabra.upper())

            # 🔥 TODAS LAS PALABRAS COMPLETADAS → GANADO
            if all("_" not in pista for pista in estado["pistas"]):
                estado["estado"] = "ganado"
                estado["mensaje"] = "🎉 NIVEL COMPLETADO"
        else:
            estado["mensaje"] = "⚠️ Ya encontrada"
    else:
        if estado["intento_libre"]:
            estado["mensaje"] = "🚀 Intento libre usado"
            estado["intento_libre"] = False
        else:
            estado["vidas"] -= 1
            estado["mensaje"] = "❌ Palabra incorrecta"

        # 💀 SIN VIDAS → PERDIDO
        if estado["vidas"] <= 0:
            estado["estado"] = "perdido"
            estado["mensaje"] = "💀 Te quedaste sin vidas"

    estado["palabra_actual"] = ""


# ==========================
# TIEMPO
# ==========================
def actualizar_tiempo(estado):
    if estado["estado"] != "jugando":
        return

    tiempo_actual = time.time()
    transcurrido = tiempo_actual - estado["tiempo_inicio"]

    restante = estado["tiempo_limite"] - int(transcurrido)
    estado["tiempo_restante"] = max(0, restante)

    if estado["tiempo_restante"] == 0:
        estado["estado"] = "perdido"
        estado["mensaje"] = "⏰ Tiempo agotado"


# ==========================
# SIGUIENTE NIVEL
# ==========================
def crear_siguiente_nivel(estado_actual, palabra_base, lista_palabras):
    """
    Solo debe llamarse si el estado anterior fue 'ganado'
    """
    return crear_estado_desde_palabras(
        palabra_base,
        lista_palabras,
        estado_actual["nivel"] + 1,
        estado_actual["puntaje"],
        estado_actual["vidas"]
    )
