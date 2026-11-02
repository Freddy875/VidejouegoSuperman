# ==============================================================================
# config.py — Valores ajustables del Nivel 1
# ------------------------------------------------------------------------------
# Objetivo: reunir en un solo lugar TODOS los números del juego (vida, daño,
# velocidades, tiempos, tamaños y colores). Para balancear el nivel solo hay
# que cambiar valores aquí, sin tocar la lógica de los demás archivos.
# Los valores marcados "(propuesta)" vienen así del GDD y se ajustan al probar.
# ==============================================================================

import os


# ------------------------------------------------------------------------------
# RUTAS
# Carpetas de imágenes originales, sprites procesados, fuentes y música.
# ------------------------------------------------------------------------------
CARPETA_BASE = os.path.dirname(os.path.abspath(__file__))
CARPETA_SPRITES = os.path.join(CARPETA_BASE, "assets", "sprites")
CARPETA_FUENTES = os.path.join(CARPETA_BASE, "assets", "fonts")
RUTA_FUENTE = os.path.join(CARPETA_FUENTES, "PressStart2P-Regular.ttf")
RUTA_MUSICA = os.path.join(CARPETA_BASE, "musica_nivel1.ogg")


# ------------------------------------------------------------------------------
# PANTALLA
# Resolución, cuadros por segundo y título de la ventana.
# ------------------------------------------------------------------------------
ANCHO = 1280
ALTO = 720
FPS = 60
TITULO = "Superman — Nivel 1: Metrópolis"
TITULO_JUEGO = "SUPERMAN"
SUBTITULO_JUEGO = "Nivel 1: Metrópolis"
# Segundos que se ve la chatarra antes de la pantalla de victoria.
VICTORIA_ESPERA = 2.0


# ------------------------------------------------------------------------------
# DEPURACIÓN
# Atajos para probar el nivel. Dejar en False para jugar normalmente.
# ------------------------------------------------------------------------------
EMPEZAR_EN_JEFE = False         # True = el nivel empieza directo en el jefe


# ------------------------------------------------------------------------------
# PROCESADO DE IMÁGENES (preparar_assets.py)
# Para cada sprite: archivo original, fondo a quitar ("negro" o "blanco"),
# medida final en pantalla (ancho o alto, en px) y si se voltea en horizontal.
# Superman debe mirar a la derecha; enemigos y misiles a la izquierda.
# Opcionales: "tolerancia" y "limpieza" (ver abajo) y "borrar": polígonos en
# pixeles de la imagen original que se eliminan (p. ej. el rayo que dispara
# el LexBot1 en su dibujo, porque en el juego el láser es aparte).
# Los fondos negros usan tolerancia baja y casi sin limpieza: los contornos
# del pixel art son casi negros y se perderían. Además usan "cierre" (radio
# en px originales) para rellenar sombras oscuras dentro del personaje.
# ------------------------------------------------------------------------------
SPRITES = {
    "superman":  {"origen": "Superman.jpeg", "fondo": "blanco", "ancho": 120, "voltear": False},
    "lexbot1":   {"origen": "LexBot1.jpeg", "fondo": "negro", "ancho": 80, "voltear": True,
                  "tolerancia": 26, "limpieza": 1, "cierre": 14,
                  "borrar": [[(845, 405), (1536, 470), (1536, 720), (1110, 615), (845, 470)]]},
    "lexbot10":  {"origen": "LexBot10.jpeg", "fondo": "negro", "ancho": 110, "voltear": False,
                  "tolerancia": 26, "limpieza": 1, "cierre": 14,
                  "borrar": [[(0, 170), (262, 170), (262, 520), (0, 520)]]},
    "lexbot20":  {"origen": "LexBot20.jpeg", "fondo": "blanco", "ancho": 150, "voltear": False},
    "misil":     {"origen": "Misil.jpeg", "fondo": "negro", "ancho": 60, "voltear": True,
                  "tolerancia": 26, "limpieza": 1, "cierre": 14},
    "jefe_fase1": {"origen": "Final Boss1.jpeg", "fondo": "blanco", "alto": 450, "voltear": False},
    "jefe_fase3": {"origen": "Final Boss2.jpeg", "fondo": "blanco", "alto": 450, "voltear": False},
}
# Distancia máxima (por canal RGB) para considerar un pixel como "fondo".
TOLERANCIA_FONDO = 40
# Pixeles del borde que se recortan para quitar halos negros o blancos
# (medidos en la imagen original, antes de reducirla).
LIMPIEZA_BORDE = 4
# Manchas sueltas más pequeñas que esto (px en la imagen original) se borran.
RUIDO_MINIMO = 400
# Fondo con desplazamiento: se reduce a la altura de la ventana.
FONDO_ORIGEN = "Metropolis.jpeg"
# Rectángulo (x, y, ancho, alto, ya en 1280×720) donde está el sol del dibujo.
# Se tapa con el color del cielo porque al repetir la imagen reflejada
# aparecían dos soles juntos; el sol del juego lo dibuja la Zona de sol.
FONDO_TAPAR_SOL = (1150, 10, 125, 110)


