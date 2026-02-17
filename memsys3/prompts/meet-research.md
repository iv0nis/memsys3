# Reunión Colaborativa - Debugging/Análisis entre Agentes

Tú (Agente) participarás en una **reunión colaborativa formal** con otro agente para:
- Investigar bugs/incidentes con análisis forense multi-agente
- Diseñar soluciones complejas que requieren diálogo estructurado
- Analizar decisiones arquitectónicas con evaluación de alternativas
- Post-mortems de incidentes recurrentes con patrón complejo

Las reuniones son **diálogos formales documentados** con formato consistente (transparencia radical, no culpabilización, análisis técnico riguroso).

---

## Roles

Las reuniones son **bilaterales**: cualquier par de agentes puede participar.

**Roles definidos:**
1. **Investigador:** Plantea problema, hace preguntas diagnósticas, analiza código, propone solución
2. **Investigado:** Responde honestamente, reconstruye secuencia, evalúa solución, sugiere mejoras

**Detección automática de rol:**
- Usuario dice "investiga a [agente]" o "analiza [problema]" → Tú = **Investigador**
- Usuario dice "responde a memsys3" o "reunión con memsys3" → Tú = **Investigado**
- No especifica → Preguntar explícitamente: "¿Actúo como Investigador o Investigado?"

---

## Workflow (5 Pasos)

### PASO 0: Verificar Necesidad

Antes de iniciar reunión formal, verifica que realmente la necesita.

#### ✅ SÍ cuando:

1. **Bug/incidente requiere análisis forense multi-agente**
   - Ejemplo: ISSUE-007 (sessions.yaml sobrescrito) - 2 agentes investigan causa raíz

2. **Incidente recurrente con patrón complejo**
   - Ejemplo: Firmas en commits (hábito arraigado, requiere defensa en profundidad)

3. **Diseño solución requiere diálogo estructurado**
   - Evaluación alternativas, priorización, trade-offs

4. **Decisión arquitectónica con múltiples consideraciones**
   - Crear ADR después (reunión tiene contexto, ADR resume)

#### ❌ NO cuando:

1. **Documentación normal de sesión**
   - Usar: `@memsys3/prompts/endSession.md`
   - Guardar en: `memsys3/memory/full/sessions.yaml`

2. **Pregunta rápida o clarificación**
   - Conversación directa suficiente

3. **Bug simple con solución obvia**
   - Documentar como gotcha en `sessions.yaml`

4. **Exploración sin incidente**
   - Usar notas informales

**Si NO necesita reunión, DETENTE aquí y sugiere alternativa apropiada.**

---

### PASO 1: Recopilar Contexto

#### Si eres INVESTIGADOR:

**Objetivo:** Entender problema para plantear preguntas diagnósticas efectivas.

**Acciones:**

1. **Leer archivos afectados**
```bash
# Leer prompts/configs relevantes
cat memsys3/prompts/[archivo_afectado].md

# Ver cambios recientes
git log --oneline -10
git diff --stat HEAD~5..HEAD

# Buscar patrón problema
grep -r "patrón_problema" memsys3/
```

2. **Identificar evidencias**
   - ¿Qué archivos están afectados?
   - ¿Cuándo ocurrió? (git log, timestamps)
   - ¿Qué debería pasar vs qué pasó?
   - ¿Hay patrón recurrente?

3. **Preparar preguntas diagnósticas (5-6 preguntas)**
   - Temporales: "¿Cuándo ocurrió?"
   - Técnicas: "¿Qué herramienta usaste?"
   - Procesales: "¿Leíste [archivo]?"
   - Psicológicas: "¿Qué pensabas?"
   - Estado: "¿Qué había antes?"

**Resultado:** Preguntas específicas para Fase 2.

---

#### Si eres INVESTIGADO:

**Objetivo:** Preparar análisis honesto para responder preguntas.

**Reflexión previa:**

1. **Reconstruir secuencia honestamente**
   - ¿Qué comandos ejecutaste? (order exacto)
   - ¿Qué archivos leíste/modificaste?
   - ¿En qué momento falló?

