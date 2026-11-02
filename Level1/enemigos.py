# ==============================================================================
# enemigos.py — LexBots, sus láseres y los misiles
# ------------------------------------------------------------------------------
# Objetivo: definir a los enemigos del Nivel 1 (GDD sección 6).
#  - LexBot1 / LexBot10 / LexBot20: entran por la derecha, se detienen,
#    flotan y disparan bolas de energía verdes (kriptonita) o rojo-magenta
#    (sol rojo). Si llegan a la izquierda se quedan flotando ahí.
#  - Misil: viaja en línea recta hacia la izquierda; se puede esquivar.
# Los valores de cada tipo viven en config.ENEMIGOS.
# ==============================================================================

import math
import random

import pygame

import config
import recursos


# ------------------------------------------------------------------------------
# LÁSER ENEMIGO
# Bola corta con núcleo blanco y halo verde o rojo-magenta, dibujada con
# cuadros (pixel art, sin círculos suaves). Viaja hacia donde estaba Superman.
# ------------------------------------------------------------------------------
class LaserEnemigo:
    def __init__(self, x, y, objetivo, dano):
        self.x, self.y = float(x), float(y)
        self.dano = dano
        self.color = random.choice((config.COLOR_LASER_VERDE, config.COLOR_LASER_ROJO))
        self.vivo = True

        # Dirección hacia el objetivo; si está detrás, dispara recto a la izquierda
        dx, dy = objetivo[0] - x, objetivo[1] - y
        if dx > -40:
            dx, dy = -1, 0
        distancia = math.hypot(dx, dy)
        self.vx = dx / distancia * config.LASER_ENEMIGO_VELOCIDAD
        self.vy = dy / distancia * config.LASER_ENEMIGO_VELOCIDAD

    @property
    def caja(self):
        r = config.LASER_ENEMIGO_RADIO
        return pygame.Rect(int(self.x) - r, int(self.y) - r, r * 2, r * 2)

    def actualizar(self, dt):
        self.x += self.vx * dt
        self.y += self.vy * dt
        # Fuera de la pantalla desaparece
        if not -50 < self.x < config.ANCHO + 50 or not -50 < self.y < config.ALTO + 50:
            self.vivo = False

    def dibujar(self, pantalla, desplazamiento=(0, 0)):
        r = config.LASER_ENEMIGO_RADIO
        x = int(self.x) + desplazamiento[0]
        y = int(self.y) + desplazamiento[1]
        # Halo en forma de cruz gruesa (bola pixelada) y núcleo blanco
        pantalla.fill(self.color, (x - r, y - r // 2, r * 2, r))
        pantalla.fill(self.color, (x - r // 2, y - r, r, r * 2))
        pantalla.fill(self.color, (x - r + 2, y - r + 2, r * 2 - 4, r * 2 - 4))
        pantalla.fill(config.COLOR_NUCLEO, (x - r // 2, y - r // 2, r, r))


# ------------------------------------------------------------------------------
# CLASE BASE DE ENEMIGO
# Vida, destello blanco al recibir daño y caja de choque.
# ------------------------------------------------------------------------------
class Enemigo:
    es_misil = False

    def __init__(self, nombre_sprite, x, y, vida, dano_choque, color_sustituto):
        self.imagen = recursos.cargar_sprite(nombre_sprite, (80, 60), color_sustituto)
        self.imagen_blanca = recursos.silueta_blanca(self.imagen)
        self.x, self.y = float(x), float(y)  # centro del enemigo
        self.vida = vida
        self.dano_choque = dano_choque
        self.destello = 0.0
        self.vivo = True

    @property
    def rect(self):
        return self.imagen.get_rect(center=(round(self.x), round(self.y)))

    @property
    def caja(self):
        # Caja de choque un poco más chica que la imagen
        return self.rect.inflate(-self.rect.width // 5, -self.rect.height // 5)

    def recibir_dano(self, cantidad):
        self.vida -= cantidad
        self.destello = config.ENEMIGO_DESTELLO
        if self.vida <= 0:
            self.vivo = False

    def empujar(self, distancia):
        # El golpe lo hace retroceder (hacia la derecha)
        self.x += distancia

    def dibujar(self, pantalla, desplazamiento=(0, 0)):
        imagen = self.imagen_blanca if self.destello > 0 else self.imagen
        pantalla.blit(imagen, self.rect.move(desplazamiento))


# ------------------------------------------------------------------------------
# LEXBOT
# Un solo comportamiento para los tres tipos; cambia según config.ENEMIGOS.
# ------------------------------------------------------------------------------
class LexBot(Enemigo):
    def __init__(self, tipo, y_fraccion):
        datos = config.ENEMIGOS[tipo]
        self.tipo = tipo
        self.datos = datos
        imagen = recursos.cargar_sprite(tipo, (80, 60), config.COLOR_LEX_VERDE)
        x = config.ANCHO + imagen.get_width() // 2  # aparece fuera, a la derecha

        # Altura de base: dentro de la pantalla aunque flote hacia arriba y abajo
        margen = imagen.get_height() // 2 + datos["flotar_amplitud"] + 10
        y = max(margen, min(config.ALTO - margen, y_fraccion * config.ALTO))
        super().__init__(tipo, x, y, datos["vida"], datos["dano_choque"], config.COLOR_LEX_VERDE)

        self.margen = margen
        self.y_base = self.y
        self.y_objetivo = self.y
        self.parada_x = random.uniform(*datos["parada_x"]) * config.ANCHO
        self.tiempo = random.uniform(0, datos["flotar_periodo"])  # desfase al flotar
        self.espera_disparo = datos["disparo_cada"] * random.uniform(0.5, 1.0)
        self.disparos_pendientes = 0
        self.espera_seguido = 0.0
        self.espera_altura = datos["cambio_altura_cada"]

    # --------------------------------------------------------------------------
    # ACTUALIZAR
    # Entrar, flotar, cambiar de altura y disparar.
    # --------------------------------------------------------------------------
    def actualizar(self, dt, jugador, lasers_enemigos):
        datos = self.datos
        self.tiempo += dt
        self.destello = max(0.0, self.destello - dt)

        # Avanza hacia la izquierda hasta su punto de parada
        if self.x > self.parada_x:
            self.x = max(self.parada_x, self.x - datos["velocidad"] * dt)
        # Nunca sale por la izquierda: ahí se queda flotando
        self.x = max(self.x, config.LEXBOT_X_MINIMA + self.rect.width // 2)

        # Cambio de altura cada cierto tiempo (LexBot10)
        if datos["cambio_altura_cada"] > 0:
            self.espera_altura -= dt
            if self.espera_altura <= 0:
                self.espera_altura = datos["cambio_altura_cada"]
                self.y_objetivo = random.uniform(self.margen, config.ALTO - self.margen)
            # Se acerca a la nueva altura poco a poco
            self.y_base += (self.y_objetivo - self.y_base) * min(1.0, 2.5 * dt)

        # Flotar: sube y baja suavemente alrededor de su altura de base
        onda = math.sin(2 * math.pi * self.tiempo / datos["flotar_periodo"])
        self.y = self.y_base + onda * datos["flotar_amplitud"]

        # Solo dispara cuando ya está completamente dentro de la pantalla
        if self.rect.right < config.ANCHO:
            self.espera_disparo -= dt
            if self.espera_disparo <= 0:
                self.espera_disparo = datos["disparo_cada"]
                self.disparos_pendientes = datos["disparos_seguidos"]
                self.espera_seguido = 0.0

        # Ráfaga: los disparos seguidos salen separados por una pausa corta
        if self.disparos_pendientes > 0:
            self.espera_seguido -= dt
            if self.espera_seguido <= 0:
                self.disparos_pendientes -= 1
                self.espera_seguido = config.DISPARO_SEGUIDO_PAUSA
                lasers_enemigos.append(LaserEnemigo(
                    self.rect.left + 10, self.y, jugador.rect.center, datos["dano_laser"]))


# ------------------------------------------------------------------------------
# MISIL
# Línea recta hacia la izquierda; si sale de la pantalla cuenta como superado.
# ------------------------------------------------------------------------------
class Misil(Enemigo):
    es_misil = True

    def __init__(self, y):
        super().__init__("misil", config.ANCHO + 40, y, config.MISIL_VIDA,
                         config.MISIL_DANO_CHOQUE, config.COLOR_MISIL_CUERPO)

    def actualizar(self, dt, jugador, lasers_enemigos):
        self.destello = max(0.0, self.destello - dt)
        self.x -= config.MISIL_VELOCIDAD * dt
        # Salió por la izquierda: esquivado
        if self.rect.right < 0:
            self.vivo = False

    def empujar(self, distancia):
        # Los misiles no retroceden (el golpe los destruye al instante)
        pass
