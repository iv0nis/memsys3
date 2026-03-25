# ISSUE-018 - actualizar.md borra archivos custom del proyecto

**Estado**: Resuelto
**Prioridad**: Alta
**Tipo**: Bug
**Fecha**: 2026-03-22

## Problema

Al actualizar memsys3 con `actualizar.md`, los archivos que el usuario creó en `memsys3/prompts/` (ej: `newSession.dev.md`, `endSession.dev.md`, `conciso.md`) se pierden porque el proceso reemplaza archivos sin preservar los que no existen en el template base.

## Evidencia

- Detectado en gitkigai (backup 12/03/2026 tiene los archivos, versión actual no)
- 6 archivos perdidos: `endSession.dev.md`, `newSession.dev.md`, `user_prompts/conciso.md`, `agent-identity.md`, `meet.md`, `migrate.md`

## Causa raíz

1. No hay detección de archivos custom del usuario
2. `rm -f memsys3/docs/*.md` en el fallback borra todo antes de copiar
3. Lista hardcodeada de prompts en el fallback es incompleta (no incluye nuevos prompts)

## Solución implementada

1. **Nuevo Paso 5.5**: Detectar archivos custom comparando `memsys3/` del proyecto vs template. Avisar al usuario.
2. **Fallback dinámico**: Reemplazar lista hardcodeada por `find` recursivo sobre el template.
3. **Eliminar `rm -f memsys3/docs/*.md`**: Nunca borrar carpetas enteras. Preferir docs huérfanos a custom perdidos.
4. **Protección git diff archivos A**: Verificar si archivo "añadido" ya existe en proyecto (posible custom del usuario con mismo nombre).
5. **Nota de bootstrap**: Documentar que el fix vive en el nuevo actualizar.md.

## Principio

En caso de duda, preservar lo del usuario. Lo del template siempre se puede recuperar del repo.

## Reunión

Deliberado en reunión `memsys3/docs/meets/20260322_1.md` (Issue 1, 5 iteraciones).
