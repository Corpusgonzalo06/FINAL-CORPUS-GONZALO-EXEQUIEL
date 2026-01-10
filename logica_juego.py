import random
import time
from mis_funciones import agregar_elemento, convertir_a_minusculas, desordenar_letras
import comodines
from usuarios import cargar_usuarios, guardar_usuarios, inicializar_datos_usuario, guardar_datos_usuario, validar_sesion
from palabras import PALABRAS
from funciones_auxiliares import mostrar_letras, mostrar_encabezado_de_juego, mostrar_encabezado_de_nivel
from validaciones import validar_palabra
from manejo_puntaje import *
from manejo_aleatoriedad import seleccionar_palabras_nivel, preparar_palabra
from customizacion_nivel import mostrar_parcialmente_palabra

def finalizar_nivel(estado_juego: dict, palabras_usadas: list, lista_palabras: list) -> None:
    """
    Descripción:
        Verifica si el nivel fue completado comparando cuántas palabras se usaron.
        Si se completó, avanza al siguiente nivel. Si no, resta un reinicio y reinicia las vidas.

    Parámetros:
        estado_juego (dict): Diccionario con información del juego (nivel, vidas, reinicios).
        palabras_usadas (list): Lista con las palabras que el jugador ya acertó.
        lista_palabras (list): Lista total de palabras que deben completarse en el nivel.

    Retorno:
        None: No retorna datos porque solo actualiza el estado del juego y muestra mensajes en pantalla.
    """
    if len(palabras_usadas) == len(lista_palabras):
        print(f"🎉 Nivel {estado_juego['nivel']} completado!")
        estado_juego["nivel"] += 1
    else:
        estado_juego["reinicios"] -= 1
        estado_juego["vidas"] = 3
        print(f"💥 Nivel no completado. Reinicios restantes: {estado_juego['reinicios']}")



def finalizar_juego(estado_juego: dict, usuario: dict) -> None:
    """
    Descripción:
        Determina si el jugador ganó o perdió según el nivel alcanzado.
        Actualiza las estadísticas del usuario (victorias o derrotas) y muestra el puntaje final.

    Parámetros:
        estado_juego (dict): Contiene el progreso del juego, incluyendo nivel y puntaje final.
        usuario (dict): Información del usuario, donde se registran victorias y derrotas.

    Retorno:
        None: No retorna ningún valor porque solo modifica los datos del usuario
        y muestra mensajes con el resultado de la partida.
    """
    if estado_juego["nivel"] > 5:
        usuario["victorias"] += 1
        print(f"\n🏆 ¡Felicitaciones, ganaste la partida!")
    else:
        usuario["derrotas"] += 1
        print(f"\n💀 Perdiste, volvé a intentarlo más tarde.")

    print(f"🏅 Puntaje final: {estado_juego['puntaje']}")


def inicializar_juego(usuario: dict, vidas: int = 3) -> dict:
    """
    Descripción:
        Configura el inicio de una nueva partida. Muestra el encabezado del juego,
        prepara los datos del usuario y crea el estado inicial del juego.

    Parámetros:
        usuario (dict): Información del usuario que será preparada para la partida.
        vidas (int): Cantidad de vidas iniciales para el jugador. Por defecto es 3.

    Retorno:
        dict: Devuelve un diccionario con todo el estado inicial del juego
        (puntaje, nivel, vidas, reinicios y comodines disponibles).
    """
    mostrar_encabezado_de_juego()
    inicializar_datos_usuario(usuario)

    estado_juego = {
        "puntaje": 0,
        "nivel": 1,
        "vidas": vidas,
        "reinicios": 3,
        "comodines_jugador": comodines.crear_comodines_iniciales(True)
    }
    return estado_juego



