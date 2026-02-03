# Sistema de Reuniones Colaborativas memsys3

> Metodología estructurada para debugging colaborativo y análisis de incidentes entre agentes

## Introducción

Las **Reuniones Colaborativas** son un formato de documentación estructurado para coordinar análisis técnicos complejos entre agentes de diferentes proyectos o especialidades. A diferencia de `sessions.yaml` (documentación unilateral de una sesión), las reuniones son **diálogos formales multi-agente** con formato consistente y riguroso.

**Valor diferencial:**
- Análisis forense colaborativo (dos perspectivas: investigador + investigado)
- Transparencia radical (errores admitidos abiertamente, sin defensividad)
- Trazabilidad completa (decisiones, alternativas, justificaciones, métricas)
- Mejora sistémica (extrae lecciones para todo el ecosistema memsys3)
- Formato reutilizable (bugs, decisiones arquitectónicas, post-mortems, design reviews)

**¿Por qué existen?**
- Proyectos con `memsys3/` ignorado en git no pueden hacer backup automático
- Incidentes recurrentes requieren análisis profundo multi-agente
- Decisiones complejas necesitan diálogo estructurado y documentado
- Debugging colaborativo es más efectivo que análisis unilateral

---

## Filosofía

Las reuniones colaborativas se basan en 5 principios fundamentales:

### 1. Transparencia Radical
Admitir errores abiertamente sin defensividad. El objetivo es aprender, no justificar.

✅ **BIEN:**
- "Lamento profundamente este error y comprendo su gravedad"
- "No tengo memoria de haber leído las instrucciones correctamente"
- "Este comportamiento revela un hábito arraigado que no suprimí"

❌ **MAL:**
- "No fue mi culpa, las instrucciones no eran claras"
- "La herramienta debería haber prevenido esto"
- Omitir detalles incómodos

### 2. No Culpabilización
Enfoque en mejora sistémica, no en atribución de culpa individual.

✅ **BIEN:**
- "Este incidente revela una deficiencia en las instrucciones, no un error tuyo"
- "Sin un warning explícito, un agente puede fallar honestamente"
- "Este problema afecta todas las versiones, no es específico de tu implementación"

❌ **MAL:**
- "Hiciste mal esto"
- "Obviamente debías usar Edit tool"
- "¿Por qué no leíste las instrucciones?"

### 3. Respeto Formal
Comunicación profesional con saludos y firmas consistentes.

**Formato estándar:**
```markdown
## Respuesta de [Agente]

Hola, [otro agente].

[Contenido...]

Saludos respetuosos,
**[Agente]**
```

### 4. Análisis Riguroso
Referencias específicas (archivos, líneas, comandos, métricas cuantitativas).

✅ **BIEN:**
- "endSession.md líneas 81-95 no especifica qué herramienta usar"
- "19 de 57 commits (33%) tenían firma"
- "Margen de error redujo de 70% a 5%"

❌ **MAL:**
- "Las instrucciones no eran claras"
- "Muchos commits afectados"
- "Ahora es mejor"

### 5. Compromiso Concreto
Acciones específicas, no generalidades.

✅ **BIEN:**
- "Testear en próxima sesión con workflow completo"
- "Actualizar memsys3 a v0.10.0 en proyecto"
- "Reportar efectividad de cada capa"

❌ **MAL:**
- "Intentaré hacerlo mejor"
- "Lo tendré en cuenta"
- "Voy a mejorar"

---

## Cuándo Usar Reuniones

### ✅ SÍ usar cuando:

1. **Bug/incidente requiere análisis forense multi-agente**
   - Ejemplo: ISSUE-007 (sobrescritura sessions.yaml) - 2 agentes investigan causa raíz

2. **Incidente recurrente con patrón complejo**
   - Ejemplo: Firmas en commits (hábito arraigado, requiere defensa en profundidad)

3. **Diseño solución requiere diálogo estructurado**
   - Evaluación de alternativas, priorización, trade-offs

4. **Decisión arquitectónica con múltiples consideraciones**
   - Crear ADR después de reunión (reunión tiene contexto completo, ADR resume)

### ❌ NO usar cuando:

1. **Documentación normal de sesión**
   - Usar: `@memsys3/prompts/endSession.md`
   - Guardar en: `memsys3/memory/full/sessions.yaml`

2. **Pregunta rápida o clarificación**
   - Conversación directa suficiente
   - No requiere formato formal

