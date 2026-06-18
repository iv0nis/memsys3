# Deploy memsys3 — Instalación inicial del Sistema Memory

## Paso 0 — Rol agéntico

Para este prompt actúas como **Setup Agent (ADR-028)**. Tu alcance: instalación inicial de memsys3 en el proyecto del usuario, end-to-end (estructura → personalización → compilación inicial de `context.yaml`). Referencia: `agents/setup-agent.yaml` (lo copiarás como parte del scaffold; léelo si necesitas reglas operativas).

**No eres** Main Agent ni Context Agent. Esos roles operan en sesiones posteriores. El SA solo se invoca en `deploy.md` y `actualizar.md`.

## Objetivo

Instalar la estructura completa de memsys3, personalizarla con el contexto del proyecto del usuario, y dejar `context.yaml` v0.1.0 compilado — un solo flujo end-to-end, sin pasos manuales posteriores.

## Contrato de ejecución (agnóstico de modelo)

Este prompt es ejecutable por cualquier LLM con tooling estándar (lectura/escritura de archivos, ejecución de comandos shell, output al usuario). **NO** depende de tools propietarias (preguntas estructuradas tipo `AskUserQuestion`, auto-expansión de `@-mention`, comandos globales `/deploy-memsys3`, etc.). Cuando este prompt pida datos al usuario, usa el canal que tu harness ofrezca:

- Si soportas preguntas estructuradas con opciones predefinidas → úsalas.
- Si solo tienes output libre → presenta los datos requeridos en bloque y espera respuesta del usuario.
- Si trabajas en modo no-interactivo (batch, playground) → el usuario debe haber rellenado `deploy-config.yaml` en la raíz del proyecto antes de invocarte (ver Paso 3).

> **Apéndice (auditoría):** este prompt fue refactorizado a agnóstico en BLUEPRINT-002 Bloque B (sesión 2026-05-18). Tabla de invariantes en `backlog/docs/informe_BLUEPRINT-002.md` §3. Si añades una tool propietaria nueva, documéntala como invariante declarativo equivalente.

## Contrato de idioma (agnóstico de modelo)

A diferencia de una sesión de trabajo, durante el deploy NO existen todavía archivos canónicos del proyecto (`project-status.yaml`, `memory.yaml`, `context.yaml` se crean en este mismo flujo). DEBES determinar el idioma de trabajo así, en este orden:

1. Responde al usuario en el idioma en que él se dirige a ti, desde el primer mensaje, NO en el default de tu harness.
2. Si el proyecto destino ya tiene `README.md` o `docs/` poblados (Paso 4), su idioma predomina para el contenido que generes.
3. El campo `idioma` del briefing (Paso 4) o de `deploy-config.yaml` (Paso 3) es la fuente AUTORITATIVA una vez captado: úsalo para todo el output al usuario Y para personalizar `project-status.yaml`, `newSession.md` y `context.yaml`.

Si estas señales entran en conflicto, pregunta al usuario antes de escribir el scaffold.

**Por qué esta sección**: distintos harnesses tienen defaults distintos (algunos a inglés pese al contexto en otro idioma). El deploy es el primer contacto cross-harness; sin contrato explícito, un proyecto puede nacer con su memoria en el idioma equivocado y arrastrarlo en cada sesión futura (anti-CDC desde el día 0).

---

## Workflow de Deployment

### Paso 1 — Clonar temporalmente memsys3

El usuario te indica el directorio de trabajo (normalmente raíz de su proyecto).

```bash
# Verificar que no hay deployment previo
if [ -d "memsys3" ]; then
  echo "⚠️  ERROR: memsys3/ ya existe en este proyecto"
  echo "Si quieres reinstalar: mv memsys3 memsys3_backup  (o)  rm -rf memsys3"
  exit 1
fi

# Limpiar memsys3_temp si quedó de una ejecución previa
[ -d "memsys3_temp" ] && rm -rf memsys3_temp

# Clonar repo
git clone https://github.com/iv0nis/memsys3 memsys3_temp
```

### Paso 2 — Copiar estructura a `memsys3/`

Scaffold completo desde `memsys3_templates/` (fuente única, ADR-023):

