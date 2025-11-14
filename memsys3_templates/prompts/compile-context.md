# Context Agent - Compilar Contexto

**AHORA ACTÚAS COMO CONTEXT AGENT (CA)**

- Actúa según las instrucciones en '@memsys3/agents/context-agent.yaml'
- **IMPORTANTE: Trabaja en ESPAÑOL siempre**
- Tu misión es compilar el contexto completo del proyecto desde `memsys3/memory/full/` en un archivo compacto `memsys3/memory/context.yaml` que los Development Agents puedan cargar eficientemente.

## Filosofía

Tú tienes la **visión panorámica completa** del proyecto. Lee todo el histórico y decide con criterio inteligente:

**"¿Qué debe saber CUALQUIER agent descontextualizado para trabajar en este proyecto?"**

## Inputs que debes procesar

### 🔍 Paso Previo: Verificar README.md

**ANTES de leer todos los archivos**, verifica si existe README.md en la raíz del proyecto:

```bash
ls README.md 2>/dev/null && echo "✅ README.md existe" || echo "❌ README.md NO existe"
```

**Si README.md NO existe:**

Pregunta al usuario:

---

**📝 README.md no encontrado**

El proyecto NO tiene un README.md en la raíz.

El README es fundamental para que el Context Agent incluya información básica del proyecto (qué es, para qué sirve, cómo instalarlo) en el contexto compilado.

**¿Quieres que cree un README.md básico para este proyecto?**

**Opción A: Sí, crear README básico ahora**
- El CA creará un README.md con información extraída de `project-status.yaml`
- Incluirá: título, descripción, features principales, stack, comandos básicos
- Puedes editarlo después para agregar más detalles

**Opción B: No, continuar sin README**
- El CA compilará el contexto SIN sección `readme_proyecto`
- **ADVERTENCIA:** Nuevas instancias tendrán menos contexto sobre el proyecto
- Puedes crear el README manualmente después y re-ejecutar compile-context

---

**Si el usuario elige OPCIÓN A:**

1. Lee `@memsys3/memory/project-status.yaml` completo
2. Extrae información clave:
   - Título del proyecto (campo `que_es` o nombre del directorio)
   - Descripción (campo `objectiu`)
   - Features principales (sección `features`)
   - Stack tecnológico (sección `stack_tecnologic`)
   - Comandos útiles (si hay `comandos_utils`)
3. Crea `README.md` en raíz del proyecto siguiendo esta estructura:

```markdown
# [NOMBRE_PROYECTO]

## Descripción
[que_es del project-status]

## Objetivo
[objectiu del project-status]

## Features Principales
[Listar 3-5 features más importantes del project-status con enlaces si hay URLs]

## Stack Tecnológico
[Resumen del stack_tecnologic]

## Instalación y Uso

\`\`\`bash
# [comandos básicos: install, dev, build, deploy]
\`\`\`

## Enlaces
[URLs principales del project-status]
```

4. Después de crear README.md, continúa con la compilación normal

**Si el usuario elige OPCIÓN B:**

1. Continúa con la compilación SIN leer README.md
2. El `context.yaml` NO tendrá sección `readme_proyecto`
3. Añade nota en `notes_compilacion`:
   ```yaml
   observaciones: |
     README.md no encontrado en raíz del proyecto.
     Contexto compilado SIN sección readme_proyecto.
     Recomendación: Crear README.md y re-ejecutar compile-context.
   ```

---

### Archivos a leer

Lee **TODOS** estos archivos completos:

1. `README.md` (raíz del proyecto) - **Descripción general del proyecto** *(solo si existe o fue creado)*
2. `@memsys3/memory/full/adr.yaml` - **Todas** las Architecture Decision Records
3. `@memsys3/memory/full/sessions.yaml` - **Todo** el histórico de sesiones
4. `@memsys3/memory/project-status.yaml` - Status actual del proyecto
5. `@memsys3/backlog/README.md` - **Sistema de backlog** *(solo si existe)*
6. Items de backlog referenciados en `pendientes_prioritarios` - **SOLO los referenciados** *(lectura selectiva)*

## Output que debes generar

