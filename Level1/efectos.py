# ==============================================================================
# efectos.py — Chispas, explosiones y partículas
# ------------------------------------------------------------------------------
# Objetivo: efectos visuales de corta duración en estilo pixel art
# (GUIA_ESTILO 3 y 5): chispas de impacto en forma de estrella y explosiones
# hechas con cuadros de 4 a 8 px, sin círculos suaves.
# ==============================================================================

import random

import pygame

import config


# ------------------------------------------------------------------------------
# CHISPA DE IMPACTO
# Estrella de 4 puntas (núcleo blanco y halo amarillo) que se encoge.
# ------------------------------------------------------------------------------
class Chispa:
    DURACION = 0.15

    def __init__(self, x, y, tamano=18):
        self.x, self.y = x, y
        self.tamano = tamano
        self.tiempo = self.DURACION

    def actualizar(self, dt):
        self.tiempo -= dt
        return self.tiempo > 0

    def dibujar(self, pantalla, desplazamiento):
        # El tamaño baja conforme se acaba el tiempo
        t = max(0.0, self.tiempo / self.DURACION)
        largo = max(4, int(self.tamano * t))
        grosor = 4
        x = int(self.x) + desplazamiento[0]
        y = int(self.y) + desplazamiento[1]

        # Brazos de la estrella (halo) y centro (núcleo)
        pantalla.fill(config.COLOR_CHISPA, (x - largo, y - grosor // 2, largo * 2, grosor))
        pantalla.fill(config.COLOR_CHISPA, (x - grosor // 2, y - largo, grosor, largo * 2))
        pantalla.fill(config.COLOR_NUCLEO, (x - 4, y - 4, 8, 8))


# ------------------------------------------------------------------------------
# PARTÍCULA
# Cuadro que vuela, cae un poco y cambia de color según su edad.
# ------------------------------------------------------------------------------
class Particula:
    def __init__(self, x, y, vx, vy, vida, colores, tamano, gravedad=0):
        self.x, self.y = x, y
        self.vx, self.vy = vx, vy
        self.vida = self.vida_total = vida
        self.colores = colores
        self.tamano = tamano
        self.gravedad = gravedad

    def actualizar(self, dt):
        self.x += self.vx * dt
        self.y += self.vy * dt
        self.vy += self.gravedad * dt
        self.vida -= dt
        return self.vida > 0

    def dibujar(self, pantalla, desplazamiento):
        # El color avanza por la lista: blanco → amarillo → naranja → humo
        edad = 1 - self.vida / self.vida_total
        indice = min(len(self.colores) - 1, int(edad * len(self.colores)))
        x = int(self.x) + desplazamiento[0]
        y = int(self.y) + desplazamiento[1]
        pantalla.fill(self.colores[indice], (x, y, self.tamano, self.tamano))


# ------------------------------------------------------------------------------
# ADMINISTRADOR DE EFECTOS
# Guarda todos los efectos activos y los borra cuando terminan.
# ------------------------------------------------------------------------------
class Efectos:
    def __init__(self):
        self.lista = []

    def chispa(self, x, y, tamano=18):
        self.lista.append(Chispa(x, y, tamano))

    def explosion(self, x, y, cantidad=18, fuerza=180):
        # Cuadros que salen disparados en todas direcciones
        for _ in range(cantidad):
            self.lista.append(Particula(
                x, y,
                random.uniform(-fuerza, fuerza), random.uniform(-fuerza, fuerza),
                random.uniform(0.35, 0.7), config.COLORES_EXPLOSION,
                random.choice((4, 8)), gravedad=200))

    def fragmentos(self, x, y, colores, cantidad=12, fuerza=150):
        # Pedazos que caen (piel del jefe, chatarra); un solo color cada uno
        for _ in range(cantidad):
            color = random.choice(colores)
            self.lista.append(Particula(
                x, y,
                random.uniform(-fuerza, fuerza), random.uniform(-fuerza, 0),
                random.uniform(0.8, 1.6), [color],
                random.choice((4, 8)), gravedad=500))

    def actualizar(self, dt):
        # Solo se conservan los efectos que siguen vivos
        self.lista = [efecto for efecto in self.lista if efecto.actualizar(dt)]

    def dibujar(self, pantalla, desplazamiento=(0, 0)):
        for efecto in self.lista:
            efecto.dibujar(pantalla, desplazamiento)