def aplicar_comodines(estado_juego: dict, palabra_base: str, lista_palabras: list) -> None:
    """
    Descripción:
        Aplica los comodines del jugador según la palabra base y la lista de palabras.
        Actualiza la cantidad de vidas del estado del juego dependiendo del comodín usado.

    Parámetros:
        estado_juego (dict): Contiene los datos actuales del juego, incluyendo vidas y comodines del jugador.
        palabra_base (str): La palabra principal con la que se evalúan los comodines.
        lista_palabras (list): Lista completa de palabras del nivel, usada por la lógica de los comodines.

    Retorno:
        None: No retorna un valor directo porque solo modifica la cantidad de vidas
        dentro del estado del juego.
    """
    estado_juego["vidas"] = comodines.manejar_comodines(
        estado_juego["comodines_jugador"],
        palabra_base,
        lista_palabras,
        estado_juego["vidas"]
    )

def obtener_intento_jugador(usuario: dict) -> dict:
    """
    Descripción:
        Registra un intento del jugador. Aumenta la cantidad de partidas jugadas,
        pide una palabra por teclado y guarda el momento exacto en que se realizó el intento.

    Parámetros:
        usuario (dict): Diccionario con la información del usuario,
        donde se incrementa la cantidad de partidas jugadas.

    Retorno:
        dict: Devuelve un diccionario con la palabra ingresada por el jugador
        y el momento en que se realizó el intento .
    """
    usuario["partidas_jugadas"] += 1
    intento = input("📝 Ingresá una palabra: ")
    momento_del_intento = time.time()

    resultado = {
        "intento": intento,
        "momento_del_intento": momento_del_intento
    }
    return resultado


def actualizar_palabras_usadas(palabras_usadas: list, intento: str) -> list:
    """
    Descripción:
        Agrega el intento del jugador a la lista de palabras usadas,
        convirtiéndolo primero a minúsculas para mantener uniformidad.

    Parámetros:
        palabras_usadas (list): Lista que contiene todas las palabras que el jugador ya ingresó.
        intento (str): La palabra que el jugador escribió en el intento actual.

    Retorno:
        list: Devuelve la lista actualizada con el nuevo intento agregado en minúsculas.
    """
    lista_actualizada = agregar_elemento(palabras_usadas, convertir_a_minusculas(intento))
    return lista_actualizada 


def mostrar_avance_del_turno(intento: str, palabras_usadas: list, lista_palabras: list, estado_juego: dict, puntos: int) -> None:
    """
    Descripción:
        Muestra en pantalla el progreso del jugador durante el turno actual.
        Indica cuántas palabras acertó, cuántas faltan y las vidas restantes,
        junto con los puntos obtenidos por el intento.

    Parámetros:
        intento (str): La palabra ingresada por el jugador (no se usa directamente, solo se muestra progreso tras ella).
        palabras_usadas (list): Lista con las palabras que el jugador acertó hasta el momento.
        lista_palabras (list): Lista total de palabras necesarias para completar el nivel.
        estado_juego (dict): Información actual del juego, incluyendo las vidas del jugador.
        puntos (int): Cantidad de puntos obtenidos por este intento.

    Retorno:
        None: No retorna ningún valor porque solo imprime el avance del turno por pantalla.
    """
    cantidad_acertadas = len(palabras_usadas)
    cantidad_totales = len(lista_palabras)
    print("--------------------------------------------------")
    print(f"✅ ¡Correcto! +{puntos} puntos | "f"Progreso: {cantidad_acertadas}/{cantidad_totales} | "f"Vidas: {estado_juego['vidas']}")
    print("---------------------------------------------------")

def procesar_acierto(intento: str, palabras_usadas: list, lista_palabras: list, estado_juego: dict, usuario: dict, racha: int, momento_del_intento: float) -> dict:
    """
    Descripción:
        Procesa un acierto del jugador. Agrega la palabra usada, calcula los puntos
        obtenidos, actualiza el puntaje total, muestra el avance del turno y aumenta la racha.

    Parámetros:
        intento (str): La palabra ingresada correctamente por el jugador.
        palabras_usadas (list): Lista de palabras ya acertadas en el nivel.
        lista_palabras (list): Lista completa de palabras requeridas para el nivel.
        estado_juego (dict): Estado actual del juego (vidas, nivel, puntaje, etc.).
        usuario (dict): Datos del usuario, donde se actualiza el puntaje total.
        racha (int): Número actual de aciertos consecutivos del jugador.
        momento_del_intento (float): Momento exacto del intento, usado para el cálculo de puntos.

    Retorno:
        dict: Devuelve un diccionario con la racha actualizada y la lista de palabras usadas.
    """
    palabras_usadas = actualizar_palabras_usadas(palabras_usadas, intento)
    puntos = calcular_puntos_turno(intento, racha, momento_del_intento)

    aplicar_puntos(usuario, estado_juego, puntos)
    mostrar_avance_del_turno(intento, palabras_usadas, lista_palabras, estado_juego, puntos)

    racha = actualizar_racha(racha)

    resultado = {
        "racha": racha,
        "palabras_usadas": palabras_usadas
    }
    return resultado


