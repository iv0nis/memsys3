# ISSUE-016 - endSession: recordatorio compile-context cuando hay muchas sesiones sin compilar

**Estado**: Abierto
**Prioridad**: Media
**Tipo**: Improvement/UX
**Fecha**: 2026-03-06

## Problema

El agente no avisa cuando `context.yaml` lleva muchas sesiones sin recompilarse. El README y otros docs de referencia rápida pueden quedar desactualizados sin que nadie lo note.

Actualmente el agente puede saberlo comparando:
- Última sesión documentada en `sessions.yaml`
- Versión de `context.yaml` (campo `compiled` o `version`)

## Propuesta

En endSession.md, añadir un paso de verificación al final que:

1. Lea `memsys3/memory/context.yaml` y extraiga `metadata.ultima_compilacion`
2. Cuente cuántas sesiones en `sessions.yaml` tienen fecha posterior a esa
3. Si hay **5 o más sesiones** sin compilar, mostrar recordatorio pasivo:

```
⚠️ context.yaml lleva X sesiones sin recompilar (última compilacion: YYYY-MM-DD)
   En tu proxima sesion limpia considera ejecutar @memsys3/prompts/compile-context.md
```

## Umbral

5 sesiones.

## Mecanismo de deteccion

Usar `ultima_compilacion` que ya existe en `context.yaml` — sin campos nuevos.
Comparar con fechas de sesiones en `sessions.yaml` (ordenado newest-first).

## Referencias

- `memsys3/prompts/endSession.md` — donde añadir el paso
- `memsys3/prompts/compile-context.md` — prompt a sugerir
- `memsys3/memory/context.yaml` — campo `metadata.ultima_compilacion`
