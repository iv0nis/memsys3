<!-- version: 0.1.0 -->

# Informe de auditoría: BLUEPRINT-001 Frente 2 — ADRs vs código real

**Item:** [`../BLUEPRINT-001-release-memsys3-v1.md`](../BLUEPRINT-001-release-memsys3-v1.md)
**Informe principal:** [`informe_BLUEPRINT-001.md`](informe_BLUEPRINT-001.md)
**Plan:** [`plan_BLUEPRINT-001.md`](plan_BLUEPRINT-001.md)
**Fecha auditoría:** 2026-05-07
**Sesión:** 2026-05-07 (Frente 2)
**Vara de medir:** `memsys3/PRINCIPLES.md` (10 principios sistémicos)

---

## 1. Resumen ejecutivo

- **ADRs aceptadas auditadas**: 20 (no 22 como decía el blueprint inicial — ver meta-finding §6).
- **Cumplimiento global**: 18/20 (90%). 2 brechas accionables + 1 observación + 1 brecha ya cubierta por Frente 3.
- **Severidad máxima**: media. Ninguna brecha bloquea release v1.0.
- **ISSUEs creados**: ISSUE-024 (meta), ISSUE-025 (ADR-007), ISSUE-026 (ADR-015).
- **Brecha ADR-021 (leak IMPROVEMENT-008)**: ya identificada en informe principal §3.3, será resuelta por Frente 3 (scaffold completo). NO se crea ISSUE separado para evitar duplicación.

## 2. Metodología

Auditoría exhaustiva con 3 forks read-only (`Agent` tipo Explore) en paralelo, cada uno con un bloque:

- **Fork A**: ADRs 001-009 (filosofía CA, rotación, contingencia, deploy/rutas/READMEs/templates).
- **Fork B**: ADRs 012-016 (README directo, gestión ADRs, commands, terminología, agnosticismo).
- **Fork C**: ADRs 017-022 (file_version, sustitución diferencial, deprecation, memory.yaml, backlog docs, PRINCIPLES.md).

Cada fork verificó AMBOS sitios (`memsys3_templates/` distribuible + `memsys3/` dogfooting) cuando aplicaba. Síntesis en sesión principal.

Esta orquestación se documentó en `memory.yaml` feedback ("Heurística de orquestación de forks") en sesión 2026-05-07 — auditoría es caso de uso paradigmático: lectura masiva sin diseño.

## 3. Tabla maestra de cumplimiento

| ADR | Título | Estado | Principle anchor |
|-----|--------|--------|------------------|
| 001 | Criterio inteligente CA vs límites arbitrarios | ✅ Cumplida | #5 |
| 002 | Rotación automática 1800-2000 líneas | ✅ Cumplida | #8 + #5 |
| 003 | Plan contingencia >150K → history/ | ✅ Cumplida | #8 + #1 |
| 004 | YAML para todo | ✅ Cumplida | #2 |
| 005 | deploy.md como prompt | ✅ Cumplida | #4 |
| 006 | Rutas unificadas memsys3/ | ✅ Cumplida | #3 + #2 |
| 007 | Separación meta-niveles READMEs | ⚠️ **Brecha** | #9 |
| 008 | Main Agent NO compila | ✅ Cumplida | #4 + #1 |
| 009 | Templates permanentes + gotchas en sessions | ✅ Cumplida | #6 + #8 |
| 010 | — | ❌ AUSENTE | n/a |
| 011 | — | ❌ AUSENTE | n/a |
| 012 | README lectura directa | ✅ Cumplida | #9 |
| 013 | Sistema gestión ADRs | ✅ Cumplida | #1 |
| 014 | Comandos globales launcher | ✅ Cumplida | #2 |
| 015 | Terminología "Main Agent" | ⚠️ **Brecha** | #9 |
| 016 | Agnosticismo + commands opcional | ✅ Cumplida (con observación) | #2 |
| 017 | file_version inmutable | ✅ Cumplida | #7 |
| 018 | Sustitución diferencial templates | ✅ Cumplida | #9 + #6 |
| 019 | Deprecation contextualizada | ✅ Cumplida | #4 + #5 |
| 020 | memory.yaml + bridge MEMORY.md | ✅ Cumplida | #1 + #2 + #3 |
| 021 | Backlog docs informe/plan | ⚠️ Cumplida con leak (ya en Frente 3) | #1 + #9 |
| 022 | PRINCIPLES.md canónico | ✅ Cumplida | #1 + meta |

## 4. Brechas detalladas (accionables)

### 4.1 ADR-007 — DEVELOPMENT.md y UPDATE.md ausentes en raíz repo

- **Esperado** (ADR-007 decisión): `docs/DEVELOPMENT.md` (audiencia: contribuidores) y `docs/UPDATE.md` (audiencia: quien actualiza memsys3) deben existir.
- **Encontrado**:
  - `README.md:217` referencia `docs/UPDATE.md` → link roto (raíz `docs/` solo tiene `comunidad/`, `reports/`).
  - Ambos archivos existen en `memsys3/docs/` (dogfooting) pero NO en raíz repo ni en scaffold distribuible.
