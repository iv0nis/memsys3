# FEATURE-007: Auditoría automática de calidad del contexto

**Estado:** Propuesto
**Prioridad:** Media
**Tipo:** Feature / Quality Assurance
**Plazo:** Long-term
**Fecha identificación:** 2025-01-30
**Depende de:** FEATURE-006 (Sistema de pesos para sesiones)

---

## Problema / Necesidad

Main Agents documentan sesiones en sessions.yaml asignando pesos (bajo/medio/alto), pero:
- **No hay verificación** de que los pesos sean apropiados
- **No hay métricas** de calidad de la contextualización
- **No hay feedback** para Main Agents que clasifican mal

**Consecuencias:**
1. **Pesos inconsistentes:** Sesiones triviales marcadas como "alto", sesiones críticas como "bajo"
2. **Context Agent confundido:** Filtrado subóptimo basado en pesos incorrectos
3. **Mala calibración:** Main Agents no aprenden de errores de clasificación
4. **Signal-to-noise degradado:** Sistema de pesos pierde efectividad

**Observación clave del usuario:**
> "CA puede comprobar si están funcionando bien las contextualizaciones si detecta que los Main Agents otorgan mal los pesos, ya que es un indicador de mala contextualización."

**Insight:**
- **Pesos mal asignados = indicador de mala contextualización del Main Agent**
- **Score de alineamiento = métrica de calidad del contexto**
- **Auditoría de calidad = metacognición del sistema**

---

## Propuesta / Solución

Implementar **sistema de auditoría automática** donde Context Agent evalúa la calidad de las contextualizaciones de Main Agents.

### Mecanismos Propuestos

#### 1. **Auditoría Automática durante compile-context**

Context Agent analiza sesiones durante compilación y detecta inconsistencias:

```yaml
# En context.yaml compilado, sección nueva:
auditoria_calidad:
  score_alineamiento: 0.78  # 0.0-1.0
  fecha_auditoria: "2025-01-30"
  sesiones_auditadas: 28

  inconsistencias_detectadas:
    - sesion: "2025-01-15-fix-typo-readme"
      peso_asignado: "alto"
      peso_esperado: "bajo"
      razon: "Fix typo sin ADRs ni decisiones → debería ser peso bajo"
      gravedad: "media"

    - sesion: "2025-01-20-adr-015-terminologia"
      peso_asignado: "medio"
      peso_esperado: "alto"
      razon: "ADR importante sin peso alto → subestimación"
      gravedad: "alta"

  recomendaciones:
    - "Revisar criterios de peso ALTO: detectados 3 casos de sobreestimación"
    - "ADRs importantes siempre deberían tener peso ALTO"
```

**Criterios de detección:**
- Sesión con ADRs creados/actualizados sin peso "alto" → inconsistencia
- Sesión con solo typos/fixes menores con peso "alto" → inconsistencia
- Sesión con "decisions" arquitectónicas sin peso "alto"/"medio" → inconsistencia
- Sesión con "gotchas" críticos sin peso "medio"/"alto" → inconsistencia

#### 2. **Skill /audit-context (Manual)**

Prompt dedicado para auditoría exhaustiva:

```bash
@memsys3/prompts/audit-context.md
```

**Workflow:**
1. Context Agent lee sessions.yaml + sessions_*.yaml completos
2. Analiza cada sesión según criterios de peso
3. Calcula score de alineamiento por categoría
4. Genera reporte detallado con recomendaciones
5. Identifica patrones de mala clasificación

**Output:**
```markdown
# Reporte de Auditoría de Calidad del Contexto

## Score Global
- **Alineamiento general:** 0.78/1.0 (Bueno)
- **Sesiones auditadas:** 28
- **Inconsistencias detectadas:** 5 (18%)

## Análisis por Categoría

### Pesos ALTOS (7 sesiones)
- ✅ Correctos: 5 (71%)
- ❌ Sobreestimados: 2 (29%)
  - `2025-01-15-fix-typo-readme`: Fix typo marcado como alto
  - `2025-01-18-refactor-minor`: Refactor menor marcado como alto

### Pesos MEDIOS (15 sesiones)
- ✅ Correctos: 14 (93%)
- ❌ Subestimados: 1 (7%)
  - `2025-01-20-adr-015-terminologia`: ADR marcado como medio

### Pesos BAJOS (6 sesiones)
- ✅ Correctos: 6 (100%)

## Patrones Detectados
1. **Sobreestimación de refactorings:** Refactorings menores clasificados como alto
2. **ADRs subestimados:** 1 ADR importante clasificado como medio (debería ser alto)

## Recomendaciones
1. ✅ Criterios de peso BAJO bien aplicados
2. ⚠️ Revisar criterios de peso ALTO: tendencia a sobreestimar refactorings
3. ⚠️ ADRs importantes SIEMPRE deben tener peso ALTO

## Score de Alineamiento por Main Agent
- Main Agent (general): 0.78/1.0 (Bueno, con margen de mejora)
```

