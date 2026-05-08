<!-- version: 0.1.0 -->

# Informe de residualidad: BLUEPRINT-001 Frente 5 — Eliminación de residualidad

**Item:** [`../BLUEPRINT-001-release-memsys3-v1.md`](../BLUEPRINT-001-release-memsys3-v1.md)
**Informe principal:** [`informe_BLUEPRINT-001.md`](informe_BLUEPRINT-001.md)
**Plan:** [`plan_BLUEPRINT-001.md`](plan_BLUEPRINT-001.md)
**Fecha:** 2026-05-08
**Sesión:** 2026-05-08 (Frente 5)
**Vara de medir:** `memsys3/PRINCIPLES.md` (especialmente principios #2 Agnosticismo y #9 Separation of Concerns)

---

## 1. Resumen ejecutivo

- **Objetivo**: 0 strings catalanes residuales, 0 referencias muertas, 0 archivos huérfanos, 0 docs obsoletos en infraestructura activa (`memsys3_templates/` distribuible + `memsys3/` dogfooting).
- **Hits accionables totales**: 22 (17 detectados por forks iniciales + 5 hallados en validación post-edits).
- **Resueltos directos**: 22 (100% — todos en scope, sin escalación a ISSUEs nuevos).
- **ISSUEs cerrados**: ISSUE-026 (deploy.md DevAgent), IMPROVEMENT-006 (depuración terminológica completa).
- **ADRs nuevas**: 0 (limpieza pura, ninguna decisión arquitectónica emergió).
- **Archivos huérfanos**: 0.
- **Docs obsoletos por antigüedad**: 0.

## 2. Metodología

3 forks read-only `Agent` tipo Explore en paralelo:
- **Fork A**: catalán residual (`[àèéíòóúïü]` + palabras catalanas distintivas) + DevAI/DevAgent/Development Agent.
- **Fork B**: referencias muertas a `viz/` y `mind.md`, archivos huérfanos (`.md` no referenciados).
- **Fork C**: docs antiguos (`mtime >60 días`), artefactos extra en raíz, verificación scaffold post-Frente 4.

Síntesis en sesión principal. Discriminación explícita de falsos positivos (acentos en español válido, refs históricas legítimas en `memory/full/`, `memory/history/`, `docs/archivo/`, `docs/meets/`, `backlog/`). Validación post-edits con greps exhaustivos sobre infraestructura activa — destapó 5 hits adicionales no cubiertos por los forks (drift en `agents/context-agent.yaml` dogfooting + UPDATE.md viz/refs masivas).

## 3. Tabla maestra de hallazgos

| Categoría | Hits | Resueltos | A ISSUE | Falsos+ |
|---|---:|---:|---:|---:|
| Catalán residual | 2 (extendido a 9 al ver bloque YAML completo) | 9 | 0 | 50+ acentos en español |
| DevAgent/DevAI/Development Agent | 12 | 12 | 0 | refs en data files compilados |
| Refs muertas viz/ y mind.md | 12 | 12 | 0 | refs en `memory/full/`, `meets/`, `backlog/ISSUE-009` |
| Archivos huérfanos `.md` | 0 | — | — | — |
| Docs obsoletos por antigüedad | 0 | — | — | — |
| **Total** | **33** | **33** | **0** | — |

## 4. Detalle por categoría

### 4.1 Catalán residual

**Hits (9 — bloque YAML ejemplo en `memory/README.md`)**:

| Archivo | Líneas | Strings catalanes | Acción |
|---|---|---|---|
| `memsys3_templates/memory/README.md` | 219-226 | `titol`, `features_implementades`, `nom`, `descripcio`, `decisions_preses`, `decisio`, `justificacio` + valores ("Sistema d'Exportació", "Text real amb...", "Millor qualitat de text") | Bloque traducido a español íntegro |
| `memsys3/memory/README.md` | 217-224 | (idéntico, sync dogfooting) | Bloque traducido a español íntegro |

Fork A flaggeó solo `descripcio:` (regex específica). Inspección visual del entorno reveló que el YAML ejemplo entero estaba en catalán — extendido en scope (sigue siendo "Catalán residual" del Bloque A).

**Falsos positivos descartados**: Acentos `é/í/ó/ú/ñ` en palabras españolas válidas (decisión, información, próximo, guía, año), `aquí` (español), `qué/cualquier/sí/son/sus` (homógrafos español-catalán pero contexto inequívocamente español).

### 4.2 Terminología obsoleta DevAgent/DevAI/Development Agent (ADR-015)

**Hits resueltos (12)**:

Distribuible (`memsys3_templates/`):
- `prompts/deploy.md:3` — `Tu (DevAgent)` → `Tu (Main Agent)`
- `prompts/endSession.md:3` — `Tu (DevAgent)` → `Tu (Main Agent)`
- `prompts/endSession.md:7` — `próximo DevAgent` → `próximo Main Agent`
- `prompts/compile-context.md:299` — `los DevAgents` → `el Main Agent`

README raíz:
- `README.md:127` — `Humans/DevAI` → `Humans/Main Agent`
- `README.md:138` — `Desarrollar (DevAI)` → `Desarrollar (Main Agent)`

Dogfooting (`memsys3/`):
- `prompts/deploy.md:3`, `prompts/endSession.md:3,7`, `prompts/compile-context.md:299` — sync templates
- `agents/context-agent.yaml:4` — `descripcion: ... optimizado para DevAI` → `optimizado para Main Agent` (drift dogfooting; templates ya estaba correcto)
- `agents/context-agent.yaml:183` — `Asegurar que DevAI pueda entender` → `Asegurar que Main Agent pueda entender` (idem drift)

**Hits NO modificados (legítimos)**: refs en `memsys3/memory/context.yaml` y `memory/full/sessions*.yaml` (data files compilados/históricos — auto-regenerables o inmutables). Documentan ADR-015, ISSUE-026, side-findings — son audit trail, no infraestructura.

### 4.3 Referencias muertas viz/ y mind.md

viz/ archivada a `memsys3/docs/archivo/viz/` (Frente histórico, ADR-009 derivada). mind.md eliminado. Toda referencia a estas rutas en infraestructura activa apunta a archivos inexistentes.

**Hits resueltos (12)**:

`memsys3/docs/DEVELOPMENT.md`:
- L95 — `├── viz/                          # Agnóstico (todo se copia)` — eliminada
- L145 — `├── viz/                          # Copiado tal cual` — eliminada
- L316-317 — entry "5. memsys3_templates/prompts/mind.md" + comando `cd memsys3/viz && python3 serve.py` — bloque eliminado

`memsys3/prompts-dev/actualizar_cat.md`:
- L101 — `prompts/mind.md` en lista "Prompts (9 archivos)" → quitada + count `9 → 8`
- L116-119 — sección entera "Visualizador (3 archivos)" + entradas viz/index.html, viewer.js, README.md → eliminada
- L121 — sección "READMEs" renumerada `5 → 4`
- L250 — `viz/*` en mensaje commit ejemplo → eliminada

`memsys3/docs/UPDATE.md` (no detectado por Fork B, hallado en re-validación):
- L17 — checklist `(viz/, templates/, prompts/, agents/)` → `(templates/, prompts/, agents/)`
- L37-40 — bloque "Visualizador (viz/)" con cp → eliminado
- L107-108 — comentario `# Visualizador` + cp → eliminados
- L132-141 — Paso 5 "Verificar" rebajado: quitado `python3 serve.py` del visualizador, queda solo verificación de contexto
- L154-160 — sección "Nueva Funcionalidad en Visualizador" → eliminada entera
- L172-180 — troubleshooting "El visualizador no carga" → eliminado entero
- L196 — checklist "Actualizar visualizador (`viz/`)" → eliminada
- L202 — checklist "Verificar visualizador funciona" → eliminada

**Hits NO modificados (legítimos)**:
- `memsys3/backlog/ISSUE-009-*.md` — comandos de ejemplo en ISSUE histórico (decisión usuario).
- `memsys3/memory/full/sessions*.yaml` — bitácoras inmutables.
- `memsys3/docs/meets/20260308_1.md`, `20260322_1.md` — transcripciones de reuniones (histórico documental).
- `memsys3/memory/project-status.yaml` y `memory/context.yaml` — datos vivos que mencionan "viz: archivado" (legítimo estado documental).

### 4.4 Archivos huérfanos

**Resultado: 0**. Verificación cruzada con grep en READMEs, PRINCIPLES, prompts y backlog. Los `.md` canónicos (`README.md`, `PRINCIPLES.md`) y top-level prompts no requieren refs externas. `prompts-dev/actualizar_cat.md` está referenciado en `FEATURE-008-multilenguaje.md`. `prompts-dev/comprobar_alineamiento.md` referenciado en `informe_BLUEPRINT-001.md`.

### 4.5 Docs obsoletos por antigüedad

**Resultado: 0**. Todos los `.md`/`.yaml` en `memsys3/docs/`, `memsys3_templates/`, raíz tienen `mtime` reciente (mayo 2026). Frente 4 (2026-05-07) refrescó la mayoría. No hay docs huérfanos por edad+desalineación.

### 4.6 Artefactos extra en raíz (decisión usuario: no tocar)

Detectados untracked: `agent4_prompt_frente4.txt`, `agent5_prompt_frente5.txt`, `multi_work.md`, `blocked_files_log.md`. Decisión confirmada en sesión: **temporales de orquestación, dejar como están**. NO se añaden a `.gitignore` (decisión explícita "no hacer nada").

### 4.7 Verificación scaffold (Frente 4 post-condición)

- ✅ `memsys3_templates/memory/templates/operations-template.log` existe.
- ✅ `memsys3_templates/backlog/IMPROVEMENT-008-*.md` ausente (leak eliminado en Frente 3).

## 5. Validación final

Greps post-edits sobre infraestructura activa (excluyendo data files compilados, históricos, archivo, meets, backlog):

```bash
# Catalán residual
grep -rnE 'descripcio:|titol:|features_implementades:|decisions_preses:|decisio:|justificacio:' \
  memsys3_templates/ memsys3/prompts/ memsys3/agents/ memsys3/memory/templates/ \
  memsys3/memory/README.md README.md PRINCIPLES.md
# → 0 hits

# DevAgent/DevAI residual
grep -rniE 'DevAI|DevAgent|Development Agent' \
  memsys3_templates/ memsys3/prompts/ memsys3/prompts-dev/ memsys3/agents/ \
  memsys3/memory/templates/ memsys3/memory/README.md \
  memsys3/docs/DEVELOPMENT.md memsys3/docs/UPDATE.md README.md PRINCIPLES.md
# → 0 hits

# viz/mind.md activos
grep -rnE '\bviz/|\bmind\.md|memsys3/viz' \
  memsys3_templates/ memsys3/prompts/ memsys3/prompts-dev/ memsys3/agents/ \
  memsys3/memory/templates/ memsys3/memory/README.md \
  memsys3/docs/DEVELOPMENT.md memsys3/docs/UPDATE.md README.md PRINCIPLES.md
# → 0 hits
```

## 6. Cierre

- BLUEPRINT-001 Frente 5 [x] — completado.
- ISSUE-026 cerrado (criterio cumplido: `grep DevAgent\|DevAI` sobre infraestructura distribuible y dogfooting → 0 hits).
- IMPROVEMENT-006 cerrado (criterio cumplido: 0 resultados de "Development Agent"/"DevAI" en infraestructura activa).
- Pendiente prioritario en `project-status.yaml` actualizado — siguiente milestone: Frente 6 (Estrategia dogfooting revisada).

## 7. Observaciones meta

1. **Cobertura de forks**: 5/22 hits no fueron detectados por los 3 forks iniciales (drift dogfooting `agents/context-agent.yaml` + refs viz/ masivas en `UPDATE.md`). Lección: para auditorías de residualidad incluir explícitamente `agents/` y `docs/UPDATE.md` en el ámbito de cada fork. Anclaje futuro: contemplar regla en `memory.yaml` feedback si se repite el patrón.

2. **Discriminación de falsos positivos**: el regex `[àèéíòóúïü]` produce 50+ falsos positivos por acentos en español válido. Útil para cribado inicial, pero requiere segunda pasada con palabras catalanas distintivas (`això|aquesta|amb|tasca|...`) y discriminación visual.

3. **No hubo decisiones arquitectónicas emergentes**: toda la limpieza es trazable a ADR-009 (viz archivado), ADR-015 (Main Agent terminology), erradicación catalán histórica (sesión 2026-04-15). No requiere ADR-025.

4. **Side-finding fuera de scope (NO accionado)**: ISSUE-025 (link roto `docs/UPDATE.md` en `README.md:217`) sigue abierto. No se resuelve en Frente 5 (es una corrección de ruta en README, scope del Frente 8 — Comunicación). Mantener pendiente.
