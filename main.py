from logica_juego import logica_principal
from usuarios import cargar_usuarios
from login import iniciar_sesion, registrar_usuario

RUTA = "usuarios.json"

def main() -> None:
    """
    Función principal del programa.

    Se encarga de:
    - Cargar los usuarios desde el archivo JSON.
    - Mostrar el menú principal.
    - Permitir iniciar sesión, registrar un usuario o salir.
    - Iniciar el juego si las credenciales son correctas.

    PARÁMETROS:
        None: La función no recibe parámetros.

    RETORNO:
        None: La función no retorna ningún valor.
    """
    usuarios = cargar_usuarios(RUTA)
    continuar = True

    while continuar:
        print("\n=== MENÚ PRINCIPAL ===")
        print("1. Iniciar sesión")
        print("2. Registrarse")
        print("3. Salir")
        opcion = input("Seleccione una opción: ")
        match opcion:
            case "1":
                usuario, nombre_usuario = iniciar_sesion(usuarios)
                if usuario != None:
                    print(f"\n🎮 Bienvenido {nombre_usuario}! Iniciando juego...\n")
                    logica_principal(usuario, RUTA, vidas=3, clave_usuario=nombre_usuario)
            case "2":
                usuarios = registrar_usuario(usuarios, RUTA)

            case "3":
                continuar = False
                print("👋 ¡Hasta luego!")

            case _:
                print("❌ Opción inválida.")

if __name__ == "__main__":
    main()
