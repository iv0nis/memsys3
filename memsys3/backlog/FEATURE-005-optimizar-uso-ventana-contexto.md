# FEATURE-005: Optimizar uso de ventana de contexto en fases tempranas del proyecto

**Estado:** Propuesto
**Prioridad:** Media-Alta
**Tipo:** Feature / Optimization
**Plazo:** Medium-term
**Fecha identificación:** 2025-01-30

---

## Problema / Necesidad

**Observación del usuario:**
"La tendencia de memsys3 debería ser intentar usar más capacidad de ventana de contexto en las primeras fases de un proyecto, porque veo que cada vez que el Context Agent hace una compilación se tardan muchas sesiones en llegar a 70k-80k tokens, y en proyectos con cientos de sesiones aún no me ha llegado a los 100k tokens. Eso implica que las compilaciones de contexto sean menos eficientes."

**Situación actual:**
- Context Agent tiene límite de 2000 líneas en context.yaml compilado
- En proyectos pequeños/nuevos, compilaciones generan ~50-70K tokens
- Proyectos con cientos de sesiones ~70-80K tokens (lejos de límite 200K)
- Context Agent aplica filtrado inteligente desde el inicio
- **Efecto:** Sub-utilización de ventana de contexto disponible en LLMs modernos

**Contexto LLM actual (2025):**
- Claude Sonnet 4.5: 200K tokens de contexto
- GPT-4 Turbo: 128K tokens
- Gemini 1.5 Pro: 1M tokens
- **Realidad:** memsys3 usa ~40-50% de capacidad disponible en la mayoría de proyectos

**Problema:**
En fases tempranas del proyecto (primeras 10-20 sesiones):
- Context Agent filtra demasiado agresivamente
- Información valiosa de sesiones iniciales se excluye prematuramente
- Main Agent carece de contexto histórico importante
- Compilaciones requieren más frecuencia para mantener contexto actualizado

**Impacto:**
1. **Ineficiencia de compilaciones:** Compilar cada 2-3 sesiones para mantener contexto fresco
2. **Pérdida de contexto valioso:** Sesiones tempranas contienen decisiones arquitectónicas fundamentales
3. **Sub-utilización de capacidad:** 200K tokens disponibles, solo se usan 60-80K
4. **Más trabajo para Context Agent:** Más compilaciones = más trabajo = más tokens

---

## Análisis

**Filosofía actual (ADR-001):**
> "El Context Agent usa criterio inteligente basándose en la pregunta:
> '¿Qué debe saber CUALQUIER agent descontextualizado para trabajar aquí?'
> Límite ÚNICO: máximo 2000 líneas en context.yaml final."

**Límite 2000 líneas equivale a:**
- ~30-35K tokens en context.yaml (solo archivo compilado)
- Lectura de archivos full/ adicionales: ~20-40K tokens
- **Total disponible para Main Agent:** ~50-80K tokens
- **Espacio sin usar:** 120-150K tokens (60-75% de capacidad)

**Fases del proyecto y necesidades de contexto:**

| Fase | Sesiones | Necesidad Contexto | Capacidad Actual |
|------|----------|-------------------|------------------|
| **Inception** | 1-10 | ⭐⭐⭐⭐⭐ MUY ALTA (decisiones fundacionales) | 🔴 Filtrado agresivo |
| **Early Development** | 10-50 | ⭐⭐⭐⭐ ALTA (patrones establecidos) | 🟡 Filtrado moderado |
| **Mature** | 50-200 | ⭐⭐⭐ MEDIA (contexto estable) | 🟢 Filtrado inteligente |
| **Legacy** | 200+ | ⭐⭐ BAJA (mayor filtrado necesario) | 🟢 Filtrado óptimo |

**Problema detectado:**
Context Agent aplica **mismo nivel de filtrado** en todas las fases → sub-óptimo en fases tempranas.

**Propuesta de filosofía adaptativa:**
> "Usar más contexto cuando el proyecto es joven (decisiones fundacionales),
> filtrar más cuando el proyecto es maduro (contexto estable)."

---

## Propuesta / Opciones

### Opción A: Límite dinámico basado en fase del proyecto (RECOMENDADA)

Modificar compile-context.md para ajustar límite según número de sesiones:

