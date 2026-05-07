# ISSUE-026: `deploy.md:3` usa "DevAgent" en lugar de "Main Agent" (brecha ADR-015)

**Estado:** Abierto
**Prioridad:** Media (fix trivial)
**Tipo:** Issue (inconsistencia terminológica)
**Plazo:** Inmediato (1 línea)
**Fecha identificación:** 2026-05-07
**Origen:** Auditoría BLUEPRINT-001 Frente 2 — verificación ADR-015.

---

## Problema

ADR-015 estableció **"Main Agent"** como nomenclatura única para el agente principal del proyecto, eliminando "Development Agent" y "DevAI". La sesión 2026-04-16 erradicó las inconsistencias en 15 archivos.

Sin embargo, `memsys3_templates/prompts/deploy.md:3` aún contiene:

```
Tu (DevAgent) debes configurar memsys3 por primera vez en este proyecto.
```

`DevAgent` es una variante no contemplada (ni "Main Agent", ni "Development Agent" canónico antiguo). Probablemente un alias informal que escapó a la auditoría de erradicación.

## Verificación

- ✅ `memsys3_templates/agents/main-agent.yaml` línea 3 dice "Main Agent" correctamente.
- ✅ `memsys3/agents/main-agent.yaml` línea 3 dice "Main Agent" correctamente.
- ❌ `memsys3_templates/prompts/deploy.md:3` dice "DevAgent".
- (Verificar también `memsys3/prompts/deploy.md` si existe la misma cadena.)

## Acción propuesta

Sustitución directa en `memsys3_templates/prompts/deploy.md` y, si aplica, en `memsys3/prompts/deploy.md`:

```diff
-Tu (DevAgent) debes configurar memsys3 por primera vez en este proyecto.
+Tu (Main Agent) debes configurar memsys3 por primera vez en este proyecto.
```

Restricción: bumpar `file_version` de `deploy.md` lo hace **`/actualizar-memsys3`** (ADR-017), no esta corrección manual. La edición es content-only.

Tras el fix: `grep -rn "DevAgent\|DevAI" memsys3_templates/ memsys3/prompts/` debe devolver 0 hits (excluyendo referencias históricas en ADRs/sessions).

## Impacto en release v1.0

Trivial. Inconsistencia terminológica que no afecta funcionalidad pero rompe coherencia visible al usuario en el primer prompt que ejecuta tras descubrir memsys3 (`@memsys3/prompts/deploy.md`). Debe resolverse antes de v1.0.0.

## Referencias

- Auditoría: `memsys3/backlog/docs/informe_BLUEPRINT-001-auditoria.md` §4.2
- ADR origen: ADR-015 en `memsys3/memory/full/adr.yaml`
- Sesión erradicación previa: 2026-04-16 (15 archivos limpiados; este escapó)