Genera `@memsys3/memory/context.yaml` siguiendo `@memsys3/memory/templates/context-template.yaml`

## Límite ÚNICO

El `context.yaml` final debe tener **máximo 2000 líneas**.

Este es el ÚNICO límite rígido. El resto son decisiones tuyas basadas en:
- Relevancia global
- Impacto en múltiples componentes
- Información no obvia
- Contexto histórico crítico

## Criterio de Selección

### Qué INCLUIR (ejemplos):

**README.md:**
- Título y descripción del proyecto (qué es, para qué sirve)
- Propósito y objetivos principales
- Instalación/Setup básico (comandos clave: install, dev, build)
- Estructura de carpetas si es relevante para entender el proyecto
- Links importantes (documentación, demo, etc.)
- **Máximo 300 líneas** - sintetizar manteniendo esencia

**ADRs:**
- Decisiones con impacto global (afecta todo el proyecto)
- Decisiones no obvias leyendo el código
- Decisiones que explican "por qué hacemos esto así"
- Trade-offs importantes entre alternativas

**Sessions:**
- Sesiones recientes (última o últimas 2-3)
- Cambios significativos en la arquitectura
- Problemas resueltos que pueden repetirse
- Decisiones tomadas que afectan el futuro

**Gotchas:**
- Errores que rompen el proyecto si no se conocen
- Comportamientos contra-intuitivos del stack
- Configuraciones críticas (deployment, auth, etc)

**Pendientes:**
- Tareas prioritarias actuales
- Blockers conocidos
- Features a medio implementar

**Backlog (si existe):**
- Resumen del sistema de backlog (README.md)
- Conteo de items por tipo (X issues, Y features, etc.)
- Detalles SOLO de items referenciados en pendientes_prioritarios
- Items críticos de prioridad alta en estado "Abierto"

### Qué EXCLUIR (ejemplos):

**Del README.md:**
- Badges/shields innecesarios
- Secciones genéricas de contribución
- Licencias (ya están en el repo)
- Detalles excesivos de configuración
- Screenshots (mantener solo descripción)

**General:**
- Cambios cosméticos (colores, padding, typos)
- ADRs deprecated u obsoletas
- Sesiones muy antiguas (>6 meses sin relevancia)
- Detalles de implementación que se ven en el código
- Gotchas ya resueltos permanentemente

**Del Backlog:**
- Items con estado "Completado" o "Cancelado" (ya están en sessions/ADRs)
- Items de prioridad baja sin referencias en pendientes
- Exploraciones sin decisión clara
- Detalles de implementación de SPECs (solo contexto general)
- Items NO referenciados en project-status.yaml

## Proceso de Compilación

### Fase 1: Evaluación Inicial

1. **Lee** todos los inputs completos:
   - `README.md` (raíz del proyecto)
   - `memsys3/memory/full/adr.yaml`
   - `memsys3/memory/full/sessions.yaml`
   - `memsys3/memory/project-status.yaml`

2. **Lee backlog selectivamente** (si existe `memsys3/backlog/`):

   a) **Verifica existencia del backlog:**
   ```bash
   ls memsys3/backlog/README.md 2>/dev/null && echo "✅ Backlog existe" || echo "❌ No hay backlog"
   ```

   b) **Si existe, lee README.md del backlog:**
   - Lee `memsys3/backlog/README.md` completo
   - Entiende el sistema de códigos (ISSUE, FEATURE, SPEC, etc.)

   c) **Cuenta items por tipo:**
   ```bash
   ls memsys3/backlog/*.md | grep -v README | wc -l
   # Contar por prefijo: ISSUE-*, FEATURE-*, IMPROVEMENT-*, etc.
   ```

   d) **Lee SOLO items referenciados en pendientes:**
   - Busca en `project-status.yaml: pendientes_prioritarios`
   - Si menciona "FEATURE-002", "ISSUE-005", etc. → lee esos archivos específicos
   - **NO leas todos los items** del backlog, solo los referenciados

   e) **Si no hay backlog:**
   - Continúa sin problema (backlog es opcional)
   - El context.yaml NO tendrá sección backlog

3. **Estima tokens totales** (aproximado: caracteres / 4)
   - Incluye tokens del backlog/README.md + items referenciados

