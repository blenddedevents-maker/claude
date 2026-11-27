# LOG del proyecto — Stoplight Party

| Fecha | Tipo | Detalle |
|---|---|---|
| 2026-11-27 | decisión | Proyecto creado a partir de la plantilla. Se guarda el PRD del usuario como base del BRIEF (borrador). |
| 2026-11-27 | assets | Logos en `02_assets/entrada/` (ambos con fondo transparente). Semáforo y flyer Club Prana en `01_referencias/visual/`. |
| 2026-11-27 | decisión | Problema detectado: el logo de Frenesí es amarillo (#E5E400) y el de Blendded es plateado. Los dos se pierden sobre fondo amarillo-naranja → se propone ponerlos sobre una placa o banda oscura sin tocar su color. |
| 2026-11-27 | instalación | npm: @fontsource/anton, barlow-condensed, archivo-black (fuentes copiadas en `03_trabajo/fonts/`). Playwright + Chromium ya instalados (exportación PNG). |
| 2026-11-27 | decisión | Logos sobre placa o banda #111 (sin tocar sus colores). Tipos: Anton (título y rojos) y Barlow Condensed (info). Semáforo en SVG generado en `flyer.html`. |
| 2026-11-27 | versión | v01 Story ×3: A tótem, B lateral a sangre, C horizontal tipo "selector" (cambio respecto al plan: "STOPLIGHT PARTY" solo tiene una O). Datos secundarios como `[ ]`. Render: `node render.js flyer.html salida_%.png a,b,c`. |