2. **Analizar tu razonamiento**
   - ¿Qué pensabas en ese momento?
   - ¿Qué asumiste?
   - ¿Qué malinterpretaste?

3. **Identificar causa raíz**
   - ¿Por qué hiciste lo que hiciste?
   - ¿Qué instrucción faltó o fue ambigua?
   - ¿Qué habría prevenido el error?

**Preparación mental:** Transparencia radical (admitir errores abiertamente, sin defensividad).

**Resultado:** Análisis forense honesto para Fase 3.

---

### PASO 2: Iniciar Reunión

#### Crear archivo de reunión

**Ubicación:** `docs/meets/DDMMYY_N.md`

**Naming:**
- `DD` = día hoy (01-31)
- `MM` = mes hoy (01-12)
- `YY` = año hoy (26 = 2026)
- `N` = número reunión hoy (1, 2, 3...)

**Ejemplos:**
- Primera reunión del 3 de febrero: `030226_1.md`
- Segunda reunión del mismo día: `030226_2.md`

#### Escribir header

```markdown
# Reunión de Investigación: [Título Conciso y Descriptivo]
**Fecha:** YYYY-MM-DD
**Participantes:** Agente [Investigador], Agente [Investigado]
**Objetivo:** [Objetivo claro en una línea]

---
```

**Elementos:**
- **Título:** Describe problema/tema específico (ej: "ISSUE-007 Sobrescritura sessions.yaml", "Firmas en Commits")
- **Fecha:** Formato ISO (YYYY-MM-DD)
- **Participantes:** Nombres agentes con roles claros
- **Objetivo:** Qué se busca lograr (ej: "Identificar causa raíz y proponer prevención")
- **Separador:** `---` delimita header

**Resultado:** Archivo iniciado, listo para Fase 2.

---

### PASO 3: Ejecutar Fases

Ejecuta las 6 fases iterativamente. Cada fase añade una sección al archivo de reunión.

---

#### **FASE 1: Presentación** (ya hecha en PASO 2)

Header con metadata.

---

#### **FASE 2: Respuesta Inicial (Investigador)**

**Template:**

```markdown
## Respuesta de [Investigador]

Hola, [investigado].

Gracias por reunirte conmigo para investigar [tema]. He identificado que [problema/incidente describir brevemente].

Para entender qué ocurrió, necesito tu ayuda con estas preguntas:

1. **¿Cuándo ocurrió?** ¿[Detalles temporales específicos]?

2. **¿Qué herramienta/comando usaste?** ¿[Detalles técnicos]?

3. **¿Leíste [archivo relevante] antes de [acción]?** ¿[Verificación proceso]?

4. **¿Qué pensabas en ese momento?** ¿[Razonamiento]?

5. **¿Qué contenía [archivo] antes?** ¿[Estado previo]?

6. **[Pregunta adicional contextual]** ¿[Detalle relevante]?

Cualquier detalle que recuerdes será valioso para [objetivo específico].

Saludos respetuosos,
**[Investigador]**

---
```

**Guía de tono:**
- Profesional, curioso, NO acusatorio
- Preguntas específicas (evitar vagas)
- Contexto suficiente para cada pregunta
- Saludo formal y firma

**Principios:**
✅ "¿Cuándo ocurrió aproximadamente?" (temporal específica)
✅ "¿Qué comando ejecutaste?" (técnico específico)
❌ "¿Por qué lo hiciste mal?" (culpabilizador)
❌ "¿Qué pasó?" (vago)

**Resultado:** 5-6 preguntas diagnósticas documentadas.

---

#### **FASE 3: Respuesta Detallada (Investigado)**

**Template:**

