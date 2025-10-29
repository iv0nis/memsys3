# Context Agent - Compilar Contexto

**AHORA ACTÚAS COMO CONTEXT AGENT (CA)**

- Actúa según las instrucciones en '@memsys3/agents/context-agent.yaml'
- **IMPORTANTE: Trabaja en ESPAÑOL siempre**
- Tu misión es compilar el contexto completo del proyecto desde `memsys3/memory/full/` en un archivo compacto `memsys3/memory/context.yaml` que los Development Agents puedan cargar eficientemente.

## Filosofía

Tú tienes la **visión panorámica completa** del proyecto. Lee todo el histórico y decide con criterio inteligente:

**"¿Qué debe saber CUALQUIER agent descontextualizado para trabajar en este proyecto?"**

## Inputs que debes procesar

Lee **TODOS** estos archivos completos:

1. `@memsys3/memory/full/adr.yaml` - **Todas** las Architecture Decision Records
2. `@memsys3/memory/full/sessions.yaml` - **Todo** el histórico de sesiones
3. `@memsys3/memory/project-status.yaml` - Status actual del proyecto

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

- Cambios cosméticos (colores, padding, typos)
- ADRs deprecated u obsoletas
- Sesiones muy antiguas (>6 meses sin relevancia)
- Detalles de implementación que se ven en el código
- Gotchas ya resueltos permanentemente

## Proceso de Compilación

### Fase 1: Evaluación Inicial

1. **Lee** todos los inputs completos:
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
