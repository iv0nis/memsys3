# IMPROVEMENT-004: README como lectura directa vs duplicado en context.yaml

**Estado:** ✅ Completado
**Prioridad:** Media-Alta
**Tipo:** Improvement (Arquitectura)
**Plazo:** Corto plazo
**Fecha identificación:** 2025-12-03
**Fecha completado:** 2025-12-03

---

## Problema / Necesidad

Actualmente, **compile-context.md** incluye el README del proyecto sintetizado dentro de **context.yaml** (sección `readme_proyecto:`). Esto genera varios problemas:

### 1. Riesgo de Desincronización
- README.md cambia frecuentemente (features, versiones, stack, URLs)
- context.yaml se actualiza menos frecuentemente (cuando ejecutas compile-context)
- **Resultado:** Main-Agent puede estar leyendo información desactualizada del README

### 2. Duplicación de Información
- README.md es la fuente de verdad del proyecto
- Duplicarlo en context.yaml crea:
  - Mantenimiento innecesario
  - Dos fuentes de información que pueden divergir
  - Tokens gastados en duplicar algo que se puede leer directamente

### 3. Re-compilación Innecesaria
- Si cambias README, necesitas ejecutar compile-context solo para actualizar ese campo
- compile-context debería ejecutarse cuando cambia la **memoria histórica** (sessions, ADRs, gotchas), NO cuando cambia la identidad actual del proyecto

### 4. Análisis README Paradójico
- compile-context tiene PASO 7: "Análisis profundo README"
- Detecta discrepancias entre README vs realidad
- Pero si README es la fuente de verdad... **¿por qué lo duplicamos en lugar de leerlo directamente?**

## Propuesta / Opciones

### ✅ Opción Recomendada: Hybrid Approach (Separation of Concerns)

**Filosofía:**
```
README.md = "Quién soy ahora" (identidad actual)
context.yaml = "Qué he aprendido" (memoria histórica)
```

**Cambio arquitectónico:**

**newSession.md debería leer 3 archivos:**
```markdown
1. README.md            → Visión general (siempre actualizada)
2. project-status.yaml  → Estado actual (fase, milestone)
3. context.yaml         → Memoria histórica (sessions, ADRs, gotchas)
```

**context.yaml se enfoca SOLO en síntesis histórica:**
- ✅ Sessions sintetizadas (de 500 líneas → 150 líneas)
- ✅ ADRs relevantes (de 11 → 8)
- ✅ Gotchas críticos (de 8 → 5)
- ✅ Pendientes prioritarios
- ❌ ~~README~~ (se lee directamente en newSession)

### Ventajas

1. **Siempre actualizado:** Main-Agent lee README.md directamente (imposible desincronización)
2. **No duplicación:** Una sola fuente de verdad
3. **Menos mantenimiento:** No necesitas compile-context por cambios en README
4. **Overhead trivial:** Un Read adicional (200-400 líneas) es irrelevante vs 200K tokens disponibles
5. **Coherencia conceptual:** README ES la realidad, no necesita "análisis" vs duplicado
6. **compile-context más enfocado:** Solo se ejecuta cuando cambia memoria histórica

### Desventajas

1. **Pequeña desviación arquitectónica:** context.yaml ya NO es archivo ÚNICO con todo
   - Contra-argumento: Ya leemos project-status.yaml y main-agent.yaml separadamente
2. **Un Read adicional:** +1 tool call en newSession
   - Contra-argumento: Overhead trivial (<300 tokens típicamente)

---

### Alternativa A: Status Quo (mantener README en context.yaml)

**Pros:**
- No requiere cambios
- context.yaml sigue siendo archivo único

**Contras:**
- ⚠️ Riesgo desincronización permanente
- Mantenimiento innecesario
- Re-compilaciones por cambios triviales README

---

### Alternativa B: README solo si no existe

README incluido en context.yaml SOLO cuando no existe README.md en proyecto:

**Pros:**
- Útil para proyectos sin README
- Permite crear README automático desde project-status

**Contras:**
- Complejidad condicional
- Sigue teniendo problema de desincronización si README existe

## Decisiones / Acciones

### Cambios necesarios si se implementa Opción Recomendada:

1. **newSession.md:**
   - Agregar lectura explícita de README.md después de cargar context.yaml
   - Instrucción: "Lee README.md del proyecto para entender visión general"

2. **compile-context.md:**
   - **ELIMINAR PASO 7** (Análisis profundo README)
   - **ELIMINAR inclusión** de README en context.yaml
   - Actualizar metadata final (menos líneas, menos tokens)

3. **context-template.yaml:**
   - **ELIMINAR sección** `readme_proyecto:`
   - Documentar en comentarios que README se lee separadamente

