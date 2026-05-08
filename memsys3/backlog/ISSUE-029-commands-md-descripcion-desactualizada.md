# ISSUE-029: commands.md menciona features pero no las nuevas (post-Frentes 1-6)

**Estado:** Abierto
**Prioridad:** Baja
**Tipo:** Documentación
**Plazo:** Antes de v1.0.0 o en Frente 8 cleanup
**Fecha identificación:** 2026-05-08
**Origen:** Smoke test BLUEPRINT-001 Frente 7

---

## Problema / Necesidad

`memsys3_templates/prompts/commands.md` (también dogfooding) genera dos comandos globales mediante heredocs:

- `/deploy-memsys3` — descripción: "Deploy memsys3 system from GitHub to current project"
- `/actualizar-memsys3` — descripción: "Update memsys3 system from GitHub in existing project"

Las notas internas del comando `/actualizar-memsys3` dicen literalmente:

> "El prompt contiene todas las instrucciones para actualización segura: detección estructura antigua, backups, copiar archivos, verificaciones, etc."

Esa descripción NO menciona las features añadidas en Frentes 1-6 del BLUEPRINT-001:

- **Sustitución diferencial templates schema** (Paso 6.4, ADR-018).
- **Deprecation contextualizada** (Paso 6.4.5, ADR-019).
- **Sincronización PRINCIPLES.md** (Paso 6.6, ADR-022).

Funcionalmente NO hay impacto: el comando es un thin launcher que ejecuta el prompt actualizar.md completo y ese prompt sí contiene la lógica nueva. Pero un usuario que lea el `.md` instalado en `~/.claude/commands/` se queda con una descripción incompleta.

## Propuesta / Opciones

### Opción A — Actualizar redacciones internas (recomendada)

Editar `memsys3_templates/prompts/commands.md` (+ dogfooding) para que la nota interna de `/actualizar-memsys3` mencione:

- "Sustitución diferencial de templates de schema según file_version (ADR-018)"
- "Sincronización de PRINCIPLES.md (ADR-022)"
- "Detección contextualizada de campos deprecated (ADR-019)"

Equivalente para `/deploy-memsys3`: mencionar PRINCIPLES.md + scaffold canónico (ADR-023).

~5 líneas por comando.

### Opción B — Diferir a Frente 8 (cleanup release)

Sin urgencia. Frente 8 actualiza README/CHANGELOG y es lugar natural para alinear todas las descripciones.

## Decisiones / Acciones

- [ ] Decidir A vs B en sesión Frente 8

## Referencias

- **Origen smoke test**: `docs/informe_BLUEPRINT-001-smoke-tests.md`
- **ADRs afectadas**: ADR-014 (launcher pattern), ADR-018, ADR-019, ADR-022, ADR-023
- **Archivos**: `memsys3/prompts/commands.md` + `memsys3_templates/prompts/commands.md`