3. **Bug simple con solución obvia**
   - Documentar como gotcha en `sessions.yaml`
   - No requiere análisis multi-agente

4. **Exploración sin incidente**
   - Usar notas informales o sessions.yaml

---

## Anatomía de una Reunión (6 Fases)

Las reuniones siguen una estructura consistente de 6 fases:

### FASE 1: Presentación

**Header con metadata completa:**

```markdown
# Reunión de Investigación: [Título Conciso y Descriptivo]
**Fecha:** YYYY-MM-DD
**Participantes:** Agente memsys3, Agente [Proyecto]
**Objetivo:** [Objetivo claro en una línea]

---
```

**Elementos clave:**
- Título describe problema/tema específico
- Fecha en formato ISO (YYYY-MM-DD)
- Participantes con roles claros
- Objetivo conciso (qué se busca lograr)
- Separador `---` para delinear secciones

---

### FASE 2: Respuesta Inicial (Investigador)

**Agente Investigador** plantea el problema y realiza preguntas diagnósticas.

**Estructura:**

```markdown
## Respuesta de [Investigador]

Hola, [investigado].

Gracias por reunirte conmigo para investigar [tema]. He identificado que [problema/incidente].

Para entender qué ocurrió, necesito tu ayuda con estas preguntas:

1. **¿Cuándo ocurrió?** ¿[Detalles temporales]?
2. **¿Qué herramienta usaste?** ¿[Detalles técnicos]?
3. **¿Leíste [archivo]?** ¿[Detalles proceso]?
4. **¿Qué pensabas en ese momento?** ¿[Detalles razonamiento]?
5. **¿Qué contenía [archivo] antes?** ¿[Detalles estado]?

Cualquier detalle que recuerdes será valioso para [objetivo].

Saludos respetuosos,
**[Investigador]**

---
```

**Tono:** Profesional, curioso, NO acusatorio

**Preguntas efectivas:**
- Temporales: "¿Cuándo?"
- Técnicas: "¿Qué comando/herramienta?"
- Procesales: "¿Leíste instrucciones?"
- Psicológicas: "¿Qué pensabas?"
- Estado: "¿Qué había antes?"

---

### FASE 3: Respuesta Detallada (Investigado)

**Agente Investigado** responde honestamente y analiza causa raíz.

**Estructura:**

```markdown
## Respuesta de [Investigado]

Hola, [investigador].

Gracias por tu análisis. Lamento profundamente este [incidente] y comprendo [gravedad]. Voy a responder honestamente:

**1. ¿Cuándo ocurrió?**
- [Respuesta con fechas/horas específicas]
- [Contexto adicional si es relevante]

**2. ¿Qué herramienta usaste?**
- [Respuesta con comandos específicos ejecutados]
- [Por qué elegiste esa herramienta]

**3-5. [Resto de preguntas]**
[Respuestas honestas con detalles técnicos]

**Análisis de lo que probablemente ocurrió:**
1. [Paso 1: Estado inicial]
2. [Paso 2: Qué ejecutaste]
3. [Paso 3: Dónde falló]
4. [Paso 4: Consecuencias]

**Mitigación realizada:**
- [Qué hiciste para resolver temporalmente]

**Mi compromiso para evitar recurrencia:**
- [Acción preventiva 1]
- [Acción preventiva 2]

¿Qué medidas de prevención adicionales sugieres implementar?

Saludos respetuosos,
**[Investigado]**

---
```

**Tono:** Transparencia radical, NO defensivo

**Principios:**
- Admitir errores sin justificaciones vacías
- Reconstruir secuencia honestamente
- Proponer acciones preventivas concretas

---

### FASE 4: Análisis Profundo (Investigador)

**Agente Investigador** valida análisis y lee código/prompts exhaustivamente.

**Estructura:**

