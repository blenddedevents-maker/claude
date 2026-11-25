# LOG del proyecto

| Fecha | Tipo | Detalle |
|---|---|---|
| 2026-11-25 | instalación | librosa 1.0.1, scipy 1.18.1, soundfile 0.14.0, pyloudnorm 0.2.0, matplotlib (pip). FFmpeg 6.1.1 del sistema (trae el filtro rubberband) |
| 2026-11-25 | análisis | **A**: melodía monofónica silbada, Fa mayor (Fa-Sol-La-Mi), afinada −23 cents, sin batería; 4 frases en rubato (≈76 / 99 / 77 / 88 BPM) |
| 2026-11-25 | análisis | **B**: 100,00 BPM exactos (ajuste de rejilla en 190 s), primer beat en 2,276 s, tónica Mi (sonoridad frigia: Mi-Fa-Sol-La-Do); la escala de A (Fa, Sol, La, Mi) encaja en la de B |
| 2026-11-25 | decisión | A suena sola y natural (frases 1-3, intro a capela). Solo la frase 4 se ajusta de ~88 a 100 BPM (factor 0,8824) para que La-Sol-Fa-Mi caigan en las 4 negras del compás 1 de B y el Fa final caiga en el compás 2 (drop) |
| 2026-11-25 | decisión | A: highpass 250 Hz, reducción de ruido, compresión suave, afinación +23 cents (rubberband con formantes preservados), reverb de sala de 1,4 s, sonoridad igualada a B −1,5 LU |
| 2026-11-25 | decisión | Transición: B entra a 15,71 s (pad de intro) con filtro paso alto de 900 Hz que se va abriendo y volumen subiendo; bass swap en el Fa final (20,38 s); echo-out ping-pong de 3/4 de beat en la última nota de A |
| 2026-11-25 | decisión | Máster: limitador a −1 dBTP, ≈ −10,5 LUFS integrado. Los WAV no se suben al repo por tamaño (se regeneran con `03_trabajo/mezcla.py`) |
| 2026-11-25 | versión | v01 → `04_salidas/borradores/mezcla-dj_25-11-2026_a_las-munequitas_v01.mp3` |
