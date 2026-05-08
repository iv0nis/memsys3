# ISSUE-027: Migrar `principios_fundacionales` de `memory.yaml` a `PRINCIPLES.md`

**Estado:** Abierto
**Prioridad:** Media
**Tipo:** Tech debt / Refactor canónico
**Plazo:** Medio plazo (cubrible en Frente 7 BLUEPRINT-001 o sub-frente)
**Fecha identificación:** 2026-05-08

---

## Problema / Necesidad

`memsys3/memory/memory.yaml` tiene una sección `principios_fundacionales` con dos entradas:

- `cdc` (Casualidad de Contexto) — añadida 2026-05-07a, antes de existir `PRINCIPLES.md`.
- `olvidan-que-olvidan` (Meta-amnesia agéntica) — añadida 2026-05-08, en línea con la convención existente.

Tras Frente 1 BLUEPRINT-001 (creación de `PRINCIPLES.md` canónico), la sección `principios_fundacionales` en `memory.yaml` es **redundante**:

- `PRINCIPLES.md` es el documento canónico de principios sistémicos (ADR-022).
- `memory.yaml` está diseñado para usuario / feedback / referencias (ADR-020), NO para principios.

**Consecuencia.** Hay **dos lugares canónicos** para los principios. Esto:

1. Viola el principio #9 Separation of Concerns (PRINCIPLES.md mismo).
2. Crea riesgo de divergencia: si un principio cambia en uno, queda stale en el otro.
3. Genera CDC sobre dónde canonizar el siguiente principio (ya ocurrido en sesión 2026-05-08: el agente sugirió añadir a `memory.yaml` por inercia — el usuario corrigió y derivó a `PRINCIPLES.md`).

## Propuesta / Opciones

### Opción A — Migración total (recomendada)

1. Mover contenido de `memory.yaml::principios_fundacionales[cdc]` y `[olvidan-que-olvidan]` a `PRINCIPLES.md`:
   - `cdc` ya está mayoritariamente cubierto por la sección #1 Anti-CDC. Verificar que toda la sustancia (definicion, rol_de_memsys3, implicacion_diseno) está reflejada y completar lo que falte.
   - `olvidan-que-olvidan` ya quedó parcialmente reflejada como "Corolario disposicional" en sección #1 (sesión 2026-05-08). Verificar que `consecuencia` y `enfoque_correcto` están bien recogidos. Si falta detalle, expandir.
2. Eliminar la sección entera `principios_fundacionales` de `memory.yaml`.
3. `memory.yaml` queda con: `metadata`, `usuario`, `feedback`, `referencias` — alineado con su propósito canónico (ADR-020).
4. Actualizar `memory-template.yaml` si tenía `principios_fundacionales` (verificar — probablemente NO).

**Pros:** Una sola fuente de verdad para principios. Cierra deuda. Refuerza separation of concerns.
**Contras:** Requiere verificación cuidadosa para no perder matices. Toca dos archivos canónicos.

### Opción B — Statu quo + nota cruzada

Dejar la duplicación pero añadir nota en `memory.yaml::principios_fundacionales` apuntando a `PRINCIPLES.md` como fuente de verdad.

**Pros:** Cero riesgo de pérdida de información.
**Contras:** No resuelve el problema, lo gestiona. Sigue habiendo dos lugares.

### Opción C — Migración parcial (CDC sí, olvidan-que-olvidan se queda)

Migrar solo `cdc` (que ya está duplicado) y dejar `olvidan-que-olvidan` en `memory.yaml` como observación de feedback.

**Pros:** Preserva el matiz de "cómo se descubrió este principio".
**Contras:** Inconsistente. El propio `olvidan-que-olvidan` ya está en PRINCIPLES.md como corolario disposicional.

## Decisiones / Acciones

**Recomendación:** Opción A. Es deuda técnica acotada, bajo riesgo si se hace con cuidado, alto retorno (clarifica el modelo canónico).

**Verificación post-migración:**
- `grep -i "principios_fundacionales" memsys3/memory/memory.yaml` → 0 hits
- Sustancia completa de CDC y olvidan-que-olvidan presente en `PRINCIPLES.md` sección #1
- `memory.yaml` schema coincide con `memory-template.yaml`
- Tests anti-CDC: agente fresco que pregunte "¿qué es CDC?" debe encontrar respuesta canónica solo en `PRINCIPLES.md`

**Anclaje al BLUEPRINT-001:**
- Encaja como sub-tarea de Frente 7 (pulir prompts/agents/scaffold) o como mini-frente independiente entre 6 y 7.
- Probable peso bajo (~30 min de trabajo cuidadoso).

## Referencias

- **Origen:** Sesión 2026-05-08, durante reflexión sobre dónde canonizar la clarificación "límites de CDC". Usuario detectó la inconsistencia.
- **Principios afectados:**
  - PRINCIPLES.md #1 (Anti-CDC) — lugar correcto del contenido
  - PRINCIPLES.md #9 (Separation of Concerns) — principio violado por la duplicación actual
- **ADRs:**
  - ADR-020 (memory.yaml — define propósito real: usuario/feedback/referencias)
  - ADR-022 (PRINCIPLES.md — define lugar canónico de principios)
- **Items relacionados:** EXPLORATION-004 (canonización proactiva — el problema que dispara este ISSUE)

<!-- version: 0.1.0 -->
