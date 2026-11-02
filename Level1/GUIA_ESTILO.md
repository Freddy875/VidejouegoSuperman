# Guía de Estilo Visual — Superman: Nivel 1

> **Versión:** 1.0 · **Fecha:** 31/oct/2026 · **Autor:** Fernando Sánchez Mejía
> Complementa a `GDD_Nivel1.md`. Los colores se **extrajeron de las imágenes de la carpeta**, así que coinciden con el arte existente.
> Todos los colores deben vivir como constantes en `config.py` (ej. `COLOR_LASER_HEROE = (255, 42, 42)`).

---

## 1. Principios de estilo
1. **Pixel art 16 bits**: contornos oscuros, colores saturados y sombreado por bloques (sin degradados suaves).
2. **Cada bando tiene su paleta**: el héroe en rojo/azul/amarillo; los enemigos en verde/morado/gris. El jugador debe distinguir al instante quién es quién.
3. **El fondo nunca compite con los personajes**: Metrópolis va en tonos más claros y menos contrastados que los sprites.
4. **Los peligros brillan**: todo lo que hace daño a Superman (láseres, misiles) tiene núcleo blanco y halo de color intenso.

---

## 2. Paletas

### 2.1 Héroe — rojo, azul y amarillo
| Uso | Hex | RGB |
|---|---|---|
| Rojo capa / botas | `#A50E0D` | 165, 14, 13 |
| Rojo luz | `#C71E17` | 199, 30, 23 |
| Rojo sombra | `#720707` | 114, 7, 7 |
| Azul traje | `#315892` | 49, 88, 146 |
| Azul luz | `#5E90BF` | 94, 144, 191 |
| Azul sombra | `#022967` | 2, 41, 103 |
| Amarillo (cinturón / emblema) | `#F5C518` | 245, 197, 24 |
| Tono piel | `#EFB576` | 239, 181, 118 |

### 2.2 LexBots — gris, verde y morado (tecnología de Lex Luthor)
| Uso | Hex | RGB |
|---|---|---|
| Verde brillante | `#38D717` | 56, 215, 23 |
| Verde lima | `#80CC35` | 128, 204, 53 |
| Verde sombra | `#2E6B1B` | 46, 107, 27 |
| Morado | `#5A295D` | 90, 41, 93 |
| Morado brillante (LexBot20) | `#7D1F73` | 125, 31, 115 |
| Morado sombra | `#2A1237` | 42, 18, 55 |
| Gris metal | `#424A4E` | 66, 74, 78 |
| Gris claro | `#7A6B71` | 122, 107, 113 |
| Ojos rojos | `#D34B54` | 211, 75, 84 |

**Progresión visual por nivel de enemigo:**
| Enemigo | Dominante | Lectura para el jugador |
|---|---|---|
| LexBot1 | Verde con poco morado | Débil |
| LexBot10 | Verde lima + morado | Medio |
| LexBot20 | Morado oscuro + gris | Peligroso |

### 2.3 Misil
| Uso | Hex |
|---|---|
| Cuerpo verde | `#048F16` |
| Verde sombra | `#28511A` |
| Brillo verde | `#07EB04` |
| Llama propulsor | `#FF9F1C` → `#FFD23F` |

### 2.4 Metrópolis — azul, dorado, amarillo y blanco
| Uso | Hex | RGB |
|---|---|---|
| Cielo | `#0177FA` | 1, 119, 250 |
| Cielo claro | `#239BFA` | 35, 155, 250 |
| Celeste / bruma | `#82B7E8` | 130, 183, 232 |
| Edificios dorados | `#DDAE5D` | 221, 174, 93 |
| Crema / ventanas iluminadas | `#F2E6B3` | 242, 230, 179 |
| Nubes | `#FFFFFF` | 255, 255, 255 |
| Sombra de edificios | `#333758` | 51, 55, 88 |
| Edificios lejanos | `#4B6196` | 75, 97, 150 |

### 2.5 Jefe final — dinosaurio robótico
| Fase | Uso | Hex |
|---|---|---|
| Piel (1–2) | Verde piel | `#5D7F19` |
| | Verde claro | `#96B82D` |
| | Verde sombra | `#2E4213` |
| | Franjas moradas | `#732944` |
| | Vientre / amarillo | `#CDBD49` |
| Mecánico (2–3) | Metal oscuro | `#242823` |
| | Metal medio | `#413731` |
| | Bronce / cables | `#907753` |
| | Núcleo y dientes brillantes | `#39FF14` |