def procesar_error(estado_juego: dict, usuario: dict) -> int:
    """
    Descripción:
        Procesa un error del jugador. Resta una vida, reinicia la racha a cero
        y registra el error en los datos del usuario.

    Parámetros:
        estado_juego (dict): Contiene el estado actual del juego, incluyendo las vidas del jugador.
        usuario (dict): Información del usuario donde se suma un error cometido.

    Retorno:
        int: Devuelve la racha reiniciada en 0, ya que un error corta cualquier racha activa.
    """
    estado_juego["vidas"] -= 1
    racha = 0

    sumar_error(usuario)
    print(f"❌ Incorrecto! Vidas restantes: {estado_juego['vidas']}")

    return racha


def procesar_intento(intento: str, palabras_usadas: list, lista_palabras: list, estado_juego: dict, usuario: dict, racha: int, momento_del_intento: float) -> dict:
    """
    Descripción:
        Determina si el intento del jugador es correcto o incorrecto.
        Si acierta, procesa el acierto y actualiza puntos, racha y palabras usadas.
        Si se equivoca, procesa el error y reinicia la racha.
        Devuelve siempre el estado actualizado de racha y palabras usadas.

    Parámetros:
        intento (str): La palabra ingresada por el jugador.
        palabras_usadas (list): Lista de palabras ya acertadas en el nivel.
        lista_palabras (list): Lista completa de palabras válidas del nivel.
        estado_juego (dict): Estado actual del juego (vidas, nivel, puntaje, etc.).
        usuario (dict): Datos del usuario donde se registran puntos y errores.
        racha (int): Racha de aciertos consecutivos antes del intento actual.
        momento_del_intento (float): Momento exacto del intento, usado para calcular puntos.

    Retorno:
        dict: Devuelve un diccionario con la racha actualizada y la lista de palabras usadas,
        dependiendo de si el intento fue correcto o no.
    """
    resultado = {
        "racha": racha,
        "palabras_usadas": palabras_usadas
    }

    if validar_palabra(intento, lista_palabras, palabras_usadas):
        resultado = procesar_acierto(
            intento, palabras_usadas, lista_palabras,
            estado_juego, usuario, racha, momento_del_intento
        )
    else:
        nueva_racha = procesar_error(estado_juego, usuario)
        resultado["racha"] = nueva_racha

    return resultado



def ejecutar_ronda(palabra_base: str, lista_palabras: list, estado_juego: dict, usuario: dict) -> list:
    """
    Descripción:
        Ejecuta una ronda completa del nivel. Mientras el jugador tenga vidas y
        queden palabras por encontrar, aplica comodines, recibe intentos del jugador
        y procesa aciertos o errores. 

    Parámetros:
        palabra_base (str): La palabra principal del nivel, utilizada para generar o validar palabras.
        lista_palabras (list): Lista total de palabras que deben acertarse en la ronda.
        estado_juego (dict): Contiene el estado del juego (vidas, nivel, puntaje, etc.).
        usuario (dict): Información del usuario utilizada para registrar intentos, puntaje y errores.

    Retorno:
        list: Devuelve la lista de palabras acertadas durante toda la ronda.
    """
    palabras_usadas = []
    racha = 0

    mostrar_parcialmente_palabra(palabra_base, lista_palabras)
    while estado_juego["vidas"] > 0 and len(palabras_usadas) < len(lista_palabras):

        aplicar_comodines(estado_juego, palabra_base, lista_palabras)
        jugada = obtener_intento_jugador(usuario)
        intento = jugada["intento"]
        momento_del_intento = jugada["momento_del_intento"]

        resultado = procesar_intento(
            intento, palabras_usadas, lista_palabras,
            estado_juego, usuario, racha, momento_del_intento
        )

        racha = resultado["racha"]
        palabras_usadas = resultado["palabras_usadas"]

    return palabras_usadas