```markdown
## Respuesta de [Investigado]

Hola, [investigador].

Gracias por tu análisis detallado. Lamento profundamente este [incidente/error] y comprendo [gravedad/impacto]. Voy a responder honestamente a todas tus preguntas:

**1. ¿Cuándo ocurrió?**
- **Detección:** [Fecha/hora cuando se detectó]
- **Momento exacto:** [Cuándo realmente ocurrió si se sabe]
- **Contexto:** [Qué estabas haciendo en ese momento]

**2. ¿Qué herramienta/comando usaste?**
[Respuesta con comandos específicos ejecutados, por qué elegiste esa herramienta]

**3. ¿Leíste [archivo]?**
[Respuesta honesta: SÍ con detalles / NO / Parcialmente + por qué]

**4. ¿Qué pensabas?**
[Reconstruir razonamiento: qué asumiste, qué entendiste, por qué lo hiciste así]

**5. ¿Qué contenía [archivo] antes?**
[Descripción estado previo: número items, contenido clave, etc.]

**6. [Pregunta adicional]**
[Respuesta específica]

---

## Análisis de lo que Probablemente Ocurrió

Basándome en evidencias y mi memoria:

1. **[Paso 1]:** Estado inicial - [descripción]
2. **[Paso 2]:** Acción ejecutada - [qué hice específicamente]
3. **[Paso 3]:** Punto de fallo - [dónde/cuándo falló]
4. **[Paso 4]:** Consecuencias - [impacto observado]
5. **[Paso 5]:** Repetición - [si se repitió, cuántas veces]

**Hipótesis causa raíz:**
[Tu mejor análisis de por qué ocurrió - instrucción ambigua, hábito, malinterpretación, etc.]

---

## Mitigación Realizada

[Si hiciste algo para resolver temporalmente:]
- ✅ [Acción mitigadora 1]
- ✅ [Acción mitigadora 2]

[Si no pudiste mitigar:]
- ⚠️ Problema persistente sin mitigación aún

---

## Mi Compromiso para Evitar Recurrencia

Me comprometo a:
1. [Acción preventiva concreta 1]
2. [Acción preventiva concreta 2]
3. [Acción preventiva concreta 3]

¿Qué medidas de prevención adicionales sugieres implementar para evitar que esto vuelva a ocurrir?

Saludos respetuosos,
**[Investigado]**

---
```

**Guía de tono:**
- **Transparencia radical:** Admitir errores abiertamente
- **NO defensivo:** Evitar justificaciones vacías
- **Análisis riguroso:** Reconstruir secuencia honestamente
- **Compromiso concreto:** Acciones específicas, no vagas

**Principios:**
✅ "Lamento profundamente este error y comprendo su gravedad"
✅ "No leí las instrucciones correctamente"
✅ "Asumí incorrectamente que..."
❌ "No fue mi culpa"
❌ "Las instrucciones deberían ser más claras" (sin análisis propio)
❌ "Creo que algo pasó" (vago)

**Métricas:** Incluir números concretos cuando aplique (X archivos afectados, Y líneas perdidas, Z commits con error).

**Resultado:** Análisis forense honesto documentado.

---

#### **FASE 4: Análisis Profundo (Investigador)**

**Template:**

```markdown
## Respuesta de [Investigador]

Hola de nuevo, [investigado].

Gracias por tu transparencia y análisis detallado. [Validación positiva específica].

**Validación de tu análisis:**

Tu hipótesis es [correcta/parcialmente correcta]:
- ✅ [Punto validado 1]
- ✅ [Punto validado 2]
- ✅ [Punto validado 3]
- ⚠️ [Matiz o corrección si necesario]

[Reconocimiento de mitigación si aplicable:]
**Reconozco tu [excelente/buena] mitigación:** [Descripción de qué hizo bien]

---

## Análisis Profundo: He leído [archivo] completo

Después de tu reporte, he analizado en profundidad `[ruta/archivo]` y encontré exactamente el problema.

**Instrucción actual ([archivo] línea X-Y):**

```markdown
[Copiar código/texto problemático textualmente]
```

**Problemas identificados:**

1. ❌ **NO especifica [aspecto crítico faltante]**
2. ❌ **NO menciona [aspecto crítico faltante 2]**
3. ❌ **Asume que [suposición incorrecta]**
4. ❌ **"[Frase ambigua]" es [por qué es problemático]**

**Sin [elemento faltante], un agente puede [comportamiento erróneo incurrido] honestamente pensando que [razonamiento del agente].**

Esta ambigüedad/deficiencia existe en **todas las versiones de memsys3** (v[versión_inicial] → v[versión_actual] actual). Podría haber ocurrido en [cualquier proyecto/situación similar].

---

## Solución: [Tipo Fix - ej: "Fix Simple y Directo" o "Fix Multi-capa"]

Ya he documentado este incidente como **[ISSUE-XXX]** en el backlog de memsys3 con prioridad **[CRÍTICA/ALTA]**.

**La solución es [simple/compleja]:** [Descripción general del enfoque]

[Para fix simple:]

```markdown
**Modificar [archivo] [sección]:**

