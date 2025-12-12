# ISSUE-002: Inconsistencia entre Versionado Git Tags vs Versión Interna

**Estado:** Pendiente
**Prioridad:** Media
**Tipo:** Tech debt / Inconsistencia
**Plazo:** Resolver antes de v1.0.0 estable
**Fecha creación:** 2025-12-01

---

## Problema

Actualmente existen **dos sistemas de versionado diferentes** que no están sincronizados:

### 1. Tags Git (Semantic Versioning Público)
- Último tag: **v0.7.1**
- Formato: `v0.x.x` (pre-release, no estable)
- Ubicación: Git tags en GitHub
- Propósito: Releases públicas del repositorio

### 2. Versión Interna (Development Tracking)
- Versión actual: **v1.9**
- Formato: `v1.x` o `Development v1.x`
- Ubicación: `project-status.yaml` (memsys3_version), `context.yaml` (version_context), `README.md`
- Propósito: Tracking iteraciones de desarrollo interno

## Evidencia de Inconsistencia

**project-status.yaml:**
```yaml
metadata:
  fase: "Development v1.9"
  memsys3_version: "v1.9 (commit: 5efffb0)"
```

**Git tag actual:**
```bash
git tag --sort=-version:refname | head -1
# v0.7.1
```

**README.md:**
```
Versión: 1.9
```

## Impacto

- **Confusión**: ¿Estamos en v0.7.1 o v1.9?
- **Documentación inconsistente**: README dice v1.9, GitHub releases dice v0.7.1
- **Comunicación**: ¿Qué versión reportar a usuarios?
- **Deployment tracking**: Proyectos desplegados no saben qué versión real de memsys3 tienen

## Contexto Histórico

Durante el desarrollo:
- Se usó "v1.x" como nomenclatura interna para iteraciones de desarrollo
- Se usó "v0.x.x" en git tags siguiendo semantic versioning (0.x = pre-release)
- Ambos sistemas evolucionaron independientemente sin sincronización

Instrucción en `github.md` (línea 8):
> "No subas la versión más allá de la 0.x.x hasta que sea estable"

Esto sugiere que git tags deben estar en 0.x.x hasta release estable.

## Solución Propuesta

### Opción A: Unificar en v0.x.x (Recomendada)

**Actualizar versión interna para coincidir con git tags:**
- v1.9 → v0.7.1
- `project-status.yaml` → memsys3_version: "v0.7.1"
- `context.yaml` → version_context: "0.7.1"
- `README.md` → Versión: 0.7.1
- Mantener "Development v0.7.x" como fase

**Ventajas:**
- Coherente con semantic versioning estándar (0.x = pre-release)
- Cumple instrucción github.md
- Un solo sistema de versionado
- Claro para usuarios: v0.x = aún no estable

**Desventajas:**
- Parece "retroceso" (v1.9 → v0.7.1)
- Requiere actualizar múltiples archivos

### Opción B: Sincronizar git tags con versión interna

**Cambiar git tags para coincidir con versión interna:**
- v0.7.1 → v1.9.0
- Próximos tags: v1.9.1, v1.10.0, etc.

**Ventajas:**
- Mantiene versión interna actual
- No hay que cambiar archivos ya actualizados

**Desventajas:**
- v1.x implica "estable" en semantic versioning (contradice realidad)
- Contradice instrucción github.md
- Menos claro para usuarios (v1.x sugiere producción ready)

### Opción C: Sistema Dual Explícito (No Recomendada)

Mantener ambos sistemas pero documentar explícitamente:
- Git tags: v0.x.x (releases públicas)
- Versión interna: v1.x (iteraciones desarrollo)

**Desventajas:**
- Confusión perpetua
- Requiere documentación constante
- Usuarios no sabrán qué versión usar

## Decisión Pendiente

**Estado actual:** Decisión pospuesta hasta futuro release.

**Acción requerida:**
- Resolver antes de v1.0.0 estable
- Actualizar TODOS los archivos con versionado a sistema único
- Documentar decisión en ADR si se elige cambio significativo

## Archivos Afectados (cuando se resuelva)

**Versionado interno:**
- `memsys3/memory/project-status.yaml` (memsys3_version)
- `memsys3/memory/context.yaml` (version_context, metadata.ultima_compilacion)
- `README.md` (Versión)
- `memsys3_templates/memory/templates/project-status-template.yaml`
- `memsys3_templates/memory/templates/context-template.yaml`

**Git:**
- Tags en GitHub
- Posiblemente `github.md` (actualizar instrucción versión)

**Prompts que referencian versión:**
- `compile-context.md` (genera version_context)
- `deploy.md` (copia versión a nuevos proyectos)
- `actualizar.md` (tracking versión durante actualizaciones)

## Referencias

- Conversación: Sesión 2025-12-01 compilación + github push
- Commit donde surgió: ed5aebe
- Tag actual: v0.7.1
- Versión interna actual: v1.9
- Instrucción github.md línea 8: "No subas la versión más allá de la 0.x.x hasta que sea estable"

## Notas

- Decisión debe tomarse ANTES de considerar el sistema "estable"
- Si se elige Opción A: Hacer en actualización mayor (con actualizar.md modificado)
- Si se elige Opción B: Actualizar github.md para quitar restricción 0.x.x
- Considerar impacto en proyectos ya desplegados con versiones antiguas
