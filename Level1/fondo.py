# ==============================================================================
# fondo.py — Fondo de Metrópolis con desplazamiento (parallax)
# ------------------------------------------------------------------------------
# Objetivo: dibujar el cielo de Metrópolis avanzando hacia la izquierda en
# tres capas (GUIA_ESTILO 6): cielo fijo, nubes lentas (0.2×) y ciudad (0.5×).
# La imagen de Metrópolis se repite alternando con su reflejo para que la
# unión entre copias no se note.
# ==============================================================================

import random

import pygame

import config
import recursos


# ------------------------------------------------------------------------------
# NUBE PIXELADA
# Genera una nube con cuadros de 8 px (sin círculos suaves).
# ------------------------------------------------------------------------------
def crear_nube(ancho_bloques, alto_bloques):
    bloque = 8
    nube = pygame.Surface((ancho_bloques * bloque, alto_bloques * bloque), pygame.SRCALPHA)
    centro_x = ancho_bloques / 2
    centro_y = alto_bloques / 2

    # Cada bloque se pinta si cae dentro de una elipse con borde irregular
    for bx in range(ancho_bloques):
        for by in range(alto_bloques):
            dx = (bx + 0.5 - centro_x) / centro_x
            dy = (by + 0.5 - centro_y) / centro_y
            if dx * dx + dy * dy < random.uniform(0.6, 1.0):
                # La parte baja de la nube es un poco más gris (luz de arriba)
                color = config.COLOR_NUBE if by < alto_bloques * 0.6 else config.COLOR_BRUMA
                nube.fill(color, (bx * bloque, by * bloque, bloque, bloque))
    nube.set_alpha(170)
    return nube


# ------------------------------------------------------------------------------
# CLASE FONDO
# Guarda la posición de cada capa y la dibuja con su velocidad.
# ------------------------------------------------------------------------------
class Fondo:
    def __init__(self):
        # Capa 1: cielo por bandas (se ve si falta la imagen de la ciudad)
        self.cielo = pygame.Surface((config.ANCHO, config.ALTO))
        bandas = [config.COLOR_CIELO, config.COLOR_CIELO_CLARO, config.COLOR_BRUMA]
        alto_banda = config.ALTO // len(bandas)
        for i, color in enumerate(bandas):
            self.cielo.fill(color, (0, i * alto_banda, config.ANCHO, alto_banda + 1))

        # Capa 3: ciudad = imagen + su reflejo, una al lado de la otra
        self.ciudad = None
        imagen = recursos.cargar_sprite("fondo_metropolis", (1, 1))
        if imagen.get_height() == config.ALTO:
            ancho = imagen.get_width()
            self.ciudad = pygame.Surface((ancho * 2, config.ALTO)).convert()
            self.ciudad.blit(imagen, (0, 0))
            self.ciudad.blit(pygame.transform.flip(imagen, True, False), (ancho, 0))

            # El letrero del Daily Planet se pega sin reflejar en la copia
            x, y, ancho_letrero, alto_letrero = config.FONDO_LETRERO
            letrero = imagen.subsurface((x, y, ancho_letrero, alto_letrero))
            self.ciudad.blit(letrero, (ancho + (ancho - x - ancho_letrero), y))

            # Velo claro para que el fondo no compita con los personajes
            velo = pygame.Surface(self.ciudad.get_size(), pygame.SRCALPHA)
            velo.fill(config.COLOR_BRUMA + (config.VELO_FONDO_ALFA,))
            self.ciudad.blit(velo, (0, 0))

        # Capa 2: nubes repartidas en la parte alta del cielo
        self.nubes = []
        for i in range(config.CANTIDAD_NUBES):
            nube = crear_nube(random.randint(10, 22), random.randint(4, 7))
            x = i * config.ANCHO / config.CANTIDAD_NUBES + random.randint(0, 120)
            y = random.randint(10, config.NUBES_Y_MAX)
            self.nubes.append([nube, x, y])

        self.avance = 0.0  # px recorridos por el nivel

    def actualizar(self, dt):
        self.avance += config.VELOCIDAD_AVANCE * dt

        # Las nubes se mueven y reaparecen por la derecha al salir
        for nube in self.nubes:
            nube[1] -= config.VELOCIDAD_AVANCE * config.PARALLAX_NUBES * dt
            if nube[1] < -nube[0].get_width():
                nube[1] = config.ANCHO + random.randint(0, 200)
                nube[2] = random.randint(10, config.NUBES_Y_MAX)

    def dibujar(self, pantalla, desplazamiento=(0, 0)):
        ox, oy = desplazamiento
        pantalla.blit(self.cielo, (0, 0))

        # Ciudad: se dibujan las copias necesarias para cubrir la pantalla.
        # Solo tiembla de lado, para no dejar una franja vacía arriba o abajo
        if self.ciudad:
            ancho = self.ciudad.get_width()
            x = -(self.avance * config.PARALLAX_CIUDAD) % ancho
            pantalla.blit(self.ciudad, (x - ancho + ox, 0))
            pantalla.blit(self.ciudad, (x + ox, 0))

        # Nubes encima de la ciudad
        for nube, x, y in self.nubes:
            pantalla.blit(nube, (x + ox, y + oy))
