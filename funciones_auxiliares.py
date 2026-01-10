from palabras import PALABRAS
from mis_funciones import agregar_elemento
import random 

def mostrar_encabezado_de_juego() -> None:
    """
    Muestra el título del juego en pantalla.

    Parámetros:
    - Ninguno.

    Retorno:
    - None: Solo imprime texto en pantalla.
    """
    print("\n")
    print("==============================================")
    print("🎮 BIENVENIDO A 'PALABRAS EN PALABRA' 🎮")
    print("==============================================")
    print("🔥 OBJETIVO: formar palabras correctas usando")
    print("   las letras que se te muestran.\n")

def mostrar_encabezado_de_nivel(nivel: int) -> None:
    """
    Imprime por pantalla el encabezado del nivel actual.

    Parámetros:
    - nivel (int): Número del nivel a mostrar.

    Retorno:
    - None: Solo imprime texto en pantalla.
    """
    print(f"\n========== NIVEL {nivel} ==========")

def mostrar_letras(letras: list) -> None:
    """
    Muestra en pantalla la lista de letras que forman la palabra base.

    Parámetros:
    - letras (list): Lista de caracteres individuales.

    Retorno:
    - None: Solo imprime las letras en pantalla.
    """
    print("\n🔠 PALABRA INICIAL :")
    i = 0
    while i < len(letras):
        print(letras[i], end=" ")
        i += 1
    print("\n------------------------------")


