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

## Proceso de Compilación

### Fase 1: Evaluación Inicial

1. **Lee** todos los inputs completos:
   - `README.md` (raíz del proyecto)
   - `memsys3/memory/full/adr.yaml`
   - `memsys3/memory/full/sessions.yaml`
   - `memsys3/memory/project-status.yaml`

2. **Estima tokens totales** (aproximado: caracteres / 4)

3. **Decide estrategia:**
   - Si < 150K tokens → Proceso normal (continúa a Fase 2)
   - Si > 150K tokens → Archivado necesario (continúa a Plan de Contingencia)

### Fase 2: Compilación Normal (< 150K tokens)

1. **Evalúa** la relevancia de cada elemento con el criterio de selección
2. **Decide** qué es imprescindible para un agent descontextualizado
3. **Sintetiza** manteniendo solo lo crítico
4. **Genera** context.yaml siguiendo el template
5. **Comprueba** que no supera 2000 líneas
6. **Añade notas** a `notes_compilacio` explicando tus criterios

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

## ⚠️ Verificación Post-Compilación

**Después de generar `context.yaml` exitosamente**, pregunta al usuario:

---

**📝 Verificación de README.md**

El contexto compilado ahora incluye una versión sintetizada de tu `README.md` del proyecto.

**¿El README.md refleja el estado actual del proyecto?**

Considera si el README incluye:
- ✅ Descripción actualizada de lo que hace el proyecto
- ✅ Objetivos y propósito actuales (no obsoletos)
- ✅ Stack tecnológico correcto (si ha cambiado)
- ✅ Instrucciones de instalación/setup vigentes
- ✅ Features principales implementadas recientemente
- ✅ Links a documentación/demo actualizados

**¿Necesitas que revise y actualice el README.md del proyecto?**

Si el usuario responde que SÍ:
1. Lee el README.md actual completo
2. Lee el project-status.yaml para ver features, stack actual, estado del proyecto
3. Identifica discrepancias (features no mencionadas, stack desactualizado, objetivos cambiados)
4. Propón actualizaciones concretas al README.md
5. Si el usuario aprueba, actualiza el README.md
6. **IMPORTANTE**: Re-ejecuta compile-context.md para incluir el README actualizado en el contexto

Si el usuario responde que NO:
- Confirma que la compilación está completa
- Recuerda que el README se puede actualizar en cualquier momento ejecutando este prompt de nuevo

---

**Razón de esta verificación:**

El README es el primer archivo que nuevas instancias verán en el contexto compilado. Mantenerlo actualizado asegura que:
- Nuevas instancias tengan información correcta del proyecto
- No haya confusión entre lo documentado y lo real
- El contexto compilado sea una fuente única de verdad

---