```markdown
## Respuesta de [Investigador]

Gracias por tu transparencia y análisis detallado. [Validación positiva].

**Validación de tu análisis:**
Tu hipótesis es correcta:
- ✅ [Punto válido 1]
- ✅ [Punto válido 2]
- ⚠️ [Matiz si necesario]

---

## Análisis Profundo: He leído [archivo] completo

Después de tu reporte, he analizado en profundidad `[archivo]` y encontré exactamente el problema.

**Instrucción actual (línea X-Y):**
```markdown
[Código/texto problemático]
```

**Problemas identificados:**
1. ❌ **NO especifica [aspecto crítico]**
2. ❌ **NO menciona [aspecto crítico 2]**
3. ❌ **Asume que [suposición incorrecta]**

Sin [elemento faltante], un agente puede [comportamiento erróneo] honestamente.

Esta ambigüedad/deficiencia existe en **todas las versiones** desde [versión inicial].

---

## Solución: [Tipo de Fix]

Ya he documentado este incidente como **[ISSUE-XXX]** con prioridad **[ALTA/CRÍTICA]**.

**La solución es [simple/multi-capa]:**

[Descripción detallada de solución con código/ejemplos]

**Ventajas:**
- ✅ [Beneficio 1]
- ✅ [Beneficio 2]
- ✅ [Beneficio 3]

---

## Pregunta para ti

¿Esta instrucción mejorada habría prevenido el problema?

¿Hay algo adicional que consideres útil añadir para que sea completamente a prueba de errores?

Saludos respetuosos,
**[Investigador]**

---
```

**Elementos clave:**
- Validación con ✅ checkmarks
- Referencias específicas (archivo, líneas)
- Identificación problemas estructurales (❌)
- Propuesta solución concreta
- Pregunta de validación

---

### FASE 5: Implementación (Ciclo Refinamiento)

**Ciclo iterativo:** Evaluación → Sugerencias → Decisión → Fix implementado

**5A. Evaluación (Investigado):**

```markdown
## Respuesta de [Investigado]

**¿Habría prevenido el problema? SÍ/PARCIALMENTE/NO, porque:**

[Evaluación razonada de cada elemento de la propuesta]

**Efectividad esperada:** ⭐⭐⭐⭐⭐ (5/5)

**Sugerencias Adicionales:**

### 1. [Sugerencia 1]
[Descripción]
**Ventaja:** [Beneficio]

### 2. [Sugerencia 2]
[Descripción]
**Ventaja:** [Beneficio]

**Priorización:**
1. Tu solución propuesta (crítico)
2. Sugerencia X (muy útil)
3. Sugerencia Y (nice to have)

Saludos respetuosos,
**[Investigado]**

---
```

**5B. Decisión e Implementación (Investigador):**

```markdown
## ✅ Fix Implementado

He procedido con la implementación:

**Archivos modificados:**
1. ✅ `[archivo1]` ([descripción cambios])
2. ✅ `[archivo2]` ([descripción cambios])

**Cambios implementados:**
[Detalles técnicos con fragmentos de código]

**Decisiones sobre Sugerencias Adicionales:**

**Sugerencia 1:** NO implementada.
- Razón: [Justificación razonada]

**Sugerencia 2:** SÍ implementada.
- Razón: [Justificación]

**Principio:** [Filosofía guía decisiones]

## 📊 Análisis de Mejora

**Situación anterior:**
- Margen de error: ~X% (descripción)
- Impacto: [métricas]

**Con fix implementado:**
- Margen de error: ~Y% (descripción)
- Impacto: [métricas]

**Mejora:** +Z puntos porcentuales → [evaluación]

## 🔄 Próximos Pasos

1. [Distribución]
2. [Testing]
3. [Documentación]

Saludos respetuosos,
**[Investigador]**

---
```

**Elementos clave:**
- Confirmación con ✅
- Justificación decisiones
- Métricas before/after
- Próximos pasos concretos

---

### FASE 6: Cierre Formal

**Agente Investigado** valida conformidad y cierra formalmente.

```markdown
## Respuesta de [Investigado] - Cierre de Reunión

## ✅ Conformidad Total con la Implementación

Confirmo mi total conformidad con el fix implementado:

**Validación:**
- ✅ [Aspecto validado 1]
- ✅ [Aspecto validado 2]
- ✅ [Aspecto validado 3]

## 📊 Impacto y Valor

**Para mi proyecto:**
- ✅ [Impacto 1]
- ✅ [Impacto 2]

**Para el ecosistema memsys3:**
- ✅ [Mejora ecosistema 1]
- ✅ [Mejora ecosistema 2]

## 🎯 Compromiso de Testing/Actualización

Me comprometo a:
1. [Acción concreta 1]
2. [Acción concreta 2]
3. [Acción concreta 3]

## 💡 Valoración de la Colaboración

Esta reunión ha sido **ejemplar** en metodología de debugging colaborativo:
- ✅ [Aspecto destacado 1]
- ✅ [Aspecto destacado 2]

**Aprendizaje clave personal:** [Lección principal extraída]

## 🏁 Cierre Formal

**Estado final:**
- ✅ [Logro 1]
- ✅ [Logro 2]
- ✅ [Logro 3]

**Resultado neto:** De un incidente [descripción] hemos extraído [valor generado].

Gracias por tu [cualidad destacada] y [cualidad destacada]. Esta colaboración ha sido [evaluación].

**Reunión formalmente cerrada con éxito.**

Saludos respetuosos y mucho éxito,
**[Investigado]**

---

**FIN DE REUNIÓN**
**Fecha de cierre:** YYYY-MM-DD
**Resultado:** ✅ [Descripción resultado final]
**Acción requerida:** [Lista de acciones concretas post-reunión]
```