def copiar_lista(palabras_fuente: list) -> list:
    todas_las_palabras = []
    for palabra in palabras_fuente:
        todas_las_palabras = agregar_elemento(todas_las_palabras, palabra)
    return todas_las_palabras


def ejecutar_palabras_nivel(palabras_nivel: list, estado_juego: dict, usuario: dict) -> None:
    """
    Descripción:
        Ejecuta todas las rondas correspondientes a un nivel. Para cada palabra base:
        prepara las palabras del nivel, ejecuta la ronda completa y luego decide si el
        nivel fue superado o no. Si el jugador se queda sin vidas, el proceso se detiene.

    Parámetros:
        palabras_nivel (list): Lista de palabras base que se deben jugar en este nivel.
        estado_juego (dict): Estado actual del juego, incluyendo vidas, nivel y puntaje.
        usuario (dict): Datos del usuario donde se registran estadísticas y puntaje.

    Retorno:
        None: No retorna ningún valor porque solo ejecuta las rondas del nivel
        y actualiza el estado del juego según el avance del jugador.
    """
    for palabra_base in palabras_nivel:
        if estado_juego["vidas"] <= 0:
            break

        lista_palabras = preparar_palabra(palabra_base, PALABRAS)

        palabras_usadas = ejecutar_ronda(palabra_base, lista_palabras, estado_juego, usuario)
        finalizar_nivel(estado_juego, palabras_usadas, lista_palabras)


def jugar_nivel(estado_juego: dict, usuario: dict) -> None:
    """
    Descripción:
        Muestra el encabezado del nivel actual,
        obtiene todas las palabras disponibles, selecciona las correspondientes al nivel
        y ejecuta sus rondas.

    Parámetros:
        estado_juego (dict): Diccionario con el estado del juego (nivel, vidas, puntaje, etc.).
        usuario (dict): Información del usuario, donde se actualizan estadísticas y puntajes.

    Retorno:
        None: No retorna datos porque solo organiza y ejecuta las acciones necesarias
        para jugar el nivel actual.
    """
    mostrar_encabezado_de_nivel(estado_juego["nivel"])

    todas_las_palabras = copiar_lista(PALABRAS)
    palabras_nivel = seleccionar_palabras_nivel(todas_las_palabras)

    ejecutar_palabras_nivel(palabras_nivel, estado_juego, usuario)


def logica_principal(usuario: dict | None, ruta: str, vidas: int = 3, clave_usuario: str | None = None) -> None:
    """
    Descripción:
        Controla el flujo general del juego. Valida la sesión del usuario, inicializa el juego,
        ejecuta todos los niveles mientras haya reinicios disponibles y luego finaliza la partida
        guardando los datos del usuario.

    Parámetros:
        usuario (dict | None): Información del usuario que inicia sesión. Puede ser None si hubo un error.
        ruta (str): Ruta del archivo donde se guardarán los datos del usuario al finalizar la partida.
        vidas (int): Cantidad de vidas iniciales por nivel. Por defecto es 3.
        clave_usuario (str | None): Clave asociada al usuario, necesaria para guardar sus datos.

    Retorno:
        None: No retorna ningún valor porque su responsabilidad es coordinar el funcionamiento
        completo del juego y guardar el progreso del usuario.
    """
    if validar_sesion(usuario, clave_usuario):
        tiempo_inicio = time.time()
        estado_juego = inicializar_juego(usuario, vidas)

        while estado_juego["nivel"] <= 5 and estado_juego["reinicios"] > 0:
            jugar_nivel(estado_juego, usuario)

        tiempo_fin = time.time()
        tiempo_partida = tiempo_fin - tiempo_inicio

        usuario["tiempo_total_juego"] = tiempo_partida
        usuario["tiempo_total"] += tiempo_partida

        guardar_datos_usuario(usuario, clave_usuario, ruta)

        finalizar_juego(estado_juego, usuario)



