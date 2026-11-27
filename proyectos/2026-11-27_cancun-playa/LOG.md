# LOG del proyecto

| Fecha | Tipo | Detalle |
|---|---|---|
| 2026-11-27 | decisión | Idea inicial: hamaca en Cancún. El usuario la simplifica a "en la playa de Cancún". Montaje local (sin IA generativa). |
| 2026-11-27 | instalación | rembg 2.0.88 (+ onnxruntime 1.29.0), modelo `birefnet-portrait` — recorte de la persona. |
| 2026-11-27 | instalación | Red del entorno: permitidos commons/upload.wikimedia.org y hosts de descargas de GitHub (fondo + modelo). |
| 2026-11-27 | referencia | Fondo: "Beautiful beach Cancun - Strand (19937387009).jpg", Wikimedia Commons, licencia CC BY 2.0 (1280 px). Requiere atribución si se publica. |
| 2026-11-27 | versión | v01: recorte + fondo desenfocado (efecto retrato), corrección de luz noche→día, light wrap en bordes, grano. Script: `03_trabajo/componer.py`. |
