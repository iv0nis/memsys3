# FEATURE-006: Sistema de pesos para sesiones (bajo/medio/alto)

**Estado:** Propuesto
**Prioridad:** Media-Alta
**Tipo:** Feature / Optimization
**Plazo:** Medium-term
**Fecha identificación:** 2025-01-30

---

## Problema / Necesidad

Actualmente, todas las sesiones en sessions.yaml se documentan con densidad similar (~95 líneas/sesión), sin distinguir entre:
- Sesiones críticas (ADRs, decisiones arquitectónicas, features core)
- Sesiones normales (features estándar, refactorings)
- Sesiones rutinarias (fixes menores, typos, mantenimiento)

**Consecuencias:**
1. **Ineficiencia:** Sesiones triviales consumen tanto espacio como sesiones críticas
2. **Signal-to-noise bajo:** Información importante diluida entre detalles menores
3. **Rotación subóptima:** Sistema no diferencia importancia al rotar
4. **Context Agent menos eficiente:** Debe filtrar sin criterio de peso previo

**Observación:**
- sessions.yaml actual: ~95 líneas/sesión promedio
- ¿Es "resumen inteligente" o "documentación completa"?
- No todas las sesiones tienen igual importancia para el proyecto

---

## Propuesta / Solución

Implementar **sistema de pesos** para clasificar sesiones según su importancia arquitectónica y estratégica.

### Escala de Pesos

| Peso | Líneas | Tipo de Sesión |
|------|--------|----------------|
| **🔴 ALTO** | ~140 | ADRs, decisiones arquitectónicas, features críticas |
| **🟡 MEDIO** | ~95 | Features normales, refactorings, mejoras estándar |
| **🟢 BAJO** | ~70 | Fixes menores, mantenimiento, out of scope |

### Criterios de Clasificación

**🔴 PESO ALTO (~140 líneas):**
- Creación/actualización de ADRs importantes
- Decisiones arquitectónicas fundamentales
- Features críticas del core del proyecto
- Cambios de stack tecnológico
- Bugs críticos con gotchas importantes
- Establecimiento de patrones que afectan desarrollo futuro

**Documentación:** Exhaustiva, con contexto completo, justificaciones, alternativas consideradas.

**🟡 PESO MEDIO (~95 líneas):**
- Features normales dentro del scope
- Refactorings significativos
- Mejoras de features existentes
- Testing y validación
- Bugs moderados resueltos
- Documentación importante

**Documentación:** Estándar, equilibrada, highlights + decisions + gotchas relevantes.

**🟢 PESO BAJO (~70 líneas):**
- Fixes menores, typos, bugs triviales
- Cambios cosméticos (CSS, UI tweaks)
- Mantenimiento rutinario (updates dependencies)
- Trabajo fuera del scope (exploraciones, experiments)
- Setup/configuración inicial
- Tareas administrativas

**Documentación:** Concisa, solo highlights esenciales, omitir detalles menores.

---

## Implementación

### 1. Modificar endSession.md

**Añadir nuevo PASO 1.5 (después de "Auto-analizar la Sesión"):**

```markdown
### 1.5. Evaluar Peso de la Sesión

Antes de documentar, determina el peso/importancia de esta sesión:

**🔴 PESO ALTO (~140 líneas):**
- Creaste ADRs o tomaste decisiones arquitectónicas
- Features críticas del core del proyecto
- Cambios fundamentales que afectan desarrollo futuro

**🟡 PESO MEDIO (~95 líneas):**
- Features normales dentro del scope
- Refactorings o mejoras significativas
- Desarrollo estándar del proyecto

**🟢 PESO BAJO (~70 líneas):**
- Fixes menores, typos, mantenimiento rutinario
- Cambios cosméticos o configuración
- Trabajo fuera del scope principal

**Ajusta la densidad de tu documentación según el peso:**

- **Peso bajo:** Highlights concisos (3-5 bullets), omitir detalles menores
- **Peso medio:** Documentación estándar (highlights + decisions + gotchas)
- **Peso alto:** Documentación exhaustiva (contexto completo, justificaciones, alternativas)
```

### 2. Añadir campo metadata en sessions-template.yaml

```yaml
- id: "YYYY-MM-DD-titulo-descriptivo"
  data: "YYYY-MM-DD"
  duracion: "~Xh"
  titulo: "Título conciso de la sesión"
  peso: "bajo|medio|alto"  # 🟢🟡🔴 Indica importancia para Context Agent
  highlights:
    - ...
```

### 3. Actualizar compile-context.md

Context Agent debe usar campo `peso:` para priorización inteligente:

```markdown
**Criterio de filtrado por peso:**
- Sesiones peso ALTO: Incluir casi completas (solo filtrar detalles muy menores)
- Sesiones peso MEDIO: Aplicar filtrado estándar (síntesis inteligente)
- Sesiones peso BAJO: Filtrar agresivamente (solo highlights esenciales)
```

---

## Beneficios

