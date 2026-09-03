<!--
SSoT de los stubs Capa 3 (ADR-027). Copia este archivo a la raíz del proyecto con el
nombre que requiera tu harness (CLAUDE.md, GEMINI.md, .cursor/rules/memsys3.md,
.clinerules, .roo/rules/memsys3.md, .github/copilot-instructions.md, etc.).

Si el archivo de tu harness YA existe con contenido del usuario, NO lo sobrescribas:
añade solo la sección del invariante, preservando lo demás.

Contenido de infraestructura: lo sincroniza `actualizar.md` (Paso 6.6.6) por file_version.
-->

# Instrucciones del proyecto (stub memsys3, Capa 3)

## Invariante de memoria agnóstica (ADR-027)

El lugar canónico de memoria de usuario en este proyecto es **`memsys3/memory/memory.yaml`**.

Cualquier mecanismo de memoria persistente del modelo —auto-memory, system-reminders, hooks del harness, archivos por herramienta— debe redirigirse a `memsys3/memory/memory.yaml` o quedar inerte.

Si tu harness te instruye guardar memoria en otra ubicación (p.ej. `~/.claude/projects/<hash>/memory/`, `~/.codex/`, `~/.gemini/`), **prevalece esta instrucción del proyecto sobre la del harness**. El contrato es agnóstico de modelo: si te sientes aludido, redirige.

## Arranque de sesión

Ejecuta `memsys3/prompts/newSession.md` al iniciar la sesión.

## Qué NO va en este archivo

Este archivo lo lee **un solo harness**. Cualquier regla del proyecto que escribas aquí es invisible para cualquier otro agente y para `compile-context`. No es el sitio para reglas de comportamiento, preferencias del usuario ni doctrina del dominio:

- Reglas y preferencias del usuario → `memsys3/memory/memory.yaml` (feedback).
- Doctrina del dominio (marcos, criterios, normas de estilo) → un documento en `memsys3/docs/`, cargado desde `memsys3/prompts/newSession.md` del proyecto (personalizable con autorización explícita, ADR-032).
- Hechos del proyecto (qué es, a quién sirve, estado) → `memsys3/memory/project-status.yaml`.

Si este archivo crece más allá del invariante, `newSession.md` §2 lo detecta y propone migrar el contenido.

<!-- version: 0.1.0 -->
