def inicializar_estadisticas(usuario_data: dict) -> None:
    claves_necesarias = {
        "partidas_jugadas": 0,
        "palabras_completadas": 0,
        "palabras_incompletas": 0,
        "puntos": 0,
        "errores_totales_juego": 0,
        "tiempo_total": 0
    }

    for clave, valor in claves_necesarias.items():
        if clave not in usuario_data:
            usuario_data[clave] = valor
