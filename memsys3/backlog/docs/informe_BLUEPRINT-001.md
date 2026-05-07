<!-- version: 0.1.0 -->

# Informe: BLUEPRINT-001 — Release memsys3 v1.0

**Item:** [`../BLUEPRINT-001-release-memsys3-v1.md`](../BLUEPRINT-001-release-memsys3-v1.md)
**Plan:** [`plan_BLUEPRINT-001.md`](plan_BLUEPRINT-001.md)
**Fecha informe:** 2026-05-07
**Sesión origen:** 2026-05-07 (ver sessions.yaml)
**Estado del item al redactar informe:** Abierto

---

## 1. Motivación

memsys3 ha llegado a v0.22.0 tras ~6 meses de iteración. El sistema funciona, pero está optimizado para el dogfooding: un usuario externo descargándolo se enfrentaría a documentación dispersa, principios implícitos, y residualidad histórica (catalán, referencias a viz archivada, etc.).

El release v1.0 no es solo un bump de versión. Es el momento de **consolidar lo que memsys3 es** en forma comunicable y operativa para terceros. La pregunta clave: *¿un equipo nuevo que adopta memsys3 puede ser autónomo en 1 día sin acceso al mantenedor?*

Hoy la respuesta es "depende del azar de qué archivos lea primero". Eso es CDC pura — y memsys3 EXISTE para combatir CDC. Por tanto v1.0 debe eliminarla en su propio onboarding.

## 2. Contexto histórico

- **2025-10-28**: nacimiento de memsys3 v1.0 inicial (renombrado luego a v0.1.0 cuando se adoptó versionado git-tag)
- **2025-11–2026-01**: deployments reales en proyectos externos (CLIENT_F, CLIENT_C, CLIENT_A, CLIENT_B, CLIENT_E, WORKSPACE_Y). Cada deployment expuso bugs (ISSUE-005, 006, 007, 018, 019, 023). Todos resueltos.
- **2026-02-03**: Sistema de Reuniones Colaborativas + defensa multi-capa firmas commits (incidente histórico, margen error LLM 70%→5%).
- **2026-04-13**: Context Agent rediseñado con ingesta por tiers hasta 150K tokens.
- **2026-04-15**: Sistema file_version independiente por archivo (21 archivos versionados).
- **2026-04-20**: ISSUE-021 detectó que la auto-memory de Claude rompía agnosticismo + human-in-the-loop.
- **2026-05-06**: ADRs 017-019 (file_version + sustitución diferencial + deprecation contextualizada). Limpieza de scaffolds memsys3_templates/memory/ (4 archivos vaciados a Modelo D — había leak de dogfooding).
- **2026-05-07**: Articulado principio CDC. ADR-020 (memory.yaml). ADR-021 (backlog docs). Decisión de hacer release v1.0.

## 3. Hallazgos

### 3.1 Principios memsys3 (inventario inicial — falta consolidación)

Detectados en esta sesión, dispersos por el código:

1. **CDC (Casualidad de Contexto)** — `memory.yaml` dogfooding. NO en templates. NO en README.
2. **Agnosticismo de modelo IA** — ADR-016. Mencionado en README.
3. **Una sola carpeta** — README. NO formalizado en ADR.
4. **Human-in-the-loop** — README ("tú decides"). NO formalizado en ADR.
5. **Criterio inteligente del CA vs límites arbitrarios** — ADR-001.
6. **file_version inmutable salvo /actualizar-memsys3** — ADR-017.
7. **Templates como documentación activa permanente** — ADR-009.
8. **Datos preservados (history/, sessions_N, adr_N)** — ADRs 002, 003.
9. **Separation of Concerns README/context** — ADR-012.
10. **Restricciones infraestructura en agents** — ADR-017.

→ NO existe `PRINCIPLES.md` canónico. Esto es la frente 1.

### 3.2 Brechas potenciales ADRs vs código (sospechosas, sin auditar)

- ADR-009 dice "templates son documentación activa permanente". Verificar que el scaffold actualmente los preserva en deploy.
- ADR-012 dice "README en lectura directa". Verificar que `compile-context.md` NO lo duplica en `context.yaml`.
- ADR-017 dice "MA y CA NO modifican file_version". Verificar que en templates está la restricción (en dogfooding está quitada por deadlock — documentado).
- ADR-018 dice "sustitución diferencial templates schema". Verificar implementación Pasos 6.4/6.4.5 en `actualizar.md` (no smoke-tested aún).
- ADR-019 dice "deprecation contextualizada". Verificar que campos deprecados en templates llevan motivo.

