# IMPROVEMENT-001: Contexto con Documentación Crítica del Sistema

**Estado:** Abierto
**Prioridad:** Alta
**Tipo:** Mejora del sistema de contexto
**Plazo:** Medio plazo
**Fecha identificación:** 2025-11-03
**Contexto:** Sesión de documentación y verificación FASE 3

---

## 📋 Problema

### Problema 1: Documentación Crítica NO Accesible en Contexto

Documentos críticos para entender el sistema NO son leídos por nuevas instancias de Claude Code:

**Documentos críticos fuera del contexto:**
- `README.md` (raíz) - Filosofía general, deployment, estructura
- `docs/DEVELOPMENT.md` - Filosofía memsys3_templates/ vs memsys3/, workflow
- `docs/UPDATE.md` - Qué archivos actualizar, qué no sobrescribir
- `memsys3_templates/README.md` - Uso del sistema, prompts, escalabilidad

**Por qué no se leen:**
- No están en `memory/full/` (que Context Agent sí lee)
- No están en `context.yaml` compilado
- Context Agent solo lee: adr.yaml, sessions.yaml, project-status.yaml
- Nuevas instancias arrancan con context.yaml que NO contiene esta información

**Consecuencia:**
Nueva instancia de Claude Code NO sabe:
- Qué es memsys3_templates/ vs memsys3/
- Filosofía de templates permanentes
- Workflow de deployment
- Qué archivos son safe vs datos del proyecto
- Conceptos fundamentales del sistema (rotación, contingencia, etc.)

### Problema 2: Ambigüedad Dev vs Sistema Distribuido

Es difícil distinguir qué contenido es:
- **Dev de memsys3**: Filosofía interna, decisiones de desarrollo, dog-fooding
- **Sistema distribuido**: Cómo funciona memsys3 cuando otros proyectos lo usan

**Ejemplo de ambigüedad:**

`DEVELOPMENT.md` contiene:
- ✅ Info crítica para CUALQUIER proyecto: filosofía de memsys3_templates/, concepto de templates permanentes
- ❌ Info específica de dev: dog-fooding con memsys3/, workflow de desarrollo interno

Pero está en `docs/` (no se distribuye), entonces proyectos que usan memsys3 NO tienen acceso a la info crítica.

**Documentos con contenido mixto:**
- `README.md` - Mezcla onboarding público + filosofía del sistema + dog-fooding
- `DEVELOPMENT.md` - Mezcla filosofía sistema + workflow dev interno
- `UPDATE.md` - Info útil para usuarios + referencias a estructura dev

---

## 🎯 Objetivo de la Mejora

**Hacer accesible información crítica del sistema en context.yaml** para que nuevas instancias tengan conocimiento fundamental sobre:

1. Filosofía de memsys3_templates/ (producto final)
2. Concepto de templates permanentes (NO se borran)
3. Workflow de deployment
4. Qué archivos contienen datos vs plantillas
5. Sistema de escalabilidad (rotación, contingencia)
6. Prompts disponibles y su propósito

**Sin:**
- Duplicar información innecesariamente
- Inflar context.yaml más allá de límites
- Romper la filosofía actual del Context Agent

---

## 💡 Propuesta de Solución

### Opción A: Context Agent Lee READMEs (Propuesta del Usuario)

**Concepto:**
- Context Agent lee `README.md` (raíz) durante compilación
- NO lee `memsys3_templates/README.md` (o tal vez sí, a decidir)
- Extrae conceptos clave y los incluye en `context.yaml`

**Implementación:**
1. Modificar `compile-context.md` para:
   - Leer README.md principal
   - Extraer secciones clave (Filosofía, Workflow, Conceptos)
   - Incluir en context.yaml bajo nueva sección (ej: `sistema:`)

2. Modificar `endSession.md` para:
   - Actualizar README.md con conocimiento nuevo si aplica
   - Mantener secciones clave sincronizadas

**Pros:**
- README.md ya existe y tiene info valiosa
- No duplica info (README es fuente de verdad)
- Context Agent ya tiene lógica de lectura y extracción

**Contras:**
- README.md puede crecer demasiado
- Difícil distinguir qué extraer vs qué no
- README.md es para humanos, no está estructurado para agents

