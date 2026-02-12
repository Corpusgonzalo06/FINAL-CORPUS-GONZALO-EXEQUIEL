import pygame

def crear_botones():
    return {
        "btn_tdah": pygame.Rect(700, 560, 200, 55),

        "rect_usuario": pygame.Rect(650, 270, 300, 40),
        "rect_contrasena": pygame.Rect(650, 360, 300, 40),

        "btn_login": pygame.Rect(700, 350, 200, 55),
        "btn_registro": pygame.Rect(700, 430, 200, 55),
        "btn_salir_juego": pygame.Rect(700, 550, 200, 55),

        "btn_submit": pygame.Rect(650, 430, 300, 50),

        "btn_jugar": pygame.Rect(700, 320, 200, 55),
        "btn_stats": pygame.Rect(700, 400, 200, 55),
        "btn_cerrar_sesion": pygame.Rect(700, 480, 200, 55),

        "btn_atras": pygame.Rect(30, 30, 140, 45)
    }
