# ISSUE-023: Desalineación schema project-status.yaml — fugas dog-fooding en archivos legacy operativos

**Estado:** Completado
**Prioridad:** Media
**Tipo:** Issue
**Plazo:** Resuelto en sesión 2026-05-06
**Fecha identificación:** 2026-05-05
**Origen:** Reporte de agente CLIENT_D (proyecto externo) en `docs/reports/2026-05-05_endSession_schema_desalineado.md`

---

## Problema

Agente externo (CLIENT_D) detectó que su `project-status.yaml` tras deployment tenía schema mezclado con catalán residual (`visio_general`, `estat_actual`, `decisions_clau`, `historic_sessions`) que no coincidía con el schema asumido por `endSession.md` ni el template canónico.

### Investigación

Verificado en `master`:
- ✅ Dog-fooding `memsys3/memory/project-status.yaml` — schema castellano correcto.
- ✅ Template canónico `memsys3_templates/memory/templates/project-status-template.yaml` — schema castellano correcto.
- ❌ Archivos operativos en `memsys3_templates/memory/` (`project-status.yaml`, `context.yaml`, `full/adr.yaml`, `full/sessions.yaml`) — snapshots congelados del propio dog-fooding memsys3 con catalán residual desde v1.3 (último cambio significativo 2025-11-03).

### Diagnóstico

Los archivos operativos en `memsys3_templates/memory/` eran fugas **dog-fooding → producto distribuible**:
- Probable residuo de cuando solo existía `memsys3_templates/` (antes de separar dog-fooding en `memsys3/`).
- Deploy actual usa los `templates/X-template.yaml` como schema canónico, no estos archivos.
- Por eso en proyectos nuevos no aparecía el problema, pero deployments antiguos (como el de CLIENT_D) tenían el snapshot legacy incrustado.

---

## Resolución

Aplicada en sesión 2026-05-06.

### Limpieza
Vaciados los 4 archivos operativos legacy a **scaffold puro Modelo D** (estructura mínima vacía, sin placeholders, sin referencias a otros archivos, con cabecera `# version: 0.1.0`):
- `memsys3_templates/memory/project-status.yaml`
- `memsys3_templates/memory/context.yaml`
- `memsys3_templates/memory/full/adr.yaml`
- `memsys3_templates/memory/full/sessions.yaml`

`memsys3_templates/memory/full/operations.log` deliberadamente NO tocado (sin template equivalente; queda como caso del plan paralelo de auditoría).

### ADRs documentando el modelo de mantenimiento

Tres ADRs creadas en `memsys3/memory/full/adr.yaml`:

- **ADR-017** — Sistema `file_version` por archivo (versionado independiente de infraestructura).
- **ADR-018** — Sustitución diferencial de templates de schema en `actualizar.md`. Alcance acotado a `memory/templates/`. Reconoce que `prompts/` y `agents/` son personalizables, no inmutables.
- **ADR-019** — Política de evolución de schema (deprecation contextualizada por agente del proyecto). upstream propone, agente contextualizado evalúa, usuario decide. Nunca impone.

### Lógica nueva en actualizar.md

Paso 6.4 reescrito para implementar sustitución diferencial (comparación file_version + AskUserQuestion en estado anómalo).
Nuevo Paso 6.4.5 (modo Extendido) para detección contextualizada de campos deprecated y huérfanos.

`file_version` de `actualizar.md` bumpeado de `0.1.0` → `0.2.0`.

---

## Comunicación a CLIENT_D

> Tu deployment necesita `/actualizar-memsys3`. El catalán residual es residuo histórico ya corregido en master desde 2026-05-06. Tras actualizar, los archivos operativos quedarán como scaffold limpio y los datos vivos del proyecto se preservarán intactos. Si tu `project-status.yaml` tiene claves catalanas, considéralas legacy: el schema canónico vive en `memsys3/memory/templates/project-status-template.yaml`.

---

## Aprendizajes

- Los **archivos operativos en `memsys3_templates/memory/`** que duplican el dog-fooding deben mantenerse como scaffold vacío, no como ejemplos pre-rellenados (riesgo de fuga).
- El **template canónico vive en `templates/`**; el operativo en `memory/` es punto de partida vacío.
- **Personalización legítima existe** en proyectos no-software (libro, marketing, dirección): la palabra "inmutable" no aplica a `prompts/` y `agents/`, solo a `memory/templates/`.
- **upstream no decide solo**: el agente contextualizado en el proyecto tiene la última palabra sobre qué campos siguen siendo útiles para ESE proyecto.

---

## Plan paralelo (futuro, no abordado aquí)

- ADR sobre completitud del scaffold en deploy (todo archivo distribuible debería tener template equivalente; `operations.log` es ejemplo de archivo sin template).
- ADR sobre estrategia de actualización para `prompts/` y `agents/` personalizables (precedente: ISSUE-018 WORKSPACE_Y con `*.dev.md`).
- Auditoría de archivos sin template: `operations.log`, `backlog/`, `docs/`.
