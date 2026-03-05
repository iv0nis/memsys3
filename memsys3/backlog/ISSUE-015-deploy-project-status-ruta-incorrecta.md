# ISSUE-015: deploy.md crea project-status.yaml en ruta incorrecta

**Estado:** Abierto
**Prioridad:** Media
**Tipo:** Bug
**Fecha identificación:** 2026-03-05

---

## Problema / Necesidad

Durante el deployment inicial de memsys3, el agente crea `project-status.yaml` en `memsys3/memory/full/` en lugar de `memsys3/memory/` (raíz de memory).

La ubicación correcta según el Paso 5 de `deploy.md` es `memsys3/memory/project-status.yaml`, y así lo referencia también `compile-context.md`. Sin embargo, el agente lo coloca en `memsys3/memory/full/project-status.yaml`.

## Causa Raíz

El Paso 2 de `deploy.md` establece el patrón `memory/full/` creando `adr.yaml` y `sessions.yaml`. El Paso 5, que sigue inmediatamente, pide crear `project-status.yaml`. El agente, con el patrón `memsys3/memory/full/` activo en su contexto, extrapola incorrectamente que `project-status.yaml` también debe ir en `full/`.

El path correcto (`memsys3/memory/project-status.yaml`) aparece solo una vez en prosa antes del bloque YAML, sin ninguna advertencia que refuerce la distinción.

## Impacto

- `project-status.yaml` queda en `memsys3/memory/full/project-status.yaml`
- `compile-context.md` referencia `memsys3/memory/project-status.yaml` → el Context Agent no lo encuentra en compilaciones posteriores
- Requiere corrección manual por parte del usuario

## Reproducibilidad

Probable en cualquier LLM. El patrón `memory/full/` queda muy presente en el contexto tras el Paso 2 y el Paso 5 no refuerza visualmente la distinción de rutas.

## Fix Aplicado

Añadido warning explícito en el Paso 5 de `memsys3_templates/prompts/deploy.md`:

```markdown
> ⚠️ IMPORTANTE: Este archivo va en `memsys3/memory/` (raíz de memory),
> NO en `memsys3/memory/full/` como `adr.yaml` y `sessions.yaml`.
```

## Referencias

- Bug report original: `bug-report-memsys3-project-status-location.md`
- Archivo afectado: `memsys3_templates/prompts/deploy.md` (Paso 5)
- Reportado tras deployment en proyecto MapGat con Claude Sonnet 4.6
