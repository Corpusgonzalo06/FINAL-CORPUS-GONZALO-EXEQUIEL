import random
from mis_funciones import agregar_elemento , desordenar_letras
from funciones_auxiliares import mostrar_letras
from palabras import PALABRAS

def seleccionar_palabras_nivel(todas_las_palabras: list, cantidad: int = 3) -> list:
    """
    Selecciona una cantidad determinada de palabras al azar sin repetir.

    Parámetros:
        todas_las_palabras (list): Lista total de palabras disponibles.
        cantidad (int): Cantidad de palabras a seleccionar.

    Retorna:
        list: Lista con palabras seleccionadas aleatoriamente sin repetición.
    """
    palabras_nivel = []

    while len(palabras_nivel) < cantidad:
        indice_aleatorio = random.randint(0, len(todas_las_palabras) - 1)
        palabra_seleccionada = todas_las_palabras[indice_aleatorio]

        repetida = False
        for palabra in palabras_nivel: ###### ver 
            if palabra == palabra_seleccionada:
                repetida = True
                break

        if not repetida:
            palabras_nivel = agregar_elemento(palabras_nivel, palabra_seleccionada)

    return palabras_nivel



def preparar_palabra(palabra_base: str, diccionario_palabras: dict) -> list:
    """
    Descripción:
        Prepara la información necesaria para jugar una ronda a partir de la palabra base.
        Desordena sus letras, las muestra por pantalla y obtiene la lista de palabras válidas
        asociadas a esa palabra base.

    Parámetros:
        palabra_base (str): La palabra principal del nivel, utilizada para generar las letras
        desordenadas y acceder a sus palabras válidas.
        diccionario_palabras (dict): Diccionario que contiene todas las palabras del juego.

    Retorno:
        list: Devuelve la lista de palabras válidas asociadas a la palabra base,
        que serán usadas en la ronda del nivel.
    """
    palabra_desordenada = desordenar_letras(palabra_base)
    mostrar_letras(palabra_desordenada)
    palabras_validas = diccionario_palabras[palabra_base]
    return palabras_validas


def mezclar_palabras(diccionario_categorias: dict, nombre_categoria: str) -> None:
    """
    Mezcla aleatoriamente el orden de las palabras dentro de una categoría.

    La mezcla solo se realiza si la categoría contiene más de una palabra.

    Parámetros:
        diccionario_categorias (dict): Diccionario de categorías.
        nombre_categoria (str): Categoría cuyas palabras se mezclarán.

    Retorna:
        None
    """
    cantidad_palabras = len(diccionario_categorias[nombre_categoria])

    if cantidad_palabras > 1:
        for i in range(cantidad_palabras):
            indice_aleatorio = random.randint(0, cantidad_palabras - 1)
            temp = diccionario_categorias[nombre_categoria][i]
            diccionario_categorias[nombre_categoria][i] = diccionario_categorias[nombre_categoria][indice_aleatorio]
            diccionario_categorias[nombre_categoria][indice_aleatorio] = temp

