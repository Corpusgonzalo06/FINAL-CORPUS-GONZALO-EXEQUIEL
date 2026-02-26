from random import randint
from manejo_mis_funciones import agregar_elemento

def sortear_posicion(largo_palabra: int) -> int:
    """
    Devuelve una posición aleatoria válida dentro de la palabra.
    
    PARÁMETROS:
        largo_palabra (int): Cantidad de letras de la palabra.
    
    RETORNO:
        int: Una posición entre 0 y largo_palabra - 1.
    """
    posicion_sorteada = randint(0, largo_palabra - 1)
    return posicion_sorteada


def comprobar_posicion_repetida(lista_posiciones: list, posicion: int) -> bool:
    """
    Verifica si una posición ya aparece en la lista de posiciones.

    PARÁMETROS:
        lista_posiciones (list): Lista de posiciones ya usadas.
        posicion (int): Posición a evaluar.

    RETORNO:
        bool: True si la posición está repetida, False en caso contrario.
    """
    indice = 0
    repetida = False

    while indice < len(lista_posiciones) and not repetida:
        if lista_posiciones[indice] == posicion:
            repetida = True
        indice += 1

    return repetida


def generar_posiciones_unicas(largo_palabra: int, cantidad_a_mostrar: int) -> list:
    """
    Genera posiciones aleatorias dentro de la palabra sin repetir ninguna.

    PARÁMETROS:
        largo_palabra (int): Longitud de la palabra.
        cantidad_a_mostrar (int): Cantidad de posiciones distintas a elegir.

    RETORNO:
        list: Lista con posiciones aleatorias no repetidas.
    """
    posiciones_visibles = []

    while len(posiciones_visibles) < cantidad_a_mostrar:
        nueva = sortear_posicion(largo_palabra)

        if not comprobar_posicion_repetida(posiciones_visibles, nueva):
            posiciones_visibles = agregar_elemento(posiciones_visibles, nueva)

    return posiciones_visibles


def generar_parcial_palabra(palabra: str) -> str:
    """
    Genera una versión parcial de la palabra mostrando 1 o 2 letras al azar.

    PARÁMETROS:
        palabra (str): Palabra original.

    RETORNO:
        str: Palabra con algunas letras visibles y el resto como "_".
    """

    largo_palabra = len(palabra)
    cantidad_letras_a_mostrar = randint(1, 2)

    posiciones_visibles = generar_posiciones_unicas(largo_palabra, cantidad_letras_a_mostrar)

    palabra_parcial = ""  

    for indice_actual in range(largo_palabra):
        mostrar_letra = False

        for indice_visible in posiciones_visibles:
            if indice_actual == indice_visible:
                mostrar_letra = True
                break
        if mostrar_letra == True:
            palabra_parcial += palabra[indice_actual] + " "
        else:
            palabra_parcial += "_ "

    return palabra_parcial

def mostrar_parcialmente_palabra(palabra_base: str, lista_palabras: list) -> list:
    """
    Muestra en pantalla las palabras con letras parcialmente reveladas y
    devuelve la lista de esas versiones parciales.

    PARÁMETROS:
        palabra_base (str): No se usa, solo está por compatibilidad.
        lista_palabras (list): Lista de palabras originales.

    RETORNO:
        list: Lista con las versiones parciales generadas.
    """
    lista_parciales = []

    print("\n🧩 Palabras a descubrir (pistas):")

    for palabra in lista_palabras:
        parcial = generar_parcial_palabra(palabra)
        lista_parciales = agregar_elemento(lista_parciales, parcial)
        print(parcial) 
 
