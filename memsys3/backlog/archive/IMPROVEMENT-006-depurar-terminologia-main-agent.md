# IMPROVEMENT-006: Depurar Terminología "Main Agent" en Todo el Sistema

**Estado**: Cerrado (2026-05-08, BLUEPRINT-001 Frente 5)
**Prioridad**: Alta
**Tipo**: Mejora
**Fecha creación**: 2025-12-17
**Fecha cierre**: 2026-05-08
**Relacionado con**: ADR-015, ISSUE-026
**Resolución**: Frente 5 cerró todos los criterios de aceptación. 12 sustituciones aplicadas en infraestructura activa: 4 en `memsys3_templates/prompts/`, 4 sync en `memsys3/prompts/`, 2 en `README.md`, 2 drift en `memsys3/agents/context-agent.yaml` (Fork inicial los pasó por alto, hallados en re-validación). Validación: `grep -rniE 'DevAI|DevAgent|Development Agent'` sobre infraestructura activa → 0 hits. Detalle: `memsys3/backlog/docs/informe_BLUEPRINT-001-residualidad.md` §4.2.

---

## Problema / Propuesta

Tras ADR-015, el sistema tiene terminología inconsistente para referirse al agente principal. Múltiples archivos usan "Development Agent", "Development Agents", o "DevAI" en lugar del término estándar "Main Agent".

**Impacto**: Confusión conceptual, documentación inconsistente, dificultad para escalar con agentes especializados futuros.

---

## Ubicaciones Identificadas

### Archivos que requieren actualización:

1. **memsys3/agents/main-agent.yaml** (línea 3)
   - Actual: `rol: Development Agent`
   - Nuevo: `rol: Main Agent`

2. **memsys3_templates/agents/main-agent.yaml** (línea 3)
   - Mismo cambio

3. **memsys3_templates/prompts/compile-context.md** (línea 7)
   - Actual: "Development Agents puedan cargar"
   - Nuevo: "el Main Agent pueda cargar" (singular, consistente)

4. **memsys3/prompts/compile-context.md**
   - Mismo cambio

5. **README.md** (raíz repositorio)
   - Buscar todas las referencias a "Development Agent", "DevAI", "Development Agents"
   - Reemplazar por "Main Agent" (singular cuando corresponda)

6. **memsys3_templates/README.md**
   - Mismo cambio

7. **Prompts varios** (buscar en memsys3/prompts/ y memsys3_templates/prompts/)
   - newSession.md
   - endSession.md
   - Otros prompts que mencionen "Development Agent"

8. **ADRs históricas** (opcional, menor prioridad)
   - Mantener texto original para consistencia histórica
   - Agregar nota al final: "UPDATE 2025-12-17: Terminología actualizada a 'Main Agent' (ver ADR-015)"

---

## Estrategia de Implementación

### Opción A (Recomendada): Depuración sistemática completa

1. **Búsqueda exhaustiva**:
   ```bash
   grep -r "Development Agent" memsys3_templates/
   grep -r "DevAI" memsys3_templates/
   grep -r "Development Agents" memsys3_templates/
   ```

2. **Actualización por categoría**:
   - Primero: agents/main-agent.yaml (templates y dog-fooding)
   - Segundo: compile-context.md (templates y dog-fooding)
   - Tercero: README.md (ambos)
   - Cuarto: Prompts restantes
   - Quinto: ADRs (notas UPDATE, no cambiar texto original)

3. **Validación**:
   - Re-ejecutar grep para confirmar 0 resultados
   - Verificar que mensajes son consistentes (singular vs plural)
   - Testing: ejecutar newSession.md y compile-context.md

### Opción B: Depuración incremental

Actualizar solo archivos críticos primero (main-agent.yaml, compile-context.md), resto después.

**Descartada**: Mantiene inconsistencia parcial.

---

## Consideraciones

### ✅ Hacer:
- Unificar TODO como "Main Agent" (singular cuando sea único agente)
- Actualizar mensajes a tono genérico: "contextualizar agentes" en lugar de "usado por Development Agents"
- Deployment de cambios: memsys3_templates/ → memsys3/ (dog-fooding)

### ❌ NO Hacer:
- NO cambiar texto original de ADRs históricas (solo agregar UPDATE)
- NO actualizar context.yaml ya compilado (se regenerará automáticamente)
- NO crear breaking changes (cambio es cosmético, no funcional)

---

## Criterios de Aceptación

✅ 0 resultados al buscar "Development Agent" en memsys3_templates/
✅ 0 resultados al buscar "DevAI" en memsys3_templates/
✅ main-agent.yaml usa "Main Agent"
✅ compile-context.md usa "Main Agent" o mensaje genérico
✅ README.md consistente con terminología
✅ Testing: newSession + compile-context ejecutan sin confusión

---

## Referencias

- ADR-015: Terminología unificada: Main Agent como nomenclatura estándar
- Sesión 2025-12-17: Feedback sobre inconsistencias detectadas
- ADR-008: Main-Agent NO debe proponer compile-context (ya usa término correcto)

---

## Notas

Mejora cosmética pero conceptualmente importante para:
- Escalabilidad del sistema (espacio para agentes especializados futuros)
- Claridad terminológica
- Consistencia documentación

Prioridad ALTA porque afecta comprensión del sistema completo.