### Opción B: Nueva Sección en context.yaml - "sistema:"

**Concepto:**
- Agregar sección `sistema:` en `context.yaml`
- Context Agent extrae/resume conceptos de múltiples fuentes
- Similar a como extrae gotchas de sessions

**Estructura propuesta:**
```yaml
sistema:
  filosofia:
    templates_permanentes: "memory/templates/ NO se borran, son guías activas"
    memsys3_templates: "Estructura EXACTA del producto final, se copia completa"
    deployment: "Clone temporal → copiar → briefing → borrar temp"

  archivos_criticos:
    con_datos: ["context.yaml", "project-status.yaml", "full/adr.yaml", "full/sessions.yaml"]
    plantillas: ["templates/*.yaml", "agents/*.yaml"]
    safe_actualizar: ["viz/", "prompts/", "templates/"]

  prompts_disponibles:
    - nombre: "newSession.md"
      proposito: "Iniciar sesión de trabajo"
    - nombre: "endSession.md"
      proposito: "Documentar sesión y aplicar rotación"
    # etc.

  escalabilidad:
    rotacion: ">1800 líneas sessions/ADRs → archivos _N"
    contingencia: ">150K tokens full/ → archivar a history/"
    limite_context: "2000 líneas máximo"
```

**Implementación:**
1. Definir estructura en `memory/templates/context-template.yaml`
2. Context Agent extrae info de:
   - README.md (secciones específicas)
   - DEVELOPMENT.md (filosofía)
   - UPDATE.md (archivos safe vs críticos)
3. Compila en sección `sistema:` de context.yaml

**Pros:**
- Estructurado y fácil de leer para agents
- Extracción inteligente (no copia todo)
- Escalable (agregar más conceptos sin inflar)

**Contras:**
- Requiere definir qué información incluir
- Posible duplicación con ADRs
- Añade complejidad al compile-context.md

### Opción C: Sección "docs_criticos:" en project-status.yaml

**Concepto:**
- Agregar referencia a documentos críticos en project-status.yaml
- Context Agent los lee opcionalmente según necesidad

**Estructura propuesta:**
```yaml
docs_criticos:
  filosofia_sistema: "docs/DEVELOPMENT.md#filosofia"
  archivos_safe: "docs/UPDATE.md#archivos-safe"
  prompts_disponibles: "memsys3_templates/README.md#prompts"
```

**Pros:**
- Mínima invasión en context.yaml
- Mantiene docs/ como fuente de verdad

**Contras:**
- Requiere que agents lean docs extras (más tokens)
- Fragmentado, no todo en context.yaml
- Depende de estructura estable de docs

### Opción D: README.md Estructurado como Fuente de Verdad

**Concepto:**
- Reestructurar README.md con secciones claramente marcadas
- Context Agent extrae secciones específicas (usando marcadores)
- endSession.md puede actualizar secciones específicas

**Estructura propuesta:**
```markdown
# memsys3

<!-- CONTEXT_START: filosofia -->
## Filosofía del Sistema
[Info crítica para agents]
<!-- CONTEXT_END: filosofia -->

<!-- CONTEXT_START: deployment -->
## Deployment
[Workflow crítico]
<!-- CONTEXT_END: deployment -->

<!-- NO_CONTEXT -->
## Para Developers
[Info específica de dev, no incluir en context]
<!-- /NO_CONTEXT -->
```

**Implementación:**
1. Agregar marcadores HTML comments en README.md
2. compile-context.md extrae bloques CONTEXT_START/END
3. endSession.md puede actualizar bloques específicos

**Pros:**
- README.md sigue siendo legible para humanos
- Extracción precisa y controlada
- Fácil mantener sincronizado

**Contras:**
- Requiere reestructurar README.md actual
- Marcadores HTML pueden confundir
- No resuelve ambigüedad dev vs sistema

---

## 🔍 Análisis de Opciones

### Recomendación: Opción B + Opción A (híbrido)

**Fase 1: Agregar sección `sistema:` en context.yaml (Opción B)**
- Define estructura clara de conceptos críticos
- Context Agent extrae de README.md y DEVELOPMENT.md
- Incluye: filosofía, archivos críticos, prompts, escalabilidad

