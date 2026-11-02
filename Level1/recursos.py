# ==============================================================================
# recursos.py — Carga de sprites, fuentes y texto con contorno
# ------------------------------------------------------------------------------
# Objetivo: centralizar la carga de imágenes y fuentes. Si falta un sprite,
# devuelve un rectángulo de color con una etiqueta para que el juego siga
# funcionando; si falta la fuente Press Start 2P, usa la fuente de Pygame.
# ==============================================================================

import os

import pygame

import config


# ------------------------------------------------------------------------------
# CACHÉS
# Cada imagen y cada tamaño de fuente se cargan una sola vez.
# ------------------------------------------------------------------------------
_sprites = {}
_fuentes = {}


# ------------------------------------------------------------------------------
# SPRITES
# Carga un PNG de assets/sprites/. Si no existe, crea un sustituto visible.
# ------------------------------------------------------------------------------
def cargar_sprite(nombre, tamano_sustituto=(80, 80), color_sustituto=(200, 0, 200)):
    if nombre in _sprites:
        return _sprites[nombre]

    ruta = os.path.join(config.CARPETA_SPRITES, nombre + ".png")
    if os.path.exists(ruta):
        imagen = pygame.image.load(ruta).convert_alpha()
    else:
        # Sustituto: rectángulo de color con el nombre escrito encima
        print(f"[AVISO] Falta {ruta}; se usa un rectángulo con etiqueta")
        imagen = pygame.Surface(tamano_sustituto, pygame.SRCALPHA)
        imagen.fill(color_sustituto)
        pygame.draw.rect(imagen, (0, 0, 0), imagen.get_rect(), 2)
        etiqueta = pygame.font.Font(None, 20).render(nombre, False, (255, 255, 255))
        imagen.blit(etiqueta, etiqueta.get_rect(center=imagen.get_rect().center))

    _sprites[nombre] = imagen
    return imagen


def silueta_blanca(imagen):
    # Copia de la imagen toda en blanco (conserva la transparencia), para
    # los destellos al recibir daño
    blanca = imagen.copy()
    blanca.fill((255, 255, 255, 0), special_flags=pygame.BLEND_RGBA_MAX)
    return blanca


def sprites_listos():
    # Hay sprites procesados si existe al menos el de Superman
    return os.path.exists(os.path.join(config.CARPETA_SPRITES, "superman.png"))


# ------------------------------------------------------------------------------
# FUENTES
# Press Start 2P si está en assets/fonts/, si no la fuente por defecto.
# ------------------------------------------------------------------------------
def fuente(tamano):
    if tamano not in _fuentes:
        if os.path.exists(config.RUTA_FUENTE):
            _fuentes[tamano] = pygame.font.Font(config.RUTA_FUENTE, tamano)
        else:
            # La fuente por defecto se ve más chica: se compensa el tamaño
            _fuentes[tamano] = pygame.font.Font(None, int(tamano * 1.6))
    return _fuentes[tamano]


# ------------------------------------------------------------------------------
# TEXTO CON CONTORNO
# Texto blanco con contorno negro de 2 px (GUIA_ESTILO 4). Devuelve el
# rectángulo dibujado. "centro" indica el punto central del texto.
# ------------------------------------------------------------------------------
def texto_contorno(pantalla, texto, tamano, centro, color=config.COLOR_TEXTO, alfa=255):
    letra = fuente(tamano)
    frente = letra.render(texto, False, color)
    sombra = letra.render(texto, False, config.COLOR_CONTORNO)
    grosor = config.CONTORNO_TEXTO

    # Se arma el texto en una superficie propia para poder desvanecerlo
    lienzo = pygame.Surface((frente.get_width() + grosor * 2,
                             frente.get_height() + grosor * 2), pygame.SRCALPHA)

    # El contorno se dibuja copiando el texto negro alrededor del original
    for dx in range(-grosor, grosor + 1):
        for dy in range(-grosor, grosor + 1):
            if dx or dy:
                lienzo.blit(sombra, (grosor + dx, grosor + dy))
    lienzo.blit(frente, (grosor, grosor))

    if alfa < 255:
        lienzo.set_alpha(alfa)
    rect = lienzo.get_rect(center=centro)
    pantalla.blit(lienzo, rect)
    return rect
