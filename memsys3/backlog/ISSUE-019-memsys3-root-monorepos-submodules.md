# ISSUE-019 - Identificar memsys3 correcto en monorepos/submodules

**Estado**: Resuelto
**Prioridad**: Alta
**Tipo**: Bug
**Fecha**: 2026-03-22

## Problema

En proyectos con múltiples instancias de memsys3 (monorepos, submodules, workspaces), el agente puede operar en el memsys3 equivocado. Los prompts usan paths relativos (`memsys3/...`) sin verificar cuál es el memsys3 correcto para la sesión.

## Evidencia

- Detectado en gitkigai: monorepo con 4+ directorios memsys3 (raíz, gitkigai_system, unin, neuroMaquina)
- El agente confunde el memsys3 de la raíz con el de un subproyecto durante sesiones largas
- Bug silencioso: todo funciona, pero en el lugar equivocado

## Causa raíz

Los prompts operativos (endSession, actualizar, compile-context) no tienen mecanismo para identificar cuál memsys3 es "el suyo" en contextos con múltiples instancias.

## Solución implementada

1. **Nuevo Paso 0 estándar en todos los prompts operativos**: Bloque que detecta `MEMSYS3_ROOT` via `$(pwd)/memsys3`, con fallback `find` inteligente si no existe, y pregunta al usuario si hay múltiples candidatos.
2. **Refactor `$MEMSYS3_ROOT`**: Todos los paths internos de actualizar.md usan `$MEMSYS3_ROOT` en vez de `memsys3/` relativo.
3. **Duplicar bloque en cada prompt** (opción A, sin archivo _common.md compartido).

## Prompts afectados

- `actualizar.md` (refactor completo Paso 0a + todos los bloques bash)
- `endSession.md` (reescrito Paso 0)
- `compile-context.md` (nuevo Paso 0)
- `backlog.md` (nuevo Paso 0)
- `adr.md` (nuevo Paso 0)
- `newSession.md` (versión simplificada)

## Nota sobre estructuras de proyecto

memsys3 debe contemplar que los proyectos pueden tener diversas estructuras: monorepos, git submodules, workspaces. La detección automática prioriza `$(pwd)/memsys3` y solo busca con `find` como fallback.

## Principio

`$(pwd)/memsys3` es el default. Si falla, buscar. Si hay ambigüedad, preguntar. Nunca asumir.

## Reunión

Deliberado en reunión `memsys3/docs/meets/20260322_1.md` (Issue 2, 5 iteraciones).