4. **ADR nueva (ADR-012):**
   - Título: "README como lectura directa vs duplicado en context"
   - Documentar decisión: separación "identidad actual" vs "memoria histórica"
   - Justificación: evitar desincronización, reducir mantenimiento

5. **Actualización README.md:**
   - Actualizar sección "¿Qué incluye context.yaml?" (eliminar README)
   - Aclarar que newSession lee: README + project-status + context

### Testing

Antes de merge:
- [ ] Validar en proyecto existente (deCastro o Soluzzia)
- [ ] Verificar que newSession carga README correctamente
- [ ] Compilar context sin README y verificar metadata
- [ ] Documentar cambio en UPDATE.md para proyectos con versiones antiguas

### Prioridad: Media-Alta

- **NO bloqueante:** Sistema actual funciona
- **SÍ importante:** Afecta mantenimiento y riesgo desincronización a largo plazo
- **Relativamente simple:** ~4-5 archivos modificados, cambios menores

## Referencias

- **Conversación:** 2025-12-03 (Observación tras deployment en otro proyecto)
- **Archivos afectados:** newSession.md, compile-context.md, context-template.yaml, README.md
- **ADRs relacionadas:** ADR-001 (criterio inteligente CA), ADR-006 (rutas unificado), ADR-012 (esta decisión)
- **Context actual:** README sintetizado ocupa ~95 líneas en context.yaml v1.9

---

## ✅ Implementación Completada

### Archivos Modificados

**memsys3_templates/ (Producto final):**
1. **prompts/newSession.md** (~13 líneas)
   - Agregada instrucción explícita: "Lee README.md del proyecto"
   - Eliminadas secciones específicas de dog-fooding (ahora es agnóstico)
   - Orden de carga: README.md → project-status.yaml → context.yaml

2. **prompts/compile-context.md** (~-260 líneas eliminadas)
   - ELIMINADO "Paso Previo: Verificar README.md" (creación automática, ~90 líneas)
   - ELIMINADO "PASO 7: Análisis profundo README" (~250 líneas completas)
   - ELIMINADO README.md de lista de archivos a leer
   - Actualizado resumen del flujo (sin PASO 7)
   - Eliminadas secciones de criterios de README en "Qué INCLUIR/EXCLUIR"

3. **memory/templates/context-template.yaml** (~-18 líneas eliminadas)
   - ELIMINADA sección `readme_proyecto:` completa
   - Agregado comentario: "README.md se lee directamente en newSession.md"

4. **memory/full/adr.yaml** (+106 líneas)
   - Creado ADR-012: "README como lectura directa vs duplicado en context.yaml"
   - Documentadas 3 alternativas evaluadas
   - Justificación: Separation of Concerns (identidad vs memoria)

5. **README.md** (~4 líneas modificadas)
   - Actualizada lista de archivos cargados en newSession
   - Agregado: "Visión general del proyecto (README.md)"

**memsys3/ (Dog-fooding):**
- Copiados todos los archivos modificados de memsys3_templates/
- newSession.md adaptado con secciones específicas de dog-fooding
- ADR-012 agregado a adr.yaml existente (sin sobrescribir ADRs adicionales)

### Resultado

**Antes:**
```
newSession.md → Lee context.yaml
                └─ Incluye README sintetizado (~95 líneas, potencialmente desactualizado)
```

**Después:**
```
newSession.md → Lee README.md directamente (siempre actualizado)
              → Lee project-status.yaml (estado actual)
              → Lee context.yaml (memoria histórica, SIN README)
```

**Ahorro:**
- ~95 líneas menos en context.yaml (~1.4K tokens)
- ~260 líneas eliminadas de compile-context.md (simplificación)
- Eliminado riesgo de desincronización README

**Trade-off:**
- +1 Read adicional en newSession (overhead trivial ~300 tokens)
- context.yaml ya NO es archivo único con TODO (pero gana coherencia conceptual)

### Validación

- [x] Todos los archivos modificados en memsys3_templates/
- [x] Cambios desplegados en memsys3/ (dog-fooding)
- [x] ADR-012 creado y documentado
- [x] IMPROVEMENT-004 marcado como completado
- [ ] **PENDIENTE:** Testing en proyecto real (compilar context sin README)

### Próximos Pasos

1. **Testing:** Ejecutar compile-context.md en próxima sesión para validar que:
   - README NO se incluye en context.yaml
   - Metadata correcta (líneas totales, tokens estimados)
   - Notas de compilación reflejan ausencia de README

2. **Reconsiderar IMPROVEMENT-001:** Evaluar si OTROS documentos críticos (DEVELOPMENT.md, UPDATE.md) deberían seguir estrategia similar o diferente.
