import pygame

# ==========================
# INICIALIZAR SONIDOS
# ==========================
def inicializar_sonidos():
    pygame.mixer.init()

    sonidos = {}

    sonidos["bien"] = pygame.mixer.Sound("bell-notification-337658.mp3")
    sonidos["mal"] = pygame.mixer.Sound("notification-power-432434.mp3")

    sonidos["bien"].set_volume(0.4)
    sonidos["mal"].set_volume(0.4)

    return sonidos


# ==========================
# REPRODUCIR EFECTO
# ==========================
def reproducir_sonido(sonidos, nombre):
    if nombre in sonidos:
        sonidos[nombre].play()


# ==========================
# MÚSICA DE FONDO
# ==========================
def reproducir_musica_fondo():
    pygame.mixer.music.load("mixkit-night-sky-hip-hop-970.mp3")
    pygame.mixer.music.set_volume(0.4)
    pygame.mixer.music.play(-1)  # loop infinito


def detener_musica():
    pygame.mixer.music.stop()
