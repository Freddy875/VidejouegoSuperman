# ==============================================================================
# main.py — Punto de entrada del Nivel 1
# ------------------------------------------------------------------------------
# Objetivo: abrir la ventana (1280×720 a 60 FPS), preparar los sprites si
# todavía no existen y ejecutar el ciclo principal del juego: leer entrada,
# actualizar el mundo, resolver choques y dibujarlo.
# Flujo: título → nivel (5 oleadas con Zona de sol + jefe final) → victoria,
# con pausa y Game Over. Música en bucle durante todo el nivel.
# Ejecutar con:  python main.py
# ==============================================================================

import random
import sys

import pygame

import config
import pantallas
import recursos
from efectos import Efectos
from entrada import Entrada
from fondo import Fondo
from jefe import Jefe
from jugador import Jugador
from oleadas import Oleadas, ZonaSol


# ------------------------------------------------------------------------------
# CLASE JUEGO
# Contiene la ventana, el reloj y todos los objetos del nivel.
# ------------------------------------------------------------------------------
class Juego:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption(config.TITULO)
        self.pantalla = pygame.display.set_mode((config.ANCHO, config.ALTO))
        self.reloj = pygame.time.Clock()
        self.entrada = Entrada()

        # Si es la primera vez, se procesan las imágenes originales
        if not recursos.sprites_listos():
            import preparar_assets
            preparar_assets.preparar()

        # Música: si no hay dispositivo de audio, el juego sigue sin sonido
        self.hay_audio = True
        try:
            pygame.mixer.init()
        except pygame.error:
            self.hay_audio = False

        self.fondo = Fondo()
        self.corriendo = True
        # Estados: "titulo", "jugando", "pausa", "game_over", "victoria"
        self.estado = "titulo"
        self.tiempo_pantalla = 0.0  # para los textos que parpadean
        self.reiniciar_nivel()

    # --------------------------------------------------------------------------
    # INICIO DEL NIVEL Y MÚSICA
    # --------------------------------------------------------------------------
    def empezar_nivel(self):
        self.reiniciar_nivel()
        self.estado = "jugando"

        # Atajo de prueba: saltar las oleadas e ir directo al jefe
        if config.EMPEZAR_EN_JEFE:
            self.oleadas.indice = len(config.OLEADAS)
            self.oleadas.estado = "fin"

        # La música suena en bucle (-1) durante todo el nivel
        if self.hay_audio:
            try:
                pygame.mixer.music.load(config.RUTA_MUSICA)
                pygame.mixer.music.set_volume(config.VOLUMEN_MUSICA)
                pygame.mixer.music.play(-1)
            except pygame.error as error:
                print("[AVISO] No se pudo reproducir la música:", error)

    def detener_musica(self, desvanecer_ms=0):
        if self.hay_audio:
            pygame.mixer.music.fadeout(desvanecer_ms) if desvanecer_ms else pygame.mixer.music.stop()

    def reiniciar_nivel(self):
        # Todo lo que cambia durante el nivel se crea aquí
        self.efectos = Efectos()
        self.jugador = Jugador(self.efectos)
        self.mensajes = pantallas.Mensajes()
        self.oleadas = Oleadas(self.mensajes)
        self.enemigos = []
        self.lasers_enemigos = []
        self.jefe = None
        self.sol_jefe = None  # Zona de sol permanente durante el jefe
        self.tiempo = 0.0  # segundos de juego (para parpadeos)
        self.espera_victoria = config.VICTORIA_ESPERA

    # --------------------------------------------------------------------------
    # EVENTOS
    # Cierre de ventana, paso de teclas a la capa de acciones y cambios de
    # pantalla (Enter para iniciar o reintentar, P / Esc para pausar).
    # --------------------------------------------------------------------------
    def leer_eventos(self):
        self.entrada.nuevo_cuadro()

        # Se revisan todos los eventos pendientes del cuadro
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                self.corriendo = False
            self.entrada.procesar_evento(evento)

        # Cada pantalla responde solo a sus acciones
        if self.estado in ("titulo", "game_over") and self.entrada.pulso("confirmar"):
            self.empezar_nivel()
        elif self.estado == "jugando" and self.entrada.pulso("pausa"):
            self.estado = "pausa"
            if self.hay_audio:
                pygame.mixer.music.pause()
        elif self.estado == "pausa" and self.entrada.pulso("pausa"):
            self.estado = "jugando"
            if self.hay_audio:
                pygame.mixer.music.unpause()
        elif self.estado == "victoria" and self.entrada.pulso("confirmar"):
            self.detener_musica()
            self.estado = "titulo"

    # --------------------------------------------------------------------------
    # PASO DEL JUEGO
    # Decide qué se actualiza según la pantalla actual.
    # --------------------------------------------------------------------------
    def paso(self, dt):
        self.tiempo_pantalla += dt

        if self.estado == "titulo":
            self.fondo.actualizar(dt)

        elif self.estado == "jugando":
            self.actualizar(dt)

            # Sin vida: Game Over
            if self.jugador.vida <= 0:
                self.estado = "game_over"
                self.detener_musica(1500)

            # Jefe hecho chatarra: tras una breve espera, pantalla de victoria
            elif self.jefe and self.jefe.terminado:
                self.espera_victoria -= dt
                if self.espera_victoria <= 0:
                    self.estado = "victoria"

        elif self.estado == "victoria":
            # La escena sigue viva detrás del texto (nubes, humo)
            self.fondo.actualizar(dt)
            self.efectos.actualizar(dt)
        # En "pausa" y "game_over" el juego queda congelado

    # --------------------------------------------------------------------------
    # ACTUALIZAR EL NIVEL
    # --------------------------------------------------------------------------
    def actualizar(self, dt):
        self.tiempo += dt
        self.fondo.actualizar(dt)
        self.jugador.actualizar(dt, self.entrada)
        self.oleadas.actualizar(dt, self.enemigos, self.jugador)
        self.mensajes.actualizar(dt)

        # Terminadas las oleadas entra el jefe, con el sol siempre activo
        if self.oleadas.estado == "fin" and self.jefe is None:
            self.jefe = Jefe(self.efectos, self.mensajes)
            self.sol_jefe = ZonaSol(permanente=True)
        if self.jefe:
            self.jefe.actualizar(dt)
            if not self.jefe.terminado:
                self.sol_jefe.actualizar(dt, self.jugador)

        # Enemigos y sus disparos
        for enemigo in self.enemigos:
            enemigo.actualizar(dt, self.jugador, self.lasers_enemigos)
        for laser in self.lasers_enemigos:
            laser.actualizar(dt)

        self.resolver_choques()

        # Se quitan los enemigos vencidos (con explosión) y los misiles esquivados
        for enemigo in self.enemigos:
            if not enemigo.vivo and enemigo.vida <= 0:
                self.efectos.explosion(enemigo.x, enemigo.y, 24 if not enemigo.es_misil else 12)
        self.enemigos = [e for e in self.enemigos if e.vivo]
        self.lasers_enemigos = [l for l in self.lasers_enemigos if l.vivo]

        self.efectos.actualizar(dt)

    # --------------------------------------------------------------------------
    # CHOQUES
    # Láser y golpe de Superman contra enemigos; láseres enemigos y cuerpos
    # de los enemigos contra Superman.
    # --------------------------------------------------------------------------
    def resolver_choques(self):
        jugador = self.jugador

        # Láseres de Superman: cada uno se gasta en el primer enemigo que toca
        for laser in jugador.lasers:
            for enemigo in self.enemigos:
                if enemigo.vivo and laser.caja.colliderect(enemigo.caja):
                    enemigo.recibir_dano(laser.dano)
                    laser.vivo = False
                    self.efectos.chispa(enemigo.caja.left + 10, laser.y)
                    break

        # Golpe: alcanza una sola vez a cada enemigo por golpe
        zona = jugador.caja_golpe
        if zona:
            for enemigo in self.enemigos:
                if enemigo.vivo and enemigo not in jugador.golpeados and zona.colliderect(enemigo.caja):
                    jugador.golpeados.add(enemigo)
                    if enemigo.es_misil:
                        enemigo.recibir_dano(enemigo.vida)  # destruido al instante
                    else:
                        enemigo.recibir_dano(config.GOLPE_DANO)
                        enemigo.empujar(config.GOLPE_EMPUJE)
                    self.efectos.chispa(zona.right - 10, zona.centery, 26)

        # Láseres enemigos contra Superman
        for laser in self.lasers_enemigos:
            if laser.caja.colliderect(jugador.caja):
                laser.vivo = False
                jugador.recibir_dano(laser.dano)

        # Choque cuerpo a cuerpo; el misil explota al chocar
        for enemigo in self.enemigos:
            if enemigo.vivo and enemigo.caja.colliderect(jugador.caja):
                if jugador.recibir_dano(enemigo.dano_choque) and enemigo.es_misil:
                    enemigo.recibir_dano(enemigo.vida)

        if self.jefe and self.jefe.vencible:
            self.choques_jefe()

    def choques_jefe(self):
        jugador, jefe = self.jugador, self.jefe
        caja_jefe = jefe.caja

        # Láseres de Superman contra el jefe
        for laser in jugador.lasers:
            if laser.vivo and laser.caja.colliderect(caja_jefe):
                jefe.recibir_dano(laser.dano)
                laser.vivo = False
                self.efectos.chispa(laser.caja.right, laser.y)

        # Golpe contra el jefe (una vez por golpe)
        zona = jugador.caja_golpe
        if zona and jefe not in jugador.golpeados and zona.colliderect(caja_jefe):
            jugador.golpeados.add(jefe)
            jefe.recibir_dano(config.GOLPE_DANO)
            self.efectos.chispa(zona.right - 10, zona.centery, 26)

        # Mordida o coletazo: daño a todo lo que esté en su franja
        if jefe.ataque_peligroso and jefe.zona_ataque.colliderect(jugador.caja):
            jugador.recibir_dano(config.JEFE_DANO_ATAQUE)

        # Chocar con el cuerpo del dinosaurio
        if caja_jefe.colliderect(jugador.caja):
            jugador.recibir_dano(config.JEFE_DANO_CHOQUE)

    # --------------------------------------------------------------------------
    # DIBUJAR
    # El título tiene su propia pantalla; las demás se dibujan encima de la
    # escena del nivel (que queda congelada en pausa y Game Over).
    # --------------------------------------------------------------------------
    def dibujar(self):
        if self.estado == "titulo":
            self.fondo.dibujar(self.pantalla)
            pantallas.dibujar_titulo(self.pantalla, self.tiempo_pantalla)
        else:
            self.dibujar_escena()
            if self.estado == "pausa":
                pantallas.dibujar_pausa(self.pantalla)
            elif self.estado == "game_over":
                pantallas.dibujar_game_over(self.pantalla, self.tiempo_pantalla)
            elif self.estado == "victoria":
                pantallas.dibujar_victoria(self.pantalla, self.tiempo_pantalla)
        pygame.display.flip()

    # --------------------------------------------------------------------------
    # ESCENA DEL NIVEL
    # Orden de capas: fondo, sol, enemigos, jefe, Superman, disparos, efectos
    # e interfaz.
    # --------------------------------------------------------------------------
    def dibujar_escena(self):
        # Sacudida de pantalla (cambio de fase del jefe): todo se desplaza
        # un poco al azar, menos la interfaz
        mover = (0, 0)
        if self.jefe and self.jefe.sacudida > 0:
            fuerza = config.SACUDIDA_FUERZA
            mover = (random.randint(-fuerza, fuerza), random.randint(-fuerza, fuerza))

        self.fondo.dibujar(self.pantalla, mover)
        self.oleadas.dibujar(self.pantalla, mover)
        if self.sol_jefe and not self.jefe.terminado:
            self.sol_jefe.dibujar(self.pantalla, mover)
        for enemigo in self.enemigos:
            enemigo.dibujar(self.pantalla, mover)
        if self.jefe:
            self.jefe.dibujar(self.pantalla, mover)
        self.jugador.dibujar(self.pantalla, mover)
        for laser in self.lasers_enemigos:
            laser.dibujar(self.pantalla, mover)
        self.efectos.dibujar(self.pantalla, mover)
        pantallas.dibujar_barra_vida(self.pantalla, self.jugador.vida, self.tiempo)
        self.mensajes.dibujar(self.pantalla)

    # --------------------------------------------------------------------------
    # CICLO PRINCIPAL
    # dt = segundos desde el cuadro anterior (se limita para evitar saltos).
    # --------------------------------------------------------------------------
    def ejecutar(self):
        while self.corriendo:
            dt = min(self.reloj.tick(config.FPS) / 1000, 0.05)
            self.leer_eventos()
            self.paso(dt)
            self.dibujar()
        pygame.quit()


if __name__ == "__main__":
    Juego().ejecutar()
    sys.exit()
