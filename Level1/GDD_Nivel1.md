# Documento de Diseño del Juego — Superman: Nivel 1 (Tutorial)

> **Versión:** 1.0 · **Fecha:** 31/oct/2026 · **Autor:** Fernando Sánchez Mejía
> **Estado:** Aprobado para desarrollo del Nivel 1
> Los valores marcados con **(propuesta)** son iniciales y se ajustan al probar el juego. Todos deben vivir en `config.py`.

---

## 1. Resumen

| Concepto | Definición |
|---|---|
| Género | Shooter de desplazamiento horizontal (*side-scroller*), inspirado en **Metal Slug** |
| Estética | Pixel art estilo 16 bits, colores saturados |
| Protagonista | Superman, siempre volando |
| Escenario | Cielo de Metrópolis (Daily Planet al fondo) |
| Propósito del nivel | **Tutorial**: enseñar las 3 habilidades básicas → **vuelo, fuerza (golpe) y rayo láser** |
| Duración objetivo | **~2 min 30 s** (lo que dura la canción) |
| Objetivo | Vencer todas las oleadas y al jefe final (dinosaurio robótico) |
| Puntuación | **No hay** en el Nivel 1 |

---

## 2. Tecnología

| Elemento | Decisión |
|---|---|
| Lenguaje / motor | **Python 3 + Pygame** |
| Plataforma | PC (Windows) |
| Entrada | **Teclado** (Nivel 1). Arquitectura preparada para añadir **control** después |
| Resolución | **1280 × 720 (16:9)**, horizontal |
| FPS | 60 |
| Futuro | Control (Xbox/PlayStation). Celular implicaría cambiar de tecnología (Pygame es limitado en móvil) |

---

## 3. Controles

| Acción | Tecla |
|---|---|
| Mover (arriba / abajo / adelante / atrás) | Flechas ↑ ↓ ← → |
| Rayo láser | **Espacio** (un disparo por pulsación) |
| Golpe | **X** |
| Pausa | **P** o **Esc** |
| Iniciar / confirmar | **Enter** |

> Mapeo futuro para control: A = láser, B = golpe, Start = pausa.
> La lectura de teclas debe pasar por una capa de "acciones" (`mover`, `laser`, `golpe`, `pausa`) para poder agregar el control sin reescribir el juego.

---

## 4. Cámara y movimiento

- El juego avanza **de izquierda a derecha**: Superman mira a la derecha y el fondo de Metrópolis se desplaza hacia la izquierda (*parallax*).
- Los enemigos **entran por la derecha** y avanzan hacia la izquierda.
- Superman se mueve **libremente por toda la pantalla** (propuesta), sin salir de sus bordes.
- Superman **siempre está volando**; no hay suelo ni gravedad.

---

## 5. Protagonista: Superman

### 5.1 Vida
- **Barra de vida de 0 a 100**, visible en la esquina superior izquierda.
- Si llega a 0 → **Game Over**.
- Tras recibir daño: **1 segundo de invulnerabilidad** (parpadea) (propuesta).

### 5.2 Habilidades del Nivel 1

| Habilidad | Tecla | Daño | Alcance | Detalles |
|---|---|---|---|---|
| **Rayo láser** (ojos) | Espacio | **2** | Toda la pantalla | Un disparo por pulsación, como bala. Pausa mínima entre disparos 0.25 s (propuesta). Color rojo |
| **Golpe** (fuerza) | X | **1** | Corto (~80 px frente a Superman) (propuesta) | Destruye **misiles al instante** y empuja ligeramente al enemigo hacia atrás. Pausa 0.4 s (propuesta) |
| **Vuelo / esquivar** | Flechas | — | — | Se esquiva solo moviéndose (sin dash) |

> El láser es **más potente** que el golpe; el golpe es útil a corta distancia y contra misiles.

### 5.3 Recarga solar ☀️
Superman funciona como una **batería solar**.
- Después de **cada oleada** aparece una **Zona de sol** en la parte superior de la pantalla.
- Si Superman se queda dentro, **recupera vida poco a poco**: +10 por segundo (propuesta).
- La zona dura **~6 segundos** (propuesta) y es **fácil de alcanzar** (es un tutorial).
- Durante la pelea con el **jefe final**, la zona de sol está **siempre activa** en la parte superior.
- Es el **único potenciador** del Nivel 1.

---

## 6. Enemigos

### 6.1 Reglas generales
- Los **LexBots deben ser vencidos**: la oleada no termina hasta derrotarlos a todos.
- Si un LexBot llega al lado izquierdo **no pasa nada**: no sale de la pantalla y **se queda flotando** hasta que Superman lo vence.
- Los **misiles sí se pueden esquivar**: si salen por la izquierda, desaparecen y cuentan como superados.
- Los LexBots **disparan láser** de color **verde (kriptonita)** o **rojo (sol rojo)**, las debilidades de Superman.
- Chocar con un enemigo también daña a Superman.