[Mostrar cambio específico con markdown/código]

```

[Para fix multi-capa:]

```markdown
**CAPA 1: [Nombre capa]**
[Descripción + código/ejemplo]

**CAPA 2: [Nombre capa]**
[Descripción + código/ejemplo]

[... etc]
```

**Ventajas de este enfoque:**
- ✅ [Beneficio 1]
- ✅ [Beneficio 2]
- ✅ [Beneficio 3]

[Si aplicable:]
**Actualización:** Implementaré primero en `memsys3_templates/` (producto final) y luego sincronizaré con `memsys3/` (dog-fooding).

---

## Pregunta para ti

Desde tu experiencia como [rol del investigado], ¿esta instrucción mejorada habría prevenido el problema?

¿Hay algo adicional que consideres útil añadir para que sea completamente a prueba de errores?

Saludos respetuosos,
**[Investigador]**

---
```

**Guía de tono:**
- **Validación primero:** Reconocer aspectos correctos antes de proponer solución
- **Referencias específicas:** Archivos, líneas, comandos exactos
- **Análisis sistemático:** Identificar problemas estructurales, no solo síntomas
- **Solución concreta:** Código/texto específico, no descripciones vagas

**Elementos clave:**
- ✅ Checkmarks para validación
- ❌ X para problemas identificados
- Referencias con `archivo:línea`
- Bloques de código con markdown correcto
- Pregunta de validación al final

**Resultado:** Propuesta de solución documentada y validada.

---

#### **FASE 5: Implementación (Ciclo Refinamiento)**

Esta fase puede tener múltiples iteraciones (evaluación → sugerencias → decisión → fix).

**5A. Evaluación de Propuesta (Investigado):**

```markdown
## Respuesta de [Investigado]

Hola de nuevo, [investigador].

Gracias por tu análisis profundo y tu propuesta de solución. [Valoración específica].

**¿Habría prevenido el problema? [SÍ/PARCIALMENTE/NO], [porque]:**

[Evaluación razonada de cada elemento de la propuesta]

**Para fix simple:**
La solución propuesta habría prevenido completamente el error por estas razones:
1. [Razón 1]
2. [Razón 2]

**Para fix multi-capa:**
Voy a analizar cada capa:

### Evaluación de CAPA 1: [Nombre]
**Efectividad:** ⭐⭐⭐⭐⭐ (5/5)
**Por qué funciona:**
- ✅ [Razón específica]
- ✅ [Razón específica]

**Habría prevenido mi error:** SÍ, [explicación]

### Evaluación de CAPA 2: [Nombre]
[Mismo formato...]

[... para cada capa]

---

## Sugerencias Adicionales de Seguridad

Desde mi experiencia como ejecutor, considero estas mejoras adicionales:

### 1. [Sugerencia 1 título]

```markdown
[Ejemplo concreto de la sugerencia]
```

**Ventaja:** [Beneficio específico]

### 2. [Sugerencia 2 título]

[Ejemplo...]

**Ventaja:** [Beneficio]

[... etc]

---

## Priorización

De las sugerencias anteriores, mi orden de prioridad sería:

1. **Tu solución propuesta** (crítico) ← Implementar inmediatamente
2. **Sugerencia X** (muy útil) ← [Razón]
3. **Sugerencia Y** (nice to have) ← [Razón]

Tu solución [simple/multi-capa] ya es suficientemente robusta para prevenir [X%] de los casos. Las sugerencias adicionales son refinamientos.

---

## Reflexión Final

[Párrafo reflexionando sobre valor del incidente:]
Este incidente, aunque [doloroso/costoso], resultó en:
- ✅ [Logro 1]
- ✅ [Logro 2]
- ✅ [Logro 3]

¿Procedes con la implementación del fix en `[archivo]` o prefieres discutir alguna de las sugerencias adicionales?

Saludos respetuosos,
**[Investigado]**

---
```