```bash
# Crear estructura
mkdir -p memsys3/{agents,memory/{full,history,templates},prompts,backlog/docs}

# Placeholders para directorios que pueden quedar vacíos
touch memsys3/memory/history/.gitkeep
touch memsys3/backlog/docs/.gitkeep

# Templates (.yaml + .md, incluye informe-template.md, plan-template.md, deploy-config-template.yaml)
cp memsys3_temp/memsys3_templates/memory/templates/*.yaml memsys3/memory/templates/
cp memsys3_temp/memsys3_templates/memory/templates/*.md   memsys3/memory/templates/

# Archivos vacíos canónicos memory/full/ (adr.yaml, sessions.yaml, operations.log) — ADR-023
cp memsys3_temp/memsys3_templates/memory/full/* memsys3/memory/full/

# Memoria root (context.yaml y memory.yaml vacíos modelo D + README)
cp memsys3_temp/memsys3_templates/memory/context.yaml memsys3/memory/
cp memsys3_temp/memsys3_templates/memory/memory.yaml  memsys3/memory/
cp memsys3_temp/memsys3_templates/memory/README.md    memsys3/memory/

# Prompts y agents (incluye setup-agent.yaml — ADR-028)
cp memsys3_temp/memsys3_templates/prompts/*.md memsys3/prompts/
cp memsys3_temp/memsys3_templates/agents/*.yaml memsys3/agents/

# PRINCIPLES.md (canónico, ADR-022)
cp memsys3_temp/memsys3_templates/PRINCIPLES.md memsys3/PRINCIPLES.md

# Backlog scaffold (solo README — items concretos NO se distribuyen, ADR-021/023)
cp memsys3_temp/memsys3_templates/backlog/README.md memsys3/backlog/
```

> **Nota (ADR-023):** los archivos `memsys3/memory/full/{adr.yaml,sessions.yaml,operations.log}` se copian desde fuente única. Tras la copia son **datos del usuario** (escribibles por Main Agent en sesiones posteriores), no infraestructura. `project-status.yaml` se crea en Paso 5.

### Paso 3 — Detección de `deploy-config.yaml` (modo declarativo)

Antes de pedir datos al usuario, comprueba si existe `deploy-config.yaml` en la raíz del proyecto:

```bash
if [ -f "deploy-config.yaml" ]; then
  echo "✅ deploy-config.yaml detectado — modo declarativo"
else
  echo "ℹ️  Sin deploy-config.yaml — modo briefing interactivo"
fi
```

- **Si existe** → léelo, valida que los campos `proyecto.nombre`, `proyecto.dominio`, `proyecto.objetivo`, `proyecto.audiencia`, `proyecto.fase`, `proyecto.idioma`, `gitignore_memsys3`, `memory_bridge` están rellenos (no vacíos). Si faltan campos críticos, completa el resto con briefing del Paso 4 solo para los huecos. Salta al Paso 5 con los datos cargados.
- **Si NO existe** → procede al Paso 4 (briefing).

Schema completo del archivo: `memsys3_templates/memory/templates/deploy-config-template.yaml` (no copiado por defecto al destino; opt-in).

### Paso 4 — Briefing del proyecto (modo interactivo)

> **Filosofía (refinamiento sesión 2026-05-12):** memsys3 es agnóstico de dominio y de stack. El SA NO pregunta por framework, lenguaje, deploy platform — son irrelevantes para la memoria. Pregunta por la **naturaleza** del proyecto: dominio, objetivo, audiencia. Si el proyecto ya tiene `README.md` poblado o `docs/` maduros, **léelos primero** y usa el briefing solo para aclarar huecos.

**Datos a captar del usuario** (presenta el bloque entero y espera respuesta; si tu harness soporta preguntas estructuradas, divide en sub-preguntas):

1. **Nombre del proyecto** — ¿Cómo se llama?
2. **Dominio** — ¿En qué área/sector trabaja? (ej: "fintech B2B", "herramienta CLI dev", "investigación académica")
3. **Objetivo** — ¿Cuál es el goal principal en 1-2 frases?
4. **Audiencia** — ¿Quién lo usa/lee? (ej: "desarrolladores senior", "estudiantes CLIENT_E", "equipo interno 5 personas")
5. **Fase** — Planificación / MVP / Beta / Producción
6. **Idioma** — ¿En qué idioma trabajamos? (afecta a UI, código, memoria del proyecto)

**Opcional** (no bloqueante):
- URLs (producción, staging, repositorio)
- Pendientes iniciales que el usuario quiera registrar

**Decisiones de deploy** (necesarias antes del Paso 8/9):
- ¿Incluir `memsys3/` en git? (recomendado: sí — anti-pérdida de contexto)
- ¿Usas un harness con auto-memory inyectada (Claude Code, etc.)? Si sí, crearemos `MEMORY.md` raíz como puntero a `memsys3/memory/memory.yaml` (ADR-020).