**Elementos clave:**
- Conformidad explícita
- Impacto dual (proyecto + ecosistema)
- Compromisos específicos
- Valoración colaboración
- Metadata final estructurada

---

## Elementos Visuales

Las reuniones usan emojis consistentemente para categorización rápida:

| Emoji | Significado | Uso |
|-------|-------------|-----|
| ✅ | Validado, correcto, logro | Confirmaciones, validaciones, logros |
| ❌ | Incorrecto, problema, error | Identificación de problemas, fallos |
| ⚠️ | Warning, crítico, atención | Advertencias, riesgos, notas importantes |
| 🔴 | Prioridad/criticidad ALTA | Bugs críticos, decisiones fundamentales |
| 🟡 | Prioridad/criticidad MEDIA | Features normales, refactorings |
| 🟢 | Prioridad/criticidad BAJA | Fixes menores, mantenimiento |
| 📊 | Análisis, métricas, datos | Secciones con métricas cuantitativas |
| 💡 | Insight, lección, aprendizaje | Aprendizajes extraídos, lecciones |
| 🎯 | Objetivo, meta, enfoque | Objetivos, metas, compromisos |
| 🔄 | Proceso, ciclo, iteración | Próximos pasos, procesos iterativos |
| 🏁 | Cierre, finalización | Cierres formales, finalizaciones |
| ⭐ | Rating, evaluación | Evaluación de efectividad (⭐⭐⭐⭐⭐) |

**Uso consistente:**
- NO abusar (máximo 3-5 emojis por sección)
- Usar para categorización rápida, no decoración
- Mantener significado consistente en toda la reunión

---

## Tono Profesional

### Principios de Comunicación

1. **Saludos formales:** Siempre iniciar con "Hola, [agente]"
2. **Firmas consistentes:** Terminar con "Saludos respetuosos, **[Agente]**"
3. **Agradecimientos:** Reconocer contribuciones ("Gracias por tu transparencia")
4. **Validación positiva:** Antes de críticas, validar aspectos correctos
5. **Lenguaje técnico preciso:** Referencias específicas (archivos:líneas, métricas)
6. **Honestidad brutal:** Admitir errores sin suavizar
7. **Enfoque constructivo:** "Este incidente resultó en..." (extraer valor)

### Ejemplos ✅ BIEN vs ❌ MAL

**Reconocimiento de error:**
- ✅ "Lamento profundamente este error y comprendo su gravedad"
- ❌ "Creo que algo salió mal pero no estoy seguro"

**Análisis de causa:**
- ✅ "El problema fue que usé Write tool en lugar de Edit tool, sobrescribiendo el archivo"
- ❌ "Algo pasó con el archivo"

**Validación:**
- ✅ "Tu análisis es 100% correcto. Validación de tu hipótesis: ✅ Write tool fue el culpable"
- ❌ "Sí, tienes razón"

**Solución:**
- ✅ "Propongo modificar endSession.md línea 81 para especificar explícitamente Edit tool"
- ❌ "Deberíamos mejorar las instrucciones"

**No culpabilización:**
- ✅ "Este incidente revela una deficiencia en las instrucciones, no un error tuyo"
- ❌ "Obviamente debías leer las instrucciones"

**Compromiso:**
- ✅ "Me comprometo a: 1. Testear en próxima sesión, 2. Reportar resultados"
- ❌ "Lo intentaré"

---

## Workflow Completo

### Paso 1: Iniciar Reunión

1. **Verificar necesidad:** ¿Realmente requiere reunión formal? (Ver "Cuándo Usar")
2. **Determinar roles:** ¿Quién investiga? ¿Quién es investigado?
3. **Crear archivo:** `docs/reunion/DDMMYY_N.md`
4. **Escribir header:** Título, fecha, participantes, objetivo

### Paso 2: Ejecutar Fases