# ------------------------------------------------------------------------------
# FONDO (PARALLAX)
# Velocidad base de avance del nivel y multiplicador de cada capa.
# ------------------------------------------------------------------------------
VELOCIDAD_AVANCE = 120          # px/s de referencia (propuesta)
PARALLAX_NUBES = 0.2            # capa de nubes (lenta)
PARALLAX_CIUDAD = 0.5           # capa de Metrópolis (media)
# Velo claro sobre la ciudad para que el fondo no compita con los sprites.
VELO_FONDO_ALFA = 60            # 0 = sin velo, 255 = blanco total
CANTIDAD_NUBES = 7
NUBES_Y_MAX = 140              # las nubes no bajan hasta los edificios
# Letrero del Daily Planet (x, y, ancho, alto en 1280×720). En la copia
# reflejada se vuelve a pegar sin reflejar para que el texto se lea bien.
FONDO_LETRERO = (688, 258, 160, 132)


# ------------------------------------------------------------------------------
# SUPERMAN
# Movimiento libre por toda la pantalla, vida y retroalimentación de daño.
# ------------------------------------------------------------------------------
JUGADOR_VELOCIDAD = 380         # px/s (propuesta)
JUGADOR_X_INICIAL = 200
JUGADOR_VIDA_MAX = 100
JUGADOR_INVULNERABLE = 1.0      # segundos tras recibir daño (propuesta)
JUGADOR_PARPADEO = 0.08         # segundos entre parpadeos
# Fracción del sprite que cuenta como caja de choque (la imagen tiene aire).
JUGADOR_HITBOX = 0.6


# ------------------------------------------------------------------------------
# HABILIDADES DE SUPERMAN
# Rayo láser (Espacio) y golpe (X).
# ------------------------------------------------------------------------------
LASER_DANO = 2
LASER_PAUSA = 0.25              # s mínimos entre disparos (propuesta)
LASER_VELOCIDAD = 1100          # px/s
LASER_LARGO = 70
LASER_GROSOR = 4
# Posición de los ojos dentro del sprite (fracción de ancho y alto).
LASER_OJOS_X = 0.62
LASER_OJOS_Y = 0.14

GOLPE_DANO = 1
GOLPE_PAUSA = 0.4               # s (propuesta)
GOLPE_ALCANCE = 80              # px frente a Superman (propuesta)
GOLPE_DURACION = 0.12           # s que el golpe está activo
GOLPE_EMPUJE = 40               # px que retrocede el enemigo golpeado


# ------------------------------------------------------------------------------
# ZONA DE SOL
# Recarga de vida después de cada oleada y permanente durante el jefe.
# ------------------------------------------------------------------------------
SOL_RECARGA = 10                # vida por segundo (propuesta)
SOL_DURACION = 6.0              # s (propuesta)
SOL_ANCHO = 420
SOL_ALTO = 170