#### 3. **Metacognición: Feedback Loop**

Context Agent puede incluir feedback en context.yaml para Main Agent:

```yaml
# En context.yaml
feedback_calidad:
  mensaje: |
    Score de alineamiento actual: 0.78/1.0

    Detectado patrón de sobreestimación en refactorings menores.
    Recuerda: peso ALTO solo para ADRs, decisiones arquitectónicas y features críticas.

    ADR-015 (terminología) fue marcado como peso MEDIO pero debería ser ALTO
    (actualización de nomenclatura estándar = decisión arquitectónica).

  accion_sugerida: "Revisar criterios de peso ALTO en endSession.md antes de documentar próxima sesión"
```

Main Agent ve este feedback en newSession.md → aprende y mejora clasificación futura.

---

## Indicadores de Mala Contextualización

| Síntoma | Score Alineamiento | Diagnóstico |
|---------|-------------------|-------------|
| Muchas sesiones peso "alto" (>40%) | < 0.5 | Sobreestimación sistemática → mala calibración |
| Todas sesiones peso "medio" | < 0.6 | Sin discriminación → falta criterio |
| ADRs sin peso "alto" | < 0.7 | No entiende arquitectura → descontextualización |
| Fixes triviales peso "alto" | < 0.6 | Confunde esfuerzo con importancia |
| Distribución equilibrada | > 0.8 | Buena contextualización ✅ |

**Score < 0.7 → Main Agent necesita mejor contexto o recalibración**

---

## Métricas de Calidad

### Score de Alineamiento (0.0 - 1.0)

**Fórmula:**
```
score = (sesiones_correctas / sesiones_totales)

Donde "correcta" = peso asignado coincide con peso esperado según criterios
```

**Rangos:**
- 0.9 - 1.0: Excelente (alineamiento casi perfecto)
- 0.8 - 0.9: Muy bueno (pocas inconsistencias)
- 0.7 - 0.8: Bueno (algunas inconsistencias, mejora posible)
- 0.6 - 0.7: Regular (inconsistencias frecuentes, revisar criterios)
- < 0.6: Deficiente (mala contextualización, recalibración necesaria)

### Distribución Esperada (proyecto maduro)

| Peso | % Esperado | Razón |
|------|-----------|-------|
| BAJO | 30-40% | Mantenimiento rutinario frecuente |
| MEDIO | 50-60% | Desarrollo estándar (bulk del trabajo) |
| ALTO | 10-20% | Decisiones críticas menos frecuentes |

**Desviaciones significativas indican problema:**
- ALTO > 40%: Sobreestimación
- MEDIO > 80%: Sin discriminación
- BAJO > 60%: Subestimación o proyecto muy maduro

---

## Implementación

### Fase 1: Criterios de Auditoría

**Definir heurísticas para detectar inconsistencias:**

```markdown
# En compile-context.md, nueva sección:

## Auditoría de Calidad (Opcional)

Si quieres auditar calidad de pesos asignados:

**Heurísticas de detección:**

1. **Peso ALTO esperado si:**
   - `adr_relacionada:` no está vacío (sesión creó/actualizó ADR)
   - `decisions:` contiene >3 decisiones arquitectónicas
   - `titulo:` contiene palabras clave: "arquitectura", "stack", "patrón", "decisión fundamental"
   - `gotchas:` contiene gotchas con criticidad "alta"

2. **Peso BAJO esperado si:**
   - `titulo:` contiene palabras clave: "typo", "fix minor", "cosmético", "config"
   - `duracion:` < 30min
   - `highlights:` tiene <3 items
   - Sin `decisions:` ni `gotchas:`

3. **Peso MEDIO por defecto** (si no cumple criterios alto ni bajo)

**Calcular score:**
- Comparar peso asignado vs peso esperado
- Score = sesiones correctas / sesiones totales
- Generar lista de inconsistencias detectadas
```