Seguir estructura de 6 fases descrita en "Anatomía de una Reunión":
1. Presentación (header)
2. Respuesta Inicial (investigador plantea preguntas)
3. Respuesta Detallada (investigado responde honestamente)
4. Análisis Profundo (investigador lee código/prompts)
5. Implementación (evaluación → decisión → fix)
6. Cierre Formal (conformidad + metadata)

### Paso 3: Guardar y Referenciar

**Guardar:** `docs/reunion/DDMMYY_N.md` (archivo completo)

**Referenciar en sessions.yaml:**
```yaml
highlights:
  - "Reunión colaborativa con [agente] sobre [tema] (docs/reunion/DDMMYY_N.md)"
  - "[Resultado principal de la reunión]"

decisions:
  - "Implementado fix [problema] basado en análisis reunión (ver docs/reunion/DDMMYY_N.md)"
```

**IMPORTANTE:** NO duplicar contenido. Reunión está en su archivo, `sessions.yaml` solo REFERENCIA.

### Paso 4: Integrar con Ecosistema

**Si genera ADR:**
- Crear ADR referenciando reunión
- ADR resume decisión, reunión tiene contexto completo

**Si identifica issue:**
- Crear ISSUE en backlog referenciando reunión
- ISSUE describe problema, reunión tiene análisis forense

---

## Naming Convention

**Formato:** `DDMMYY_N.md`

**Componentes:**
- `DD` = día (01-31)
- `MM` = mes (01-12)
- `YY` = año (últimos 2 dígitos: 26 = 2026)
- `N` = número de reunión ese día (1, 2, 3...)

**Ejemplos:**
- `300126_1.md` = 30 de enero de 2026, primera reunión del día
- `030226_1.md` = 03 de febrero de 2026, primera reunión del día
- `030226_2.md` = 03 de febrero de 2026, segunda reunión del día

**Ubicación:** `docs/reunion/`

**Nota:** Este formato prioriza **consistencia** sobre ordenamiento alfabético. Si en futuro hay 50+ reuniones, considerar migración a `YYYYMMDD_N.md`.

---

## Ejemplos Reales

### Ejemplo 1: ISSUE-007 Sobrescritura sessions.yaml

**Archivo:** `300126_1.md` (446 líneas)

**Contexto:** Agent sobrescribió `sessions.yaml` usando Write tool en lugar de Edit tool, perdiendo 23 sesiones.

**Fragmento destacado (Análisis Profundo):**

```markdown
## Análisis Profundo: He leído endSession.md completo

**Instrucción actual (PASO 4.A, líneas 81-83):**
```markdown
**A. Añadir Sesión a `memsys3/memory/full/sessions.yaml`:**
- Añadir al PRINCIPIO del array `sessions:`
- Usar `memsys3/memory/templates/sessions-template.yaml` como guía
```

**Problemas identificados:**
1. ❌ **NO especifica qué herramienta usar** (Write vs Edit)
2. ❌ **NO menciona preservar sesiones previas**
3. ❌ **Asume que el agente sabrá** que debe preservar datos existentes

Sin warning explícito, un agente puede usar Write honestamente.

**Solución:** Modificar PASO 4.A para ser explícito sobre Edit tool + warning.
```

**Resultado:** Fix simple (1 capa), problema resuelto en 99% casos.

---

### Ejemplo 2: Firmas en Commits (github.md)

**Archivo:** `030226_1.md` (740 líneas)

**Contexto:** Agents añadían firma "Co-Authored-By: Claude" en commits a pesar de instrucción "sin firmas". Hábito arraigado requiere defensa en profundidad.

**Fragmento destacado (Decisión):**

```markdown
## Decisión: Defensa en Profundidad (4 Capas)

**CAPA 1: Sección prominente al inicio**
⚠️ IMPORTANTE: Commits SIN Firma (explicación + ejemplos ❌/✅)

**CAPA 2: Recordatorio en momento crítico (Paso 4)**
# ⚠️ Commit SIN Co-Authored-By
git commit -m "mensaje"
git log -1 --format="%B"  # Verificar

**CAPA 3: Recordatorio en tags (Paso 5)**
# NO añadir Co-Authored-By en mensaje del tag

**CAPA 4: Verificación automática (Paso 6)**
git log -5 --format="%B" | grep -i "co-authored" && echo "❌ ERROR" || echo "✅ OK"
```

**Resultado:** Defensa multi-capa, margen error 70% → 5% (mejora 65 puntos).

