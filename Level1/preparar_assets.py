# ==============================================================================
# preparar_assets.py — Procesado de imágenes del Nivel 1
# ------------------------------------------------------------------------------
# Objetivo: convertir los JPEG originales de la carpeta en sprites PNG listos
# para el juego: quita el fondo negro o blanco (lo vuelve transparente),
# limpia el borde para que no queden halos, recorta el espacio sobrante y
# reduce la imagen al tamaño en pantalla definido en config.py.
# Los originales NO se modifican; el resultado se guarda en assets/sprites/.
# Se puede volver a ejecutar cuando se quiera:  python preparar_assets.py
# ==============================================================================

import os

import pygame

import config


# ------------------------------------------------------------------------------
# MÁSCARA DEL FONDO
# Marca como fondo solo los pixeles del color de fondo que están conectados
# con el borde de la imagen. Así no se borran zonas negras o blancas que
# forman parte del personaje (ojos, contornos, dientes).
# ------------------------------------------------------------------------------
def mascara_fondo(imagen, color_fondo, tol, radio_cierre):
    # Todos los pixeles "parecidos" al color de fondo, estén donde estén
    parecidos = pygame.mask.from_threshold(
        imagen, color_fondo + (255,), (tol, tol, tol, 255))

    # Cierre: rellena huecos estrechos del personaje (sombras casi negras
    # pegadas al contorno) para que el fondo no se "cuele" por ellos
    if radio_cierre > 0:
        solido = parecidos.copy()
        solido.invert()
        solido = adelgazar(engrosar(solido, radio_cierre), radio_cierre)
        parecidos = solido
        parecidos.invert()
    return conectado_al_borde(parecidos)


# ------------------------------------------------------------------------------
# REGIONES CONECTADAS AL BORDE
# De una máscara, conserva solo las regiones que tocan el borde de la imagen.
# ------------------------------------------------------------------------------
def conectado_al_borde(parecidos):
    ancho, alto = parecidos.get_size()

    # Puntos semilla repartidos por los cuatro bordes de la imagen
    semillas = []
    for x in range(0, ancho, 8):
        semillas.append((x, 0))
        semillas.append((x, alto - 1))
    for y in range(0, alto, 8):
        semillas.append((0, y))
        semillas.append((ancho - 1, y))

    # Se suma cada región de fondo que toque el borde (una sola vez cada una)
    fondo = pygame.mask.Mask((ancho, alto))
    for semilla in semillas:
        if parecidos.get_at(semilla) and not fondo.get_at(semilla):
            fondo.draw(parecidos.connected_component(semilla), (0, 0))
    return fondo


# ------------------------------------------------------------------------------
# LIMPIEZA DEL BORDE
# Engrosa la máscara del fondo unos pixeles para "comerse" el halo que deja
# el JPEG alrededor del personaje.
# ------------------------------------------------------------------------------
def engrosar(mascara, radio):
    resultado = mascara.copy()

    # Se dibuja la máscara desplazada en todas direcciones dentro del radio
    for dx in range(-radio, radio + 1):
        for dy in range(-radio, radio + 1):
            resultado.draw(mascara, (dx, dy))
    return resultado


def adelgazar(mascara, radio):
    # Adelgazar = engrosar lo contrario y volver a invertir
    invertida = mascara.copy()
    invertida.invert()
    resultado = engrosar(invertida, radio)
    resultado.invert()
    return resultado


# ------------------------------------------------------------------------------
# QUITAR RUIDO
# Conserva solo las partes del personaje de tamaño razonable; borra manchas
# sueltas que el JPEG dejó en el fondo.
# ------------------------------------------------------------------------------
def quitar_ruido(mascara_personaje):
    limpia = pygame.mask.Mask(mascara_personaje.get_size())

    # Cada componente conectado mayor al mínimo se conserva
    for parte in mascara_personaje.connected_components(config.RUIDO_MINIMO):
        limpia.draw(parte, (0, 0))
    return limpia