- **Discusión**: el fork A propuso copiarlos a `memsys3_templates/docs/`, pero el ADR los define para audiencias **del repo**, no del scaffold desplegado (un usuario desplegado no contribuye al desarrollo upstream). El lugar correcto es **raíz repo** (`docs/DEVELOPMENT.md`, `docs/UPDATE.md`).
- **Severidad**: Media (link roto público en README.md).
- **ISSUE**: `ISSUE-025`.

### 4.2 ADR-015 — `deploy.md:3` usa "DevAgent" en lugar de "Main Agent"

- **Archivo**: `memsys3_templates/prompts/deploy.md:3`
- **Esperado** (ADR-015): "Main Agent" como nomenclatura única.
- **Encontrado**: `Tu (DevAgent) debes configurar memsys3...`
- **Severidad**: Media (inconsistencia terminológica, fix trivial: 1 línea).
- **ISSUE**: `ISSUE-026`.

### 4.3 ADR-021 — Leak `IMPROVEMENT-008-*.md` en `memsys3_templates/backlog/`

- **Archivo**: `memsys3_templates/backlog/IMPROVEMENT-008-deploy-agnostico-memoria-antes-agente.md`
- **Esperado**: scaffold distribuible solo contiene `README.md` + `docs/.gitkeep`.
- **Encontrado**: archivo de dogfooting filtrado al template.
- **Severidad**: Baja.
- **Acción**: NO se crea ISSUE separado. Esta brecha ya está identificada en `informe_BLUEPRINT-001.md §3.3` y será resuelta por **Frente 3** (Scaffold completo en deploy). Anotada aquí para trazabilidad.

## 5. Observaciones (no accionables, registro)

### 5.1 ADR-016 — README sin mención explícita de la jerarquía agnóstica

- **Estado**: Cumplida. El README menciona agnosticismo (L12: "funciona con cualquier modelo de IA") y `PRINCIPLES.md` lo formaliza completamente como Principio #2.
- **Observación del fork B**: el README no destaca explícitamente la jerarquía `templates → prompts → commands` (fuente de verdad).
- **Decisión**: NO se crea ISSUE. Tras Frente 1 (PRINCIPLES.md publicado), la jerarquía está formalmente documentada. El README puede mejorarse en Frente 8 (comunicación) si se quiere reforzar el mensaje, pero no es brecha de ADR.

## 6. Meta-finding: ADRs 010-011 ausentes

- **Hallazgo**: el índice de `memsys3/memory/full/adr.yaml` lista 20 ADRs aceptadas (001-009 + 012-022). Los IDs **010 y 011 no existen** en ningún archivo del repo (verificado en `adr.yaml`, `sessions*.yaml`, no hay `adr_1.yaml`).
- **Causa probable**: skipped al numerar (descartadas durante drafting o IDs reservados que nunca se llenaron). No hay registro histórico.
- **Impacto**: el blueprint y el informe principal hablaban de "21" o "22 ADRs" — eran proyecciones erróneas. Conteo real: 20 ADRs aceptadas.
- **ISSUE**: `ISSUE-024` (deuda histórica, prioridad baja). Deja huella para investigación futura.

## 7. Anclaje a PRINCIPLES.md (verificación cruzada)

Cada ADR auditada se ancla a uno o más principios canónicos:

- **#1 Anti-CDC**: ADRs 003, 008, 013, 020, 021, 022.
- **#2 Agnosticismo**: ADRs 004, 006, 014, 016, 020.
- **#3 Una sola carpeta**: ADRs 006, 020.
- **#4 Human-in-the-loop**: ADRs 005, 008, 019.
- **#5 Criterio inteligente vs límites**: ADRs 001, 002, 019.
- **#6 Templates como documentación activa**: ADRs 009, 018.
- **#7 file_version inmutable**: ADR 017.
- **#8 Datos preservados**: ADRs 002, 003, 009.
- **#9 Separation of Concerns**: ADRs 007, 012, 015, 018, 021.
- **#10 Restricciones infraestructura**: ADR 017 (incluido implícitamente).

**Conclusión**: los 10 principios tienen al menos 1 ADR de respaldo. PRINCIPLES.md es coherente con el corpus ADR — la articulación de Frente 1 fue correcta.

## 8. Decisión sobre Frente 2

- **Frente 2 cierra como completado.**
- 0 brechas críticas. 2 ISSUEs accionables (medios) + 1 ISSUE meta (bajo). 1 brecha conocida cubierta por Frente 3.
- **Siguiente milestone**: Frente 3 (Scaffold completo en deploy). Resuelve la brecha ADR-021 leak entre otros.

## 9. Referencias

- ADRs origen: ver índice en `memsys3/memory/full/adr.yaml`.
- Forks transcripts: efímeros (no persistidos por diseño anti-contexto-bloat).
- ISSUEs creados: `ISSUE-024`, `ISSUE-025`, `ISSUE-026`.
- Principios canónicos: `memsys3/PRINCIPLES.md`.
