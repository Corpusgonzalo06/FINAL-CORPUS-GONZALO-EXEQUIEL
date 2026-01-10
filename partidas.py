import random
from mis_funciones import agregar_elemento
from manejo_aleatoriedad import mezclar_palabras
from validaciones import validar_fila

def leer_archivo(ruta_archivo: str) -> list:
    """
    Lee un archivo de texto línea por línea.

    Parámetros:
        ruta_archivo (str): Ruta del archivo a leer.

    Retorna:
        list: Lista con todas las líneas del archivo. Si el archivo no existe,
              retorna una lista vacía y muestra un mensaje de advertencia.
    """
    lineas = []
    try:
        archivo = open(ruta_archivo, "r", encoding="utf-8")
        lineas = archivo.readlines()
        archivo.close()
    except FileNotFoundError:
        print(f"⚠️ No se encontró el archivo: {ruta_archivo}")
    return lineas


def separar_por_comas(linea: str) -> dict:
    """
    Separa una línea de texto en columnas usando la coma como delimitador.

    Parámetros:
        linea (str): Línea del archivo CSV.

    Retorna:
        dict: Contiene:
            - "valores" (list): Lista con las columnas .
            - "total_columnas" (int): Cantidad de columnas .
    """
    lista_columnas = []
    columna_actual = ""
    total_columnas = 0

    for caracter in linea:
        if caracter == "," or caracter == "\n":
            if total_columnas == len(lista_columnas):
                lista_columnas = agregar_elemento(lista_columnas, "")
            lista_columnas[total_columnas] = columna_actual
            total_columnas += 1
            columna_actual = ""
        else:
            columna_actual += caracter

    resultado = {
        "valores": lista_columnas,
        "total_columnas": total_columnas
    }

    return resultado



def inicializar_categoria(diccionario_categorias: dict, nombre_categoria: str) -> None:
    """
    Crea la categoría en el diccionario si aún no existe.

    Parámetros:
        diccionario_categorias (dict): Diccionario general de categorías.
        nombre_categoria (str): Clave de la categoría a inicializar.

    Retorna:
        None
    """
    existe_categoria = False
    for categoria in diccionario_categorias:
        if categoria == nombre_categoria:
            existe_categoria = True
            break
    if not existe_categoria:
        diccionario_categorias[nombre_categoria] = []

            
def palabra_repetida(lista_palabras: list, palabra: str) -> bool:
    """
    Verifica si una palabra ya fue cargada en una lista.

    Parámetros:
        lista_palabras (list): Lista de palabras ya existentes.
        palabra (str): Palabra a verificar.

    Retorna:
        bool: True si la palabra está repetida, False si no.
    """
    repetida = False
    for i in lista_palabras:
        if i == palabra:
            repetida = True
            break
    return repetida



def agregar_palabra(diccionario_categorias: dict, nombre_categoria: str, palabra: str) -> None:

    """
    Agrega una palabra a una categoría evitando duplicados y valores vacíos.

    Parámetros:
        diccionario_categorias (dict): Diccionario que contiene las categorías.
        nombre_categoria (str): Categoría donde se agregará la palabra.
        palabra (str): Palabra a agregar.

    Retorna:
        None
    """
    puede_agregarse = True

    if palabra == "":
        puede_agregarse = False

    if not palabra_repetida(diccionario_categorias[nombre_categoria], palabra):
        palabra_no_repetida = True
    else:
        palabra_no_repetida = False
        puede_agregarse = False

    if puede_agregarse and palabra_no_repetida:
        diccionario_categorias[nombre_categoria] = agregar_elemento(diccionario_categorias[nombre_categoria], palabra)



def cargar_fila_en_diccionario(diccionario_categorias: dict, columnas: list, cantidad_columnas: int) -> dict:
    """
    Procesa una fila del archivo CSV e incorpora su información al diccionario.
 
    Parámetros:
        diccionario_categorias (dict): Diccionario principal de categorías.
        columnas (list): Columnas obtenidas de la fila.
        cantidad_columnas (int): Número total de columnas detectadas.

    Retorna:
        dict: Diccionario actualizado con la categoría y sus palabras.
    """
    if validar_fila(cantidad_columnas):
        nombre_categoria = columnas[0]

        inicializar_categoria(diccionario_categorias, nombre_categoria)

        indice = 1
        while indice < cantidad_columnas:
            palabra_actual = columnas[indice]
            agregar_palabra(diccionario_categorias, nombre_categoria, palabra_actual)
            indice += 1

        mezclar_palabras(diccionario_categorias, nombre_categoria)

    return diccionario_categorias
