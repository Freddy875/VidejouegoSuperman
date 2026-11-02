# ==============================================================================
# entrada.py — Capa de acciones del jugador
# ------------------------------------------------------------------------------
# Objetivo: traducir teclas a ACCIONES del juego (mover, laser, golpe, pausa,
# confirmar). El resto del juego solo pregunta por acciones, nunca por
# teclas; así, para agregar un control (Xbox/PlayStation) solo hay que
# completar este archivo, sin reescribir el juego.
# Mapeo futuro de control: A = láser, B = golpe, Start = pausa.
# ==============================================================================

import pygame


# ------------------------------------------------------------------------------
# MAPEO DE TECLAS
# Cada acción puede tener varias teclas.
# ------------------------------------------------------------------------------
TECLAS_ACCION = {
    "laser": [pygame.K_SPACE],
    "golpe": [pygame.K_x],
    "pausa": [pygame.K_p, pygame.K_ESCAPE],
    "confirmar": [pygame.K_RETURN, pygame.K_KP_ENTER],
}
TECLAS_MOVER = {
    "arriba": [pygame.K_UP],
    "abajo": [pygame.K_DOWN],
    "izquierda": [pygame.K_LEFT],
    "derecha": [pygame.K_RIGHT],
}


# ------------------------------------------------------------------------------
# CLASE ENTRADA
# Junta los eventos de cada cuadro y responde preguntas por acción.
# ------------------------------------------------------------------------------
class Entrada:
    def __init__(self):
        # Acciones que se pulsaron en este cuadro (un disparo por pulsación)
        self.pulsadas = set()

    def nuevo_cuadro(self):
        # Se llama al inicio de cada cuadro, antes de leer los eventos
        self.pulsadas.clear()

    def procesar_evento(self, evento):
        # Se revisa si la tecla pulsada pertenece a alguna acción
        if evento.type == pygame.KEYDOWN:
            for accion, teclas in TECLAS_ACCION.items():
                if evento.key in teclas:
                    self.pulsadas.add(accion)
        # Aquí se agregará pygame.JOYBUTTONDOWN cuando haya control

    def pulso(self, accion):
        # True solo en el cuadro en que se presionó la acción
        return accion in self.pulsadas

    def movimiento(self):
        # Dirección de vuelo (dx, dy) entre -1 y 1 según las flechas
        teclas = pygame.key.get_pressed()

        def alguna(nombre):
            return any(teclas[t] for t in TECLAS_MOVER[nombre])

        dx = int(alguna("derecha")) - int(alguna("izquierda"))
        dy = int(alguna("abajo")) - int(alguna("arriba"))

        # En diagonal se normaliza para no ir más rápido
        if dx and dy:
            return dx * 0.7071, dy * 0.7071
        return dx, dy
