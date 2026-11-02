# ==============================================================================
# oleadas.py — Secuencia de oleadas y zonas de sol del Nivel 1
# ------------------------------------------------------------------------------
# Objetivo: lanzar las oleadas de config.OLEADAS una tras otra. Cada oleada
# muestra su mensaje, hace aparecer a sus enemigos según el horario y termina
# solo cuando todos fueron vencidos (o, en misiles, destruidos o esquivados)
# y ya se mostraron sus mensajes de tutorial. Después de cada oleada aparece
# una Zona de sol en la parte superior donde Superman recarga su vida.
# ==============================================================================

import math
import random

import pygame

import config
from enemigos import LexBot, Misil


# ------------------------------------------------------------------------------
# ZONA DE SOL
# Sol pixelado arriba al centro con rayos semitransparentes. Si Superman
# está dentro, recupera SOL_RECARGA de vida por segundo. Puede durar
# SOL_DURACION segundos o ser permanente (pelea contra el jefe).
# ------------------------------------------------------------------------------
class ZonaSol:
    def __init__(self, permanente=False):
        self.permanente = permanente
        self.tiempo = config.SOL_DURACION
        self.rect = pygame.Rect(0, 0, config.SOL_ANCHO, config.SOL_ALTO)
        self.rect.midtop = (config.ANCHO // 2, 0)
        self.reloj = 0.0  # para la animación de los rayos

        # Sol pixelado: círculo chico agrandado sin suavizar (cuadros de 4 px)
        chico = pygame.Surface((24, 24), pygame.SRCALPHA)
        pygame.draw.circle(chico, config.COLOR_SOL, (12, 12), 11)
        self.sol = pygame.transform.scale(chico, (96, 96))

    @property
    def activa(self):
        return self.permanente or self.tiempo > 0

    def actualizar(self, dt, jugador):
        self.reloj += dt
        if not self.permanente:
            self.tiempo -= dt

        # Recarga: basta con que una parte de Superman toque la zona
        jugador.cargando = self.activa and self.rect.colliderect(jugador.caja)
        if jugador.cargando:
            jugador.recargar(config.SOL_RECARGA * dt)

    def dibujar(self, pantalla, desplazamiento=(0, 0)):
        if not self.activa:
            return

        # En el último segundo la zona parpadea para avisar que se va
        if not self.permanente and self.tiempo < 1.0 and int(self.tiempo * 8) % 2 == 0:
            return

        # Rayos: franjas verticales que laten suavemente
        rayos = pygame.Surface(self.rect.size, pygame.SRCALPHA)
        latido = 0.8 + 0.2 * math.sin(self.reloj * 4)
        alfa = int(config.SOL_RAYOS_ALFA * latido)
        ancho_franja = 20
        for i, x in enumerate(range(0, self.rect.width, ancho_franja)):
            # Franjas alternas más y menos intensas
            alfa_franja = alfa if i % 2 == 0 else alfa // 2
            rayos.fill(config.COLOR_SOL_RAYOS + (alfa_franja,), (x, 0, ancho_franja, self.rect.height))
        pantalla.blit(rayos, self.rect.move(desplazamiento))

        # Círculo del sol en la parte alta de la zona
        centro = self.sol.get_rect(midtop=(self.rect.centerx, 6))
        pantalla.blit(self.sol, centro.move(desplazamiento))


# ------------------------------------------------------------------------------
# GRUPO DE MISILES
# Reparte los misiles en franjas de altura distintas para que no se encimen.
# ------------------------------------------------------------------------------
def crear_grupo_misiles():
    franjas = 6
    alto_franja = config.ALTO / franjas
    elegidas = random.sample(range(franjas), config.MISILES_POR_GRUPO)

    # Cada misil va al centro de su franja, con un desfase horizontal
    misiles = []
    for orden, franja in enumerate(elegidas):
        misil = Misil(alto_franja * (franja + 0.5))
        misil.x += orden * 60
        misiles.append(misil)
    return misiles


# ------------------------------------------------------------------------------
# CLASE OLEADAS
# Estados: "pausa" (antes de una oleada), "combate", "sol" (recarga después
# de cada oleada) y "fin" (no quedan más oleadas: sigue el jefe).
# ------------------------------------------------------------------------------
class Oleadas:
    def __init__(self, mensajes):
        self.mensajes = mensajes
        self.indice = -1               # oleada actual (aún ninguna)
        self.estado = "pausa"
        self.espera = config.PAUSA_ENTRE_OLEADAS
        self.reloj = 0.0               # segundos desde que empezó la oleada
        self.pendientes = []           # apariciones que aún no ocurren
        self.sol = None                # Zona de sol actual
        self.sol_explicado = False     # el mensaje del sol sale solo una vez

    @property
    def numero(self):
        return self.indice + 1

    # --------------------------------------------------------------------------
    # INICIAR OLEADA
    # --------------------------------------------------------------------------
    def iniciar_siguiente(self):
        self.indice += 1
        if self.indice >= len(config.OLEADAS):
            self.estado = "fin"
            return
        oleada = config.OLEADAS[self.indice]
        self.estado = "combate"
        self.reloj = 0.0
        self.pendientes = sorted(oleada["aparecen"])
        self.mensajes.mostrar_oleada(oleada["mensaje"])
        self.mensajes.agregar_tutorial(oleada.get("tutorial", []))

    # --------------------------------------------------------------------------
    # ACTUALIZAR
    # Agrega a "enemigos" los que toca que aparezcan, revisa si se terminó la
    # oleada y controla la Zona de sol entre oleadas.
    # --------------------------------------------------------------------------
    def actualizar(self, dt, enemigos, jugador):
        jugador.cargando = False

        if self.estado == "sol":
            self.sol.actualizar(dt, jugador)
            # Al apagarse el sol sigue la próxima oleada (o el jefe)
            if not self.sol.activa:
                self.sol = None
                if self.indice + 1 >= len(config.OLEADAS):
                    self.estado = "fin"
                else:
                    self.estado = "pausa"
                    self.espera = config.PAUSA_ENTRE_OLEADAS

        elif self.estado == "pausa":
            self.espera -= dt
            if self.espera <= 0:
                self.iniciar_siguiente()

        elif self.estado == "combate":
            self.reloj += dt

            # Aparecen todos los enemigos cuyo momento ya llegó
            while self.pendientes and self.pendientes[0][0] <= self.reloj:
                _, tipo, altura = self.pendientes.pop(0)
                if tipo == "misiles":
                    enemigos.extend(crear_grupo_misiles())
                else:
                    enemigos.append(LexBot(tipo, altura))

            # Fin de la oleada: nadie pendiente, nadie vivo y tutorial visto
            if not self.pendientes and not enemigos and self.mensajes.tutorial_terminado:
                self.estado = "sol"
                self.sol = ZonaSol()
                if not self.sol_explicado:
                    self.sol_explicado = True
                    self.mensajes.agregar_tutorial([config.SOL_MENSAJE])

    def dibujar(self, pantalla, desplazamiento=(0, 0)):
        if self.sol:
            self.sol.dibujar(pantalla, desplazamiento)
