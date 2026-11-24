# LOG del proyecto

| Fecha | Tipo | Detalle |
|---|---|---|
| 2026-11-24 | decisión | Formato IG 4:5, estilo neón nocturno, leyenda de colores (respuestas del usuario) |
| 2026-11-24 | instalación | Fuentes @fontsource/anton 5.3.0 y @fontsource/bebas-neue 5.3.0 (woff2, OFL) → 02_assets/generados/fuentes. |
| 2026-11-24 | instalación | Playwright + Chromium (preinstalados en el entorno) para renderizar HTML → PNG |
| 2026-11-24 | versión | v01: 04_salidas/borradores/portada-semaforo-frenesi_ig-4x5_v01.png (2160x2700) y _1080_v01.jpg. Fuente editable: 03_trabajo/portada.html |
| 2026-11-24 | decisión | Cambio de dirección (v02): estilo foto con flash como la referencia del teléfono (01_referencias/visual/ref-telefono-malalts.webp), semáforo en 3D, logos de Blendded (organizador) y Frenesí, título blanco "FIESTA DEL SEMÁFORO", sin frase sobre el objeto |
| 2026-11-24 | instalación | bpy 5.3.0 (Blender como módulo de Python, render Cycles) para el semáforo 3D; scipy para analizar los logos; fuente @fontsource/unbounded (800/900) |
| 2026-11-24 | versión | v02: 04_salidas/borradores/fiesta-semaforo-blendded_ig-4x5_v02.jpg/.png (2160x2700). Fuentes: 03_trabajo/semaforo_3d.py → postpro.py → portada_v02.html. Render base a 1080x1350 (el de 1620x2025 superaba el tiempo límite) |
| 2026-11-24 | decisión | v03: semáforo más realista (módulos, tornillos, bisagras, abrazaderas, matriz LED, polvo y chorretones, foto con flash nocturno y desenfoque) y título POR DETRÁS del semáforo (render + máscara en capas). Título partido "SEMÁ | FORO" alrededor del poste para que se lea entero |
| 2026-11-24 | versión | v03: 04_salidas/borradores/fiesta-semaforo-blendded_ig-4x5_v03.jpg/.png (2160x2700). Render 1620x2025 nativo. Fuentes: 03_trabajo/semaforo_3d_v03.py → postpro_v03.py → portada_v03.html |
| 2026-11-24 | decisión | v04 "realista como la referencia": semáforo anclado a una persiana metálica, foto de cerca con gran angular y flash directo (sombra dura), título pintado en la persiana con chorreones (textura sobre la chapa), revelado tipo foto (claridad, sombras azuladas, aberración cromática, grano) |
| 2026-11-24 | instalación | fonttools + brotli (conversión de fuentes woff2 → ttf para PIL/Blender) |
| 2026-11-24 | versión | v04: 04_salidas/borradores/fiesta-semaforo-blendded_ig-4x5_v04.png/.jpg (2160x2700). Fuentes: rotulo_textura.py → semaforo_3d_v04.py → postpro_v04.py → portada_v04.html |
