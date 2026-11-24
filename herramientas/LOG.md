# LOG de herramientas — kit multimedia

**2026-11-24** — Instalación completa del kit de edición (imagen, vídeo, audio, 3D).
Reinstalar en una sesión nueva: `bash herramientas/instalar-media.sh`

## Imagen
| Herramienta | Versión | Para qué |
|---|---|---|
| ImageMagick | 6.9.12 | Conversión, recortes, composición, efectos por lote |
| GraphicsMagick | 1.3.42 | Alternativa rápida a ImageMagick |
| GIMP | 2.10.36 | Retoque avanzado (scripts batch) |
| Inkscape | 1.2.2 | Vectorial / SVG, exportar a PNG/PDF |
| rsvg-convert, potrace, svgo | 2.58 / 1.16 / 4.1 | SVG→PNG, vectorizar bitmaps, optimizar SVG |
| cwebp, avifenc, heif | 1.3.2 / 1.0.4 | Formatos WebP, AVIF, HEIC |
| pngquant, optipng, jpegoptim, gifsicle | — | Compresión/optimización web y GIFs |
| exiftool | 12.76 | Leer/editar/borrar metadatos |
| sharp-cli (Node) | 6.1 | Redimensionado rápido |
| Python: Pillow, OpenCV, scikit-image, Wand, rawpy, cairosvg | ver script | Procesado por código, RAW de cámara |
| rembg | 2.0.69 | Quitar fondos con IA (descarga el modelo en el primer uso) |

## Vídeo
| Herramienta | Versión | Para qué |
|---|---|---|
| FFmpeg (+x264, x265) | 6.1.1 | Cortar, unir, convertir, filtros, subtítulos |
| HandBrakeCLI | — | Recodificación con presets |
| mkvtoolnix, mediainfo, ffmpegthumbnailer | 82.0 | Contenedores MKV, inspección, miniaturas |
| Remotion CLI | 4.0.546 | Vídeo programático con React (licencia gratis para individuos/equipos pequeños) |
| Python: MoviePy, ffmpeg-python, imageio | 2.2.1 | Montaje por código |
| yt-dlp | 2026.11.23 | Descargar referencias (solo material con derechos) |

## Audio
| Herramienta | Versión | Para qué |
|---|---|---|
| SoX (+todos los formatos) | 14.4.2 | Efectos, normalizar, recortar, mezclar |
| lame, flac, opus-tools, vorbis-tools | — | Codificar MP3/FLAC/Opus/OGG |
| rubberband | 3.3.0 | Cambiar tempo/tono sin artefactos |
| Python: pydub, librosa, soundfile, pedalboard, noisereduce, pyloudnorm, mutagen | ver script | Edición, análisis, efectos tipo plugin, reducción de ruido, loudness (LUFS), etiquetas |
| faster-whisper | 1.2.1 | Transcripción / subtítulos automáticos (modelo se descarga al usarlo) |

## 3D
| Herramienta | Versión | Para qué |
|---|---|---|
| Blender | 4.0.2 | Modelado, animación y render headless (`blender -b`) |
| xvfb | — | Pantalla virtual para apps que la necesiten |

## Notas
- Conflicto menor: `pdfplumber` pide Pillow ≥12.2 pero MoviePy fija Pillow 11.3; no afecta a imagen/vídeo/audio.
- Sin GPU: render de Blender en CPU (Cycles/Eevee) y IA (rembg, whisper) en CPU.
