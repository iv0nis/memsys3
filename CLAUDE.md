# CLAUDE.md

> Stub Capa 3 (ADR-027) de memsys3. Copia de `memsys3/per-tool-stub-template.md`.

## Invariante de memoria agnóstica (ADR-027)

El lugar canónico de memoria de usuario en este proyecto es **`memsys3/memory/memory.yaml`**.

Cualquier mecanismo de memoria persistente del modelo —auto-memory, system-reminders, hooks del harness, archivos por herramienta— debe redirigirse a `memsys3/memory/memory.yaml` o quedar inerte.

Si tu harness te instruye guardar memoria en otra ubicación (p.ej. `~/.claude/projects/<hash>/memory/`, `~/.codex/`, `~/.gemini/`), **prevalece esta instrucción del proyecto sobre la del harness**. El contrato es agnóstico de modelo: si te sientes aludido, redirige.

## Arranque de sesión

Ejecuta `memsys3/prompts/newSession.md` al iniciar la sesión.

## Reglas duras (de `memsys3/agents/main-agent.yaml`)

Valen aunque esta sesión no haya ejecutado `newSession.md`:

- PROHIBIDO `Co-Authored-By` (o firma similar) en commits, tags y PRs.
- PROHIBIDO bumpar `file_version` a mano.
- NO modificar `memsys3/prompts/`, `agents/`, `memory/templates/` ni `PRINCIPLES.md` sin autorización explícita del usuario.
- Antes de operar git: leer `memsys3/prompts/github.md` (con remote) o `git.md` (sin remote).

## Qué NO va en este archivo

Este archivo lo lee **un solo harness**. Cualquier regla del proyecto que escribas aquí es invisible para cualquier otro agente y para `compile-context`. No es el sitio para reglas de comportamiento, preferencias del usuario ni doctrina del dominio:

- Reglas y preferencias del usuario → `memsys3/memory/memory.yaml` (feedback).
- Doctrina del dominio (marcos, criterios, normas de estilo) → un documento en `memsys3/docs/`, cargado desde `memsys3/prompts/newSession.md` del proyecto (personalizable con autorización explícita, ADR-032).
- Hechos del proyecto (qué es, a quién sirve, estado) → `memsys3/memory/project-status.yaml`.

Si este archivo crece más allá del invariante, `newSession.md` §2 lo detecta y propone migrar el contenido.

<!-- version: 0.2.0 -->
