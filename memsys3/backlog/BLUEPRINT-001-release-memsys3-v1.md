# BLUEPRINT-001: Release memsys3 v1.0 — auditoría, pulido y consolidación

**Estado:** Abierto
**Prioridad:** Alta
**Tipo:** Blueprint arquitectónico
**Plazo:** Medio plazo (estimado: 4-8 sesiones según frente)
**Fecha identificación:** 2026-05-07
**Sesión origen:** 2026-05-07 (ADR-020, ADR-021, principio CDC)

---

## Problema / Necesidad

Antes del primer release público v1.0 de memsys3, el sistema necesita:

1. **Documentar formalmente sus principios** (CDC, agnosticismo, una-sola-carpeta, human-in-the-loop, criterio inteligente, file_version inmutable). Hoy están dispersos en ADRs y agents, sin un core canónico.
2. **Auditar coherencia ADRs vs código real**: 21 ADRs aceptadas, ¿se respetan todas en prompts/agents/templates? Hay sospecha de brechas.
3. **Verificar completitud del scaffold en deploy**: todos los directorios y templates deben crearse aunque vacíos. Detectado: `operations.log` no tiene template, `memsys3_templates/backlog/` tenía leak de dogfooding (IMPROVEMENT-008).
4. **Consolidar estrategia de dogfooding**: ADR-011 cubrió la separación, pero conviene revalidar tras 6 meses de uso real.
5. **Eliminar residualidad**: catalán residual, referencias muertas a viz/mind.md, archivos huérfanos, docs obsoletos.
6. **Pulir deploy / actualizar / commands**: Pasos 6.4/6.4.5 nuevos sin smoke test, casos edge, mensajes a usuario.
7. **Comunicación**: README.md raíz, web memsys3.org placeholder, wiki sincronizada.

Sin esto, v1.0 sería un release con CDC alta: los usuarios externos dependerían del azar de qué ejemplos vean para entender el sistema.

## Propuesta / Opciones

**Estrategia adoptada (ver plan):** ejecutar los 7 frentes en orden lógico, principios primero (vara para medir el resto), residualidad y pulido al final.

**Estructura:** 7 frentes, cada uno con criterios de done explícitos. Cada frente puede convertirse en sub-items de backlog si crece.

## Decisiones / Acciones

- [x] Articular principio CDC (sesión 2026-05-07, anotado en `memory.yaml`)
- [x] ADR-020 (memory.yaml + bridge MEMORY.md para Claude)
- [x] ADR-021 (backlog + informe/plan opcionales, anti-CDC)
- [x] Frente 1: Principios sistémicos canónicos — `PRINCIPLES.md` creado (fuente única en `memsys3_templates/`, copia real en `memsys3/`, stub en raíz). 10 principios con CDC como #1. ADR-022. `deploy.md` Paso 2 + `actualizar.md` Paso 6.6 (sustitución diferencial). `newSession.md` instruye carga. (sesión 2026-05-07)
- [x] Frente 2: Auditoría ADRs vs código real (1 a 1) — completado sesión 2026-05-07. Reporte: [`docs/informe_BLUEPRINT-001-auditoria.md`](docs/informe_BLUEPRINT-001-auditoria.md). 18/20 ADRs cumplidas. Brechas → ISSUE-024 (meta 010/011 ausentes), ISSUE-025 (ADR-007 docs/UPDATE.md link roto), ISSUE-026 (ADR-015 deploy.md "DevAgent"). ADR-021 leak cubierto por Frente 3.
- [ ] Frente 3: Scaffold completo en deploy (verificar y completar)
- [x] Frente 4: Completitud de templates — completado sesión 2026-05-07. ADR-024 formaliza criterio **data-vs-as-is** (handle citable) + `operations-template.log` creado en ambos sitios (templates + dogfooting). Side-finding: sync `context-template.yaml` dogfooting (DevAI → Main Agent, brecha ADR-015 latente). Cierra pendiente prioritario 3 de project-status.yaml.
- [x] Frente 5: Eliminación de residualidad — completado sesión 2026-05-08. Reporte: [`docs/informe_BLUEPRINT-001-residualidad.md`](docs/informe_BLUEPRINT-001-residualidad.md). 33 hits resueltos en 14 archivos (catalán YAML ejemplo en memory/README.md ×2; DevAgent/DevAI ×12 en prompts/agents/README cierra ISSUE-026 + IMPROVEMENT-006; viz/mind.md ×12 en DEVELOPMENT.md + UPDATE.md + actualizar_cat.md). 0 archivos huérfanos. 0 docs obsoletos. Sin ADR nueva. Siguiente: Frente 6.
- [x] Frente 6: Estrategia dogfooting revisada — completado sesión 2026-05-08. **ADR-025** formaliza la estrategia (commitear `memsys3/` + protocolo anti-leak en dos capas) — primera ADR sobre dogfooting versionado (ISSUE-024 confirmó que ADR-011 nunca existió, era convención informal en README:235-247). Capa 1: hook `.githooks/pre-commit` (bash agnóstico) que veta items `[A-Z]+-[0-9]+-*.md` en `memsys3_templates/backlog/`. Capa 2: bloque PASO 6.5 añadido a `comprobar_alineamiento.md`. Mecanismos descartados (regla en `actualizar.md`, CI check). ISSUE-028 abierto para CI check futuro. README raíz actualizado con instrucción `git config core.hooksPath .githooks`. Cierra vector IMPROVEMENT-008 sistémicamente.
- [ ] Frente 7: Pulir deploy/actualizar/commands + smoke tests

## Criterio de "release v1.0"

- 7 frentes completados
- 0 brechas detectadas en auditoría ADRs
- Scaffold en deploy crea TODO (verificable: `ls memsys3/` post-deploy en proyecto limpio coincide con inventario canónico)
- 0 strings catalanes residuales
- README.md raíz alineado con principios
- Web memsys3.org desplegada (al menos placeholder)
- CHANGELOG.md con notas de release
- Tag git `v1.0.0`

## Referencias

- **Informe:** [`docs/informe_BLUEPRINT-001.md`](docs/informe_BLUEPRINT-001.md)
- **Plan:** [`docs/plan_BLUEPRINT-001.md`](docs/plan_BLUEPRINT-001.md)
- **ADRs origen:** ADR-020 (memory.yaml), ADR-021 (backlog docs)
- **Sesión origen:** 2026-05-07 (ver `sessions.yaml`)
- **Items relacionados:**
  - ISSUE-006 (.gitignore backups)
  - ISSUE-021 (auto-memory Claude — cerrado por ADR-020)
  - ISSUE-022 (hook pre-commit anti-firma)
  - FEATURE-012 (glosario conceptos)
- **Pendientes prioritarios afectados:** todos los 1-7 de `project-status.yaml`