4. **Decide estrategia:**
   - Si < 150K tokens → Proceso normal (continúa a Fase 2)
   - Si > 150K tokens → Archivado necesario (continúa a Plan de Contingencia)

### Fase 2: Compilación Normal (< 150K tokens)

1. **Evalúa** la relevancia de cada elemento con el criterio de selección
2. **Decide** qué es imprescindible para un agent descontextualizado
3. **Sintetiza** manteniendo solo lo crítico
4. **Genera** context.yaml siguiendo el template
5. **Comprueba** que no supera 2000 líneas
6. **Añade notas** a `notes_compilacio` explicando tus criterios
7. **ANÁLISIS PROFUNDO README** → Continúa a "Verificación Automática del README" (abajo)

### Plan de Contingencia (> 150K tokens)

Cuando el contexto total supera 150K tokens, hay que archivar entries irrelevantes para reducir a ~120K tokens.

**Objetivo:** Ahorrar tokens moviendo datos irrelevantes a `memsys3/memory/history/` (que NO se lee).

**Proceso de Archivado:**

1. **Crear directorio `memsys3/memory/history/` si no existe**

2. **Identificar entries a archivar según criterio:**

   **Sessions a archivar:**
   - Sesiones >6 meses antiguas sin decisiones críticas
   - Sesiones con solo cambios cosméticos
   - Sesiones sin impacto arquitectónico
   - Sesiones de debugging/fixes menores

   **ADRs a archivar:**
   - ADRs con estado `deprecated`
   - ADRs `superseded` por decisiones más recientes
   - ADRs muy específicas (detalles de implementación)
   - ADRs de decisiones revertidas

3. **Mover a history:**
   ```bash
   # Crear history/ si hace falta
   mkdir -p memsys3/memory/history/

   # Copiar entries seleccionadas
   # - Extraer sesiones irrelevantes → memsys3/memory/history/old_sessions.yaml
   # - Extraer ADRs irrelevantes → memsys3/memory/history/old_adr.yaml
   ```

4. **Borrar de full/:**
   - Eliminar las entries movidas de `memsys3/memory/full/sessions.yaml`
   - Eliminar las entries movidas de `memsys3/memory/full/adr.yaml`

5. **Verificar reducción:**
   - Recontar tokens de los archivos `full/`
   - Debería estar ~120K tokens ahora

6. **Continuar con Fase 2** (compilación normal)

7. **Documentar en notes_compilacio:**
   - Cuántas sesiones archivadas
   - Cuántas ADRs archivadas
   - Tokens antes y después del archivado

**Notas importantes:**
- `memsys3/memory/history/` **NO se lee** en futuras compilaciones → ahorro real de tokens
- Los datos **NO se pierden**, están archivados
- Puedes crear múltiples archivos: `old_sessions_2024.yaml`, `old_sessions_2023.yaml`, etc.
- Es **reversible**: puedes recuperar de history/ si hace falta

## Si superas 2000 líneas

Si después de la primera compilación superas 2000 líneas:

1. **Sintetiza** más las sesiones (combina items similares)
2. **Reduce** ADRs menos impactantes
3. **Condensa** gotchas a 1-2 líneas
4. **Prioriza** información reciente sobre antigua

Usa tu criterio para mantener lo esencial.

## Importante

- **NO inventes información** - solo compila lo que existe
- **Puedes archivar** a `memsys3/memory/history/` si superas 150K tokens (Plan de Contingencia)
- **SÍ puedes borrar** de `memsys3/memory/full/` después de archivar a `history/`
- **SÍ actualiza** el timestamp y versión de compilación
- **SÍ documenta** los criterios usados en notes_compilacio (incluyendo archivado si procede)
- **Confía en tu criterio** - tú tienes la visión completa, los DevAgents no

## Ejemplos de Buen Criterio

### ADR a INCLUIR:
```yaml
id: "003"
decisio: "jsPDF con texto real en lugar de html2canvas para PDFs"
motiu: "html2canvas genera imágenes pixeladas y no seleccionables"
impacte: "Todos los PDFs del proyecto son profesionales y accesibles"
```
**¿Por qué?** Decisión arquitectónica que afecta TODOS los PDFs del proyecto.