**Fase 2: Context Agent lee README.md (Opción A)**
- compile-context.md lee README.md principal
- Extrae secciones relevantes para `sistema:`
- Mantiene README.md como fuente de verdad

**Fase 3: endSession.md mantiene README.md (Opción A)**
- Si hay cambios significativos en sistema, actualizar README.md
- Instrucciones en endSession.md para mantener sincronizado

**Por qué este híbrido:**
- Estructurado (Opción B) pero no inventa info
- Usa README existente (Opción A) como fuente
- Escalable y mantenible
- No rompe filosofía actual del Context Agent

---

## 🚧 Desafíos a Resolver

1. **Qué información incluir**
   - Definir lista exhaustiva de conceptos críticos
   - Balancear completitud vs tokens

2. **Separar dev vs sistema**
   - Clarificar qué partes de DEVELOPMENT.md son genéricas
   - Tal vez crear SYSTEM.md separado de DEVELOPMENT.md

3. **Límite de tokens**
   - context.yaml tiene límite 2000 líneas
   - Agregar sección `sistema:` consume líneas
   - Puede requerir priorización o compresión

4. **Mantenimiento**
   - Mantener README.md, DEVELOPMENT.md y context.yaml sincronizados
   - Evitar duplicación innecesaria
   - Clear ownership de cada concepto

5. **Ambigüedad memsys3_templates/README.md**
   - ¿Debe Context Agent leerlo también?
   - ¿O solo README.md raíz?
   - Requiere decisión clara

---

## 📋 Pasos Sugeridos

### Inmediato (Exploración)

1. **Inventariar conceptos críticos**
   - Listar qué info DEBE estar en context.yaml
   - Categorizar por importancia
   - Estimar tokens necesarios

2. **Prototipar sección `sistema:`**
   - Crear estructura YAML de ejemplo
   - Validar que cabe en límite 2000 líneas
   - Verificar utilidad para agents

3. **Evaluar ambigüedad docs/**
   - Revisar DEVELOPMENT.md línea por línea
   - Marcar qué es dev-specific vs genérico
   - Considerar split en dos documentos

### Implementación (Cuando se decida)

4. **Modificar context-template.yaml**
   - Agregar sección `sistema:` con estructura
   - Documentar campos y propósito

5. **Modificar compile-context.md**
   - Agregar lógica de lectura de README.md
   - Extracción de conceptos clave
   - Población de sección `sistema:`

6. **Modificar endSession.md**
   - Instrucciones para actualizar README.md si aplica
   - Mantener sincronización

7. **Documentar en ADR**
   - Decisión de qué información incluir
   - Razón de estructura elegida
   - Trade-offs aceptados

---

## 🎯 Impacto Esperado

**Si se implementa correctamente:**

✅ Nuevas instancias de Claude Code sabrán:
- Filosofía fundamental de memsys3
- Qué archivos son plantillas vs datos
- Workflow de deployment y actualización
- Conceptos de escalabilidad (rotación, contingencia)
- Prompts disponibles y su uso

✅ Reducción de confusión:
- Menos preguntas básicas sobre el sistema
- Menos errores por desconocimiento de filosofía
- Mejor onboarding para nuevos projects

✅ Mejor mantenimiento:
- Info crítica centralizada en context.yaml
- Sincronización clara entre docs y contexto
- README.md sigue siendo fuente de verdad

---

## 📚 Referencias

- **Sesión identificación:** 2025-11-03-verificacion-escalabilidad
- **Documentos relevantes:**
  - README.md (raíz)
  - docs/DEVELOPMENT.md
  - docs/UPDATE.md
  - memsys3_templates/README.md
  - memory/templates/context-template.yaml
  - prompts/compile-context.md
  - prompts/endSession.md

---

## 💬 Notas

- Este improvement es complementario a ISSUE-001 (escalabilidad mantenimiento)
- Ambos abordan problemas de mantenibilidad y escalabilidad
- ISSUE-001: automatización de verificación
- IMPROVEMENT-001: accesibilidad de info crítica

**Pregunta abierta:** ¿Debería memsys3_templates/README.md también incluirse? Tiene info valiosa sobre uso de prompts y filosofía.

**Consideración:** Si proyecto crece, puede tener sentido tener SYSTEM.md (info genérica del sistema) separado de DEVELOPMENT.md (workflow dev).
