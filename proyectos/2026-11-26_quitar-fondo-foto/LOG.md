# LOG del proyecto

| Fecha | Tipo | Detalle |
|---|---|---|
| | decisión / instalación / versión | |

## 2026-11-26 — Quitar fondo a foto
- Entrada: `02_assets/entrada/img_5602.jpeg` (1620x1080).
- Instalado: `rembg[cpu]` 2.0.88 (Python) + modelo `birefnet-portrait` (recorte de personas con borde fino).
- Salida: `04_salidas/borradores/foto-sin-fondo_v01.png` (PNG con transparencia, misma resolución).
- Aprobado por el usuario: v01 copiado a `04_salidas/final/foto-sin-fondo.png`.
- Segunda foto: `02_assets/entrada/img_5554.jpeg` → `04_salidas/borradores/foto2-sin-fondo_v01.png` (mismo proceso).
- Tercera foto: `img_5571.jpeg` → fondo quitado en la foto completa, recortada por la cintura (y=770) y ajustada al sujeto → `04_salidas/borradores/foto3-cintura-sin-fondo_v01.png` (428x710).
- foto3 v02: retoque de papada con deformación suave (tipo licuar) en la línea de la mandíbula, ~3-5 px hacia la cara; sin tocar ojos, nariz ni boca. Script: `03_trabajo/liquify.py`. Instalado: opencv-python-headless (remap).
