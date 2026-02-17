import pygame

def crear_botones_disponibles():
    botones = {}

    # --- Botones del menú ---
    botones["btn_tdah"] = pygame.Rect(700, 560, 200, 55)
    botones["btn_jugar"] = pygame.Rect(700, 320, 200, 55)
    botones["btn_stats"] = pygame.Rect(700, 400, 200, 55)
    botones["btn_cerrar_sesion"] = pygame.Rect(700, 480, 200, 55)

    # --- Login / Registro ---
    botones["rect_usuario"] = pygame.Rect(650, 270, 300, 40)
    botones["rect_contrasena"] = pygame.Rect(650, 360, 300, 40)

    botones["btn_login"] = pygame.Rect(700, 350, 200, 55)
    botones["btn_registro"] = pygame.Rect(700, 430, 200, 55)
    botones["btn_salir_juego"] = pygame.Rect(700, 550, 200, 55)

    botones["btn_submit"] = pygame.Rect(650, 430, 300, 50)

    # --- Navegación ---
    botones["btn_atras"] = pygame.Rect(30, 30, 140, 45)

    return botones
