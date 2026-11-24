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
