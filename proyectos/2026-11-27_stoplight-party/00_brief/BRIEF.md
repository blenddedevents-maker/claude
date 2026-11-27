# BRIEF — Stoplight Party (Blendded @ Frenesí)

Estado: **borrador** (2026-11-27). Pendiente de datos secundarios y elección de propuesta.
PRD original completo en `01_referencias/texto/prd-original.md`.

## 1. Qué es
Flyer de la "Stoplight Party": la fiesta del semáforo (🟢 soltero/a · 🟡 es complicado · 🔴 pillado/a),
organizada por **Blendded** en **Frenesí**, el **23 de diciembre de 2026**.

## 2. Para qué y para quién
Evento de ~3.000 personas, público de 18 a 30 años. Uso principal: stories de Instagram (que la gente lo comparta), además de post e impresión.

## 3. Estilo y tono
- Cartelería de club o festival actual: energía, moderno, nada de plantilla de Canva.
- **Elemento central:** semáforo redibujado en SVG con **las 3 luces encendidas** y un glow de neón intenso proyectado sobre el fondo. Referencia de forma: `01_referencias/visual/semaforo-referencia.jpg` (no se usa tal cual).
- **Fondo:** degradado amarillo→naranja (#FFC21A → #FF8A00), con grano, textura o rayos.
- **Título:** verde neón (#00E05A). **Subtítulos:** rojo (#E8121C). **Contornos, sombras y texto pequeño:** #111.
- **Legibilidad obligatoria:** contorno oscuro, sombra dura de sticker/3D o glow. Tiene que leerse en el móvil de un vistazo.
- Referencia de género (solo concepto, no se copia): `flyer-club-prana-ref.jpg`.

## 4. Jerarquía
1. STOPLIGHT PARTY (enorme, verde, display gruesa)
2. Logo de Blendded arriba ("Blendded presenta"), el más visible de los dos logos
3. Fecha 23 DIC / 23.12 en rojo
4. Subtítulos en rojo: @ Frenesí, hora
5. Leyenda del semáforo, "Ven con tu color" (opcional)
6. Logo de Frenesí abajo, junto a la info del venue
7. Info secundaria: hora, dirección, precio/entradas, web/@instagram, line-up, +18

## 5. Entregables
| Archivo | Formato | Medidas | Notas |
|---|---|---|---|
| Propuestas A/B/C | PNG | 1080×1920 | Solo Story; el usuario elige una |
| Story/Reel | PNG | 1080×1920 | Zona segura: 250 px libres arriba y abajo |
| Post IG | PNG | 1080×1350 (4:5) | Composición adaptada, sin estirar |
| Impresión | PDF | A3 vertical, 300 ppp, +3 mm de sangrado (303×426 mm) | |

## 6. Material disponible (`02_assets/entrada/`)
| Archivo | Formato | Fondo | Colores | Observación |
|---|---|---|---|---|
| logo-blendded_original.webp | WebP 2000×667 | Transparente ✅ | Plata/blanco cromado (#FCFBFC) con destellos y glow violeta | Poco contraste sobre amarillo: necesita base o placa oscura |
| logo-frenesi_original.png | PNG 1434×432 | Transparente ✅ | Amarillo lima plano (#E5E400) | **Casi invisible sobre fondo amarillo**: necesita placa oscura. Resolución justa para A3 |

## 7. Herramientas previstas
HTML/CSS + SVG inline, Google Fonts y Playwright/Chromium para exportar PNG y PDF.

## 8. Restricciones
No deformar ni recolorear los logos y darles aire. No usar la foto del semáforo tal cual. Nada a `final/` sin aprobación.

## 9. Criterio de éxito
Que se lea de un vistazo en el móvil, que las 3 luces se vean claramente encendidas, que nada se salga de los márgenes y que tenga nivel de evento de 3.000 personas y den ganas de compartirlo.

## 10. Datos pendientes (placeholders si no llegan)
[HORA] · [DIRECCIÓN] · [PRECIO / ENTRADAS] · [WEB / @INSTAGRAM] · [LINE-UP] · confirmar "+18"