### Fase 2: Auditoría Automática en compile-context

1. Modificar `memsys3_templates/prompts/compile-context.md`
2. Añadir paso opcional de auditoría después de compilar sessions
3. Incluir sección `auditoria_calidad:` en context.yaml si se detectan inconsistencias

### Fase 3: Skill /audit-context

1. Crear `memsys3_templates/prompts/audit-context.md`
2. Workflow completo de auditoría exhaustiva
3. Genera reporte markdown detallado
4. Testing con sessions.yaml real del dog-fooding

### Fase 4: Feedback Loop

1. Modificar `memsys3_templates/prompts/newSession.md`
2. Leer sección `feedback_calidad:` de context.yaml si existe
3. Mostrar feedback al Main Agent al inicio de sesión
4. Main Agent aprende de errores previos

---

## Casos de Uso

### Caso 1: Proyecto Nuevo (Calibración Inicial)

**Primeras 10 sesiones:** Score bajo esperado (Main Agent aprendiendo criterios)
- Auditoría detecta sobreestimaciones frecuentes
- Feedback loop corrige en sesiones siguientes
- Score mejora gradualmente hasta > 0.8

### Caso 2: Proyecto Maduro (Validación Continua)

**Score histórico > 0.8:** Auditoría automática detecta pocas inconsistencias
- Auditoría se ejecuta cada 5-10 compilaciones (no en cada una)
- Solo genera feedback si score cae < 0.7

### Caso 3: Cambio de Main Agent

**Nuevo agente toma proyecto:** Score puede caer inicialmente
- Auditoría detecta desalineación con criterios del proyecto
- Feedback loop acelera aprendizaje
- Score se recupera después de 5-10 sesiones

---

## Consideraciones

### Complejidad vs Beneficio

**Complejidad añadida:**
- Heurísticas de detección pueden ser complejas
- Auditoría consume tokens adicionales (lectura full sessions)
- Mantenimiento de criterios si cambian requisitos

**Beneficio:**
- Calidad del contexto mejorada continuamente
- Main Agents aprenden de errores
- Sistema auto-corrige desviaciones
- Metacognición: sistema evalúa su propia calidad

**Balance:** Beneficio supera complejidad en proyectos maduros (>50 sesiones)

### Falsos Positivos

**Problema:** Heurísticas pueden detectar "inconsistencias" que no lo son.

**Ejemplo:**
- Sesión documenta refactor extenso con decisiones importantes
- Main Agent correctamente asigna peso "alto"
- Heurística detecta "refactor" en título → sugiere peso "medio"
- **Falso positivo**

**Mitigación:**
- Heurísticas deben ser sugerencias, no reglas estrictas
- Context Agent usa criterio inteligente (no solo keywords)
- Feedback presenta como "recomendaciones", no "errores"

---

## Referencias

- **Conversación:** Sesión 2025-01-30, visión futura de auditoría de alineamiento
- **Depende de:** FEATURE-006 (Sistema de pesos debe existir primero)
- **Filosofía:** Metacognición del sistema, auto-evaluación de calidad
- **Inspiración:** MLOps model monitoring, continuous quality assurance

---

## Notas Adicionales

**Innovación clave:**
- memsys3 no solo gestiona contexto, sino que **evalúa la calidad de su propia gestión**
- Sistema aprende y mejora continuamente (feedback loop)
- Context Agent como "auditor de calidad" además de "compilador"

**Diferencial competitivo:**
- Otros sistemas de contexto son estáticos
- memsys3 con auditoría es **adaptativo y auto-correctivo**
- Calidad del contexto garantizada a lo largo del tiempo

**Escalabilidad:**
- En proyectos pequeños: auditoría manual ocasional
- En proyectos grandes: auditoría automática continua
- Sistema se adapta a la madurez del proyecto

**Testing requerido:**
- [ ] Implementar heurísticas de detección en compile-context.md
- [ ] Auditar sessions.yaml del dog-fooding (calcular score actual)
- [ ] Crear prompt audit-context.md con workflow completo
- [ ] Validar que feedback loop mejora score a lo largo del tiempo
- [ ] Testing con Main Agents diferentes (variabilidad en clasificación)