# ------------------------------------------------------------------------------
# PROCESAR UN SPRITE
# Aplica todos los pasos a una imagen y la guarda como PNG transparente.
# ------------------------------------------------------------------------------
def procesar_sprite(nombre, datos):
    ruta_origen = os.path.join(config.CARPETA_BASE, datos["origen"])
    if not os.path.exists(ruta_origen):
        print(f"  [FALTA] {datos['origen']} -> el juego usará un rectángulo con etiqueta")
        return

    # Copia RGBA de la imagen original (el archivo original no se toca)
    original = pygame.image.load(ruta_origen)
    imagen = pygame.Surface(original.get_size(), pygame.SRCALPHA)
    imagen.blit(original, (0, 0))

    # 1) Máscara del fondo y limpieza del borde
    color = (0, 0, 0) if datos["fondo"] == "negro" else (255, 255, 255)
    tolerancia = datos.get("tolerancia", config.TOLERANCIA_FONDO)
    limpieza = datos.get("limpieza", config.LIMPIEZA_BORDE)
    cierre = datos.get("cierre", 0)
    fondo = engrosar(mascara_fondo(imagen, color, tolerancia, cierre), limpieza)

    # 2) Máscara del personaje = lo contrario del fondo
    personaje = fondo.copy()
    personaje.invert()

    # Zonas del dibujo que no forman parte del sprite (se borran a mano)
    for poligono in datos.get("borrar", []):
        zona = pygame.Surface(imagen.get_size(), pygame.SRCALPHA)
        pygame.draw.polygon(zona, (255, 255, 255, 255), poligono)
        personaje.erase(pygame.mask.from_surface(zona), (0, 0))

    # Sin manchas sueltas
    personaje = quitar_ruido(personaje)

    # 3) Volver transparente el fondo: se multiplica por una plantilla
    #    blanca opaca (personaje) / negra transparente (fondo)
    plantilla = personaje.to_surface(setcolor=(255, 255, 255, 255),
                                     unsetcolor=(0, 0, 0, 0))
    imagen.blit(plantilla, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)

    # 4) Recortar al rectángulo que ocupa el personaje
    rectangulos = personaje.get_bounding_rects()
    if not rectangulos:
        print(f"  [ERROR] {datos['origen']}: no se encontró el personaje")
        return
    caja = rectangulos[0].unionall(rectangulos[1:])
    imagen = imagen.subsurface(caja).copy()

    # 5) Reducir al tamaño en pantalla (vecino más cercano: pixeles nítidos)
    ancho, alto = imagen.get_size()
    if "ancho" in datos:
        nuevo = (datos["ancho"], round(alto * datos["ancho"] / ancho))
    else:
        nuevo = (round(ancho * datos["alto"] / alto), datos["alto"])
    imagen = pygame.transform.scale(imagen, nuevo)

    # 6) Voltear si el personaje mira hacia el lado equivocado
    if datos.get("voltear"):
        imagen = pygame.transform.flip(imagen, True, False)

    destino = os.path.join(config.CARPETA_SPRITES, nombre + ".png")
    pygame.image.save(imagen, destino)
    print(f"  [OK] {datos['origen']} -> {nombre}.png {nuevo[0]}x{nuevo[1]}")


# ------------------------------------------------------------------------------
# PROCESAR EL FONDO
# Metrópolis no lleva transparencia: solo se ajusta a la altura de la ventana.
# ------------------------------------------------------------------------------
def procesar_fondo():
    ruta_origen = os.path.join(config.CARPETA_BASE, config.FONDO_ORIGEN)
    if not os.path.exists(ruta_origen):
        print(f"  [FALTA] {config.FONDO_ORIGEN} -> se usará solo el cielo y las nubes")
        return
    original = pygame.image.load(ruta_origen)
    ancho, alto = original.get_size()
    nuevo = (round(ancho * config.ALTO / alto), config.ALTO)
    fondo = pygame.transform.scale(original, nuevo)

    # Tapar el sol: cada fila se pinta con el color del cielo a su izquierda
    x, y, ancho_sol, alto_sol = config.FONDO_TAPAR_SOL
    for fila in range(y, y + alto_sol):
        color = fondo.get_at((x - 4, fila))
        fondo.fill(color, (x, fila, ancho_sol, 1))

    pygame.image.save(fondo, os.path.join(config.CARPETA_SPRITES, "fondo_metropolis.png"))
    print(f"  [OK] {config.FONDO_ORIGEN} -> fondo_metropolis.png {nuevo[0]}x{nuevo[1]}")


# ------------------------------------------------------------------------------
# PROGRAMA PRINCIPAL
# Procesa todas las imágenes de la tabla SPRITES de config.py.
# ------------------------------------------------------------------------------
def preparar():
    os.makedirs(config.CARPETA_SPRITES, exist_ok=True)
    print("Preparando imágenes en", config.CARPETA_SPRITES)

    # Cada sprite de la tabla se procesa por separado
    for nombre, datos in config.SPRITES.items():
        procesar_sprite(nombre, datos)
    procesar_fondo()
    print("Listo.")


if __name__ == "__main__":
    preparar()