### 6.2 Tabla de enemigos

| Enemigo | Archivo | Vida | Láseres para vencerlo | Golpes | Daño láser | Daño por choque | Disparo (propuesta) |
|---|---|---|---|---|---|---|---|
| **Misil** | `Misil.jpeg` | 1 | 1 | 1 | — | 10 | No dispara; viaja en línea recta |
| **LexBot1** | `LexBot1.jpeg` | 2 | **1** | 2 | 5 | 5 | 1 láser cada 3 s |
| **LexBot10** | `LexBot10.jpeg` | 6 | **3** | 6 | 8 | 10 | 1 láser cada 2 s |
| **LexBot20** | `LexBot20.jpeg` | 12 | **6** | 12 | 12 | 15 | 2 láseres seguidos cada 2 s |

### 6.3 Comportamiento (propuesta)
- **LexBot1:** entra por la derecha, se detiene en el tercio derecho y flota subiendo y bajando suavemente. El más lento.
- **LexBot10:** igual, pero más rápido y cambia de altura con más frecuencia.
- **LexBot20:** más grande; se acerca más a Superman antes de detenerse.
- **Misiles:** entran por la derecha en **grupos de 3**, a distintas alturas, en línea recta.

---

## 7. Jefe final: Dinosaurio robótico

| Concepto | Definición |
|---|---|
| Apariencia | Al inicio parece un **dinosaurio de carne y hueso**. Conforme recibe daño, **se le cae la piel sintética** y revela su **estructura mecánica** |
| Vida | **Oculta** (el jugador no la ve). 60 puntos = 30 láseres (propuesta) |
| Punto débil | **Ninguno**; cualquier impacto le hace daño |
| Zona de sol | Activa durante toda la pelea |
| Otros enemigos | **Ninguno** durante esta pelea (ni misiles ni LexBots) |

### 7.1 Fases

| Fase | Vida restante | Imagen | Aspecto |
|---|---|---|---|
| 1 | 100 % – 66 % | `Final Boss1.jpeg` | Piel completa |
| 2 | 66 % – 33 % | ⚠️ **Pendiente** (imagen intermedia) | Piel rota, se ven partes metálicas |
| 3 | 33 % – 0 % | `Final Boss2.jpeg` | Robot expuesto |

> Mientras no exista la imagen de la fase 2, se usa `Final Boss1.jpeg` con partículas de piel cayendo.
> Al cambiar de fase: sacudida de pantalla y lluvia de pedazos de piel.

### 7.2 Ataques (se alternan)

| Ataque | Zona que golpea | Cómo se esquiva | Daño |
|---|---|---|---|
| **Mordida** | Parte **alta** de la pantalla | Superman **baja** | 20 |
| **Coletazo** | Parte **baja** de la pantalla | Superman **sube** | 20 |

- Cada ataque tiene un **aviso de ~1 segundo** antes de lanzarse (rugido o destello) (propuesta).
- En cada fase los ataques son un poco **más rápidos** (propuesta).
- Ojo: la mordida golpea arriba, donde está el sol → el jugador debe decidir cuándo recargar.

### 7.3 Victoria
Al llegar a 0 de vida, el dinosaurio **queda hecho chatarra** (explosión y piezas cayendo) → pantalla de **Victoria**.

---

## 8. Estructura del nivel (oleadas)

| # | Oleada | Enemigos | Tiempo aprox. (propuesta) |
|---|---|---|---|
| 1 | **Tutorial** | 1 LexBot1 + mensajes: "Flechas = volar", "Espacio = láser", "X = golpe" | 0:00 – 0:15 |
| ☀️ | Zona de sol | Recarga | |
| 2 | **Grupo** | 5 LexBot1 | 0:20 – 0:40 |
| ☀️ | Zona de sol | Recarga | |
| 3 | **Lluvia de misiles** | 12 misiles en grupos de 3 | 0:45 – 1:05 |
| ☀️ | Zona de sol | Recarga | |
| 4 | **Élite** | 3 LexBot10 | 1:10 – 1:30 |
| ☀️ | Zona de sol | Recarga | |
| 5 | **Pesado** | 1 LexBot20 + 2 LexBot1 | 1:35 – 1:55 |
| ☀️ | Zona de sol | Recarga antes del jefe | |
| 6 | **Jefe final** | Dinosaurio robótico (con sol permanente) | 2:00 – 2:30 |