```yaml
# Límites dinámicos context.yaml
fases:
  inception:      # 1-10 sesiones
    limite_lineas: 3000  # ~50K tokens context.yaml
    filosofia: "Incluir TODO: ADRs completos, todas las sesiones, gotchas detallados"

  early_dev:      # 11-50 sesiones
    limite_lineas: 2500  # ~40K tokens context.yaml
    filosofia: "Filtrado ligero: mantener decisiones fundacionales completas"

  mature:         # 51-150 sesiones
    limite_lineas: 2000  # ~30K tokens context.yaml (actual)
    filosofia: "Filtrado moderado: síntesis inteligente de sesiones antiguas"

  legacy:         # 150+ sesiones
    limite_lineas: 2000  # ~30K tokens context.yaml
    filosofia: "Filtrado agresivo: solo highlights y decisiones críticas"
```

**Implementación en compile-context.md:**
```markdown
## PASO PREVIO: Determinar fase del proyecto

Cuenta sesiones en sessions.yaml + sessions_*.yaml:
- Si 1-10 sesiones: FASE INCEPTION → límite 3000 líneas
- Si 11-50 sesiones: FASE EARLY_DEV → límite 2500 líneas
- Si 51-150 sesiones: FASE MATURE → límite 2000 líneas
- Si 150+ sesiones: FASE LEGACY → límite 2000 líneas

Usa el límite correspondiente al compilar context.yaml.
```

**Pros:**
- Adaptativo a necesidades reales del proyecto
- Aprovecha ventana de contexto moderna (200K tokens)
- Decisiones fundacionales mejor preservadas
- Menos compilaciones en proyectos jóvenes
- Compatible con filosofía ADR-001 (criterio inteligente)

**Contras:**
- Más complejidad en compile-context.md
- Context Agent debe contar sesiones primero
- Límites requieren calibración (testing empírico)

### Opción B: Modo "full context" opcional para proyectos pequeños

Agregar flag `--full` en compile-context.md:

```bash
# Modo estándar (actual)
@memsys3/prompts/compile-context.md

# Modo full context (proyectos < 50 sesiones)
@memsys3/prompts/compile-context.md --full
```

**Modo full:**
- Incluir TODAS las sesiones (no solo síntesis)
- Incluir TODOS los ADRs (sin filtrado)
- Límite: 5000 líneas (~80K tokens)

**Pros:**
- Usuario controla nivel de detalle
- Simple de implementar
- Útil para debugging y onboarding

**Contras:**
- Requiere intervención manual del usuario
- No automático según fase del proyecto

### Opción C: Priorizar sesiones tempranas en filtrado

Modificar criterio de Context Agent:

**Regla adicional:**
"Las primeras 10 sesiones del proyecto tienen prioridad ALTA (casi nunca filtrar).
Estas contienen decisiones fundacionales que impactan todo el desarrollo futuro."

**Implementación:**
```markdown
Al compilar sessions:
1. Sesiones 1-10: Incluir COMPLETAS (highlights + decisions + gotchas)
2. Sesiones 11-30: Incluir highlights + decisions (filtrar gotchas resueltos)
3. Sesiones 31+: Síntesis inteligente según criticidad
```

**Pros:**
- Preserva memoria fundacional del proyecto
- Simple de implementar
- No requiere cálculos de fase

**Contras:**
- Solo beneficia sesiones, no ADRs o gotchas
- Menos flexible que Opción A

---

## Decisiones / Acciones

**Decisión:** Implementar **Opción A** (límite dinámico) + elementos de **Opción C** (priorizar tempranas)

**Justificación:**
- Opción A se adapta automáticamente a fase del proyecto
- Opción C refuerza preservación de decisiones fundacionales
- Combinación: máxima eficiencia sin intervención manual
- Aprovecha capacidad 200K tokens de LLMs modernos

**Implementación:**

1. **Modificar memsys3_templates/prompts/compile-context.md:**
   - Agregar PASO 0: "Determinar fase del proyecto"
   - Implementar tabla de límites dinámicos
   - Documentar filosofía por fase
   - Actualizar instrucciones de compilación con límite variable

2. **Actualizar criterio de sessions:**
   - Sesiones 1-10: prioridad MUY ALTA (incluir completas)
   - Sesiones 11-50: prioridad ALTA (highlights + decisions)
   - Sesiones 50+: prioridad según criticidad + recencia

