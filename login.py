from usuarios import guardar_usuarios
from estadisticas import inicializar_estadisticas
from mis_funciones import limpiar_texto


def buscar_usuario(usuarios: dict, nombre: str) -> bool:
    """
    Verifica si un usuario existe en el diccionario de usuarios.

    Parámetros:
        usuarios (dict): Diccionario de usuarios, donde la clave es el nombre
                         (str) y el valor es un diccionario con información del usuario.
                         Ejemplo: {"Gonzalo": {"contraseña": "1234"}}
        nombre (str): Nombre del usuario a buscar. Ejemplo: "Gonzalo"

    Retorna:
        bool: True si el usuario existe, False si no.
    """
    encontrado = False  
    for clave in usuarios:  
        if clave == nombre: 
            encontrado = True
            break

    return encontrado  


def obtener_usuario(usuarios: dict, nombre: str) -> dict | None:
    """
    Obtiene la información de un usuario si existe.

    Parámetros:
        usuarios (dict): Diccionario de usuarios. Ejemplo: {"Gonzalo": {"contraseña": "1234"}}
        nombre (str): Nombre del usuario a obtener. Ejemplo: "Gonzalo"

    Retorna:
        dict | None: Diccionario con la información del usuario si existe, None si no existe.
                     Ejemplo: {"contraseña": "1234"}
    """
    usuario_encontrado = None  

    for clave in usuarios:     
        if clave == nombre:    
            usuario_encontrado = usuarios[clave]
            break

    return usuario_encontrado 


def registrar_usuario(usuarios: dict, ruta: str) -> dict:
    """
    Registra un nuevo usuario en el diccionario si no existe ya
    y guarda automáticamente los cambios en el archivo JSON.

    Parámetros:
        usuarios (dict): Diccionario con los usuarios actuales.
                         Ejemplo: {"Gonzalo": {"contraseña": "1234"}}
        ruta (str): Ruta del archivo para guardar los usuarios. Ejemplo: "usuarios.json"

    Retorna:
        dict: Diccionario actualizado con el nuevo usuario agregado.
    """
    nombre = limpiar_texto(input("Ingrese su nombre de usuario: "))  
    existe = buscar_usuario(usuarios, nombre)  

    if (not existe):
        contraseña = limpiar_texto(input("Ingrese su contraseña: "))  
        nuevo_usuario = {"contraseña": contraseña}  
        inicializar_estadisticas(nuevo_usuario)     

        usuarios[nombre] = nuevo_usuario            


        guardar_usuarios(usuarios, ruta)

        print(f"✅ Usuario {nombre} registrado correctamente.")
    else:
        print("⚠️ El usuario ya existe.")

    return usuarios



def iniciar_sesion(usuarios: dict) -> tuple:
    """
    Permite iniciar sesión verificando existencia del usuario y su contraseña.

    Parámetros:
        usuarios (dict): Diccionario con los usuarios registrados.
                         Ejemplo: {"Gonzalo": {"contraseña": "1234"}}

    Retorna:
        tuple:
            usuario_logeado (dict | None): Diccionario con la información del usuario si el login es correcto, None si falla.
            clave_usuario (str | None): Nombre del usuario si el login es correcto, None si falla.
    """
    nombre = limpiar_texto(input("Ingrese su nombre de usuario: "))  

    usuario_logeado = None  
    clave_usuario = None

    no_existe = buscar_usuario(usuarios, nombre)  

    if (not no_existe) or (nombre == ""):
        print("❌ Usuario no encontrado.")

    else:
        contraseña = limpiar_texto(input("Ingrese su contraseña: "))
        usuario_encontrado = obtener_usuario(usuarios, nombre)        

        if usuario_encontrado["contraseña"] != contraseña:
            print("❌ Contraseña incorrecta.")
        else:
            faltan_estadisticas = True  
            for clave in usuario_encontrado:  
                if clave == "puntos":
                    faltan_estadisticas = False
                    break

            if faltan_estadisticas:
                inicializar_estadisticas(usuario_encontrado)

            usuario_logeado = usuario_encontrado  
            clave_usuario = nombre
            print("✅ Inicio de sesión exitoso.")

    return usuario_logeado, clave_usuario
