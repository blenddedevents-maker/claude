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
| 2026-11-26 | decisión | Feedback: color demasiado exagerado → versión suave: original + 40 % de la corrección (blend normal, opacidad 0,4) en los dos clips del usuario |
| 2026-11-26 | decisión | El clip 1 ahora sale del original sin etalonar (tramo 3,40–6,10 s, localizado por correlación de audio y comprobado visualmente), en vez del archivo ya etalonado |
| 2026-11-26 | versión | v03: `reel-subtitulos-transicion_v03.mp4` (12,77 s). Filtros en `03_trabajo/filtro-suave-*_v03.txt` |
| 2026-11-26 | decisión | v04: cuarto clip (grabación de pantalla del iPhone, HEVC 120 fps VFR → 30 fps). Recorte de las franjas negras (crop 1180×2096 en y=230) |
| 2026-11-26 | decisión | Transición clip 3 → 4: corte seco pregunta-respuesta («…reguetón antiguo?» → «Vamos a hacerlo»); el clip 3 se acorta a 4,8 s para dejar menos pausa. Golpe de zoom (+10 % → 100 % en 0,35 s) sincronizado con la entrada del beat (1,23 s del clip 4) |
| 2026-11-26 | decisión | Color del clip 4: igualación previa (más exposición y gamma, más calidez, menos morado) + la misma corrección suave al 40 % |
| 2026-11-26 | decisión | Subtítulos del clip 4: «Vamos a hacerlo» (luego solo hay música, sin voz). Final de 10 s con fundido a negro y de audio |
| 2026-11-26 | versión | v04: `reel-subtitulos-transicion_v04.mp4` (22,5 s). Subtítulos en `03_trabajo/subtitulos_v04.ass` |
| 2026-11-26 | decisión | Feedback: cortar el clip 3 antes de que el usuario vaya hacia la cámara. Nuevo final a 7,12 s del original (justo al acabar «antiguo», cuya voz termina a ~7,20 s), con fundido de audio de 0,06 s. El clip 3 pasa de 4,8 s a 4,27 s |
| 2026-11-26 | versión | v05: `reel-subtitulos-transicion_v05.mp4` (22,0 s). Subtítulos desplazados en `03_trabajo/subtitulos_v05.ass` |
