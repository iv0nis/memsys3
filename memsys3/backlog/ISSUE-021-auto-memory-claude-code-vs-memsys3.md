# ISSUE-021: Auto-memory de Claude Code interfiere con memsys3

**Estado:** Abierto
**Prioridad:** Alta
**Tipo:** Issue
**Plazo:** Short-term
**Fecha identificación:** 2026-04-20
**Origen:** Conversación con agente gitkigai (Claude Code con auto-memory activa)

---

## Problema

Claude Code tiene un sistema de **auto-memory** propio (`~/.claude/projects/<proyecto>/memory/MEMORY.md`) que guarda automáticamente perfil de usuario, feedback y contexto en cada conversación, independientemente de memsys3.

En proyectos con memsys3 desplegado, esto genera **dos sistemas de memoria paralelos**:

1. **memsys3** (multimodal, agnóstico, explícito, human-in-the-loop): `memsys3/memory/`
2. **auto-memory de Claude Code** (específico Claude, implícito, automático): `~/.claude/projects/.../memory/MEMORY.md`

El agente sigue la instrucción de sistema "auto memory" sin distinguir que el proyecto tiene memsys3 como sistema propio, y acaba escribiendo datos del usuario en MEMORY.md en lugar de (o además de) en memsys3.

### Síntoma concreto observado

El agente usó "Banyoles" como valor por defecto silencioso al rellenar un campo "lugar" porque lo tenía guardado en MEMORY.md como "Ubicación: Banyoles, Girona" **sin contexto de para qué sirve ni cuándo aplicarlo**. Aplicó el dato como default en vez de preguntar.

La raíz no es el error de defecto silencioso (corregible caso a caso), sino el **origen**: datos del usuario viven en MEMORY.md fuera del control de memsys3.

---

## Por qué importa

- **Rompe el principio agnóstico (ADR-016):** MEMORY.md solo existe en Claude Code. Si el usuario cambia a Gemini/Codex, pierde esos datos
- **Rompe el human-in-the-loop:** memsys3 exige que el usuario decida qué se guarda; auto-memory guarda sin pedir permiso
- **Duplicación y desincronización:** el mismo dato puede existir en ambos sistemas con valores distintos
- **Fuga de contexto a directorio del sistema:** datos del proyecto acaban en `~/.claude/` fuera del repositorio

---

## Propuesta (a investigar)

### Opción A: Desactivar auto-memory en proyectos con memsys3

Documentar cómo desactivar la instrucción "auto memory" de Claude Code:
- Revisar `~/.claude/settings.json` y `~/.claude/settings.local.json`
- Identificar el ajuste exacto que la activa
- Añadir guía a `memsys3/docs/` o `deploy.md`

**⚠️ Hallazgo posterior (2026-04-20, segunda conversación con gitkigai):**
La instrucción auto-memory **NO es editable desde settings.json** — está inyectada por el harness de Claude Code directamente. El agente confirmó: "Los settings.json no controlan auto-memory — es una instrucción inyectada por el harness de Claude Code, no editable desde aquí."

Esto invalida parcialmente Opción A como solución limpia. El workaround aplicado en gitkigai fue:
- Vaciar MEMORY.md y convertirlo en puntero a memsys3 con prohibición de escritura nueva
- Pero los archivos `.md` sueltos del sistema auto-memory (feedback_*, project_*, user_*) siguen existiendo como histórico

**Alcance real del problema (ampliado):** no es solo MEMORY.md. El sistema auto-memory crea archivos individuales por tipo:
- `feedback_*.md` — reglas de comportamiento dadas por el usuario
- `project_*.md` — hechos del proyecto
- `user_*.md` — hechos del usuario

Caso real gitkigai: 9 archivos acumulados (4 feedback, 4 project, 1 user) todos con info duplicable en memsys3 (sessions.yaml, project-status.yaml, prompts, o el propuesto MEMORY_memsys3.yaml).

### Opción B: Instrucción en CLAUDE.md del proyecto

Añadir instrucción en CLAUDE.md (si existe) que le diga al agente: "Este proyecto usa memsys3. NO escribas en MEMORY.md. Toda memoria persistente va en `memsys3/memory/`."

**Pros:** Claude Code lee CLAUDE.md automáticamente
**Contras:** Específico de Claude Code (igual que el problema)

### Opción C: Limpieza periódica + prompt dedicado

Crear prompt `memsys3/prompts/limpiar-memory-claude.md` que migre lo relevante de MEMORY.md a memsys3 y vacíe MEMORY.md.

### Opción D: Crear `MEMORY_memsys3.yaml` estructurado (a valorar)

Archivo YAML dentro de memsys3 que guarde **datos puros** (sin instrucciones de comportamiento), estructurados por naturaleza del dato, para cubrir la función legítima que hoy asume MEMORY.md de Claude Code.

