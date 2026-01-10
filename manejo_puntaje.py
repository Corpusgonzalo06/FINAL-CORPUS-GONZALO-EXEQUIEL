import time
def calcular_puntos_por_palabra(palabra: str, tiempo_respuesta: float) -> int:
    """
    Calcula los puntos obtenidos según la palabra ingresada y el tiempo de respuesta.

    PARÁMETROS:
        palabra (str): Palabra ingresada por el usuario.
        tiempo_respuesta (float): Tiempo en segundos que tardó el usuario en responder.

    RETORNO:
        int: Cantidad total de puntos otorgados por la palabra.
    """
    puntos = len(palabra)

    if len(palabra) > 4:
        puntos += 2

    if tiempo_respuesta < 5:
        puntos += 3
    elif tiempo_respuesta < 10:
        puntos += 1

    return puntos


def sumar_puntos_por_acierto(usuario: dict, puntos: int) -> None:
    """
    Suma los puntos obtenidos por un acierto y actualiza las estadísticas del usuario.

    PARÁMETROS:
        usuario (dict): Diccionario que contiene los datos del usuario.
        puntos (int): Cantidad de puntos ganados por la palabra acertada.

    RETORNO:
        None
    """
    usuario["palabras_acertadas"] += 1
    usuario["puntos"] += puntos


def sumar_error(usuario: dict) -> None:
    """
    Registra un error cometido por el usuario al fallar una palabra.

    PARÁMETROS:
        usuario (dict): Diccionario que contiene los datos del usuario.

    RETORNO:
        None
    """
    usuario["palabras_erradas"] += 1




def calcular_puntos_turno(intento: str, racha: int, tiempo_respuesta: float) -> int:
    """
    Calcula los puntos de un turno, sumando bonus por racha.

    PARÁMETROS:
        intento (str): Palabra ingresada por el jugador.
        racha (int): Racha actual de aciertos.
        tiempo_respuesta (float): Tiempo que tardó el jugador en responder.

    RETORNO:
        int: Puntos obtenidos en el turno.
    """
    puntos = calcular_puntos_por_palabra(intento, tiempo_respuesta)
    if racha >= 2:
        puntos += 2
    return puntos



def aplicar_puntos(usuario: dict, estado_juego: dict, puntos: int) -> None:
    """
    Descripción:
        Suma los puntos obtenidos en el turno al puntaje total del juego
        y también registra esos puntos en los datos del usuario.

    Parámetros:
        usuario (dict): Diccionario del usuario donde se acumulan los puntos ganados.
        estado_juego (dict): Estado actual del juego, donde se actualiza el puntaje total.
        puntos (int): Cantidad de puntos obtenidos en el intento.

    Retorno:
        None: No retorna ningún valor porque solo actualiza los puntajes
        dentro del usuario y del estado del juego.
    """
    estado_juego["puntaje"] += puntos
    sumar_puntos_por_acierto(usuario, puntos)



def actualizar_racha(racha: int) -> int:
    """
    Descripción:
        Aumenta en 1 la racha actual de aciertos.

    Parámetros:
        racha (int): Número actual de aciertos consecutivos.

    Retorno:
        int: Devuelve la racha actualizada después del acierto.
    """
    racha = racha + 1
    return racha