### Paso 5 — Registrar versión de memsys3

```bash
cd memsys3_temp
MEMSYS3_VERSION=$(git describe --tags --always)
MEMSYS3_COMMIT=$(git log -1 --format=%h)
cd ..
```

### Paso 6 — Crear `project-status.yaml`

> ⚠️ Va en `memsys3/memory/` (raíz de memory), **NO** en `memsys3/memory/full/`.

Lee `memsys3/memory/templates/project-status-template.yaml` para el schema completo. Crea `memsys3/memory/project-status.yaml` con los datos del briefing/config:

```yaml
# Project Status — [NOMBRE_PROYECTO]

metadata:
  ultima_actualizacion: "[FECHA_HOY]"
  actualizado_por: "Setup Agent (Initial Deployment)"
  fase: "[FASE]"
  memsys3_version: "[MEMSYS3_VERSION del Paso 5]"
  memsys3_deployed: "[FECHA_HOY]"

vision_general:
  que_es: "[DOMINIO + descripción 1 línea]"
  objetivo: "[OBJETIVO]"
  audiencia: "[AUDIENCIA]"

estado_actual:
  fase: "[FASE]"
  ultima_feature: "Deployment inicial de memsys3"
  siguiente_milestone: "[Si user lo indicó, si no: vacío]"

features: {}

urls:
  # production, staging, repository — solo si user las dio
  {}

pendientes_prioritarios: []  # rellenar si user indicó pendientes_iniciales

decisiones_clave: {}
historico_sesiones: []
```

### Paso 7 — Personalizar `prompts/newSession.md`

Edita `memsys3/prompts/newSession.md` añadiendo (en la sección 1 "Cargar contexto"):

```markdown
- En este proyecto trabajaremos en [DESCRIPCION_BREVE basada en dominio/objetivo].
- Idioma de trabajo: [IDIOMA].
- Lee memsys3/memory/project-status.yaml y memsys3/memory/context.yaml
- Actúa según las instrucciones en memsys3/agents/main-agent.yaml
```

> Nota: en harnesses que soportan auto-expansión `@-mention` (Claude Code, Cursor, Cline) puedes prefijar las rutas con `@` para inyección inline. La forma sin `@` funciona en todos los harnesses.

### Paso 8 — Configurar `.gitignore`

Según la decisión del usuario (Paso 4):

**Si INCLUIR `memsys3/` en git (recomendado):**
- No modifiques `.gitignore`.
- Verifica que `memsys3/` no esté excluido:
  ```bash
  grep -q "^memsys3" .gitignore 2>/dev/null && echo "⚠️ memsys3/ aparece en .gitignore — considera eliminarlo" || echo "✅ memsys3/ versionado"
  ```

**Si EXCLUIR `memsys3/` de git:**
- Append a `.gitignore` (o créalo) con:
  ```
  # memsys3 — Sistema de gestión de contexto (local only)
  memsys3/
  ```
- Advierte al usuario:
  > ⚠️ Con esta opción, en harnesses que usan `@-mention` con auto-expansión (Claude Code, Cursor) las menciones a archivos dentro de `memsys3/` no funcionarán. Usa instrucciones directas: "Ejecuta memsys3/prompts/newSession.md".

### Paso 9 — Bridge MEMORY.md (opcional, según Paso 4)

Si el usuario indicó que su harness inyecta auto-memory (Claude Code, etc.), crea `MEMORY.md` en raíz del proyecto destino como puntero al canónico (ADR-020):

```markdown
# MEMORY

Este proyecto usa **memsys3**. Toda la memoria de usuario y feedback vive en
`memsys3/memory/memory.yaml`. Léelo para preferencias, reglas y perfil del usuario.

**No escribas en este archivo** — usa `memsys3/memory/memory.yaml` (append + datado).
Schema: `memsys3/memory/templates/memory-template.yaml`. Ver ADR-020.
```

Si el usuario NO necesita el bridge → omitir paso. `memory.yaml` funciona igual (graceful degradation).

### Paso 10 — Propagación de `AGENTS.md` (invariante agnóstico de memoria)

`AGENTS.md` es el estándar cross-tool (agents.md) leído por Codex, Cline, Copilot, Kilo, Warp nativamente, y por Cursor/Aider vía config. Contiene el invariante de memoria agnóstica (ADR-027) que redirige cualquier auto-memory del harness a `memsys3/memory/memory.yaml`.

