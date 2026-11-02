# ==============================================================================
# pantallas.py — Interfaz y pantallas del juego
# ------------------------------------------------------------------------------
# Objetivo: dibujar el HUD (barra de vida y mensajes) y las pantallas de
# título, pausa, Game Over y victoria (GDD sección 9, GUIA_ESTILO 4).
# ==============================================================================

import math

import pygame

import config
import recursos


# ------------------------------------------------------------------------------
# VELO OSCURO
# Capa semitransparente sobre el juego congelado (pausa, Game Over, victoria).
# ------------------------------------------------------------------------------
def oscurecer(pantalla, alfa):
    velo = pygame.Surface((config.ANCHO, config.ALTO), pygame.SRCALPHA)
    velo.fill((0, 0, 0, alfa))
    pantalla.blit(velo, (0, 0))


def texto_parpadeante(pantalla, texto, centro, tiempo):
    # Visible 2/3 del tiempo, para llamar la atención sin cansar
    if (tiempo % 0.9) < 0.6:
        recursos.texto_contorno(pantalla, texto, config.TAMANO_FUENTE_MEDIANA, centro)


# ------------------------------------------------------------------------------
# PANTALLA DE TÍTULO
# Nombre del juego, Metrópolis de fondo, Superman flotando y "Presiona Enter".
# El fondo lo dibuja main.py antes de llamar a esta función.
# ------------------------------------------------------------------------------
def dibujar_titulo(pantalla, tiempo):
    centro_x = config.ANCHO // 2
    recursos.texto_contorno(pantalla, config.TITULO_JUEGO, config.TAMANO_FUENTE_GRANDE * 2,
                            (centro_x, 130), config.COLOR_HEROE_AMARILLO)
    recursos.texto_contorno(pantalla, config.SUBTITULO_JUEGO, config.TAMANO_FUENTE_MEDIANA,
                            (centro_x, 215))

    # Superman al doble de tamaño (sin suavizar), subiendo y bajando
    superman = recursos.cargar_sprite("superman", (120, 160), config.COLOR_HEROE_AZUL)
    grande = pygame.transform.scale(superman, (superman.get_width() * 2, superman.get_height() * 2))
    flotar = int(math.sin(tiempo * 2) * 12)
    pantalla.blit(grande, grande.get_rect(center=(centro_x, 430 + flotar)))

    texto_parpadeante(pantalla, "Presiona Enter", (centro_x, config.ALTO - 60), tiempo)


