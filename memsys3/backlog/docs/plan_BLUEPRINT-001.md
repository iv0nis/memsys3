<!-- version: 0.1.0 -->

# Plan: BLUEPRINT-001 — Release memsys3 v1.0

**Item:** [`../BLUEPRINT-001-release-memsys3-v1.md`](../BLUEPRINT-001-release-memsys3-v1.md)
**Informe:** [`informe_BLUEPRINT-001.md`](informe_BLUEPRINT-001.md)
**Fecha plan:** 2026-05-07
**Estimación:** XL — 6-8 sesiones de trabajo (1 por frente, algunas combinables)

---

## 0. Prerequisitos

Antes de empezar CUALQUIER frente:

1. Leer `informe_BLUEPRINT-001.md` completo (este informe es la fuente de verdad anti-CDC)
2. Leer las 21 ADRs en `memsys3/memory/full/adr.yaml` (índice + cualquiera referenciada)
3. Verificar estado limpio del repo:
   ```bash
   git status
   git log --oneline -5
   ```
4. Confirmar versión actual: `grep memsys3_version memsys3/memory/project-status.yaml`
5. **NUNCA firmar commits con `Co-Authored-By:`** (regla dura, ADR-016 + `memory.yaml` feedback)
6. **NUNCA bumpar `file_version` manualmente** durante ejecución — solo `/actualizar-memsys3` (ADR-017). Excepción documentada: dogfooding del propio repo memsys3.

## 1. Bloques de trabajo

Los frentes son ordenados por dependencia. Empezar por (1) — define la vara para medir los demás.

---

### Frente 1 — Principios sistémicos canónicos

**Objetivo:** Crear `PRINCIPLES.md` canónico que documente formalmente los principios de memsys3, eliminando la dispersión actual.

**Archivos afectados:**
- `PRINCIPLES.md` (raíz repo) — NUEVO
- `memsys3_templates/PRINCIPLES.md` — NUEVO (sync para distribución)
- `memsys3/PRINCIPLES.md` — NUEVO (dogfooding sync)
- `README.md` raíz — link a PRINCIPLES.md
- `memsys3_templates/memory/README.md` — link a PRINCIPLES.md
- `memsys3/prompts/newSession.md` y templates — instrucción "lee PRINCIPLES.md si existe"

**Pasos:**
1. Inventariar principios desde el informe sección 3.1
2. Para cada principio: nombre, definición concisa, ADR/archivo donde está formalizado, ejemplo de aplicación
3. Estructura sugerida `PRINCIPLES.md`:
   ```
   # Principios memsys3
   ## 1. Anti-CDC (Casualidad de Contexto)
   ## 2. Agnosticismo de modelo IA
   ## 3. Una sola carpeta
   ## 4. Human-in-the-loop
   ## 5. Criterio inteligente vs límites arbitrarios
   ## 6. Templates como documentación activa permanente
   ## 7. file_version inmutable salvo /actualizar-memsys3
   ## 8. Datos siempre preservados (history/, rotación)
   ## 9. Separation of Concerns README/context/sessions/memory
   ## 10. Restricciones de infraestructura en agents
   ```
4. Cada principio: máx 30 líneas. Total ~300 líneas.
5. Sincronizar a templates (memsys3_templates/) y dogfooding (memsys3/) si decidimos que se distribuye.
6. Si `PRINCIPLES.md` se distribuye → actualizar `deploy.md` para copiarlo.
7. Crear ADR-022 documentando esta decisión (PRINCIPLES como core canónico).

**Criterio de done:**
- [ ] `PRINCIPLES.md` existe en raíz, lista los 10 principios
- [ ] CDC y "anti-CDC como propósito de memsys3" explicitados como #1
- [ ] Cada principio enlaza ADR(s) que lo formalizan
- [ ] README.md raíz menciona PRINCIPLES.md como referencia
- [ ] ADR-022 creada
- [ ] Decidido si se distribuye (templates) o solo es repo-level

---

### Frente 2 — Auditoría ADRs vs código real

**Objetivo:** Verificar que las 21 ADRs aceptadas se respetan en prompts/agents/templates. Documentar brechas detectadas como ISSUEs.