- La siguiente oleada empieza solo cuando la anterior está vencida (o, en misiles, cuando todos fueron destruidos o salieron).
- Mensaje breve al iniciar cada oleada (ej. "¡Cuidado: misiles!").

---

## 9. Pantallas

| Pantalla | Contenido |
|---|---|
| **Título / inicio** | Nombre del juego, Metrópolis de fondo, "Presiona Enter" |
| **Juego** | Barra de vida (arriba izq.), mensajes de tutorial y de oleada |
| **Pausa** | Juego congelado, "Pausa – P para continuar" |
| **Game Over** | "Game Over", Enter = reintentar el nivel |
| **Victoria** | Dinosaurio hecho chatarra, "¡Nivel 1 completado! – Próximamente Nivel 2" |

---

## 10. Audio

| Elemento | Archivo | Uso |
|---|---|---|
| Música | `musica_nivel1.ogg` (OGG Vorbis, 2:34) | Todo el nivel, incluido el jefe. **Se repite en bucle** si el nivel se alarga |
| Original | `Soaring above the metropolis.ogg` | Respaldo; no usar en código (internamente es MP4) |
| Efectos de sonido | Pendiente | Opcional: láser, golpe, explosión, rugido |

---

## 11. Recursos gráficos (carpeta `Level1`)

| Archivo | Uso en el juego | Fondo de la imagen |
|---|---|---|
| `Superman.jpeg` | Sprite del protagonista | Revisar |
| `Metropolis.jpeg` | Fondo con desplazamiento | Escena completa |
| `LexBot1.jpeg` | Enemigo débil | Negro |
| `LexBot10.jpeg` | Enemigo medio | Negro |
| `LexBot20.jpeg` | Enemigo fuerte | Blanco |
| `Misil.jpeg` | Proyectil enemigo | Negro |
| `Final Boss1.jpeg` | Jefe – fase 1 | Revisar |
| `Final Boss2.jpeg` | Jefe – fase 3 | Blanco |
| `Scene1.jpeg` | Referencia: Superman vs LexBot10 | — |
| `Scene2.jpeg` | Referencia: Superman esquiva misiles | — |
| `Scene3.jpeg` | Referencia: Superman vs LexBot20 | — |
| `FinalScene.jpeg` | Referencia: pelea contra el dinosaurio | — |

**Notas técnicas:**
- Las imágenes son JPEG grandes (≈1300–1600 px) con **fondo negro o blanco**. Hay que **quitar el fondo** (volverlo transparente) y **reducir** su tamaño para usarlas como sprites. Conviene guardar las versiones procesadas como PNG en `assets/sprites/` sin modificar los originales.
- Tamaños en pantalla (propuesta): Superman ~120 px de ancho · LexBot1 ~80 px · LexBot10 ~110 px · LexBot20 ~150 px · Misil ~60 px · Jefe ~450 px de alto.
- Las imágenes `Scene*` son **solo referencia visual** de cómo debe verse cada momento.

### 11.1 Colores de referencia
| Elemento | Colores |
|---|---|
| Superman | Rojo, azul y amarillo |
| LexBots | Gris, verde y morado |
| Metrópolis | Azul, dorado, amarillo y blanco |
| Láser de Superman | Rojo |
| Láser de LexBots | Verde (kriptonita) o rojo (sol rojo) |

> La **guía de estilo visual** detallada (paletas en hexadecimal y reglas de pixel art) se entregará como documento aparte.

---

## 12. Reglas resumidas
1. Superman siempre vuela; el nivel avanza de izquierda a derecha.
2. Espacio = láser (2 de daño), X = golpe cuerpo a cuerpo (1 de daño, destruye misiles).
3. Los LexBots deben ser vencidos; si llegan a la izquierda, se quedan flotando.
4. Los misiles se pueden esquivar, destruir con láser o golpear.
5. La vida (0–100) baja con láseres, misiles y choques; se recupera en las zonas de sol.
6. Vida en 0 = Game Over. Vencer al dinosaurio = Victoria.
7. No hay puntuación ni otros potenciadores en el Nivel 1.

---

## 13. Ideas para niveles futuros
- **Dash:** impulso rápido con breve invulnerabilidad.
- **Aliento de hielo** (súper soplido).
- **Láser continuo** al mantener presionada la tecla.
- **Nubes que bloquean el sol** (zonas temporales y permanentes) y **súper aliento para dispersarlas**.
- **Dinosaurio que escupe fuego.**
- Nuevos enemigos más difíciles y nuevos diseños de personajes.
- Otros potenciadores (sin escudo: no es una habilidad de Superman; él es resistente/invulnerable).
- Soporte para **control** y, más adelante, versión para **celular**.
- Puntuación y récords.