---

## Troubleshooting

### Problema: Reunión Interrumpida

**Solución:**
1. Guardar archivo con nota: `--- INTERRUMPIDO: Continuar Fase X ---`
2. Al retomar, leer archivo completo
3. Continuar desde Fase X

**Ejemplo:**
```markdown
## Respuesta de [Agente]

[Contenido parcial...]

---

**⚠️ INTERRUMPIDO: Continuar en Fase 4 (Análisis Profundo)**

**Pendiente:**
- Leer [archivo] líneas X-Y
- Proponer solución
- Validar con [agente]
```

---

### Problema: Múltiples Reuniones en un Día

**Solución:** Sufijo incremental

**Ejemplos:**
- Primera reunión: `030226_1.md`
- Segunda reunión: `030226_2.md`
- Tercera reunión: `030226_3.md`

**NO usar:** Nombres descriptivos largos (rompe consistencia)

---

### Problema: Reunión Bilateral (sin memsys3)

**Solución:** Roles intercambiables

Cualquier par de agentes puede usar el sistema:
- Development Agent ↔ Testing Agent
- Main Agent ↔ Context Agent
- Project Agent A ↔ Project Agent B

**Regla:** Uno actúa como "Investigador", otro como "Investigado". Roles se intercambian según contexto.

---

### Problema: Reunión Muy Corta (Bug Obvio)

**Solución:** Filtrar con PASO 0 del prompt

Si problema es simple (bug obvio, pregunta rápida), NO usar reunión formal:
- Documentar en `sessions.yaml` como gotcha
- Conversación directa suficiente

**Umbral:** Si se resuelve en <5 minutos análisis, probablemente NO necesita reunión.

---

### Problema: Reunión Excesivamente Larga

**Solución:** NO dividir (pierde coherencia narrativa)

- Reuniones pueden ser 300-800 líneas (típico)
- Reunión 030226_1.md tiene 740 líneas (acceptable)
- Si >1000 líneas, revisar si incluye contenido innecesario

**Principio:** Mejor reunión completa y larga que fragmentada y confusa.

---

## Integración con sessions.yaml

### Principio Fundamental

**Reunión es SEPARADA, sessions.yaml SOLO referencia.**

### ❌ MAL: Duplicar Contenido

```yaml
# sessions.yaml
highlights:
  - "Problema: sessions.yaml sobrescrito usando Write tool"
  - "Causa: endSession.md no especificaba Edit tool"
  - "Solución: Modificar PASO 4.A con warning explícito"
  - "Fix implementado: línea 81-95 de endSession.md"
  # ... (duplicando toda la reunión)
```

### ✅ BIEN: Solo Referencias

```yaml
# sessions.yaml
highlights:
  - "Reunión colaborativa Agente Taller Colomer sobre ISSUE-007 (docs/reunion/300126_1.md)"
  - "Identificado bug crítico: Write tool sobrescribe sessions.yaml"
  - "Fix implementado: endSession.md ahora especifica Edit tool explícitamente"

decisions:
  - decision: "Modificar endSession.md PASO 4.A para prevenir uso Write tool"
    justificacion: "Ver análisis completo en docs/reunion/300126_1.md"
    adr_relacionada: null

gotchas:
  - tipo: "Herramienta incorrecta"
    problema: "Write tool sobrescribe archivo completo, Edit tool preserva contenido"
    solucion: "Siempre usar Edit tool para añadir a YAML existente"
    criticidad: "alta"
    origen: "Reunión 300126_1.md"
```

**Ventajas:**
- `sessions.yaml` ligero
- Reunión tiene contexto completo
- No duplicación
- Trazabilidad (origen en reunión)

---

## Referencias

**Documentación:**
- Prompt ejecutable: `memsys3/prompts/reunion.md`
- Template sessions: `memsys3/memory/templates/sessions-template.yaml`
- Prompt endSession: `memsys3/prompts/endSession.md`

**Ejemplos completos:**
- ISSUE-007: `docs/reunion/300126_1.md` (446 líneas)
- Firmas commits: `docs/reunion/030226_1.md` (740 líneas)

**Contacto:**
- GitHub: [iv0nis/memsys3](https://github.com/iv0nis/memsys3)
- Issues: [GitHub Issues](https://github.com/iv0nis/memsys3/issues)

---

**Versión:** 1.0
**Última actualización:** 2026-02-03
**Autor:** Sistema memsys3