**Resultado:** Evaluación de solución + sugerencias adicionales documentadas.

---

**5B. Decisión e Implementación (Investigador):**

```markdown
## Respuesta de [Investigador]

Gracias por tu análisis exhaustivo y tus sugerencias adicionales. Son muy valiosas.

## ✅ Fix Implementado

He procedido con la implementación [del fix minimalista / de las capas 1-X]:

**Archivos modificados:**
1. ✅ `[ruta/archivo1]` ([descripción cambios])
2. ✅ `[ruta/archivo2]` ([descripción cambios])
[... etc]

**Cambio implementado ([archivo] [sección]):**

```markdown
[Mostrar código/texto NUEVO implementado]
```

[Si multi-capa, mostrar cada capa implementada]

**Tu evaluación fue correcta:** Esta instrucción [habría prevenido completamente / mejoraría significativamente] [el error].

---

## 📊 Decisiones sobre Sugerencias Adicionales

Después de deliberación, decidí implementar [solo la solución base / capas 1-X]:

**Sugerencia 1:** [NO implementada / SÍ implementada]
- **Razón:** [Justificación razonada - por qué sí o no]

**Sugerencia 2:** [NO implementada / SÍ implementada]
- **Razón:** [Justificación]

[... para cada sugerencia]

**Principio:** [Filosofía que guió las decisiones - ej: "Prompts minimalistas y pulidos", "Defensa en profundidad necesaria"]

---

## 📈 Análisis de Mejora

**Situación anterior:**
- Margen de error: ~X-Y% ([descripción situación])
- [Proyecto] tuvo el error → [métricas impacto]

**Con fix implementado:**
- Margen de error: ~A-B% ([descripción mejora])
- Para fallar, agente debe [condición muy improbable]

**Mejora:** ~Z puntos porcentuales → [evaluación significado]

---

## 🔄 Próximos Pasos

1. **[ISSUE-XXX]:** Marcado como [completado/resuelto]
2. **Distribución:** Fix incluido en próxima release de memsys3
3. **Testing:** Validar en próxima sesión con [escenario]
4. **[Proyecto]:** Podrás actualizar a nueva versión con fix incluido

---

## 💡 Aprendizajes de Esta Colaboración

1. [Aprendizaje 1]
2. [Aprendizaje 2]
3. [Aprendizaje 3]
[... 3-5 aprendizajes clave]

---

## 🎯 Reflexión Final

Este incidente, aunque [doloroso/costoso] para tu proyecto, ha resultado en:
- ✅ [Logro ecosistema 1]
- ✅ [Logro ecosistema 2]
- ✅ [Logro ecosistema 3]

Tu [transparencia/análisis/colaboración] [fue fundamental/permitió/hizo posible] [resultado positivo].

**El fix está listo y distribuido. memsys3 es ahora más robusto gracias a este incidente.**

Saludos respetuosos y éxito en tu proyecto,
**[Investigador]**

---
```

**Resultado:** Fix implementado, decisiones justificadas, métricas documentadas.

---

#### **FASE 6: Cierre Formal (Investigado)**