### 3.3 Scaffold completitud

**Inventario actual `memsys3_templates/`:**
```
memsys3_templates/
├── agents/main-agent.yaml, context-agent.yaml
├── memory/
│   ├── README.md
│   ├── context.yaml
│   ├── memory.yaml          ← NUEVO ADR-020 (creado 2026-05-07)
│   ├── project-status.yaml
│   ├── full/                ← VACÍO (¿debería tener placeholders?)
│   ├── history/             ← VACÍO
│   └── templates/
│       ├── adr-template.yaml
│       ├── context-template.yaml
│       ├── memory-template.yaml      ← NUEVO ADR-020
│       ├── project-status-template.yaml
│       ├── sessions-template.yaml
│       ├── informe-template.md       ← NUEVO ADR-021
│       └── plan-template.md          ← NUEVO ADR-021
├── prompts/ (~17 archivos)
└── backlog/
    ├── README.md
    ├── IMPROVEMENT-008-...md         ← LEAK de dogfooding (debería estar vacío)
    └── docs/.gitkeep                 ← NUEVO ADR-021
```

**Hallazgos scaffold:**
- ✅ `backlog/docs/` ya creado en deploy/actualizar (Bloque B sesión 2026-05-07)
- ❌ `memsys3_templates/backlog/IMPROVEMENT-008-*.md` es leak de dogfooding (debería ser solo README.md vacío + docs/)
- ❌ `memsys3_templates/memory/full/` está vacío. ¿Debería tener `adr.yaml`, `sessions.yaml`, `operations.log` con frontmatter pero arrays vacíos? Hoy `deploy.md` los crea via `cat > ... << EOF`. Inconsistente: las plantillas de schema están en `templates/` pero las plantillas de "datos vacíos" están inline en `deploy.md`.
- ❌ `operations.log` NO tiene template equivalente en `memory/templates/` (pendiente prioritario 3 en project-status).
- ❌ `memsys3_templates/memory/history/` no existe físicamente (se crea en deploy con .gitkeep).

### 3.4 Residualidad detectada o sospechada