---

## 3. Efectos y proyectiles

| Elemento | Núcleo | Halo | Forma |
|---|---|---|---|
| **Láser de Superman** | `#FFFFFF` | `#FF2A2A` | Línea recta delgada y larga |
| **Láser enemigo verde (kriptonita)** | `#FFFFFF` | `#39FF14` | Bola / pulso corto |
| **Láser enemigo rojo (sol rojo)** | `#FFFFFF` | `#C2185B` (rojo-magenta) | Bola / pulso corto |
| **Impacto / chispa** | `#FFFFFF` | `#FFD23F` | Estrella de 4–8 puntas |
| **Explosión** | `#FFFFFF` → `#FFD23F` → `#FF9F1C` → `#5A5A5A` (humo) | | Cuadros de 4–8 px |
| **Piel cayendo (jefe)** | Paleta de piel 2.5 | | Fragmentos irregulares que caen |

> ⚠️ **Regla de claridad:** el láser rojo enemigo usa un tono **rojo-magenta** y forma de **bola**, para no confundirse con el láser de Superman (rojo puro y en línea).

### 3.1 Zona de sol ☀️
| Uso | Hex | Opacidad |
|---|---|---|
| Círculo del sol | `#FFF4C2` | 100 % |
| Rayos / área de recarga | `#FFE680` | 35–50 % |
| Destello al recargar (en Superman) | `#FFD23F` | Parpadeo suave |

---

## 4. Interfaz (HUD)

| Elemento | Especificación |
|---|---|
| Barra de vida | Arriba a la izquierda, ~300 × 20 px, marco `#1B1825` de 2 px |
| Color de la barra | 100–51: `#3DDC5A` (verde) · 50–26: `#FFC93C` (amarillo) · 25–0: `#E63946` (rojo, parpadea) |
| Etiqueta | "SUPERMAN" sobre la barra |
| Texto general | Blanco `#FFFFFF` con contorno negro `#000000` de 2 px |
| Mensajes de tutorial | Centro-abajo, aparecen 3 s y se desvanecen |
| Mensajes de oleada | Centro, grandes, 2 s ("¡Cuidado: misiles!") |
| Fuente | **Press Start 2P** (Google Fonts, licencia libre OFL), tamaños 16 / 24 / 40 px |

---

## 5. Reglas de pixel art para el código

1. **Escalado sin suavizar:** usar `pygame.transform.scale` (vecino más cercano), **nunca** `smoothscale`, para que los pixeles se vean nítidos.
2. **Tamaños en pantalla** (de `GDD_Nivel1.md`): Superman ~120 px · LexBot1 ~80 · LexBot10 ~110 · LexBot20 ~150 · Misil ~60 · Jefe ~450 px de alto.
3. **Orientación:** Superman mira a la **derecha**; enemigos y misiles a la **izquierda** (voltear la imagen con `pygame.transform.flip` si hace falta).
4. **Transparencia:** quitar el fondo negro o blanco de los JPEG y guardar como PNG con canal alfa en `assets/sprites/`. Limpiar el borde (1–2 px) para que no queden halos negros o blancos.
5. **Luz:** viene de **arriba** (el sol); las sombras caen hacia abajo.
6. **Partículas:** cuadros de 4 u 8 px, sin círculos suaves.
7. **Retroalimentación:**
   - Superman herido → parpadeo blanco 1 s (invulnerable).
   - Enemigo herido → destello blanco de 0.1 s.
   - Cambio de fase del jefe → sacudida de pantalla de 0.5 s.

---

## 6. Fondo (parallax)

| Capa | Velocidad | Contenido |
|---|---|---|
| 1 – Cielo | 0 (fija) | Degradado por bandas de `#0177FA` a `#82B7E8` |
| 2 – Nubes | Lenta (0.2×) | Nubes blancas pixeladas |
| 3 – Ciudad | Media (0.5×) | `Metropolis.jpeg` repetida en bucle horizontal |

---

## 7. Lista de verificación visual
- [ ] Se distingue a Superman de los enemigos solo por color.
- [ ] Los láseres enemigos no se confunden con el de Superman.
- [ ] El fondo es más claro y menos contrastado que los sprites.
- [ ] Ningún sprite tiene bordes borrosos ni halos de fondo.
- [ ] La barra de vida se lee bien sobre el cielo azul.