# ------------------------------------------------------------------------------
# PAUSA, GAME OVER Y VICTORIA
# Se dibujan encima del juego congelado.
# ------------------------------------------------------------------------------
def dibujar_pausa(pantalla):
    oscurecer(pantalla, 140)
    recursos.texto_contorno(pantalla, "Pausa", config.TAMANO_FUENTE_GRANDE,
                            (config.ANCHO // 2, config.ALTO // 2 - 30))
    recursos.texto_contorno(pantalla, "P para continuar", config.TAMANO_FUENTE_MEDIANA,
                            (config.ANCHO // 2, config.ALTO // 2 + 30))


def dibujar_game_over(pantalla, tiempo):
    oscurecer(pantalla, 170)
    recursos.texto_contorno(pantalla, "Game Over", config.TAMANO_FUENTE_GRANDE * 2,
                            (config.ANCHO // 2, config.ALTO // 2 - 40), config.COLOR_VIDA_BAJA)
    texto_parpadeante(pantalla, "Enter = reintentar el nivel",
                      (config.ANCHO // 2, config.ALTO // 2 + 60), tiempo)


def dibujar_victoria(pantalla, tiempo):
    # Velo ligero: se sigue viendo al dinosaurio hecho chatarra
    oscurecer(pantalla, 90)
    recursos.texto_contorno(pantalla, config.JEFE_MENSAJE_VICTORIA, config.TAMANO_FUENTE_GRANDE,
                            (config.ANCHO // 2, 170), config.COLOR_HEROE_AMARILLO)
    recursos.texto_contorno(pantalla, "Próximamente Nivel 2", config.TAMANO_FUENTE_MEDIANA,
                            (config.ANCHO // 2, 240))
    texto_parpadeante(pantalla, "Enter = volver al título",
                      (config.ANCHO // 2, config.ALTO - 60), tiempo)


# ------------------------------------------------------------------------------
# MENSAJES EN PANTALLA
# Mensaje de oleada (centro, grande, 2 s) y mensajes de tutorial
# (centro-abajo, 3 s cada uno, uno tras otro). Ambos se desvanecen al final.
# ------------------------------------------------------------------------------
class Mensajes:
    def __init__(self):
        self.oleada = None        # [texto, segundos restantes]
        self.tutorial = None
        self.cola_tutorial = []

    def mostrar_oleada(self, texto):
        self.oleada = [texto, config.MENSAJE_OLEADA_DURACION]

    def agregar_tutorial(self, textos):
        self.cola_tutorial.extend(textos)

    @property
    def tutorial_terminado(self):
        return self.tutorial is None and not self.cola_tutorial

    def actualizar(self, dt):
        # Descuenta el tiempo de cada mensaje y lo quita al terminar
        if self.oleada:
            self.oleada[1] -= dt
            if self.oleada[1] <= 0:
                self.oleada = None
        if self.tutorial:
            self.tutorial[1] -= dt
            if self.tutorial[1] <= 0:
                self.tutorial = None
        # El tutorial empieza cuando ya se fue el mensaje de oleada
        if self.tutorial is None and self.cola_tutorial and self.oleada is None:
            self.tutorial = [self.cola_tutorial.pop(0), config.MENSAJE_TUTORIAL_DURACION]

    def dibujar(self, pantalla):
        if self.oleada:
            recursos.texto_contorno(pantalla, self.oleada[0], config.TAMANO_FUENTE_GRANDE,
                                    (config.ANCHO // 2, int(config.ALTO * 0.4)),
                                    alfa=_alfa(self.oleada[1]))
        if self.tutorial:
            recursos.texto_contorno(pantalla, self.tutorial[0], config.TAMANO_FUENTE_MEDIANA,
                                    (config.ANCHO // 2, config.ALTO - 70),
                                    alfa=_alfa(self.tutorial[1]))


def _alfa(restante):
    # Opaco casi todo el tiempo; se desvanece en los últimos instantes
    if restante >= config.MENSAJE_DESVANECER:
        return 255
    return int(255 * restante / config.MENSAJE_DESVANECER)


# ------------------------------------------------------------------------------
# BARRA DE VIDA
# Arriba a la izquierda, con etiqueta "SUPERMAN". Cambia de color según la
# vida y parpadea cuando queda poca.
# ------------------------------------------------------------------------------
def dibujar_barra_vida(pantalla, vida, tiempo):
    x, y = config.BARRA_X, config.BARRA_Y
    ancho, alto = config.BARRA_ANCHO, config.BARRA_ALTO
    marco = config.BARRA_MARCO

    recursos.texto_contorno(pantalla, "SUPERMAN", config.TAMANO_FUENTE_CHICA,
                            (x + 70, y - 16))

    # Marco oscuro y fondo de la barra
    pantalla.fill(config.COLOR_BARRA_MARCO, (x - marco, y - marco, ancho + marco * 2, alto + marco * 2))
    pantalla.fill(config.COLOR_BARRA_FONDO, (x, y, ancho, alto))

    # Color según la vida restante
    if vida > 50:
        color = config.COLOR_VIDA_ALTA
    elif vida > 25:
        color = config.COLOR_VIDA_MEDIA
    else:
        color = config.COLOR_VIDA_BAJA
        # Con poca vida la barra parpadea (4 veces por segundo)
        if int(tiempo * 8) % 2 == 0:
            color = config.COLOR_BARRA_FONDO

    relleno = int(ancho * vida / config.JUGADOR_VIDA_MAX)
    pantalla.fill(color, (x, y, relleno, alto))
    # Franja clara arriba: la luz viene del sol
    if relleno > 0:
        brillo = tuple(min(255, c + 50) for c in color)
        pantalla.fill(brillo, (x, y, relleno, 4))