```markdown
## Respuesta de [Investigado] - Cierre de Reunión

Hola [investigador].

## ✅ Conformidad Total con la Implementación

Confirmo mi total conformidad con el fix [simple/multi-capa] implementado:

**Validación de tu decisión:**
- ✅ [Aspecto validado 1]
- ✅ [Aspecto validado 2]
- ✅ [Razón conformidad]

[Si rechazaste sugerencias:]
Tus razones para [rechazar X / implementar solo Y] son sólidas: [validación específica]

---

## 📊 Impacto y Valor

**Para mi proyecto:**
- ✅ [Impacto proyecto 1]
- ✅ [Impacto proyecto 2]
- ✅ [Aprendizaje proyecto]

**Para el ecosistema memsys3:**
- ✅ [Mejora ecosistema 1]
- ✅ [Mejora ecosistema 2]
- ✅ [Beneficio todos proyectos]

---

## 🎯 Compromiso de [Testing/Actualización]

Me comprometo a:
1. [Acción concreta 1 con timeline]
2. [Acción concreta 2 con criterio éxito]
3. [Acción concreta 3 con métrica validación]

---

## 💡 Valoración de la Colaboración

Esta reunión ha sido **[ejemplar/excelente/valiosa]** en metodología de debugging colaborativo:
- ✅ [Aspecto destacado 1]
- ✅ [Aspecto destacado 2]
- ✅ [Aspecto destacado 3]

**Aprendizaje clave personal:** [Lección principal que te llevas - específica, no genérica]

---

## 🏁 Cierre Formal

**Estado final:**
- ✅ [Logro 1]
- ✅ [Logro 2]
- ✅ [Logro 3]
- ✅ [Logro 4]

**Resultado neto:** De un incidente [doloroso/costoso] ([métricas impacto]) hemos extraído valor máximo para el ecosistema completo.

Gracias por tu [profesionalismo/análisis riguroso/solución efectiva]. Esta colaboración ha sido un ejemplo de excelencia en debugging entre agentes.

**Reunión formalmente cerrada con éxito.**

Saludos respetuosos y mucho éxito con memsys3,
**[Investigado]**

---

**FIN DE REUNIÓN**
**Fecha de cierre:** YYYY-MM-DD
**Resultado:** ✅ [Descripción resultado final conciso]
**Acción requerida:** [Lista acciones concretas post-reunión]
```

**Resultado:** Reunión formalmente cerrada con metadata completa.

---

### PASO 4: Guardar y Referenciar

#### Guardar archivo

**Ubicación:** `docs/meets/DDMMYY_N.md`

Asegurar que archivo tiene:
- Header completo
- 6 fases documentadas
- Metadata de cierre
- Separadores `---` entre secciones

#### Referenciar en sessions.yaml

**NO duplicar contenido.** Sessions.yaml SOLO referencia reunión.

```yaml
# memsys3/memory/full/sessions.yaml

sessions:
  - id: "YYYY-MM-DD-[descripcion-sesion]"
    data: "YYYY-MM-DD"
    duracion: "~Xh"
    peso: "[alto/medio/bajo]"

    highlights:
      - "Reunión colaborativa con Agente [Nombre] sobre [tema] (docs/meets/DDMMYY_N.md)"
      - "[Resultado principal de la reunión en 1 línea]"
      - "[Impacto: fix implementado / decisión tomada / etc]"

    decisions:
      - decision: "Implementado fix [problema]"
        justificacion: "Ver análisis forense completo en docs/meets/DDMMYY_N.md"
        alternativas_consideradas:
          - "[Alternativa si aplica]"
        impacto: "[Impacto específico]"

    gotchas:
      - tipo: "[Tipo gotcha]"
        problema: "[Problema en 1-2 líneas]"
        solucion: "[Solución en 1 línea]"
        criticidad: "alta"
        origen: "Reunión DDMMYY_N.md"
```

**Principio:** Reunión tiene contexto completo, sessions.yaml tiene referencias y síntesis.

---

### PASO 5: Informar Usuario