# ------------------------------------------------------------------------------
# ENEMIGOS
# Valores de la tabla 6.2 del GDD y comportamiento de la sección 6.3.
# ------------------------------------------------------------------------------
ENEMIGOS = {
    "lexbot1": {
        "vida": 2, "dano_laser": 5, "dano_choque": 5,
        "disparo_cada": 3.0, "disparos_seguidos": 1,
        "velocidad": 120,              # px/s al entrar (el más lento)
        "parada_x": (0.70, 0.90),      # rango de X donde se detiene (fracción del ancho)
        "flotar_amplitud": 30, "flotar_periodo": 3.0,
        "cambio_altura_cada": 0,       # 0 = no cambia de altura
    },
    "lexbot10": {
        "vida": 6, "dano_laser": 8, "dano_choque": 10,
        "disparo_cada": 2.0, "disparos_seguidos": 1,
        "velocidad": 200,
        "parada_x": (0.68, 0.88),
        "flotar_amplitud": 40, "flotar_periodo": 2.0,
        "cambio_altura_cada": 2.5,     # s entre cambios de altura
    },
    "lexbot20": {
        "vida": 12, "dano_laser": 12, "dano_choque": 15,
        "disparo_cada": 2.0, "disparos_seguidos": 2,
        "velocidad": 140,
        "parada_x": (0.50, 0.60),      # se acerca más a Superman
        "flotar_amplitud": 25, "flotar_periodo": 3.5,
        "cambio_altura_cada": 0,
    },
}
# Si un LexBot llega al borde izquierdo se queda flotando en esta X mínima.
LEXBOT_X_MINIMA = 10
# Separación entre los disparos seguidos del LexBot20.
DISPARO_SEGUIDO_PAUSA = 0.25
ENEMIGO_DESTELLO = 0.1          # s de destello blanco al recibir daño

LASER_ENEMIGO_VELOCIDAD = 420   # px/s
LASER_ENEMIGO_RADIO = 7

MISIL_VIDA = 1
MISIL_DANO_CHOQUE = 10
MISIL_VELOCIDAD = 330           # px/s
MISILES_POR_GRUPO = 3
MISIL_PAUSA_GRUPOS = 3.5        # s entre grupos de 3


# ------------------------------------------------------------------------------
# JEFE FINAL — DINOSAURIO ROBÓTICO
# Vida oculta, fases por porcentaje y ataques alternados con aviso.
# ------------------------------------------------------------------------------
JEFE_VIDA = 60                  # = 30 láseres (propuesta)
JEFE_FASE2 = 0.66               # % de vida donde empieza la fase 2
JEFE_FASE3 = 0.33               # % de vida donde empieza la fase 3
JEFE_DANO_ATAQUE = 20
JEFE_DANO_CHOQUE = 10
JEFE_X = 860                    # centro horizontal de descanso
JEFE_Y = 400                    # centro vertical de descanso
JEFE_VELOCIDAD_ENTRADA = 150    # px/s al entrar a escena
JEFE_HITBOX = 0.7               # fracción del sprite que recibe y hace daño
JEFE_EMBESTIDA = 260            # px que avanza hacia la izquierda al atacar
JEFE_MENSAJE = "¡Jefe final: dinosaurio robótico!"
JEFE_PIEL_CADA = 0.3            # s entre pedazos de piel que caen en fase 2
JEFE_DERROTA_DURACION = 2.5     # s de explosiones antes de quedar en chatarra
JEFE_MENSAJE_VICTORIA = "¡Nivel 1 completado!"
COLOR_AVISO = (230, 57, 70)     # franja que avisa dónde va a golpear
AVISO_ALFA = 90
# Por fase: [aviso (s), duración del ataque (s), pausa entre ataques (s)].
JEFE_TIEMPOS = {
    1: (1.0, 0.7, 2.0),
    2: (0.85, 0.6, 1.6),
    3: (0.7, 0.5, 1.2),
}
# Zonas de ataque (fracción del alto): mordida arriba, coletazo abajo.
JEFE_MORDIDA_ZONA = (0.0, 0.45)
JEFE_COLETAZO_ZONA = (0.55, 1.0)
SACUDIDA_DURACION = 0.5         # s al cambiar de fase
SACUDIDA_FUERZA = 10            # px