- **Catalán residual**: erradicado en sesión 2026-04-15, pero conviene grep final con `[àèéíòóúïü]` antes de release.
- **Referencias a viz/**: archivadas a `memsys3/docs/archivo/viz/`. Verificar que no quedan referencias activas en prompts/agents/README.
- **mind.md**: eliminado. Verificar que no se referencia.
- **Archivos huérfanos**: `IMPROVEMENT-008-...md` en templates (mencionado arriba).
- **`memsys3/memory/README.md`** existe en templates, ¿se usa? ¿es necesario?
- **`memsys3_templates/memory/context.yaml` y `project-status.yaml`** están en distribuible. ¿En qué estado? Deberían ser scaffolds vacíos (Modelo D), verificar.

### 3.5 Estrategia dogfooding (a revisar)

ADR-011 separó agnóstico (`memsys3_templates/`) vs específico (`memsys3/` raíz, prompts solo dogfooding). Tras 6 meses:

- El patrón funciona, pero sincronización dogfooding↔templates depende de `comprobar_alineamiento.md` (manual al final de sesión).
- Pregunta abierta: ¿memsys3/ (la instancia interna) debería ir al `.gitignore` del repo memsys3 para que no contamine el código distribuible? Hoy se commitea.
- Trade-off: si se ignora, perdemos historial real como ejemplo. Si se commitea, hay riesgo de contaminación cruzada (como IMPROVEMENT-008 leak).

### 3.6 deploy / actualizar / commands

- **deploy.md**: paso 9 (bridge MEMORY.md) recién añadido (ADR-020), sin probar.
- **actualizar.md**: pasos 6.4 (sustitución diferencial) y 6.4.5 (deprecation) recién añadidos en v0.22.0, sin smoke test (pendiente prioritario 1).
- **commands.md**: opcional Claude-específico (ADR-016). ¿Debería tener un README cómo desinstalar? ¿Cómo migrar a otro modelo?

## 4. Restricciones y principios

Esta release v1.0 debe respetar TODOS los principios memsys3 que ella misma documenta. En particular:

- **CDC**: el release debe REDUCIR CDC, no añadirla. Cada decisión: "¿esto requiere que el usuario adivine, o le doy archivo canónico?"
- **Agnosticismo**: nada Claude-específico debe quedar en agnóstico. Todo lo Claude debe ser opt-in.
- **Una sola carpeta**: nada nuevo fuera de `memsys3/` (excepto MEMORY.md bridge opcional).
- **Human-in-the-loop**: el deploy y actualizar siguen pidiendo confirmación, no se vuelven más automáticos.
- **file_version**: solo `/actualizar-memsys3` bumpa. Si v1.0 toca archivos, los bumps deben ir coordinados.
- **No firmar commits con Co-Authored-By** (ADR-016 + memory.yaml feedback).

## 5. Alternativas consideradas

### Alt A: Release v1.0 = solo bump de versión, sin auditoría
**Descartada**: convertiría v1.0 en v0.22.0 con etiqueta nueva. CDC alta para usuarios externos.

### Alt B: Release v1.0 con auditoría parcial (solo principios + residualidad)
**Descartada**: deja brechas ADRs sin verificar y scaffold incompleto. Aceptable como v0.23.0, no como v1.0.

### Alt C: Release v1.0 con auditoría exhaustiva (los 7 frentes)
**ADOPTADA**. Mayor coste, pero v1.0 representa "memsys3 estable y comunicable a terceros". Hacerlo bien una vez.

### Alt D: Hacer 2 releases (v0.23.0 con frentes 1-3, v1.0 con resto)
**Pospuesta**: viable si el plan se hace inviable en una sola tanda. El plan actual asume Alt C, pero deja puerta abierta a sub-releases si los bloqueos son grandes.

## 6. Open questions

1. **¿`PRINCIPLES.md` se ubica en `memsys3_templates/` o solo en raíz repo?** Argumento por raíz: es identidad del PROYECTO memsys3, no del scaffold desplegado. Argumento por templates: usuarios deberían tener los principios accesibles tras deploy. → Probable respuesta: ambos, con sync.
2. **¿`memsys3/` (instancia dogfooding) va al `.gitignore` del repo?** Decisión pendiente para frente 6. Ver trade-off arriba.
3. **¿`operations.log` necesita template equivalente?** Hay precedente: el formato de inicialización está hardcoded en `deploy.md`. → Sí, por consistencia con ADR-009.
4. **¿BLUEPRINT-001 se ejecuta en una única sesión larga o en serie de sesiones cortas?** Recomendación del plan: serie. Cada frente es ~1-2 sesiones.
5. **¿Quién/qué sesión ejecuta cada frente?** Sesión actual (2026-05-07) ha generado este informe + plan. Las sesiones de ejecución pueden ser distintas — el plan debe ser auto-suficiente (anti-CDC).

## 7. Referencias

- **ADRs**:
  - ADR-001 (criterio inteligente CA)
  - ADR-008 (Main Agent NO compila)
  - ADR-009 (templates permanentes + gotchas en sessions)
  - ADR-011 (separación agnóstico/específico)
  - ADR-012 (README lectura directa)
  - ADR-016 (agnosticismo de modelo)
  - ADR-017 (file_version)
  - ADR-018 (sustitución diferencial)
  - ADR-019 (deprecation contextualizada)
  - ADR-020 (memory.yaml)
  - ADR-021 (backlog docs anti-CDC)
- **Sesiones críticas**:
  - 2026-05-07 (origen + ADR-020/021/principio CDC)
  - 2026-05-06 (ADRs 017-019 + limpieza scaffolds)
  - 2026-04-15 (file_version + erradicación catalán)
  - 2026-02-03 (defensa firmas commits)
- **Items relacionados**:
  - ISSUE-006 (backups .gitignore — Alta prioridad)
  - ISSUE-021 (auto-memory — cerrado por ADR-020)
  - ISSUE-022 (hook pre-commit anti-firma)
  - ISSUE-023 (CLIENT_D — cerrado en v0.22.0)
  - FEATURE-012 (glosario)
- **Archivos clave para auditoría**:
  - `memsys3/memory/full/adr.yaml` (21 ADRs)
  - `memsys3_templates/` (todo el scaffold)
  - `memsys3/prompts/deploy.md` y `actualizar.md`
  - `README.md` raíz
- **Externas**:
  - Repo: https://github.com/iv0nis/memsys3
  - Web: https://memsys3.org (pendiente desplegar)
  - Wiki: https://github.com/iv0nis/memsys3/wiki