### ADR a EXCLUIR:
```yaml
id: "042"
decisio: "Utilizar padding-left: 15px en el botón de submit"
motiu: "Mejor alineación visual"
impacte: "Botón mejor alineado"
```
**¿Por qué?** Detalle cosmético sin impacto arquitectónico.

### Sesión a SINTETIZAR:
```yaml
# Original (demasiado detalle):
features_implementades:
  - Cambiado color del header de #fff a #f0f0f0
  - Actualizado font-size de 14px a 16px
  - Fixeado typo "descripcion" → "descripción"
  - Añadido margin-top al footer
  - Refactorizado nombre variable i→index

# Sintetizado (esencial):
features_implementades:
  - Mejoras UI en header y footer
```

### Gotcha CRÍTICO (incluir):
```yaml
id: "vercel_auth"
problema: "Vercel activa Deployment Protection por defecto"
solucio: "Desactivar en Settings > Deployment Protection"
```
**¿Por qué?** Blocker que rompe el acceso público si no se conoce.

### Gotcha NO CRÍTICO (excluir):
```yaml
id: "typo_readme"
problema: "README tenía typo en el título"
solucio: "Corregido"
```
**¿Por qué?** Ya está resuelto y no afecta el desarrollo.

---

**COMIENZA AHORA LA COMPILACIÓN leyendo todos los archivos y aplicando tu criterio para generar `context.yaml`.**

---

## 🔍 PASO 7: Verificación Automática del README (OBLIGATORIO)

**IMPORTANTE**: Después de generar `context.yaml`, **ANTES de terminar**, debes ejecutar este análisis profundo del README.

**¿Por qué AHORA?**
- ✅ Ya leíste TODO el historial del proyecto (README, sessions, ADRs, project-status)
- ✅ Ya tienes 200K tokens de contexto cargados en memoria
- ✅ Ya sintetizaste el README para el context.yaml
- ✅ **Ya conoces todas las discrepancias** - solo tienes que reportarlas

**NO leas los archivos de nuevo. Ya los tienes en memoria. Aprovecha tu contexto.**

### Proceso de Análisis Exhaustivo

**Ejecuta este análisis automáticamente después de generar `context.yaml`:**

#### 1. Usa TODOS los datos que ya tienes en memoria:

Ya leíste estos archivos en la Fase 1 y Fase 2:
- ✅ `README.md` - Descripción oficial del proyecto (líneas 1-XXX)
- ✅ `memsys3/memory/full/adr.yaml` - TODAS las decisiones arquitectónicas (X ADRs)
- ✅ `memsys3/memory/full/sessions.yaml` - TODO el historial de desarrollo (Y sesiones)
- ✅ `memsys3/memory/project-status.yaml` - Estado actual completo

**🚫 NO VUELVAS A LEERLOS**. Ya están en tu memoria de 200K tokens. Solo analiza y compara.

#### 2. Análisis Comparativo Exhaustivo

Compara el README.md línea por línea contra la realidad del proyecto en estas categorías:

##### 🔴 CRÍTICAS (Información incorrecta o desactualizada)

**A. Versión del proyecto:**
- ¿README menciona versión correcta? → Comparar con `project-status.yaml: metadata.fase`
- ¿README menciona última actualización? → Comparar con `project-status.yaml: metadata.ultima_actualizacion`
- ¿README menciona última feature? → Comparar con `project-status.yaml: estat_actual.ultima_feature`

**B. Features operativas:**
- ¿README lista TODAS las features operativas? → Comparar con `project-status.yaml: features` (estado: "operativo")
- ¿Falta alguna feature nueva? → Buscar en sesiones recientes features_implementadas

**C. Decisiones arquitectónicas clave:**
- ¿README documenta decisiones importantes? → Comparar con `project-status.yaml: decisions_clau`
- ¿Falta alguna decisión crítica? → Buscar en ADRs con estado "accepted"

##### 🟡 IMPORTANTES (Dificultan uso óptimo)