### 1. **Eficiencia de Rotación**
- Balance natural entre volumen y relevancia
- Sesiones importantes ocupan más espacio (justificado)
- Sesiones rutinarias ocupan menos (eficiente)

**Ejemplo:**
- Rotación anterior: 20 sesiones × 95 líneas = 1900 líneas
- Con pesos: (5 alto × 140) + (10 medio × 95) + (5 bajo × 70) = 1650 líneas
- **Beneficio:** Mismo número de sesiones, menos líneas, mejor signal-to-noise

### 2. **Context Agent Más Eficiente**
- Puede filtrar sesiones peso bajo más agresivamente
- Preservar sesiones peso alto casi completas en context.yaml
- Criterio inteligente: prioriza por peso + recencia + criticidad

### 3. **Escalabilidad Mejorada**
- Proyectos con muchas sesiones rutinarias rotan menos frecuentemente
- Proyectos con decisiones críticas preservan contexto completo
- Sistema se adapta automáticamente al tipo de trabajo

### 4. **Main Agent Mejor Informado**
- Sesiones importantes tienen contexto rico y completo
- Sesiones triviales no contaminan con ruido
- Signal-to-noise ratio mejorado significativamente

### 5. **Conciencia de Importancia**
- Main Agents más conscientes de la importancia relativa de su trabajo
- Reflexión sobre impacto de cada sesión
- Mejor auto-evaluación del progreso del proyecto

---

## Visión Futura: Auditoría de Alineamiento

**Capacidad de auto-evaluación del sistema:**

Context Agent puede auditar calidad de pesos asignados:
- Sesiones triviales marcadas como "alto" → Main Agent sobreestima importancia
- Sesiones críticas marcadas como "bajo" → Main Agent subestima importancia
- **Score de alineamiento:** Indicador de calidad de contextualización del Main Agent

**Posibles mecanismos:**
1. **Auditoría automática:** Context Agent detecta inconsistencias durante compile-context
2. **Skill de comprobación:** `/audit-context` genera reporte de calidad
3. **Metacognición del sistema:** Feedback loop para mejorar Main Agents futuros

**Ver FEATURE-007 o IMPROVEMENT para diseño detallado de auditoría.**

---

## Consideraciones

### Riesgo: Subjetividad en Clasificación
**Problema:** Main Agents pueden clasificar inconsistentemente.

**Mitigación:**
1. Criterios claros y ejemplos concretos en endSession.md
2. Context Agent puede auditar y sugerir correcciones
3. Sistema aprende patrones de clasificación a lo largo del tiempo

### Complejidad Adicional
**Problema:** PASO 1.5 añade decisión adicional en workflow.

**Mitigación:**
1. Criterios simples y claros (no requiere análisis profundo)
2. Beneficio (eficiencia) supera costo (decisión rápida)
3. Con práctica, la clasificación se vuelve intuitiva

---

## Plan de Implementación

**Fase 1: Implementación básica**
1. Modificar `memsys3_templates/prompts/endSession.md` (añadir PASO 1.5)
2. Actualizar `memsys3_templates/memory/templates/sessions-template.yaml` (añadir campo `peso:`)
3. Sincronizar con `memsys3/` (dog-fooding)

**Fase 2: Context Agent aware**
1. Modificar `memsys3_templates/prompts/compile-context.md`
2. Implementar criterio de filtrado por peso
3. Testing con sesiones reales de diferentes pesos

**Fase 3: Auditoría de calidad** (ver FEATURE-007)
1. Diseñar prompt `audit-context.md`
2. Implementar métricas de alineamiento
3. Sistema de feedback para Main Agents

---

## Referencias

- **Conversación:** Sesión 2025-01-30, discusión sobre densidad de sesiones
- **Contexto:** Análisis de sessions.yaml (~95 líneas/sesión promedio)
- **Filosofía:** ADR-001 (Criterio inteligente, NO límites arbitrarios)
- **Relacionado:** FEATURE-005 (Optimizar uso ventana contexto), ISSUE-007 (Sobreescritura sessions.yaml)

---

## Notas Adicionales

**Alineación con principios memsys3:**
- ✅ Criterio inteligente (ADR-001): No límite fijo, adaptativo según importancia
- ✅ Escalabilidad: Sistema se adapta al volumen y tipo de trabajo
- ✅ Preservación de lo crítico: Sesiones importantes nunca se pierden
- ✅ Eficiencia de tokens: Balance óptimo entre detalle y consumo

**Testing requerido:**
- [ ] Documentar 3 sesiones de cada peso (bajo/medio/alto)
- [ ] Verificar densidad resultante (~70, ~95, ~140 líneas)
- [ ] Compilar contexto con Context Agent y verificar filtrado por peso
- [ ] Evaluar si criterios son suficientemente claros para Main Agents

**Métricas de éxito:**
- Distribución de pesos razonable (no todo "alto" o todo "medio")
- Rotación menos frecuente con igual número de sesiones
- Context.yaml con mejor signal-to-noise ratio
- Main Agents reportan criterios claros y útiles
