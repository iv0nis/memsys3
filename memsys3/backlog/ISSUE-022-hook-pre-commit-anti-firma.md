# ISSUE-022: Hook pre-commit anti-firma Co-Authored-By

**Estado:** Abierto
**Prioridad:** Media
**Tipo:** Issue
**Plazo:** Mid-term
**Fecha identificación:** 2026-04-30
**Origen:** Incident report de proyecto externo (Agent B hizo commits con Co-Authored-By: Claude pese a existir `github.md` prohibiéndolo, forzando reescritura de historia con `filter-branch` + `force-push` que puso en riesgo otros agentes paralelos)

---

## Problema

`github.md` documenta explícitamente la regla "commits SIN firma Co-Authored-By" e incluye verificación post-commit con grep. Aun así, el comportamiento por defecto del agente Claude Code es añadir la firma, y la regla se incumple cuando el agente no tiene `github.md` cargado en contexto al commitar.

La defensa actual es **documental**: depende de que el agente lea y siga `github.md`. No hay impedimento real.

### Cadena causal típica del incidente

1. Agente hace commit ignorando regla → añade `Co-Authored-By: Claude`
2. Push a remoto con firmas
3. Detección posterior → necesidad de eliminarlas → reescritura con `filter-branch`
4. `force-push` pone en riesgo a otros agentes paralelos (escenario multi-agente)

Si el paso 1 estuviera bloqueado por defensa real, el resto no ocurre.

---

## Mitigación parcial ya aplicada (2026-04-30)

Sesión 2026-04-30: añadida restricción `operaciones_git` en `main-agent.yaml` (template + dog-fooding) que obliga al agente a leer `github.md` antes de cualquier `git commit/push/tag/merge/rebase`. Bumped `file_version` 0.1.0 → 0.2.0.

**Esto reduce probabilidad pero no la elimina:** sigue siendo defensa documental. Un agente podría:
- Saltarse la lectura del prompt
- Leerlo pero ignorar la regla por hábito arraigado del modelo
- No tener cargado `main-agent.yaml` (sesión sin contexto memsys3)

Por eso este ISSUE sigue abierto: defensa real (hook) complementa la documental.

---

## Propuesta

### Hook pre-commit local en repo memsys3 dog-fooding

Crear `.githooks/pre-commit` que rechace cualquier commit con `Co-Authored-By` en el mensaje. Activar con:

```bash
git config core.hooksPath .githooks
```

**Esqueleto:**

```bash
#!/usr/bin/env bash
# .githooks/pre-commit
# Rechaza commits con Co-Authored-By (política memsys3, ver github.md)

COMMIT_MSG_FILE="${1:-$(git rev-parse --git-path COMMIT_EDITMSG)}"

if grep -qi "co-authored-by" "$COMMIT_MSG_FILE"; then
  echo "❌ ERROR: Commit contiene 'Co-Authored-By'."
  echo "   Política memsys3: commits SIN firma de agente."
  echo "   Ver memsys3/prompts/github.md sección 'Commits SIN Firma'."
  exit 1
fi

exit 0
```

Nota: el hook real es `commit-msg`, no `pre-commit` (pre-commit no recibe el mensaje). Validar al implementar.

---

## Por qué NO va en `memsys3_templates/`

Romper`ía ADR-016` (agnóstico de modelo IA). El problema "agente añade firma automática" es específico de Claude Code; otros modelos no tienen ese hábito. Meter el hook en templates impondría infraestructura git específica de Claude a todos los proyectos que desplieguen memsys3.

**Lugar correcto:** repo memsys3 dog-fooding (`/.githooks/`). Si en el futuro otros proyectos lo quieren, se documenta como **opción** en `memsys3/docs/` pero no se distribuye automáticamente.

---

## Alternativas consideradas

### A) Cargar `github.md` siempre en `newSession.md`
**Descartada:** consume tokens en cada sesión aunque no toque git. Mucho ruido para defensa que solo aplica al ~30% de sesiones.

### B) Restricción condicional en `main-agent.yaml` (✅ aplicada)
Defensa documental, eficiente en tokens, agnóstica. Ya implementada en sesión 2026-04-30. Reduce probabilidad pero no garantiza cumplimiento.

### C) Hook local en repo memsys3 (este ISSUE)
Defensa real. Específica de este repo, no se distribuye. Complementa B.

### D) Hook distribuido en templates
Descartada por romper ADR-016.

---

## TODO

- Validar si el hook correcto es `commit-msg` (recibe ruta del mensaje) o `pre-commit` (no la recibe)
- Decidir si el hook se versiona en el repo (recomendado: sí, en `.githooks/`)
- Documentar activación en `README.md` del repo o en `memsys3/docs/` como guía opcional para otros proyectos
- Considerar si extender el hook a otras reglas de `github.md` (ej: detectar versiones inconsistentes)
- Evaluar si añadir hook análogo en plantilla `deploy.md` como **opción** que el usuario active manualmente

---

## Referencias

- **Prompt afectado:** `memsys3/prompts/github.md` (regla "Commits SIN Firma", líneas 16-23)
- **Cambio relacionado:** `main-agent.yaml` v0.2.0 (restricción `operaciones_git`, sesión 2026-04-30)
- **ADR relacionado:** ADR-016 (agnóstico de modelo IA → no distribuir el hook)
- **Gotcha relacionado:** `habitos_arraigados_llm` (context.yaml, criticidad alta)
