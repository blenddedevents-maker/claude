# LOG del proyecto

| Fecha | Tipo | Detalle |
|---|---|---|
| 2026-11-26 | instalación | faster-whisper 1.2.1 (pip) para transcribir el audio |
| 2026-11-26 | instalación | Modelo Whisper small (CTranslate2 int8) del paquete npm `@skillninja/shortmovie-telop-model-p0..p3` (Hugging Face está bloqueado en el entorno). SHA-256 verificado; se guarda solo en el scratchpad (no en el repo, ~250 MB) |
| 2026-11-26 | decisión | Transcripción: «Estoy seguro de que esta canción te la sabes» (0,00–2,48 s), con tiempos por palabra |
| 2026-11-26 | decisión | Subtítulos estilo reel: Inter Black en mayúsculas, contorno negro, grupos de 1–3 palabras, palabra activa en amarillo y entrada con rebote |
| 2026-11-26 | decisión | Corte al concierto a los 2,70 s (fotograma en el que la mano tapa del todo la cámara). El concierto entra con un leve zoom de impacto (+14 % → 100 % en 0,45 s) y escalado de 576×1024 a 1080×1920 |
| 2026-11-26 | versión | v01: `reel-subtitulos-transicion_v01.mp4` (7,7 s, H.264 CRF 17, AAC 192k). Subtítulos en `03_trabajo/subtitulos_v01.ass` |
| 2026-11-26 | decisión | v02: se añade un tercer clip (estudio) tras el concierto. Entra a los 2,85 s del original, con la mano aún tapando la cámara (transición inversa), y dura 5,05 s |
| 2026-11-26 | decisión | Etalonaje del estudio: el mismo filtro del primer vídeo más una igualación previa (temperatura más cálida, menos verde en medios, -3,5 % de brillo, +7 % de contraste, +8 % de saturación) para casar con el primer clip. En `03_trabajo/filtro-etalonaje-estudio_v02.txt` |
| 2026-11-26 | decisión | Subtítulos del clip 3: «Pero ¿qué pasaría si lo hiciésemos en reguetón antiguo?» (grafía RAE: reguetón) |
| 2026-11-26 | versión | v02: `reel-subtitulos-transicion_v02.mp4` (12,77 s). Subtítulos en `03_trabajo/subtitulos_v02.ass` |
