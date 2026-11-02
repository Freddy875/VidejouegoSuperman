# ==============================================================================
# jefe.py — Jefe final: dinosaurio robótico
# ------------------------------------------------------------------------------
# Objetivo: pelea final del Nivel 1 (GDD sección 7).
#  - Vida oculta (el jugador no la ve) y sin punto débil.
#  - 3 fases según la vida restante: piel completa, piel rota (se usa la
#    imagen de la fase 1 con pedazos de piel cayendo, porque falta la
#    imagen intermedia) y robot expuesto.
#  - Alterna MORDIDA (golpea la parte alta) y COLETAZO (golpea la parte
#    baja), cada uno con un aviso previo; en cada fase ataca más rápido.
#  - Al llegar a 0 explota y queda hecho chatarra.
# ==============================================================================

import math
import random

import pygame

import config
import recursos


# ------------------------------------------------------------------------------
# COLORES DE LOS PEDAZOS
# Piel para los cambios de fase y metal para la chatarra (GUIA_ESTILO 2.5).
# ------------------------------------------------------------------------------
COLORES_PIEL = [config.COLOR_JEFE_PIEL, config.COLOR_JEFE_PIEL_CLARA,
                config.COLOR_JEFE_PIEL_SOMBRA, config.COLOR_JEFE_FRANJA,
                config.COLOR_JEFE_VIENTRE]
COLORES_METAL = [config.COLOR_JEFE_METAL_OSCURO, config.COLOR_JEFE_METAL_MEDIO,
                 config.COLOR_JEFE_BRONCE, config.COLOR_JEFE_NUCLEO]


