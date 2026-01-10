def inicializar_estadisticas(usuario_data: dict) -> None:
    """
    Inicializa las estadísticas de un usuario si no existen.

    Parámetros:
    - usuario_data (dict): Diccionario del usuario donde se agregarán
      las claves de estadísticas faltantes.

    Retorno:
    - None: No devuelve nada, solo modifica el diccionario recibido.
    """
    claves_necesarias = {
        "partidas_jugadas": 0,
        "palabras_acertadas": 0,
        "palabras_erradas": 0,
        "victorias": 0,
        "derrotas": 0,
        "puntos": 0,
        "tiempo_total": 0,
        "tiempo_total_juego": 0,
        "errores_totales_juego": 0
    }

    for clave in claves_necesarias:
        if clave not in usuario_data:
            usuario_data[clave] = claves_necesarias[clave]