# ------------------------------------------------------------------------------
# MENSAJES
# Duración de textos de tutorial y de inicio de oleada.
# ------------------------------------------------------------------------------
MENSAJE_TUTORIAL_DURACION = 3.0
MENSAJE_OLEADA_DURACION = 2.0
MENSAJE_DESVANECER = 0.5        # s finales en que el mensaje se desvanece
PAUSA_ENTRE_OLEADAS = 1.0       # s antes de lanzar la siguiente oleada


# ------------------------------------------------------------------------------
# OLEADAS (GDD sección 8)
# Cada oleada: mensaje de inicio, mensajes de tutorial (opcional) y lista de
# apariciones (segundos desde el inicio de la oleada, tipo, altura 0–1).
# El tipo "misiles" lanza un grupo de MISILES_POR_GRUPO a distintas alturas.
# ------------------------------------------------------------------------------
OLEADAS = [
    {
        "mensaje": "¡Defiende Metrópolis!",
        "tutorial": ["Flechas = volar", "Espacio = láser", "X = golpe"],
        "aparecen": [(2.0, "lexbot1", 0.5)],
    },
    {
        "mensaje": "¡Llegan refuerzos!",
        "aparecen": [(0.5, "lexbot1", 0.2), (3.0, "lexbot1", 0.8), (5.5, "lexbot1", 0.5),
                     (8.0, "lexbot1", 0.35), (10.5, "lexbot1", 0.65)],
    },
    {
        "mensaje": "¡Cuidado: misiles!",
        # 12 misiles = 4 grupos de 3, separados por MISIL_PAUSA_GRUPOS
        "aparecen": [(0.5 + i * MISIL_PAUSA_GRUPOS, "misiles", 0) for i in range(4)],
    },
    {
        "mensaje": "¡LexBots de élite!",
        "aparecen": [(0.5, "lexbot10", 0.3), (5.0, "lexbot10", 0.7), (9.5, "lexbot10", 0.5)],
    },
    {
        "mensaje": "¡Peligro: LexBot pesado!",
        "aparecen": [(0.5, "lexbot20", 0.5), (5.0, "lexbot1", 0.2), (8.0, "lexbot1", 0.8)],
    },
]
# Mensaje de tutorial que aparece la primera vez que sale la Zona de sol.
SOL_MENSAJE = "Vuela al sol para recargar vida"


# ------------------------------------------------------------------------------
# AUDIO
# ------------------------------------------------------------------------------
VOLUMEN_MUSICA = 0.6


# ------------------------------------------------------------------------------
# COLORES — HÉROE (GUIA_ESTILO 2.1)
# ------------------------------------------------------------------------------
COLOR_HEROE_ROJO = (165, 14, 13)
COLOR_HEROE_ROJO_LUZ = (199, 30, 23)
COLOR_HEROE_ROJO_SOMBRA = (114, 7, 7)
COLOR_HEROE_AZUL = (49, 88, 146)
COLOR_HEROE_AZUL_LUZ = (94, 144, 191)
COLOR_HEROE_AZUL_SOMBRA = (2, 41, 103)
COLOR_HEROE_AMARILLO = (245, 197, 24)
COLOR_HEROE_PIEL = (239, 181, 118)


# ------------------------------------------------------------------------------
# COLORES — LEXBOTS Y MISIL (GUIA_ESTILO 2.2 y 2.3)
# ------------------------------------------------------------------------------
COLOR_LEX_VERDE = (56, 215, 23)
COLOR_LEX_VERDE_LIMA = (128, 204, 53)
COLOR_LEX_VERDE_SOMBRA = (46, 107, 27)
COLOR_LEX_MORADO = (90, 41, 93)
COLOR_LEX_MORADO_BRILLANTE = (125, 31, 115)
COLOR_LEX_MORADO_SOMBRA = (42, 18, 55)
COLOR_LEX_GRIS = (66, 74, 78)
COLOR_LEX_GRIS_CLARO = (122, 107, 113)
COLOR_LEX_OJOS = (211, 75, 84)

