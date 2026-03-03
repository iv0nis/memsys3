# Sistema de Backlog

## Qué es

El backlog gestiona el trabajo futuro del proyecto. Cada item es un archivo Markdown en `memsys3/backlog/` con un prefijo que indica su tipo.

## Prefijos

| Prefijo | Uso |
|---------|-----|
| `ISSUE-XXX` | Problemas técnicos, bugs, tech debt |
| `FEATURE-XXX` | Nueva funcionalidad |
| `IMPROVEMENT-XXX` | Mejora de funcionalidad existente |
| `SPEC-XXX` | Especificación técnica detallada |
| `BLUEPRINT-XXX` | Diseño arquitectónico alto nivel |
| `EXPLORATION-XXX` | Investigación sin solución clara |

## Estados

`Propuesto` → `Abierto` → `En Progreso` → `Completado` / `Cancelado` / `Rechazado` / `Bloqueado`

**Nunca borrar items completados** — son documentación histórica.

## Estructura de un item

```markdown
# TIPO-XXX: Título descriptivo

**Estado:** Abierto
**Prioridad:** Alta|Media|Baja
**Tipo:** Tipo
**Fecha identificación:** YYYY-MM-DD

---

## Problema / Necesidad
[Descripción]

## Comportamiento esperado
[Qué debería pasar]

## Impacto
[Qué afecta]
```

## Operaciones

Usar `@memsys3/prompts/backlog.md` para:
- **Consultar** — ver items por tipo/estado
- **Crear** — nuevo item con prefijo y numeración secuencial
- **Actualizar** — cambiar estado y prioridad

## Integración con el sistema

Los pendientes prioritarios del backlog se reflejan en `project-status.yaml` y el Context Agent los incluye en `context.yaml` para que el agente los tenga presentes al iniciar sesión.