# ------------------------------------------------------------------------------
# CLASE JEFE
# Estados: "entrando", "espera", "aviso", "ataque", "derrotado", "chatarra".
# ------------------------------------------------------------------------------
class Jefe:
    def __init__(self, efectos, mensajes):
        self.efectos = efectos
        self.mensajes = mensajes

        # Imágenes por fase (la fase 2 reutiliza la de la fase 1)
        fase1 = recursos.cargar_sprite("jefe_fase1", (600, 450), config.COLOR_JEFE_PIEL)
        fase3 = recursos.cargar_sprite("jefe_fase3", (600, 450), config.COLOR_JEFE_METAL_MEDIO)
        self.imagenes = {1: fase1, 2: fase1, 3: fase3}
        self.blancas = {f: recursos.silueta_blanca(img) for f, img in self.imagenes.items()}

        # Chatarra: el robot oscurecido y caído de lado
        chatarra = fase3.copy()
        chatarra.fill((110, 100, 100, 255), special_flags=pygame.BLEND_RGBA_MULT)
        self.imagen_chatarra = pygame.transform.rotate(chatarra, 25)

        self.vida = config.JEFE_VIDA
        self.fase = 1
        self.estado = "entrando"
        self.x = config.ANCHO + fase1.get_width() / 2   # entra por la derecha
        self.y = config.JEFE_Y
        self.temporizador = 0.0
        self.siguiente_ataque = "mordida"
        self.ataque_actual = None
        self.destello = 0.0
        self.sacudida = 0.0
        self.espera_piel = 0.0
        self.espera_explosion = 0.0
        self.reloj = 0.0

        self.mensajes.mostrar_oleada(config.JEFE_MENSAJE)

    # --------------------------------------------------------------------------
    # POSICIÓN Y CAJAS
    # Durante el ataque el dinosaurio embiste hacia la izquierda; en la
    # mordida levanta la cabeza y en el coletazo se voltea y baja la cola.
    # --------------------------------------------------------------------------
    @property
    def imagen(self):
        imagen = self.imagenes[self.fase]
        if self.estado == "ataque" and self.ataque_actual == "coletazo":
            return pygame.transform.flip(imagen, True, False)
        return imagen

    def desplazamiento_ataque(self):
        # Sube y baja con forma de "campana": avanza rápido y regresa
        if self.estado != "ataque":
            return 0, 0
        duracion = config.JEFE_TIEMPOS[self.fase][1]
        avance = math.sin(math.pi * (1 - self.temporizador / duracion))
        if self.ataque_actual == "mordida":
            return -config.JEFE_EMBESTIDA * avance, -60 * avance
        return -config.JEFE_EMBESTIDA * avance, 130 * avance

    @property
    def rect(self):
        dx, dy = self.desplazamiento_ataque()
        return self.imagen.get_rect(center=(round(self.x + dx), round(self.y + dy)))

    @property
    def caja(self):
        rect = self.rect
        escala = config.JEFE_HITBOX
        return rect.inflate(-int(rect.width * (1 - escala)), -int(rect.height * (1 - escala)))

    @property
    def zona_ataque(self):
        # Franja de toda la pantalla que golpea el ataque en curso (o el aviso)
        if self.estado not in ("aviso", "ataque"):
            return None
        tipo = self.ataque_actual
        arriba, abajo = config.JEFE_MORDIDA_ZONA if tipo == "mordida" else config.JEFE_COLETAZO_ZONA
        return pygame.Rect(0, int(arriba * config.ALTO), config.ANCHO, int((abajo - arriba) * config.ALTO))

    @property
    def ataque_peligroso(self):
        # Solo hace daño durante el ataque, no durante el aviso
        return self.estado == "ataque"

    @property
    def vencible(self):
        # Solo recibe daño mientras pelea (no al entrar ni ya derrotado)
        return self.estado in ("espera", "aviso", "ataque")

    @property
    def terminado(self):
        return self.estado == "chatarra"

    # --------------------------------------------------------------------------
    # DAÑO Y FASES
    # --------------------------------------------------------------------------
    def recibir_dano(self, cantidad):
        if not self.vencible:
            return
        self.vida -= cantidad
        self.destello = config.ENEMIGO_DESTELLO

        # Cambio de fase según el porcentaje de vida restante
        porcentaje = self.vida / config.JEFE_VIDA
        nueva_fase = 1 if porcentaje > config.JEFE_FASE2 else (2 if porcentaje > config.JEFE_FASE3 else 3)
        if nueva_fase > self.fase and self.vida > 0:
            self.fase = nueva_fase
            self.sacudida = config.SACUDIDA_DURACION
            # Lluvia de pedazos de piel desde varios puntos del cuerpo
            for _ in range(6):
                x, y = self.punto_al_azar()
                self.efectos.fragmentos(x, y, COLORES_PIEL, cantidad=10, fuerza=220)

        if self.vida <= 0:
            self.estado = "derrotado"
            self.temporizador = config.JEFE_DERROTA_DURACION
            self.sacudida = config.SACUDIDA_DURACION

    def punto_al_azar(self):
        caja = self.caja
        return random.randint(caja.left, caja.right), random.randint(caja.top, caja.bottom)

    # --------------------------------------------------------------------------
    # ACTUALIZAR
    # Máquina de estados: entrar, esperar, avisar, atacar, y derrota.
    # --------------------------------------------------------------------------
    def actualizar(self, dt):
        self.reloj += dt
        self.destello = max(0.0, self.destello - dt)
        self.sacudida = max(0.0, self.sacudida - dt)
        aviso, duracion, pausa = config.JEFE_TIEMPOS[self.fase]

        if self.estado == "entrando":
            # Camina hacia su lugar; al llegar empieza a pelear
            self.x -= config.JEFE_VELOCIDAD_ENTRADA * dt
            if self.x <= config.JEFE_X:
                self.x = config.JEFE_X
                self.estado = "espera"
                self.temporizador = pausa

        elif self.estado == "espera":
            self.temporizador -= dt
            if self.temporizador <= 0:
                # Prepara el siguiente ataque y alterna el tipo
                self.ataque_actual = self.siguiente_ataque
                self.siguiente_ataque = "coletazo" if self.ataque_actual == "mordida" else "mordida"
                self.estado = "aviso"
                self.temporizador = aviso

        elif self.estado == "aviso":
            self.temporizador -= dt
            if self.temporizador <= 0:
                self.estado = "ataque"
                self.temporizador = duracion

        elif self.estado == "ataque":
            self.temporizador -= dt
            if self.temporizador <= 0:
                self.estado = "espera"
                self.temporizador = pausa

        elif self.estado == "derrotado":
            # Explosiones y chatarra cayendo mientras se hunde
            self.temporizador -= dt
            self.y += 40 * dt
            self.espera_explosion -= dt
            if self.espera_explosion <= 0:
                self.espera_explosion = 0.15
                x, y = self.punto_al_azar()
                self.efectos.explosion(x, y, 16, 220)
                self.efectos.fragmentos(x, y, COLORES_METAL, cantidad=6, fuerza=200)
            if self.temporizador <= 0:
                self.estado = "chatarra"
                self.sacudida = config.SACUDIDA_DURACION
                self.efectos.explosion(self.x, self.y, 40, 320)

        # Fase 2: la piel sintética se sigue cayendo poco a poco
        if self.fase == 2 and self.vencible:
            self.espera_piel -= dt
            if self.espera_piel <= 0:
                self.espera_piel = config.JEFE_PIEL_CADA
                x, y = self.punto_al_azar()
                self.efectos.fragmentos(x, y, COLORES_PIEL, cantidad=3, fuerza=80)

    # --------------------------------------------------------------------------
    # DIBUJAR
    # Primero el aviso (franja roja que parpadea con el nombre del ataque),
    # luego el dinosaurio con su destello blanco si recibió daño.
    # --------------------------------------------------------------------------
    def dibujar(self, pantalla, desplazamiento=(0, 0)):
        if self.estado == "aviso" and int(self.reloj * 10) % 2 == 0:
            zona = self.zona_ataque
            franja = pygame.Surface(zona.size, pygame.SRCALPHA)
            franja.fill(config.COLOR_AVISO + (config.AVISO_ALFA,))
            pantalla.blit(franja, zona.move(desplazamiento))
            texto = "¡MORDIDA! ¡BAJA!" if self.ataque_actual == "mordida" else "¡COLETAZO! ¡SUBE!"
            recursos.texto_contorno(pantalla, texto, config.TAMANO_FUENTE_MEDIANA,
                                    (config.ANCHO // 3, zona.centery))

        if self.estado == "chatarra":
            # Hundido en la parte baja de la pantalla, caído de lado
            rect = self.imagen_chatarra.get_rect(midbottom=(round(self.x), config.ALTO + 170))
            pantalla.blit(self.imagen_chatarra, rect.move(desplazamiento))
            return

        imagen = self.imagen
        if self.destello > 0:
            imagen = self.blancas[self.fase]
            if self.estado == "ataque" and self.ataque_actual == "coletazo":
                imagen = pygame.transform.flip(imagen, True, False)
        # Derrotado: tiembla mientras explota
        temblor = (random.randint(-4, 4), random.randint(-4, 4)) if self.estado == "derrotado" else (0, 0)
        pantalla.blit(imagen, self.rect.move(desplazamiento[0] + temblor[0], desplazamiento[1] + temblor[1]))
