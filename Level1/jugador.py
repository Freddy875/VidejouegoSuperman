# ==============================================================================
# jugador.py — Superman
# ------------------------------------------------------------------------------
# Objetivo: controlar a Superman: vuelo libre por toda la pantalla (sin
# gravedad ni suelo), vida de 0 a 100 con invulnerabilidad y parpadeo tras
# recibir daño, rayo láser de los ojos (Espacio) y golpe cercano (X).
# ==============================================================================

import math

import pygame

import config
import recursos


# ------------------------------------------------------------------------------
# LÁSER DE SUPERMAN
# Línea roja delgada y larga con núcleo blanco que viaja hacia la derecha.
# ------------------------------------------------------------------------------
class LaserHeroe:
    def __init__(self, x, y):
        self.x = float(x)
        self.y = y
        self.dano = config.LASER_DANO
        self.vivo = True

    @property
    def caja(self):
        return pygame.Rect(int(self.x), self.y - config.LASER_GROSOR,
                           config.LASER_LARGO, config.LASER_GROSOR * 2)

    def actualizar(self, dt):
        self.x += config.LASER_VELOCIDAD * dt
        # Al salir por la derecha deja de existir
        if self.x > config.ANCHO:
            self.vivo = False

    def dibujar(self, pantalla, desplazamiento=(0, 0)):
        x = int(self.x) + desplazamiento[0]
        y = self.y + desplazamiento[1]
        grosor = config.LASER_GROSOR
        # Halo rojo y núcleo blanco (GUIA_ESTILO 3)
        pantalla.fill(config.COLOR_LASER_HEROE, (x, y - grosor, config.LASER_LARGO, grosor * 2))
        pantalla.fill(config.COLOR_NUCLEO, (x + 4, y - grosor // 4 - 1, config.LASER_LARGO - 8, max(2, grosor // 2)))


# ------------------------------------------------------------------------------
# CLASE JUGADOR
# Posición en decimales para un movimiento suave; el rect es para dibujar.
# ------------------------------------------------------------------------------
class Jugador:
    def __init__(self, efectos):
        self.efectos = efectos
        self.imagen = recursos.cargar_sprite("superman", (120, 160), config.COLOR_HEROE_AZUL)
        # Versión blanca de la silueta para el parpadeo al recibir daño
        self.imagen_blanca = recursos.silueta_blanca(self.imagen)
        # Silueta dorada para el destello al recargar en la Zona de sol
        self.imagen_dorada = self.imagen.copy()
        self.imagen_dorada.fill(config.COLOR_SOL_DESTELLO + (0,), special_flags=pygame.BLEND_RGBA_MAX)
        self.cargando = False     # True mientras está dentro de la Zona de sol
        self.tiempo = 0.0         # reloj propio para animaciones

        self.rect = self.imagen.get_rect(center=(config.JUGADOR_X_INICIAL, config.ALTO // 2))
        self.x, self.y = float(self.rect.x), float(self.rect.y)
        self.vida = config.JUGADOR_VIDA_MAX
        self.invulnerable = 0.0  # segundos restantes

        # Habilidades
        self.lasers = []
        self.espera_laser = 0.0   # segundos para poder disparar otra vez
        self.espera_golpe = 0.0
        self.golpe_activo = 0.0   # segundos que le quedan al golpe en curso
        self.golpeados = set()    # enemigos ya alcanzados por este golpe

    # --------------------------------------------------------------------------
    # CAJAS DE CHOQUE
    # El cuerpo es más chico que la imagen (capa y aire alrededor); el golpe
    # es una zona de GOLPE_ALCANCE px frente a Superman.
    # --------------------------------------------------------------------------
    @property
    def caja(self):
        escala = config.JUGADOR_HITBOX
        caja = self.rect.copy()
        caja.width = int(self.rect.width * escala)
        caja.height = int(self.rect.height * escala)
        caja.center = self.rect.center
        return caja

    @property
    def caja_golpe(self):
        # Solo existe mientras el golpe está activo
        if self.golpe_activo <= 0:
            return None
        return pygame.Rect(self.caja.right, self.rect.top,
                           config.GOLPE_ALCANCE, int(self.rect.height * 0.6))

    # --------------------------------------------------------------------------
    # ACTUALIZAR
    # Movimiento, habilidades y temporizadores.
    # --------------------------------------------------------------------------
    def actualizar(self, dt, entrada):
        dx, dy = entrada.movimiento()
        self.x += dx * config.JUGADOR_VELOCIDAD * dt
        self.y += dy * config.JUGADOR_VELOCIDAD * dt

        # Límites: no puede salir de los bordes de la ventana
        self.x = max(0, min(self.x, config.ANCHO - self.rect.width))
        self.y = max(0, min(self.y, config.ALTO - self.rect.height))
        self.rect.topleft = (round(self.x), round(self.y))

        # Temporizadores que bajan con el tiempo
        self.tiempo += dt
        self.invulnerable = max(0.0, self.invulnerable - dt)
        self.espera_laser = max(0.0, self.espera_laser - dt)
        self.espera_golpe = max(0.0, self.espera_golpe - dt)
        self.golpe_activo = max(0.0, self.golpe_activo - dt)

        # Láser: un disparo por pulsación, con pausa mínima entre disparos
        if entrada.pulso("laser") and self.espera_laser <= 0:
            self.disparar_laser()

        # Golpe: activo un instante, con pausa antes del siguiente
        if entrada.pulso("golpe") and self.espera_golpe <= 0:
            self.golpe_activo = config.GOLPE_DURACION
            self.espera_golpe = config.GOLPE_PAUSA
            self.golpeados.clear()
            zona = self.caja_golpe
            self.efectos.chispa(zona.centerx, zona.centery, 24)

        # Avance de cada láser; se quitan los que ya terminaron
        for laser in self.lasers:
            laser.actualizar(dt)
        self.lasers = [laser for laser in self.lasers if laser.vivo]

    def disparar_laser(self):
        # El rayo sale de los ojos de Superman
        ojos_x = self.rect.x + int(self.rect.width * config.LASER_OJOS_X)
        ojos_y = self.rect.y + int(self.rect.height * config.LASER_OJOS_Y)
        self.lasers.append(LaserHeroe(ojos_x, ojos_y))
        self.espera_laser = config.LASER_PAUSA
        self.efectos.chispa(ojos_x, ojos_y, 10)

    # --------------------------------------------------------------------------
    # VIDA
    # Daño (con invulnerabilidad de 1 s) y recarga solar.
    # --------------------------------------------------------------------------
    def recibir_dano(self, cantidad):
        # Durante la invulnerabilidad los golpes no cuentan
        if self.invulnerable > 0 or self.vida <= 0:
            return False
        self.vida = max(0, self.vida - cantidad)
        self.invulnerable = config.JUGADOR_INVULNERABLE
        return True

    def recargar(self, cantidad):
        self.vida = min(config.JUGADOR_VIDA_MAX, self.vida + cantidad)

    # --------------------------------------------------------------------------
    # DIBUJAR
    # Mientras es invulnerable alterna entre su imagen y la silueta blanca;
    # al golpear se adelanta unos pixeles para que el golpe se sienta.
    # --------------------------------------------------------------------------
    def dibujar(self, pantalla, desplazamiento=(0, 0)):
        for laser in self.lasers:
            laser.dibujar(pantalla, desplazamiento)

        imagen = self.imagen
        if self.invulnerable > 0:
            fase = int(self.invulnerable / config.JUGADOR_PARPADEO)
            if fase % 2 == 0:
                imagen = self.imagen_blanca

        adelanto = 12 if self.golpe_activo > 0 else 0
        posicion = self.rect.move(desplazamiento[0] + adelanto, desplazamiento[1])
        pantalla.blit(imagen, posicion)

        # Recargando: brillo dorado que sube y baja suavemente
        if self.cargando and self.vida < config.JUGADOR_VIDA_MAX:
            self.imagen_dorada.set_alpha(int(60 + 60 * abs(math.sin(self.tiempo * 5))))
            pantalla.blit(self.imagen_dorada, posicion)
