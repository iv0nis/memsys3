# IMPROVEMENT-003: Sincronización Automática de Versión y Metadata en github.md

**Estado:** Pendiente
**Prioridad:** Media
**Tipo:** Mejora de sistema
**Plazo:** Sin urgencia
**Fecha creación:** 2025-12-01

---

## Propuesta

Mejorar `github.md` para que sincronice automáticamente la metadata de versión en `project-status.yaml` cuando se hace push a GitHub.

### Estructura Actual de Metadata

```yaml
metadata:
  memsys3_version: "v1.9 (commit: 5efffb0)"  # Versión + commit combinados
  memsys3_deployed: "2025-10-28"
```

### Estructura Propuesta (Opción A Mejorada)

```yaml
metadata:
  memsys3_version: "v1.9"              # MANUAL - Versión semántica (milestone)
  memsys3_commit: "5efffb0"            # AUTO - Hash del commit (actualizado por github.md)
  memsys3_last_push: "2025-12-01"      # AUTO - Fecha del último push exitoso
  memsys3_deployed: "2025-10-28"       # MANUAL - Fecha deployment inicial
```

## Motivación

**Problema actual:**
- La versión en `project-status.yaml` puede quedar desincronizada con el repo git
- No hay forma automática de saber cuándo fue el último push
- Versión semántica y commit hash están mezclados en un solo campo

**Beneficio propuesto:**
- Separación clara: versión (manual/intencional) vs commit (automático)
- `memsys3_last_push` siempre refleja el último push exitoso
- Sincronización automática reduce errores humanos
- Metadata más precisa para tracking de deployments

## Decisiones Técnicas

**Respuestas a preguntas clave:**

1. **¿Dónde actualizar memsys3_version manualmente?** → Opción A: En endSession.md cuando hay milestone
2. **¿Formato de memsys3_commit?** → Opción A: Solo hash corto (7 caracteres): `"5efffb0"`
3. **¿Cuándo actualizar los campos?** → Opción A: ANTES del commit (paso 2.5 en github.md)
4. **¿Qué pasa si push falla?** → `memsys3_last_push` quedaría con fecha falsa (principal caveat)

## Archivos Afectados

**Templates (distribuibles):**
- `memsys3_templates/prompts/github.md` - Agregar lógica actualización metadata
- `memsys3_templates/memory/templates/project-status-template.yaml` - Nuevos campos metadata

**Dog-fooding:**
- `memsys3/prompts/github.md` - Sincronizar con template
- `memsys3/memory/project-status.yaml` - Migrar estructura metadata
- `memsys3/memory/templates/project-status-template.yaml` - Sincronizar con template

## Referencias

- Conversación: Sesión 2025-12-01 compile-context
- Plan detallado: `~/.claude/plans/cryptic-yawning-sutton.md`
- ADR relacionada: Pendiente (considerar ADR-012 si se implementa)

## Notas

- Compatibilidad hacia atrás: Proyectos con estructura antigua `memsys3_version: "v0.6.1 (commit: xxx)"` necesitarían migración en `actualizar.md`
- Caveat principal: Si push falla después de actualizar metadata, `memsys3_last_push` sería incorrecta
- Alternativa evaluada: Actualizar DESPUÉS del push exitoso (genera commit adicional "chore: sync metadata")