```bash
if [ -f "AGENTS.md" ]; then
  echo "ℹ️  AGENTS.md ya existe en raíz — revisar manualmente para mergear el invariante"
  # Si ya existe contenido del usuario, NO sobrescribir. Verificar si tiene la sección
  # "Invariante de memoria agnóstica" — si no, append desde memsys3_temp/memsys3_templates/AGENTS.md.
else
  cp memsys3_temp/memsys3_templates/AGENTS.md AGENTS.md
  echo "✅ AGENTS.md creado en raíz del proyecto"
fi
```

### Paso 11 — Eliminar clone temporal

```bash
rm -rf memsys3_temp
```

### Paso 12 — Compilación inline de `context.yaml` v0.1.0

> **Justificación (ADR-028 ↔ ADR-008):** ADR-008 prohíbe que el Main Agent proponga `compile-context` porque acumula tokens en sesiones de trabajo cargadas. Aquí el Setup Agent ejecuta compile-context inline en una sesión de **deploy** (no de trabajo): los tokens acumulados son los del propio deploy (briefing + scaffold), que SON el material a sintetizar. No hay sesgo de sesión externa. Por eso ADR-028 articula que el SA compila inline en deploy sin violar ADR-008 en espíritu.

Lee y ejecuta `memsys3/prompts/compile-context.md` ahora. El Context Agent generará `memsys3/memory/context.yaml` v0.1.0 con el contenido recién escrito (project-status + scaffold). El archivo final no debe quedar vacío.

### Paso 13 — Mensaje final unificado al usuario

```
✅ memsys3 deployment completado end-to-end

Estructura instalada:
- memsys3/PRINCIPLES.md (10 principios sistémicos, ADR-022)
- memsys3/agents/ (main-agent, context-agent, setup-agent)
- memsys3/prompts/ (newSession, endSession, compile-context, deploy, actualizar, ...)
- memsys3/memory/ (project-status.yaml personalizado, memory.yaml, context.yaml v0.1.0)
- memsys3/memory/full/ (adr.yaml, sessions.yaml, operations.log inicializados)
- memsys3/memory/templates/ (guías permanentes)
- memsys3/backlog/ (README + docs/ scaffold)

Archivos en raíz (según decisiones del briefing):
- AGENTS.md (invariante memoria agnóstica, ADR-027)
- MEMORY.md (opcional, bridge para harnesses con auto-memory inyectada)

Próximo paso:
→ Ejecuta memsys3/prompts/newSession.md para comenzar a trabajar.

Escalabilidad automática (ya activa):
📈 Rotación: >1800 líneas → sessions_N.yaml, adr_N.yaml
📦 Plan Contingencia: >150K tokens → archivado a memory/history/
🔍 Context compilado: máximo 2000 líneas por sesión
```

---

## Notas importantes

- **Templates permanentes**: `memory/templates/` son guías que Main Agent y Setup Agent consultan en sesiones futuras. No los borres.
- **Personalización mínima**: solo `project-status.yaml` y `newSession.md` se personalizan en el deploy. El resto del scaffold es agnóstico.
- **Agnosticismo de modelo (ADR-016 + ADR-027)**: este prompt funciona en Claude Code, Cursor, Cline, Codex, Gemini CLI, Aider, Roo, Windsurf, Copilot, Warp y cualquier LLM con tooling de lectura/escritura/shell. Si tu harness añade un nuevo mecanismo de auto-memoria persistente, redirígelo a `memsys3/memory/memory.yaml` (invariante AGENTS.md).
- **Setup Agent vs Main Agent**: SA solo opera en `deploy.md` y `actualizar.md`. Tras este deploy, el desarrollo cotidiano lo lleva el Main Agent (`agents/main-agent.yaml`). No mezclar roles.

## Troubleshooting

- **"git clone falla"** → verifica conexión + `git --version`.
- **"mkdir falla"** → directorio de trabajo correcto + permisos.
- **"Templates no se copian"** → verifica que `memsys3_temp/memsys3_templates/` existe tras el clone.
- **"compile-context genera context.yaml vacío"** → bug en el deploy (datos no llegaron al Context Agent), no en compile-context. Revisa que `project-status.yaml` quedó bien escrito en Paso 6.

---

**Deployment completado. Sistema operativo end-to-end.**
<!-- version: 0.3.0 -->
