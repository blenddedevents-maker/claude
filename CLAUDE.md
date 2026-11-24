# Reglas de trabajo para Claude Code

Este repositorio es un taller creativo y técnico. Se trabaja en **dos fases**:

1. **Fase IDEA** (usuario + Claude, conversación): se pule qué buscamos, para qué, con qué estilo y qué entregables. Resultado: un `BRIEF.md` cerrado. En esta fase **no se construye nada**, solo se pregunta, se propone y se documenta.
2. **Fase EJECUCIÓN** (Claude Code): con el brief aprobado, Claude Code hace el trabajo final siguiendo el orden estricto de abajo.

El usuario decide cuándo se pasa de una fase a otra ("brief aprobado, ejecuta").

## 1. Herramientas: instalar sin pedir permiso

- Claude Code puede **instalar cualquier herramienta, librería o aplicación** que mejore el resultado (Remotion, Blender, Three.js, FFmpeg, ImageMagick, Playwright, Python/Node packages, etc.) sin pedir permiso.
- **Sí debe preguntar** cuando haya que **elegir entre varias opciones** que cambian el resultado (ej. animación 3D: ¿Blender, Three.js o Remotion + React Three Fiber?). Presentar 2-3 opciones, recomendar una y explicar en una línea por qué.
- También preguntar si una herramienta necesita **cuenta, clave API o pago**.
- Registrar cada instalación en `LOG.md` del proyecto (qué, versión, para qué).
- Nota: el entorno es un contenedor efímero. Lo que deba conservarse se guarda en el repo (commit + push).

## 2. Estructura obligatoria de cada proyecto

Cada trabajo nuevo se crea copiando `plantillas/proyecto/` a `proyectos/AAAA-MM-DD_nombre-corto/`:

```
proyectos/AAAA-MM-DD_nombre/
├── 00_brief/BRIEF.md        ← la idea cerrada (fuente de verdad)
├── 01_referencias/          ← todo lo que inspira, nunca se modifica
│   ├── visual/  audio/  texto/  tecnica/
├── 02_assets/
│   ├── entrada/             ← archivos que aporta el usuario
│   └── generados/           ← lo que crea Claude (imágenes, modelos, audio)
├── 03_trabajo/              ← código, escenas, archivos fuente editables
├── 04_salidas/
│   ├── borradores/          ← versiones v01, v02… para revisar
│   └── final/               ← solo lo aprobado
└── LOG.md                   ← diario: decisiones, instalaciones, versiones
```

Reglas de orden:
- Nombres en minúsculas, sin espacios ni tildes: `escena-intro_v03.mp4`.
- Versionar siempre (`_v01`, `_v02`…); nunca sobrescribir una versión revisada.
- Nada va a `final/` sin aprobación explícita del usuario.
- Referencias y archivos de entrada son de solo lectura.

## 3. Orden de ejecución (Fase EJECUCIÓN)

1. Leer `BRIEF.md` completo. Si falta algo crítico → preguntar antes de empezar.
2. Proponer un plan corto (pasos, herramientas, entregables) y esperar OK.
3. Instalar herramientas necesarias y anotarlas en `LOG.md`.
4. Organizar referencias y assets en sus carpetas.
5. Producir un **borrador rápido** (v01) para validar dirección.
6. Iterar con el feedback del usuario (v02, v03…).
7. Exportar a `final/` cuando el usuario apruebe. Commit + push.

## 4. Comunicación

- Idioma: español.
- Antes de decisiones creativas importantes, preguntar; en decisiones técnicas menores, decidir y explicar.
- Al terminar cada paso, resumir en 2-3 líneas qué se hizo y qué falta.