**Archivos afectados (lectura):**
- `memsys3/memory/full/adr.yaml`
- `memsys3_templates/` (todo el scaffold)
- `memsys3/agents/*.yaml` y `memsys3_templates/agents/*.yaml`
- `memsys3_templates/prompts/*.md`

**Pasos:**
1. Leer ADRs por orden numérico (001-021)
2. Para cada ADR aceptada, identificar:
   - ¿Qué archivos deberían reflejarla?
   - ¿Lo hacen?
   - Si no: documentar gap como nuevo ISSUE (descriptivo, prioridad estimada)
3. Brechas sospechosas iniciales (informe sección 3.2):
   - ADR-009: `templates/` se preservan en deploy/actualizar
   - ADR-012: `compile-context.md` NO duplica README en context.yaml
   - ADR-017: restricción file_version está en `memsys3_templates/agents/main-agent.yaml`
   - ADR-018: Pasos 6.4/6.4.5 implementados (no smoke-tested)
   - ADR-019: campos deprecados llevan motivo
4. Generar reporte: `memsys3/backlog/docs/informe_BLUEPRINT-001-auditoria.md` (o en mismo doc)
5. Crear ISSUEs por cada brecha real

**Criterio de done:**
- [ ] Las 21 ADRs revisadas 1 a 1
- [ ] 0 brechas críticas pendientes (todas tienen ISSUE creado o están resueltas)
- [ ] Reporte de auditoría en `backlog/docs/`

---

### Frente 3 — Scaffold completo en deploy

**Objetivo:** El scaffold creado por `deploy.md` debe contener TODOS los directorios y archivos del sistema, aunque vacíos. Verificar y completar.

**Archivos afectados:**
- `memsys3_templates/prompts/deploy.md`
- `memsys3_templates/prompts/actualizar.md`
- `memsys3_templates/memory/full/` (potencialmente añadir adr.yaml/sessions.yaml/operations.log vacíos)
- `memsys3_templates/backlog/` (limpiar IMPROVEMENT-008 leak)

**Pasos:**
1. Definir inventario canónico de scaffold (qué directorios + qué archivos vacíos):
   ```
   memsys3/
   ├── agents/main-agent.yaml, context-agent.yaml
   ├── memory/
   │   ├── README.md
   │   ├── context.yaml          (vacío Modelo D)
   │   ├── memory.yaml           (vacío Modelo D)
   │   ├── project-status.yaml   (personalizado en deploy)
   │   ├── full/
   │   │   ├── adr.yaml          (frontmatter + array vacío)
   │   │   ├── sessions.yaml     (frontmatter + array vacío)
   │   │   └── operations.log    (frontmatter + array vacío)
   │   ├── history/.gitkeep
   │   └── templates/ (todos los *-template.{yaml,md})
   ├── prompts/ (~17 archivos)
   └── backlog/
       ├── README.md
       └── docs/.gitkeep
   ```
2. Limpiar `memsys3_templates/backlog/IMPROVEMENT-008-*.md` (leak dogfooding)
3. Decidir: ¿plantillas de "datos vacíos" (`adr.yaml` vacío, etc.) van inline en deploy.md (estado actual) o se mueven a `memory/templates/` con sufijo distintivo?
   - Opción A (statu quo): mantener inline en deploy.md
   - Opción B: añadir `*-empty.yaml` en templates, deploy los copia
   - **Recomendación**: Opción B por consistencia ADR-009 (templates como documentación activa permanente)
4. Si Opción B: crear `adr-empty.yaml`, `sessions-empty.yaml`, `operations-empty.log` en templates
5. Actualizar deploy.md para copiar desde templates en vez de heredoc inline
6. Crear ADR-023 documentando la decisión "scaffold completitud"
7. Smoke test: deploy en proyecto de prueba, verificar todo el inventario

**Criterio de done:**
- [ ] Inventario canónico documentado en ADR-023
- [ ] `memsys3_templates/backlog/IMPROVEMENT-008-*.md` eliminado
- [ ] Smoke test en proyecto limpio: `ls -R memsys3/` post-deploy coincide con inventario
- [ ] Si Opción B: 3 nuevos templates *-empty.* + deploy.md actualizado

---

### Frente 4 — Completitud de templates

**Objetivo:** Cada archivo del scaffold tiene template equivalente en `memory/templates/`.