COLOR_MISIL_CUERPO = (4, 143, 22)
COLOR_MISIL_SOMBRA = (40, 81, 26)
COLOR_MISIL_BRILLO = (7, 235, 4)
COLOR_MISIL_LLAMA_1 = (255, 159, 28)
COLOR_MISIL_LLAMA_2 = (255, 210, 63)


# ------------------------------------------------------------------------------
# COLORES — METRÓPOLIS (GUIA_ESTILO 2.4)
# ------------------------------------------------------------------------------
COLOR_CIELO = (1, 119, 250)
COLOR_CIELO_CLARO = (35, 155, 250)
COLOR_BRUMA = (130, 183, 232)
COLOR_EDIFICIO_DORADO = (221, 174, 93)
COLOR_CREMA = (242, 230, 179)
COLOR_NUBE = (255, 255, 255)
COLOR_EDIFICIO_SOMBRA = (51, 55, 88)
COLOR_EDIFICIO_LEJANO = (75, 97, 150)


# ------------------------------------------------------------------------------
# COLORES — JEFE FINAL (GUIA_ESTILO 2.5)
# ------------------------------------------------------------------------------
COLOR_JEFE_PIEL = (93, 127, 25)
COLOR_JEFE_PIEL_CLARA = (150, 184, 45)
COLOR_JEFE_PIEL_SOMBRA = (46, 66, 19)
COLOR_JEFE_FRANJA = (115, 41, 68)
COLOR_JEFE_VIENTRE = (205, 189, 73)
COLOR_JEFE_METAL_OSCURO = (36, 40, 35)
COLOR_JEFE_METAL_MEDIO = (65, 55, 49)
COLOR_JEFE_BRONCE = (144, 119, 83)
COLOR_JEFE_NUCLEO = (57, 255, 20)


# ------------------------------------------------------------------------------
# COLORES — EFECTOS Y PROYECTILES (GUIA_ESTILO 3)
# ------------------------------------------------------------------------------
COLOR_NUCLEO = (255, 255, 255)
COLOR_LASER_HEROE = (255, 42, 42)
COLOR_LASER_VERDE = (57, 255, 20)
COLOR_LASER_ROJO = (194, 24, 91)        # rojo-magenta, en forma de bola
COLOR_CHISPA = (255, 210, 63)
COLORES_EXPLOSION = [(255, 255, 255), (255, 210, 63), (255, 159, 28), (90, 90, 90)]

COLOR_SOL = (255, 244, 194)
COLOR_SOL_RAYOS = (255, 230, 128)
SOL_RAYOS_ALFA = 100                    # ~40 % de opacidad
COLOR_SOL_DESTELLO = (255, 210, 63)


# ------------------------------------------------------------------------------
# INTERFAZ (HUD) — GUIA_ESTILO 4
# ------------------------------------------------------------------------------
BARRA_X = 20
BARRA_Y = 44
BARRA_ANCHO = 300
BARRA_ALTO = 20
BARRA_MARCO = 2
COLOR_BARRA_MARCO = (27, 24, 37)
COLOR_BARRA_FONDO = (60, 56, 70)
COLOR_VIDA_ALTA = (61, 220, 90)         # 100–51
COLOR_VIDA_MEDIA = (255, 201, 60)       # 50–26
COLOR_VIDA_BAJA = (230, 57, 70)         # 25–0 (parpadea)
COLOR_TEXTO = (255, 255, 255)
COLOR_CONTORNO = (0, 0, 0)
CONTORNO_TEXTO = 2
TAMANO_FUENTE_CHICA = 16
TAMANO_FUENTE_MEDIANA = 24
TAMANO_FUENTE_GRANDE = 40