3. **Calibrar límites mediante testing:**
   - Compilar proyectos reales en diferentes fases
   - Medir tokens generados por fase
   - Ajustar límites si necesario (3000/2500/2000)

4. **Actualizar ADR-001:**
   - Documentar límite dinámico (no fijo 2000)
   - Mantener filosofía "criterio inteligente"
   - Agregar tabla de límites por fase

5. **Sincronizar con memsys3/prompts/compile-context.md** (dog-fooding)

6. **Testing exhaustivo:**
   - Proyecto inception (<10 sesiones): verificar ~50K tokens en context
   - Proyecto early dev (20 sesiones): verificar ~40K tokens
   - Proyecto mature (100 sesiones): verificar ~30K tokens (actual)
   - Validar que compilaciones son menos frecuentes en proyectos jóvenes

---

## Casos de Uso / Ejemplos

### Ejemplo 1: Proyecto nuevo (5 sesiones)
**Antes (límite fijo 2000 líneas):**
- Context Agent filtra agresivamente desde inicio
- Incluye 3 de 5 sesiones (síntesis)
- context.yaml: 800 líneas (~12K tokens)
- Main Agent usa ~30K tokens totales
- **Problema:** 170K tokens sin usar, decisiones fundacionales filtradas

**Después (límite dinámico 3000 líneas):**
- Context Agent en modo INCEPTION
- Incluye 5 de 5 sesiones (completas)
- context.yaml: 1800 líneas (~27K tokens)
- Main Agent usa ~50K tokens totales
- **Beneficio:** Decisiones fundacionales preservadas, contexto rico

### Ejemplo 2: Proyecto maduro (200 sesiones)
**Antes y Después (límite 2000 líneas):**
- Context Agent filtra inteligentemente
- Incluye top 20 sesiones más críticas (síntesis)
- context.yaml: 2000 líneas (~30K tokens)
- Main Agent usa ~70K tokens totales
- **Sin cambios:** Filtrado agresivo es correcto en fase legacy

---

## Referencias

- **ADR relacionado:** ADR-001 (Criterio inteligente CA), ADR-002 (Rotación)
- **Prompt afectado:** `memsys3/prompts/compile-context.md`
- **Capacidad LLM:** Claude Sonnet 4.5 (200K tokens), Gemini 1.5 Pro (1M tokens)
- **Observación usuario:** 2025-01-30
- **Filosofía memsys3:** "Criterio inteligente, NO límites arbitrarios"

---

## Notas Adicionales

**Ventajas adicionales:**
1. **Menos compilaciones en proyectos jóvenes:**
   - Proyecto inception: compilar cada 5-8 sesiones (vs 2-3 actual)
   - Ahorro de trabajo Context Agent

2. **Mejor onboarding de nuevos agents:**
   - Agente nuevo en proyecto joven tiene contexto fundacional completo
   - No necesita leer archivos full/ para entender decisiones tempranas

3. **Escalabilidad mejorada:**
   - Proyectos pequeños: uso eficiente de ventana contexto
   - Proyectos grandes: filtrado agresivo (como ahora)

**Riesgos a mitigar:**
1. **Límites demasiado altos:**
   - Si 3000 líneas genera >200K tokens → reducir a 2500
   - Calibración empírica necesaria

2. **Complejidad adicional en compile-context.md:**
   - Context Agent debe contar sesiones correctamente
   - Incluir sessions.yaml + sessions_*.yaml en conteo

**Métrica de éxito:**
- Proyectos inception (1-10 sesiones): compilar cada 5+ sesiones (vs 2-3 actual)
- Context.yaml en inception: 1500-2500 líneas (~25-40K tokens)
- Main Agent reporta "contexto suficiente" sin compilaciones frecuentes

**Filosofía memsys3 reforzada:**
> "El sistema debe adaptarse a las necesidades del proyecto,
> no forzar al proyecto a adaptarse al sistema."

**Testing requerido:**
- [ ] Implementar límite dinámico en compile-context.md
- [ ] Compilar proyecto real con 5 sesiones (inception)
- [ ] Compilar proyecto real con 30 sesiones (early dev)
- [ ] Compilar proyecto real con 150 sesiones (mature)
- [ ] Medir tokens por fase y ajustar límites
- [ ] Validar frecuencia de compilaciones reducida en inception
- [ ] Actualizar ADR-001 con límites dinámicos
- [ ] Sincronizar fix con memsys3/ (dog-fooding)