**Archivos afectados:**
- `memsys3/memory/templates/` y `memsys3_templates/memory/templates/`

**Pasos:**
1. Inventariar archivos del scaffold final (post-Frente 3)
2. Verificar 1-a-1: cada archivo tiene template en `memory/templates/`
3. Crear los faltantes:
   - `operations-template.log` (pendiente prioritario 3 de project-status)
   - Posibles faltantes detectados en auditoría
4. Sincronizar memsys3/memory/templates/ ↔ memsys3_templates/memory/templates/

**Criterio de done:**
- [ ] Cada archivo del scaffold tiene template
- [ ] Templates sincronizados en ambos sitios
- [ ] Pendiente prioritario 3 cerrado

---

### Frente 5 — Eliminación de residualidad

**Objetivo:** 0 strings catalanes, 0 referencias muertas, 0 archivos huérfanos.

**Pasos:**
1. **Catalán residual:**
   ```bash
   grep -rni '[àèéíòóúïü]' memsys3_templates/ | grep -v '\.git'
   grep -rniE '\b(això|aquesta|aquest|tasca|tasques|també|només|amb)\b' memsys3_templates/
   ```
2. **Referencias a viz / mind.md:**
   ```bash
   grep -rn 'viz\|mind\.md' memsys3_templates/ memsys3/agents/ README.md
   ```
3. **Archivos huérfanos:**
   - `memsys3/memory/README.md` — verificar que se distribuye y se referencia
   - Cualquier `.md` en `memsys3_templates/` no referenciado desde otro archivo
4. **Docs obsoletos:**
   - Revisar `memsys3/docs/` y `memsys3_templates/` por archivos no actualizados desde >2 meses
5. Limpiar / refactorizar / eliminar según corresponda
6. Crear ISSUEs si algún ítem requiere decisión fuera del scope del frente

**Criterio de done:**
- [ ] `grep -rni '[àèéíòóúïü]' memsys3_templates/` → 0 hits
- [ ] 0 referencias activas a viz/mind.md
- [ ] Inventario archivos huérfanos vacío

---

### Frente 6 — Estrategia dogfooding revisada

**Objetivo:** Decidir y documentar el rol de `memsys3/` (instancia interna) en el repo.

**Pasos:**
1. Leer ADR-011 (separación agnóstico/específico)
2. Evaluar trade-off: `memsys3/` ¿se commitea o `.gitignore`?
   - Pro commitear: ejemplo real de uso, historial visible, valida agnosticismo del scaffold
   - Pro ignorar: aísla código distribuible, evita leaks como IMPROVEMENT-008
   - **Híbrido**: commitear pero con regla explícita de "0 leaks" (auditoría continua)
3. Decidir y documentar como ADR-024 (extensión o supersede de ADR-011)
4. Si se decide ignorar: añadir a `.gitignore` raíz, hacer último commit del estado dogfooding como referencia
5. Si se decide commitear: documentar protocolo anti-leak (linter, hook pre-commit, o auditoría manual periódica)

**Criterio de done:**
- [ ] ADR-024 con decisión razonada
- [ ] `.gitignore` ajustado (si aplica)
- [ ] Protocolo anti-leak definido (si aplica)

---

### Frente 7 — Pulir deploy / actualizar / commands + smoke tests

**Objetivo:** Validar end-to-end los flujos críticos antes de v1.0.

**Pasos:**
1. **Smoke test deploy** en proyecto de prueba limpio:
   - Ejecutar `/deploy-memsys3`
   - Verificar inventario completo (Frente 3)
   - Validar Paso 9 (bridge MEMORY.md) — opt-in funciona
   - Validar Paso 8 (.gitignore) — Opciones A/B funcionan
2. **Smoke test actualizar** en proyecto con memsys3 v0.22.0:
   - Ejecutar `/actualizar-memsys3`
   - Validar Paso 6.4 (sustitución diferencial templates schema)
   - Validar Paso 6.4.5 (deprecation contextualizada)
   - Tres casos: archivo sin file_version, archivo igual, archivo destino > upstream
3. **Smoke test commands.md**: instalación de comandos globales en máquina limpia
4. Documentar gotchas detectados en sessions.yaml
5. Crear ISSUEs por cualquier bug encontrado
6. Pulir mensajes a usuario en deploy/actualizar (claridad, errores recuperables)