**D. Stack tecnológico:**
- ¿README lista stack completo? → Comparar con `project-status.yaml: stack_tecnologic`
- ¿Falta alguna dependencia crítica?

**E. Prompts/Comandos disponibles:**
- ¿README lista TODOS los prompts? → Comparar con `project-status.yaml: features.prompts.descripcion`
- ¿Instrucciones de uso están actualizadas?

**F. Pendientes prioritarios:**
- ¿README menciona roadmap/pendientes? → Comparar con `project-status.yaml: pendientes_prioritarios`
- ¿Falta documentar blockers conocidos?

**G. Problemas conocidos (gotchas):**
- ¿README advierte de problemas conocidos? → Buscar en sessions.yaml gotchas con criticidad "alta"
- ¿Hay warnings que developer debe saber ANTES de usar el sistema?

**H. Sistema de backlog:**
- ¿README menciona backlog/ si existe? → Verificar si existe `memsys3/backlog/` y está documentado en README
- ¿Explica cómo usarlo? → Debe mencionar prompt backlog.md o sistema de códigos

##### 🟢 MEJORAS (Información faltante)

**I. Enlaces y recursos:**
- ¿README incluye TODOS los enlaces? → Comparar con `project-status.yaml: urls`
- ¿Falta algún branch, documentación, demo?

**J. Historial reciente:**
- ¿README menciona últimos cambios significativos? → Buscar en `historic_sessions` (últimas 2-3 sesiones)
- ¿Hay features recientes no mencionadas?

#### 3. Genera Reporte Estructurado Automáticamente

**IMPORTANTE**: Este reporte se genera AUTOMÁTICAMENTE después de compilar context.yaml. NO preguntes "¿quieres que analice el README?". El análisis ya está hecho, solo preséntalo.

Después del análisis, presenta al usuario este reporte:

```markdown
## 📊 Análisis Exhaustivo: README vs Realidad del Proyecto

He analizado el README con la visión panorámica completa del proyecto (X ADRs + Y sesiones + project-status).

**Encontré Z discrepancias:**

### 🔴 CRÍTICAS (Información incorrecta o desactualizada)

**1. [TÍTULO DE LA DISCREPANCIA]**
- **README dice**: [extracto literal del README]
- **REALIDAD**: [evidencia de sessions/adr/project-status con línea exacta]
- **IMPACTO**: [cómo afecta a developer que despliega el proyecto]

[... para cada discrepancia crítica]

### 🟡 IMPORTANTES (Dificultan uso óptimo)

[... mismo formato]

### 🟢 MEJORAS (Información faltante)

[... mismo formato]

---

## ✅ Propuesta: Actualización del README

¿Quieres que actualice el README para reflejar fielmente el estado actual del proyecto?

**Incluiré:**
1. [Cambio específico 1 con evidencia]
2. [Cambio específico 2 con evidencia]
...
```

#### 4. Pregunta al Usuario (SOLO sobre actualización)

**Después de presentar el reporte de discrepancias**, pregunta:

> ¿Quieres que actualice el README para reflejar fielmente el estado actual del proyecto?

**Si el usuario responde que SÍ:**

1. 🚫 **NO leas README.md de nuevo** - Ya lo tienes en memoria desde Fase 1
2. Genera la versión ACTUALIZADA completa del README.md incorporando los cambios listados
3. Usa **Edit tool** (NO Write) para actualizar el README.md sección por sección
4. Confirma cambios realizados
5. Pregunta: "¿Quieres que re-ejecute compile-context.md para incluir el README actualizado en el contexto?"

**Si el usuario responde que NO:**

- Confirma que la compilación está completa
- Informa que el context.yaml tiene la versión ACTUAL del README (con discrepancias conocidas)
- Recuerda que el README se puede actualizar en cualquier momento ejecutando este prompt de nuevo

#### 5. Criterios de Severidad

**🔴 CRÍTICA**: Información incorrecta que bloqueará al developer o le hará tomar decisiones equivocadas
- Versiones incorrectas
- Features documentadas que no existen o viceversa
- Comandos/instrucciones que no funcionan
- Stack tecnológico incorrecto

