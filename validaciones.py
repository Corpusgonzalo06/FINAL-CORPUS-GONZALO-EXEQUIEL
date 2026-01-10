from mis_funciones import crear_mi_separador, convertir_a_minusculas, agregar_elemento

def limpiar_palabra(palabra: str) -> str:
    """
    Limpia la palabra eliminando espacios y tabulaciones,
    y convirtiéndola a minúsculas usando funciones propias.

    Parámetros:
        palabra (str): Palabra a limpiar.

    Retorna:
        str: Palabra limpia lista para validar.
    """
    partes = crear_mi_separador(palabra, " ")
    palabra_limpia = ""
    i = 0
    while i < len(partes):
        if partes[i] != "":
            palabra_limpia = partes[i]
        i += 1
    palabra_limpia = convertir_a_minusculas(palabra_limpia)
    return palabra_limpia

def es_palabra_permitida(palabra: str, lista_permitida: list) -> bool:
    """
    Verifica si la palabra existe dentro de la lista de palabras permitidas.

    Parámetros:
        palabra (str): Palabra a validar.
        lista_permitida (list): Lista de palabras válidas.

    Retorna:
        bool: True si la palabra está permitida, False si no.
    """
    encontrada = False
    i = 0
    while i < len(lista_permitida):
        if lista_permitida[i] == palabra:
            encontrada = True
            break
        i += 1
    return encontrada

def fue_palabra_usada(palabra: str, lista_usadas: list) -> bool:
    """
    Verifica si la palabra ya fue usada previamente.

    Parámetros:
        palabra (str): Palabra a validar.
        lista_usadas (list): Lista de palabras usadas anteriormente.

    Retorna:
        bool: True si la palabra ya fue usada, False si no.
    """
    usada = False
    i = 0
    while i < len(lista_usadas):
        if lista_usadas[i] == palabra:
            usada = True
            break
        i += 1
    return usada


def validar_palabra(palabra: str, lista_permitida: list, lista_usadas: list) -> bool:
    """
    Valida si una palabra es válida según la lista de palabras permitidas
    y si no ha sido usada previamente, usando un solo return.

    Parámetros:
        palabra (str): Palabra a validar.
        lista_permitida (list): Lista de palabras permitidas.
        lista_usadas (list): Lista de palabras ya usadas.

    Retorna:
        bool: True si la palabra es válida y no ha sido usada, False si no.
    """
    es_valida = False

    palabra_limpia = limpiar_palabra(palabra)

    if palabra_limpia != "":
        if es_palabra_permitida(palabra_limpia, lista_permitida) and not fue_palabra_usada(palabra_limpia, lista_usadas):
            es_valida = True

    return es_valida

def validar_fila(cantidad_columnas: int) -> bool:
    """
    Una fila es válida si tiene al menos una categoría y una palabra.
    """
    fila_valida = False

    if cantidad_columnas >= 2:
        fila_valida = True

    return fila_valida