**Naturaleza de los datos (a definir):**
- **Proyecto:** nombre, alias, dominio, stakeholders
- **Usuario:** nombre, cómo quiere ser llamado, ubicación, idioma preferido, rol
- **Preferencias de trabajo:** tono, nivel de detalle, idioma de commits, etc.
- **Otros campos específicos del proyecto:** a definir durante briefing/deploy

**Nota sobre feedback:** el sistema auto-memory de Claude Code guarda 3 tipos (user, project, feedback). Los dos primeros son datos puros y encajan en MEMORY_memsys3.yaml. **El tercero (feedback) NO son datos sino reglas de comportamiento** — no pertenecen aquí. Ejemplos reales vistos: "usar mv -n para evitar sobrescribir", "no corregir typos en comentarios". Lugar correcto a decidir: prompt dedicado, sección en main-agent.yaml, o archivo aparte `memsys3/memory/behavior-rules.yaml`. Este ISSUE cubre solo datos; las reglas de comportamiento podrían requerir un ISSUE o FEATURE separado.

**Principios:**
- Solo datos, NO instrucciones ("siempre haz X" va en otro sitio: prompts, CLAUDE.md, feedback)
- Estructurado (YAML) para que cualquier agente lo lea sin ambigüedad
- Agnóstico: funciona con cualquier modelo de IA (cumple ADR-016)
- Algunos campos predefinidos en el template + espacio libre para datos específicos del proyecto

**Beneficios:**
- Elimina la necesidad real que Claude Code intenta cubrir con auto-memory
- Datos portables entre modelos
- Human-in-the-loop: el usuario decide qué se guarda durante deploy/briefing
- Separación clara: **datos** (este archivo) vs **memoria histórica** (context.yaml) vs **estado** (project-status.yaml) vs **instrucciones** (prompts, agents)

**Preguntas abiertas:**
- ¿Se rellena en deploy.md (briefing) o con prompt dedicado?
- ¿Schema fijo o extensible por proyecto?
- ¿Va en `memsys3/memory/` junto a context.yaml y project-status.yaml?
- ¿Cómo se integra con newSession.md (se carga siempre)?

---

## Conversación origen (resumen)

**Parte 1 — detección:**
- Usuario detecta que agente usó "Banyoles" como default silencioso
- Agente reconoce: lo tiene en MEMORY.md como "Ubicación: Banyoles, Girona" sin contexto de uso
- Usuario: "nosotros no trabajamos con memory.md, trabajamos con memsys, es multimodal, memory es solo de claude"
- Agente confirma: sigue instrucción de sistema "auto memory" que guarda en MEMORY.md sin distinguir proyectos con memsys3

**Parte 2 — investigación (corrección importante):**
- Usuario pregunta si la instrucción se puede editar
- Agente inicialmente responde "Sí, está en settings.json" → **INCORRECTO**
- Tras intentarlo, agente corrige: "Los settings.json no controlan auto-memory — es una instrucción inyectada por el harness de Claude Code, no editable desde aquí"
- Workaround aplicado: vaciar MEMORY.md y convertirlo en puntero a memsys3
- Descubrimiento del alcance real: además de MEMORY.md, el sistema auto-memory crea archivos individuales:
  - `feedback_*.md` (reglas de comportamiento): mv_colisiones, no_corregir_typos_comentarios, no_llm_markers, no_respuestas_ia
  - `project_*.md` (hechos de proyecto): colico_nefritico_2026_04_16, paddely, pec_programacion_entregada, root_cleanup
  - `user_*.md` (hechos de usuario): elena
- 9 archivos acumulados en un solo proyecto, todos con info duplicable en memsys3

Ruta MEMORY.md en el caso observado:
`/home/ivonis/.claude/projects/-home-ivonis-gitkigai/memory/MEMORY.md`

---

## TODO (decisiones pendientes)

- **Separar feedback en ISSUE propio?** El sistema auto-memory crea 3 tipos (user, project, feedback). Los 2 primeros son datos y caben en MEMORY_memsys3.yaml (Opción D). El tercero (reglas de comportamiento: "usar mv -n", "no corregir typos en comentarios") NO es dato. Pendiente decidir: ¿van en main-agent.yaml, prompt dedicado, archivo `behavior-rules.yaml`, o no-problema? No abrir ISSUE separado hasta tener más patrones reales de uso en múltiples proyectos.

---

## Referencias

- **ADR relacionado:** ADR-016 (memsys3 agnóstico de modelo de IA)
- **Principio afectado:** Human-in-the-loop (README.md)
- **Archivos a investigar:** `~/.claude/settings.json`, `~/.claude/settings.local.json`
- **Relacionado con:** ISSUE-020 (protocolo post-compact — otro punto donde auto-memory y memsys3 colisionan)