**Criterio de done:**
- [ ] Deploy smoke-tested, 0 bugs
- [ ] Actualizar smoke-tested (3 casos templates schema), 0 bugs
- [ ] Commands.md smoke-tested
- [ ] Pendiente prioritario 1 (smoke test actualizar.md) cerrado
- [ ] Mensajes a usuario revisados

---

### Frente 8 (cierre release) — Comunicación + tag v1.0.0

**Objetivo:** Cerrar la release.

**Pasos:**
1. Actualizar `README.md` raíz con propuesta de valor consolidada (post-PRINCIPLES.md)
2. Crear `CHANGELOG.md` con notas de v1.0.0 (consolidando v0.X.Y → v1.0.0)
3. Desplegar web `memsys3.org` (al menos placeholder con redirect/landing minimal)
4. Sincronizar wiki GitHub con principios y nuevas convenciones (informe/plan)
5. Workflow github.md: tag `v1.0.0` con metadata rica
   - **NO firma Co-Authored-By** (defensa multi-capa)
   - AskUserQuestion para confirmar versión
6. Anunciar release (GitHub release notes)

**Criterio de done:**
- [ ] README raíz actualizado
- [ ] CHANGELOG.md creado
- [ ] Web .org desplegada (aunque sea placeholder)
- [ ] Wiki sincronizada
- [ ] Tag `v1.0.0` creado y empujado
- [ ] Release notes publicadas

---

## 2. Validación final (release v1.0)

Antes de tagear v1.0.0:

- [ ] Los 8 frentes con todos sus criterios de done marcados
- [ ] 0 brechas ADRs sin resolver
- [ ] Smoke tests deploy + actualizar OK
- [ ] 0 catalán residual
- [ ] PRINCIPLES.md publicado
- [ ] CHANGELOG.md publicado
- [ ] Web placeholder live
- [ ] Sessions.yaml documenta todas las sesiones del BLUEPRINT
- [ ] BLUEPRINT-001 estado: Completado

## 3. Restricciones de ejecución

- **NO firmar commits con `Co-Authored-By:`** (regla dura, defensa 4 capas en github.md)
- **NO bumpar `file_version` manualmente** — solo dejar que `/actualizar-memsys3` lo haga al desplegar v1.0.0 en proyectos
- **NO ejecutar `compile-context` desde la sesión que ejecuta este plan** — solo en sesión nueva (ADR-008). Sí sugerir endSession con compilación al final de cada frente largo.
- **Antes de cualquier git commit/push/tag**: leer `@memsys3/prompts/github.md` (regla dura main-agent.yaml)
- **Confirmación humana** antes de cualquier acción destructiva (rm, git reset --hard, eliminar archivos del scaffold)

## 4. Riesgos conocidos

| Riesgo | Probabilidad | Mitigación |
|---|---|---|
| Frente 2 (auditoría) destapa muchas brechas → BLUEPRINT-001 se infla | Media | Crear ISSUEs separados, posponer no-críticos a v1.1 |
| Frente 3 (Opción B *-empty templates) rompe deploy en proyectos existentes | Baja | Smoke test exhaustivo Frente 7 antes de release |
| Smoke tests Frente 7 detectan bugs que requieren refactor grande | Media | Considerar Alt D del informe (release v0.23.0 intermedia) |
| Web memsys3.org no se puede desplegar en plazo | Baja | Placeholder estático Vercel/Netlify <30min |
| Catalán residual oculto en archivos no obvios | Baja | grep amplio en Frente 5, NO solo en *.md |

## 5. Sesión recomendada para ejecutar

**Frentes 1, 2, 3, 4**: sesión fresca cada uno, en orden. La lucidez de la sesión actual (2026-05-07) está volcada en este plan + informe — un agente fresco con esos dos documentos puede ejecutar sin CDC.

**Frente 5**: combinar con Frente 4 si quedan recursos.

**Frente 6**: sesión propia (es decisión arquitectónica, requiere deliberación con usuario).

**Frente 7**: sesión dedicada con tiempo para smoke tests reales (no en seco).

**Frente 8**: sesión de cierre, dedicada exclusivamente. Workflow github.md crítico.

**Total estimado**: 6-8 sesiones según paralelización.