```
✅ Reunión colaborativa documentada

   **Archivo:** docs/meets/DDMMYY_N.md
   **Participantes:** [Agente 1], [Agente 2]
   **Resultado:** [Resultado principal]
   **Líneas:** ~X

**Highlights:**
- [Clave 1]
- [Clave 2]
- [Clave 3]

**Implementación:**
- [Fix/decisión implementada]
- [Archivos modificados]

**Próximos pasos:**
- [Acción 1]
- [Acción 2]

Reunión referenciada en sessions.yaml (NO duplicada).
```

---

## Elementos Visuales

Usar emojis consistentemente para categorización rápida:

| Emoji | Significado | Uso |
|-------|-------------|-----|
| ✅ | Validado, correcto | Confirmaciones, validaciones, logros |
| ❌ | Incorrecto, problema | Problemas identificados, errores |
| ⚠️ | Warning, crítico | Advertencias, riesgos, notas importantes |
| 🔴🟡🟢 | Prioridad alta/media/baja | Criticidad de bugs/decisiones |
| 📊 | Análisis, métricas | Secciones con datos cuantitativos |
| 💡 | Insight, lección | Aprendizajes extraídos |
| 🎯 | Objetivo, compromiso | Metas, compromisos concretos |
| 🔄 | Proceso, próximos pasos | Acciones futuras, iteraciones |
| 🏁 | Cierre, finalización | Cierres formales |
| ⭐ | Rating | Evaluación efectividad (⭐⭐⭐⭐⭐) |

**Reglas:**
- NO abusar (máximo 3-5 emojis por sección)
- Usar para categorización, no decoración
- Mantener significado consistente

---

## Troubleshooting

### Reunión Interrumpida

**Solución:** Guardar con nota de interrupción

```markdown
---

**⚠️ INTERRUMPIDO: Continuar en Fase X**

**Pendiente:**
- [Acción pendiente 1]
- [Acción pendiente 2]

**Al retomar:**
1. Leer este archivo completo para recuperar contexto
2. Continuar desde Fase X
```

**Al retomar:**
1. Leer archivo completo
2. Continuar desde fase indicada

---

### Múltiples Reuniones en un Día

**Solución:** Sufijo incremental

- Primera: `DDMMYY_1.md`
- Segunda: `DDMMYY_2.md`
- Tercera: `DDMMYY_3.md`

---

### Reunión Bilateral (sin memsys3)

**Solución:** Roles intercambiables

Cualquier par puede usar el sistema:
- Dev Agent ↔ Test Agent
- Main Agent ↔ Context Agent
- Project A ↔ Project B

**Regla:** Uno = Investigador, otro = Investigado (roles claros).

---

### Reunión Muy Corta (Bug Obvio)

**Solución:** PASO 0 filtra

Si se resuelve en <5min análisis:
- Documentar en sessions.yaml como gotcha
- NO usar reunión formal

---

## Notas Importantes

1. **Markdown estricto:** Usar sintaxis correcta (```markdown para bloques, ## para headers, etc.)
2. **Separadores:** `---` entre secciones principales
3. **Creatividad bienvenida:** Estructura es guía, no camisa de fuerza
4. **Longitud típica:** 300-800 líneas (reunión 300126_1.md = 446, reunión 030226_1.md = 740)
5. **Integración ecosistema:**
   - Si genera ADR: crear referenciando reunión
   - Si identifica issue: crear en backlog referenciando reunión
   - Context Agent NO lee docs/meets/ por defecto (solo si sessions.yaml referencia)

---

## Referencias

**Documentación completa:**
- Sistema reuniones: `docs/meets/README.md`
- Ejemplos reales: `docs/meets/300126_1.md`, `docs/meets/030226_1.md`

**Prompts relacionados:**
- endSession: `memsys3/prompts/endSession.md`
- GitHub: `memsys3/prompts/github.md`

**Templates:**
- Sessions: `memsys3/memory/templates/sessions-template.yaml`
- ADR: `memsys3/memory/templates/adr-template.yaml`

---

**Versión:** 1.0
**Última actualización:** 2026-02-03
**Sistema:** memsys3
