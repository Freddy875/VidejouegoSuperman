# Prompt para Claude Code — Nivel 1

Copia todo lo que está debajo de la línea y pégalo en Claude Code, abierto en la carpeta `Level1`.

---

Vamos a programar el **Nivel 1 (tutorial)** de mi videojuego en **Python 3 + Pygame**.

**Fuente de verdad:** lee completos `GDD_Nivel1.md` (reglas) y `GUIA_ESTILO.md` (colores y estilo visual) en esta carpeta antes de escribir código. Todas las reglas, valores, oleadas, controles y archivos están ahí. Si algo no está definido, elige la opción más simple, déjala como constante en `config.py` y avísame.

## Recursos
- Usa **únicamente las imágenes de esta carpeta** como sprites y fondo (tabla de la sección 11 del GDD). No dibujes los personajes con código.
- **No modifiques los archivos originales.** Crea versiones procesadas (fondo negro/blanco convertido en transparente y tamaño reducido) en `assets/sprites/` como PNG, con un script `preparar_assets.py` que yo pueda volver a ejecutar.
- Si falta una imagen (por ejemplo, la fase 2 del jefe), usa la indicada en el GDD como sustituto o un rectángulo de color con una etiqueta de texto, y anótalo en el README.
- Música: `musica_nivel1.ogg` en bucle durante todo el nivel.
- Las imágenes `Scene1`, `Scene2`, `Scene3` y `FinalScene` son **solo referencia visual**.

## Estructura sugerida
```
Level1/
├── main.py              # punto de entrada
├── config.py            # TODOS los valores ajustables (vida, daño, velocidades, tiempos)
├── preparar_assets.py   # quita fondos y redimensiona imágenes
├── entrada.py           # capa de acciones (mover, laser, golpe, pausa) — lista para agregar control
├── jugador.py
├── enemigos.py          # LexBot1, LexBot10, LexBot20, Misil
├── jefe.py              # dinosaurio robótico (3 fases, mordida/coletazo)
├── oleadas.py           # secuencia de oleadas y zonas de sol
├── pantallas.py         # título, pausa, game over, victoria
├── assets/sprites/
└── README.md            # cómo instalar y ejecutar
```

## Requisitos clave (resumen del GDD)
- 1280×720, 60 FPS, desplazamiento horizontal de Metrópolis (parallax).
- Flechas = mover libre · Espacio = láser (2 de daño, un disparo por pulsación) · X = golpe cercano (1 de daño, destruye misiles) · P/Esc = pausa · Enter = iniciar.
- Vida 0–100 con barra visible; recarga en zonas de sol después de cada oleada y permanente durante el jefe.
- Los LexBots deben vencerse; si llegan a la izquierda se quedan flotando. Los misiles se pueden esquivar.
- Láseres enemigos verdes o rojos.
- Jefe: vida oculta, 3 fases por % de vida, alterna mordida (arriba) y coletazo (abajo) con aviso previo.
- Sin puntuación. Duración objetivo ~2:30.

## Forma de trabajo
1. Primero muéstrame un **plan** breve (archivos y orden de desarrollo).
2. Desarrolla por etapas y que cada una se pueda ejecutar:
   a) ventana + fondo + Superman moviéndose
   b) láser y golpe
   c) LexBot1 y oleada tutorial
   d) resto de oleadas y zonas de sol
   e) jefe final
   f) pantallas y música
3. Al terminar cada etapa, dime cómo probarla (`python main.py`).
4. Código **documentado en español** con mi estilo: encabezado de archivo con bloque de `=` (título y objetivo); cada sección en un bloque con línea de `-` arriba, título, descripción y línea de `-` abajo; comentarios explicativos dentro de ciclos y bloques.
5. Incluye `requirements.txt` (pygame) y un README con instrucciones para Windows.
