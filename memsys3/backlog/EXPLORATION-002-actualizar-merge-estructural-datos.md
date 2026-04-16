# EXPLORATION-002: Actualización inteligente de archivos de datos

- **Estado:** Propuesto
- **Prioridad:** Alta
- **Tipo:** Exploración
- **Fecha:** 2026-04-16

## Problema

Cuando `/actualizar-memsys3` actualiza un proyecto de una versión antigua (ej: v0.12 → v0.20), copia correctamente los archivos de infraestructura (prompts, agents, templates). Pero los archivos de **datos del proyecto** (`context.yaml`, `project-status.yaml`) no absorben las mejoras estructurales de los templates nuevos.

### Ejemplo real

Proyecto actualizado de v0.12 a v0.20. Al compilar context.yaml:
- `version_context: "2.0"` — inventado, debería ser `"v0.20.0"` (leído de project-status.yaml)
- El CA no "vio" que el template nuevo tiene campos/secciones que antes no existían
- El context.yaml generado no refleja las mejoras del template nuevo

### El problema de fondo

`actualizar.md` tiene 3 categorías de archivos:
1. **Infraestructura** (prompts/, agents/) → se sobrescriben → OK
2. **Templates** (memory/templates/) → se sobrescriben → OK
3. **Datos del proyecto** (context.yaml, project-status.yaml, sessions.yaml) → NO se tocan → los cambios estructurales del template nuevo no llegan

El CA usa el template como guía para compilar, pero si el template cambió entre versiones (nuevos campos, nuevas secciones, metadata diferente), el CA puede:
- Ignorar los campos nuevos
- Inventar valores (como version_context: "2.0")
- Seguir con la estructura vieja

## Preguntas a investigar

1. **¿Qué archivos de datos se ven afectados?** — ¿Solo context.yaml o también project-status.yaml, sessions.yaml?
2. **¿El CA ya debería manejar esto?** — Si el template nuevo es la guía, ¿por qué el CA no genera la estructura nueva automáticamente?
3. **¿Es problema del CA o del actualizar.md?** — ¿Debería actualizar.md hacer un paso de "reconciliación" post-copia?
4. **¿Merge automático o señalización?** — ¿Debería el sistema mergear automáticamente, o solo señalar al usuario "estos campos son nuevos, revisa"?
5. **¿Cómo detectar qué cambió entre versiones de templates?** — diff entre template viejo (backup) y template nuevo
6. **¿Qué pasa con campos ambiguos como version_context?** — ¿Debería tener instrucción explícita de dónde leer el valor?

## Escenarios a considerar

- **Actualización menor** (v0.20.0 → v0.20.1): probablemente no hay cambios de estructura
- **Actualización mayor** (v0.12 → v0.20): muchos cambios de estructura, campos nuevos, secciones nuevas
- **Primera compilación post-actualización**: momento crítico donde el CA debe generar la estructura nueva

## Posibles enfoques

### A. Mejorar instrucciones del CA
Que compile-context.md/context-agent.yaml sean más explícitos: "genera EXACTAMENTE la estructura del template, no inventes campos, lee valores de project-status.yaml".

### B. Paso de reconciliación en actualizar.md
Después de copiar archivos, un paso que compare template viejo vs nuevo y señale diferencias al usuario.

### C. Validación post-compilación
Después de compilar, verificar que el context.yaml generado tiene todos los campos del template.

### D. Changelog de templates
Mantener un changelog de qué cambió en cada versión de los templates, para que el CA sepa qué es nuevo.

## Contexto adicional

- `version_context` en el template decía `"[NUMERO_VERSION]"` — ambiguo. Ya corregido a `"[valor de memsys3_version en project-status.yaml]"` en esta sesión
- El sistema de `file_version` (v0.20.0) versiona cada archivo independientemente, pero no hay mecanismo para que un proyecto destino "vea" qué cambió entre su file_version y la nueva

## Referencias

- `memsys3_templates/memory/templates/context-template.yaml`
- `memsys3_templates/prompts/compile-context.md`
- `memsys3_templates/agents/context-agent.yaml`
- `memsys3_templates/prompts/actualizar.md`
- Sesión 2026-04-16 (detección del problema)
