# Superman — Nivel 1 (Tutorial)

Shooter de desplazamiento horizontal en Python 3 + Pygame. Las reglas están en `GDD_Nivel1.md` y el estilo visual en `GUIA_ESTILO.md`.

## Instalación (Windows)

1. Instala Python 3.10 o más reciente desde <https://www.python.org/downloads/>. Durante la instalación, marca **"Add Python to PATH"**.
2. Abre PowerShell en esta carpeta (`Level1`) y ejecuta:

```powershell
python -m pip install -r requirements.txt
```

3. (Opcional) Descarga la fuente **Press Start 2P** desde Google Fonts y copia `PressStart2P-Regular.ttf` en `assets/fonts/`. Si no está, el juego usa la fuente por defecto de Pygame.

## Ejecutar

```powershell
python main.py
```

La primera vez, el juego genera solo los sprites en `assets/sprites/`. Para regenerarlos (por ejemplo, después de cambiar tamaños en `config.py`):

```powershell
python preparar_assets.py
```

## Controles

| Acción | Tecla |
|---|---|
| Volar | Flechas |
| Láser | Espacio (un disparo por pulsación) |
| Golpe | X |
| Pausa / continuar | P o Esc |
| Iniciar / reintentar | Enter |

## Estructura del nivel

Título → 5 oleadas (Tutorial, Grupo, Lluvia de misiles, Élite, Pesado), con una **Zona de sol** de 6 s después de cada una → **Jefe final**, con el sol siempre activo → **Victoria**. Si la vida llega a 0: **Game Over** (Enter reintenta el nivel). La música `musica_nivel1.ogg` suena en bucle durante todo el nivel.

## Archivos

| Archivo | Contenido |
|---|---|
| `main.py` | Punto de entrada, estados del juego (título, jugando, pausa, Game Over, victoria), choques y música |
| `config.py` | **Todos** los valores ajustables: vida, daño, velocidades, tiempos, oleadas y colores |
| `preparar_assets.py` | Quita fondos, recorta y reduce las imágenes a `assets/sprites/` |
| `recursos.py` | Carga de sprites (con sustituto si falta uno), fuentes y texto con contorno |
| `entrada.py` | Capa de acciones (`mover`, `laser`, `golpe`, `pausa`, `confirmar`), lista para agregar un control |
| `fondo.py` | Metrópolis con parallax |
| `jugador.py` | Superman: vuelo, vida, láser y golpe |
| `enemigos.py` | LexBot1, LexBot10, LexBot20, sus láseres y el misil |
| `oleadas.py` | Secuencia de oleadas y Zona de sol |
| `jefe.py` | Dinosaurio robótico: 3 fases, mordida y coletazo con aviso, derrota |
| `efectos.py` | Chispas, explosiones y fragmentos (cuadros de 4–8 px) |
| `pantallas.py` | Barra de vida, mensajes y pantallas |

## Probar el jefe directamente

En `config.py`, cambia `EMPEZAR_EN_JEFE = False` a `True`. Recuerda volver a ponerlo en `False` para jugar el nivel completo.

## Sustitutos y decisiones propias

- **Jefe, fase 2:** falta la imagen intermedia. Se usa `Final Boss1.jpeg` con pedazos de piel cayendo continuamente (lo indicado en el GDD). Al agregar la imagen, súmala a `SPRITES` en `config.py` (por ejemplo `"jefe_fase2"`) y úsala en `jefe.py` (`self.imagenes`).
- **Fuente:** Press Start 2P no viene incluida; ver el paso 3 de la instalación.
- **Fondo:** `Metropolis.jpeg` ya trae cielo y nubes, así que se usa como capa de ciudad (0.5×) y se repite alternando con su reflejo para que no se note la unión. En la copia reflejada se vuelve a pegar el letrero del Daily Planet sin reflejar (`FONDO_LETRERO`). El sol del dibujo se tapa (`FONDO_TAPAR_SOL`) porque al reflejarlo salían dos soles. La capa de cielo por bandas solo se ve si falta la imagen.
- **LexBot1:** su imagen trae un rayo dibujado; se borra en el procesado (opción `borrar` en `config.SPRITES`) porque el láser del juego es aparte. La imagen se voltea para que mire a la izquierda.
- **LexBot10:** se borra el destello del cañón.
- **Misil:** se voltea para que apunte a la izquierda.
- **Fondos negros:** los LexBots y el misil usan tolerancia baja y "cierre" (rellenar sombras oscuras) para no perder sus partes oscuras.
- **Aviso del jefe:** franja roja parpadeante sobre la zona que va a golpear, con el texto "¡MORDIDA! ¡BAJA!" o "¡COLETAZO! ¡SUBE!".
- **Si falta un sprite**, el juego dibuja un rectángulo de color con su nombre.
- **Sin sonido:** si no hay dispositivo de audio, el juego funciona sin música.