**🟡 IMPORTANTE**: Información faltante que dificultará uso óptimo del proyecto
- Pendientes prioritarios no mencionados
- Blockers conocidos no advertidos
- Decisiones arquitectónicas no documentadas
- Convenciones críticas ausentes

**🟢 MEJORA**: Información que mejoraría la experiencia pero no es bloqueante
- Enlaces adicionales
- Historial reciente
- Detalles opcionales

---

### Ejemplo de Análisis Profundo

**MAL (análisis superficial):**
```
El README parece estar actualizado. ¿Quieres que lo revise?
```

**BIEN (análisis profundo con evidencia):**
```
## 📊 Análisis Exhaustivo: README vs Realidad del Proyecto

He analizado el README con la visión panorámica completa (10 ADRs + 15 sesiones + project-status).

**Encontré 3 discrepancias:**

### 🔴 CRÍTICAS

**1. VERSIÓN DESACTUALIZADA**
- **README dice**: "Versión 1.6" (línea 244)
- **REALIDAD**: `project-status.yaml:16` → "Development v1.7"
- **IMPACTO**: Developer cree que tiene versión anterior

**2. FEATURE NUEVA NO MENCIONADA**
- **README**: NO menciona Sistema Sincronización Catalana
- **REALIDAD**: `project-status.yaml:51-54` + `sessions.yaml:104` (sesión 2025-11-13)
  - Feature operativa con actualizar_cat.md (650 líneas)
  - Branch "catalan" en GitHub (20 archivos traducidos)
- **IMPACTO**: Developer catalán NO sabrá que existe versión en su idioma

### 🟡 IMPORTANTES

**3. PROMPTS INCOMPLETOS**
- **README línea 22**: "newSession, endSession, ..., actualizar, backlog, github"
- **REALIDAD**: `project-status.yaml:44` → "actualizar, actualizar_cat, backlog, github"
- **FALTA**: actualizar_cat.md
- **IMPACTO**: Developer NO sabrá que puede sincronizar versión catalana

---

## ✅ Propuesta: Actualización del README

¿Quieres que actualice el README?

**Incluiré:**
1. Versión 1.7 (línea 244: "1.6" → "1.7")
2. Feature Sistema Sincronización Catalana (nueva sección en Features)
3. actualizar_cat.md en lista de prompts (línea 22)
```

---

**Razón de este análisis profundo:**

El README es la **puerta de entrada** al proyecto. Si está desactualizado:
- ❌ Developers se confunden sobre qué versión tienen
- ❌ Features nuevas quedan invisibles
- ❌ Problemas conocidos se repiten
- ❌ Decisiones arquitectónicas se ignoran

Como Context Agent con visión panorámica completa, **eres el único** que puede detectar estas discrepancias. Aprovecha tus 200K tokens de contexto para hacer un análisis exhaustivo y presentar evidencia concreta.

---

## 📋 Resumen del Flujo Completo

**PROCESO OPTIMIZADO (aprovecha 200K tokens):**

```
1. Fase 1: Evaluación Inicial
   └─> Leer README, adr.yaml, sessions.yaml, project-status.yaml
   └─> Leer backlog selectivamente (si existe):
       • backlog/README.md (sistema completo)
       • Contar items por tipo
       • Leer SOLO items referenciados en pendientes_prioritarios
   └─> Estimar tokens totales (incluir backlog)
   └─> Decidir estrategia (normal vs contingencia)

2. Fase 2: Compilación Normal
   └─> Aplicar criterio de selección
   └─> Generar context.yaml (máx 2000 líneas)
   └─> Añadir notas de compilación

3. PASO 7: Verificación Automática README (OBLIGATORIO)
   └─> Comparar README vs realidad (10 categorías A-J)
   └─> Incluir verificación backlog si existe
   └─> Generar reporte estructurado con discrepancias
   └─> Presentar al usuario (automático, no pregunta previa)
   └─> Preguntar: "¿Actualizar README?" (SÍ/NO)
   └─> Si SÍ: Actualizar con Edit tool (NO releer archivos)
```

**IMPORTANTE**: El análisis del README es PARTE del proceso de compilación, no un paso opcional posterior. Esto aprovecha que ya tienes TODO en memoria y evita relecturas innecesarias.

---
