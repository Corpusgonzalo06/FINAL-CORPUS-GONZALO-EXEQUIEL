from mis_funciones import *

def revelar_palabra_base(palabra_base: str) -> None:
    """
    Descripción:
        Muestra por pantalla la palabra base del nivel sin modificar nada del juego.

    PARÁMETROS:
        palabra_base (str): La palabra principal que se usará en ese nivel.

    RETORNO:
        None: No retorna nada porque solo imprime la palabra base.
    """
    print(f"💡 La palabra base es: {palabra_base}")


def eliminar_restricciones(vidas: int) -> int:
    """
    Descripción:
        Elimina temporalmente las restricciones del turno, permitiendo un intento
        sin perder vidas.

    PARÁMETROS:
        vidas (int): Cantidad actual de vidas del jugador.

    RETORNO:
        int: Devuelve la misma cantidad de vidas ya que no se descuenta ninguna.
    """
    print("🚀 Restricciones eliminadas. Tenés un intento libre sin perder vida.")
    vidas_actualizadas = vidas
    return vidas_actualizadas


def dar_pista_extra(palabra_base: str) -> None:
    """
    Descripción:
        Muestra una pista al jugador indicando la primera letra de una palabra válida.

    PARÁMETROS:
        palabra_base (str): La palabra base desde donde se extrae la pista.

    RETORNO:
        None: Solo imprime una pista en pantalla.
    """
    letra = palabra_base[0]
    letra_minuscula = convertir_a_minusculas(letra)
    print("🕵️ Pista extra: Una palabra empieza con '" + letra_minuscula + "'")


def usar_comodin(opcion: int, palabra_base: str, lista_palabras: list, vidas: int) -> int:
    """
    Descripción:
        Ejecuta el comodín seleccionado por el jugador en base a la opción elegida.

    PARÁMETROS:
        opcion (int): Número del comodín elegido.
        palabra_base (str): Palabra base del nivel.
        lista_palabras (list): Lista de palabras válidas del nivel (no siempre usada).
        vidas (int): Vidas actuales del jugador.

    RETORNO:
        int: Devuelve las vidas actualizadas después de aplicar el comodín.
    """
    vidas_actualizadas = vidas

    if opcion == 1:
        revelar_palabra_base(palabra_base)
    elif opcion == 2:
        vidas_actualizadas = eliminar_restricciones(vidas)
    elif opcion == 3:
        dar_pista_extra(palabra_base)
    else:
        print("⚠️ Comodín desconocido")

    return vidas_actualizadas


def validar_uso_comodin(texto_inicial: str) -> bool:
    """
    Descripción:
        Valida si el jugador quiere o no usar un comodín, aceptando solo 'si' o 'no'.

    PARÁMETROS:
        texto_inicial (str): La primera respuesta ingresada por el jugador.

    RETORNO:
        bool: Devuelve True si quiere usar un comodín, False si no.
    """
    usar_bandera = False
    respuesta_valida = False
    texto = convertir_a_minusculas(texto_inicial)

    while respuesta_valida == False:
        match texto:
            case "si":
                usar_bandera = True
                respuesta_valida = True
            case "no":
                usar_bandera = False
                respuesta_valida = True
            case _:
                print("Por favor, ingresá 'si' o 'no'.")
                texto = convertir_a_minusculas(input("¿Querés usar un comodín? (si/no): "))

    return usar_bandera


def obtener_comodines_disponibles(comodines_jugador: dict) -> list:
    """
    Descripción:
        Revisa el diccionario de comodines del jugador y devuelve solo los que aún están disponibles.

    PARÁMETROS:
        comodines_jugador (dict): Diccionario donde cada comodín está marcado como True (disponible) o False.

    RETORNO:
        list: Lista con los nombres de los comodines disponibles.
    """
    disponibles = []
    for nombre in comodines_jugador:
        if comodines_jugador[nombre] == True:
            disponibles = agregar_elemento(disponibles, nombre)
    return disponibles


def mostrar_comodines(disponibles: list) -> None:
    """
    Descripción:
        Muestra por pantalla los comodines que el jugador tiene disponibles.

    PARÁMETROS:
        disponibles (list): Lista de nombres de comodines habilitados.

    RETORNO:
        None: Solo imprime los comodines.
    """
    print("\n🎁 Comodines disponibles:")
    i = 0
    numero = 1
    while i < len(disponibles):
        print(f"{numero}. {disponibles[i]}")
        numero += 1
        i += 1


def leer_opcion_numerica(texto: str) -> int:
    """
    Descripción:
        Convierte un texto a número entero si es válido.

    PARÁMETROS:
        texto (str): Texto ingresado que debería representar un número.

    RETORNO:
        int: Número convertido, o None si el texto no es válido.
    """
    resultado = None 
    es_val = ver_si_es_numero_valido(texto)
    if es_val == True:
        resultado = convertir_a_entero(texto)
    return resultado


def manejar_comodines(comodines_jugador: dict, palabra_base: str, lista_palabras: list, vidas_actuales: int) -> int:
    """
    Descripción:
        Controla todo el proceso de uso de comodines:
        - pregunta si el jugador quiere usar uno,
        - muestra los disponibles,
        - valida la opción,
        - aplica el comodín elegido.

    PARÁMETROS:
        comodines_jugador (dict): Diccionario con el estado de los comodines.
        palabra_base (str): Palabra base del nivel.
        lista_palabras (list): Lista de palabras válidas del nivel.
        vidas_actuales (int): Cantidad actual de vidas del jugador.

    RETORNO:
        int: Devuelve las vidas actualizadas según el comodín aplicado.
    """
    resultado = vidas_actuales

    usar = validar_uso_comodin(input("¿Querés usar un comodín? (si/no): "))

    if usar == True:
        disponibles = obtener_comodines_disponibles(comodines_jugador)

        if len(disponibles) > 0:
            mostrar_comodines(disponibles)

            opcion_txt = input("Elegí un comodín: ")
            opcion = leer_opcion_numerica(opcion_txt)

            valido = True
            cantidad = len(disponibles)

            if opcion == None:
                print("⚠️ Entrada inválida.")
                valido = False
            elif opcion < 1 or opcion > cantidad: 
                print("⚠️ Ese número no corresponde a ningún comodín.")
                valido = False

            if valido == True:
                nombre = disponibles[opcion - 1]
                comodines_jugador[nombre] = False

                if nombre == "revelar_palabra_base":
                    opcion_comodin = 1
                elif nombre == "eliminar_restricciones":
                    opcion_comodin = 2
                elif nombre == "pista_extra":
                    opcion_comodin = 3
                else:
                    opcion_comodin = 0

                resultado = usar_comodin(opcion_comodin, palabra_base, lista_palabras, resultado)
        else:
            print("⚠️ No te quedan comodines disponibles.")

    return resultado


def crear_comodines_iniciales(valor=True):
    """
    Descripción:
        Crea un diccionario con los comodines iniciales del jugador,
        todos activados por defecto.

    PARÁMETROS:
        valor (bool): Estado inicial para todos los comodines (por defecto, True).

    RETORNO:
        dict: Diccionario con los comodines habilitados o no según el valor recibido.
    """
    revelar_palabras = valor
    eliminar_restricciones = valor
    pista_extra = valor

    comodines = {
        "revelar_palabra_base": revelar_palabras,
        "eliminar_restricciones": eliminar_restricciones,
        "pista_extra": pista_extra
    }
    return comodines
