# BRIEF — Saludo animado para Sergi Moea

Estado: **borrador** (2026-11-24) — pendiente de aprobación del usuario

## 1. Qué es
Un clip vertical de 5-8 s donde un reguetonero animado **inventado** ("Kiko Flow", nombre provisional) mira a cámara y suelta: *"¡Ey, Sergi Moea! Un saludo, mi gente. ¡Dale!"*

## 2. Para qué y para quién
- Regalo/broma para un amigo: Sergi Moea.
- Uso: WhatsApp e Instagram/TikTok stories.

## 3. Estilo y tono
- **Personaje:** reguetonero 100 % ficticio, estilo cartoon 2D/3D exagerado: gafas de sol enormes, gorra, cadena dorada gigante con su inicial "K", chaqueta de colores. **No se parece a ningún artista real** (ni cara, ni tatuajes, ni nombre).
- **Ambiente:** fondo de neón (morado, rosa, cian), luces de discoteca, humo.
- **Tono:** chulo, divertido, con energía de videoclip. Exagerado, nada serio.
- **Ritmo:** beat de dembow original que entra fuerte desde el segundo 0.
- **Texto en pantalla:** "SALUDOS PA' SERGI MOEA 🔥" grande, animado al ritmo.

## 4. Entregables
| Archivo | Formato | Medidas / duración | Notas |
|---|---|---|---|
| `saludo-sergi_v01.mp4` | MP4 (H.264 + AAC) | 1080×1920, 30 fps, 5-8 s | Borrador para validar dirección |
| `saludo-sergi_vXX.mp4` | MP4 | ídem | Versión final aprobada → `04_salidas/final/` |

## 5. Material disponible
Ninguno por ahora. Todo lo genera Claude Code (personaje, fondo, beat, voz).
Opcional: una foto de Sergi para meter un "marco" con su cara al final → `02_assets/entrada/`.

## 6. Herramientas previstas
- **Personaje y animación:** Blender 4.0 (personaje low-poly cartoon, render en CPU) — alternativa más rápida: 2D con Remotion/SVG. *Elegir antes de ejecutar.*
- **Voz:** síntesis de voz genérica en español (p. ej. Piper TTS, local y gratis) + efectos con pedalboard (autotune ligero, eco). La voz **no imita a ninguna persona real**.
- **Beat:** dembow sintetizado por código (Python) — original, sin samples con derechos.
- **Montaje y texto:** FFmpeg / Remotion.

## 7. Restricciones
- NO usar la cara, voz, nombre ni marca de ningún artista real (nada de Anuel AA ni parecidos).
- NO usar música con derechos.
- Duración máxima 8 s.

## 8. Criterio de éxito
- Se entiende claramente "Saludos a Sergi Moea" a la primera.
- El personaje tiene gracia y la estética es de videoclip.
- Se ve bien en móvil y pesa poco (< 10 MB) para mandarlo por WhatsApp.

## Preguntas abiertas
1. ¿Te vale el nombre "Kiko Flow" o le ponemos otro?
2. Personaje en **3D (Blender)** o **2D cartoon (más rápido)**?
3. ¿Quieres añadir una foto de Sergi al final?
