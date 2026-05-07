<!-- version: 0.1.0 -->
<!--
Template: plan_PREFIJO-NNN.md
Ubicación: memsys3/backlog/docs/plan_PREFIJO-NNN.md
Propósito: pasos ejecutables para agente fresco. Anti-CDC (ADR-021).

QUÉ va aquí:
  - Pasos concretos de ejecución, en orden
  - Archivos afectados con paths
  - Criterios de done por paso y globales
  - Tests/validaciones a realizar

QUÉ NO va aquí:
  - Por qué se hace → usa informe_PREFIJO-NNN.md
  - Resumen del item → usa el item PREFIJO-NNN-titulo.md
-->

# Plan: PREFIJO-NNN — [Título]

**Item:** [`PREFIJO-NNN-titulo.md`](../PREFIJO-NNN-titulo.md)
**Informe:** [`informe_PREFIJO-NNN.md`](informe_PREFIJO-NNN.md)
**Fecha plan:** YYYY-MM-DD
**Estimación:** [tamaño aproximado: S / M / L / XL — sesiones estimadas]

---

## 0. Prerequisitos

¿Qué debe existir / estar leído antes de empezar?
- Leer informe completo
- ADRs relevantes (listar)
- Estado de archivos clave (verificar)

## 1. Bloques de trabajo

Divide la ejecución en bloques. Cada bloque es independiente o tiene
dependencia explícita. Un bloque típico cabe en una sesión de trabajo.

### Bloque A — [nombre]

**Objetivo:** [qué consigue este bloque]

**Archivos afectados:**
- `path/al/archivo1.md` — [qué cambia]
- `path/al/archivo2.yaml` — [qué cambia]

**Pasos:**
1. [Paso concreto]
2. [Paso concreto]
3. [Paso concreto]

**Criterio de done:**
- [ ] [Verificable]
- [ ] [Verificable]

### Bloque B — [nombre]

[...]

## 2. Validación final

Cómo verificar que el item está completo:
- [ ] Tests pasan
- [ ] Cambios commiteados con mensaje [formato]
- [ ] Archivos sincronizados dogfooding ↔ templates (si aplica)
- [ ] Item de backlog actualizado a "Completado"
- [ ] Sesión documentada en sessions.yaml

## 3. Restricciones de ejecución

Qué NO debe hacer el agente que ejecute:
- ¿Tocar `memory/templates/`? Solo si el item lo requiere explícitamente
- ¿Bumpear `file_version`? Solo `/actualizar-memsys3` (ADR-017)
- ¿Hacer commits con `Co-Authored-By:`? PROHIBIDO (ADR-016, defensa github.md)
- [Otras específicas del item]

## 4. Riesgos conocidos

Cosas que pueden salir mal y cómo recuperarse:
- Riesgo X → mitigación Y

## 5. Sesión recomendada para ejecutar

¿Misma sesión donde se diseñó? ¿Sesión fresca? ¿Por qué?
