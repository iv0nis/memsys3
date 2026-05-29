# Changelog

Todos los cambios notables de memsys3 documentados aquí.

Formato basado en [Keep a Changelog](https://keepachangelog.com/).
Versionado según [Semantic Versioning](https://semver.org/).

## [Unreleased]

## [0.28.1] - 2026-05-29
### Changed
- `github.md`: el workflow de release ahora actualiza `CHANGELOG.md` en cada tag — Paso 4 ampliado + nuevo sub-paso 4.1 (formato Keep-a-Changelog). Corrige un hueco sistémico: el workflow no contemplaba el CHANGELOG, por lo que v0.25.0–v0.28.0 se publicaron sin entrada (sesión 2026-05-27).
- `actualizar.md`: callout en Paso 2 — el CHANGELOG no es fuente de verdad de versión (lo es el tag git).
- `compile-context.md`: Fase 3 lee la especificación del template literalmente.
### Fixed
- ISSUE-024: `adr.yaml` restaura ADR-010 y ADR-011 al índice como entradas vacantes documentadas (existieron pero desaparecieron del índice en el reset de versionado v1.9→v0.8.0); neutraliza referencias colgantes y una contradicción interna del índice (sesión 2026-05-29).
### Docs
- Reconstrucción de las entradas de CHANGELOG para v0.25.0–v0.28.0 (estaban ausentes).

## [0.28.0] - 2026-05-21
### Added
- **`newSession.md` v0.3.0 — imperatividad cross-harness** (sesión 2026-05-21): refactor del prompt crítico tras reunión investigación con Agent Gemini (`memsys3/docs/meets/20260521_1.md`). Tres mejoras estructurales que suben imperatividad sin romper agnosticismo:
  - §0.5 contrato de idioma explícito (ningún archivo canónico instruía sobre idioma de respuesta — defaults del harness ganaban).
  - §1 carga de contexto imperativa numerada con condición de completitud.
  - §2 Capa 3 instrucción imperativa primero (DEBES) + justificación después.
- Stubs Capa 3 commiteados como artefactos canónicos: `CLAUDE.md`, `GEMINI.md` (junto a `AGENTS.md` ya existente).
- Smoke tests cross-harness validados: codex CLI 2026-05-20 + gemini CLI 2026-05-21 pre-fix y post-fix. Tres backends ortogonales (OpenAI gpt-5.5, Google gemini-2.5-flash, Anthropic dev).
### Fixed
- Bug cross-harness: redacción declarativa en bullets era interpretada por LLMs prudentes (Gemini confirmado) como referencias diferidas, no como protocolo a ejecutar.
- Bug idioma: defaults del harness ganaban sin contrato canónico.
- Gotchas canonizados: `gemini-cli-no-pollea`, `protocolo-declarativo-vs-imperativo`.

## [0.27.0] - 2026-05-19
### Added
- **Setup Agent operativo** (ADR-028, BLUEPRINT-002 Bloque A 2026-05-16): tercer rol agéntico del sistema, responsable del lifecycle memsys3 (deploy + actualizar). `agents/setup-agent.yaml` en dogfooding + template, file_version 0.1.0. Permisos amplios sobre infraestructura + datos; único autorizado a bumpear `file_version`. 5 restricciones (alcance acotado, firma commits, datos de sesión, memoria agnóstica, operaciones git).
- **`deploy.md` agnóstico desde nacimiento** (BLUEPRINT-002 Bloque B refactor 2026-05-18): no agnostificado a posteriori, escrito agnóstico desde el primer commit. Eliminadas tools propietarias del core.
  - Paso 0 SA + contrato de ejecución agnóstico (sin `AskUserQuestion` ni `@-mention`).
  - Detección `deploy-config.yaml` (modo declarativo opt-in).
  - Briefing por naturaleza del proyecto (dominio/objetivo/audiencia, no stack).
  - Propagación `AGENTS.md` a raíz del proyecto destino.
  - Compilación inline de `context.yaml` v0.1.0 (justificación ADR-028 vs ADR-008).
- `AGENTS.md` SSoT en `memsys3_templates/` (estándar agents.md cross-tool).
- `deploy-config-template.yaml`: fallback declarativo opt-in agnóstico.
### Changed
- Convención de commits: atómicos por bloque vía workflow `github.md` (no acumular hacia v1.0.0). Anula convención previa.
### BREAKING
- `deploy.md` elimina `AskUserQuestion`/comandos globales del core (agnóstico). Compatibilidad: harnesses propietarios siguen funcionando vía contrato declarativo.

## [0.26.0] - 2026-05-13
### Added
- **ADR-028 Setup Agent** (sesión 2026-05-12): declaración del tercer rol agéntico responsable del lifecycle memsys3 (deploy + actualizar). Alcance reducido por diseño. Implementación pendiente en BLUEPRINT-002.
- **EXPLORATION-005**: tensión flexibilidad MA amoldando memsys3 al dominio vs robustez principio #10. Separada para no acoplar a ADR-028.
- **BLUEPRINT-002**: implementación de ADR-028 en 5 bloques ejecutables (item + informe + plan, gitignored en `memsys3/backlog/`).
- `memsys3/README.md` scaffold-mirror dogfooding añadido.
### Changed
- **ADR-027 UPDATE Capa 3 — trigger declarativo** (sesión 2026-05-11): refinamiento de `AskUserQuestion` estático a trigger declarativo en `newSession.md`. No enumera modelos (coherente con principio de agnosticismo). `AGENTS.md` root minimizado a solo invariante de memoria agnóstica.

## [0.25.0] - 2026-05-10
### Added
- **ADR-027 memoria agnóstica multi-modelo** (sesión 2026-05-10): extiende ADR-020 sin invalidarla. Diseño en 3 capas:
  - Capa 1: invariante canónico textual en 4 archivos × 2 (`newSession.md`, `compile-context.md`, `main-agent.yaml`, `context-agent.yaml`, en dogfooding + templates).
  - Capa 2: `AGENTS.md` en raíz del repo (estándar agents.md; cobertura nativa Codex/Cline/Copilot/Kilo/Warp; vía config Cursor/Aider).
  - Capa 3: bridges per-modelo opcionales (pendiente en `deploy.md`, no bloqueante v1.0.0).
- ADR-020 sigue vigente (`memory.yaml` canónica); ADR-027 generaliza el bridge sin invalidarla.
### Fixed
- Typo sistémico `dogfooting → dogfooding` (13 archivos, 56 ocurrencias, todas las variantes incluyendo mayúsculas).

## [0.24.1] - 2026-05-08
### Added
- **BLUEPRINT-001 Frente 7 completado**: 6 smoke tests end-to-end para deploy/actualizar/commands y hook anti-leak validados.
- Paso 2.7 defensivo en `endSession.md` (EXPLORATION-004 Opción A): canonización proactiva anti-CDC con recordatorio disposicional referenciando PRINCIPLES.md #1.
- `backlog/docs/informe_BLUEPRINT-001-smoke-tests.md` como documento anti-CDC.
- ISSUE-029 abierto: descriptions internas `commands.md` no cubren features post-Frentes 1-6.
### Fixed
- 2 feedbacks canonizados a `memory.yaml` (locks solo paralelismo humano confirmado; plans deben cubrir sub-pasos opcionales).
- 1 gotcha canonizado: `exit-code-pipe-bash`.

## [0.24.0] - 2026-05-08
### Added
- **Integración multi-work dogfooding** (temporal pre-v1.0): sistema de coordinación entre agentes paralelos con locks explícitos.
- `memsys3/prompts/multi_work.md`: workflow 5 pasos (pre-plan check, append, trabajo libre, cleanup, caducidad >4h).
- `memsys3/blocked_files_log.md`: log central operacional de bloqueos.
- Bloque `coordinacion_paralela` inline en `main-agent.yaml`.

> Nota: este sistema se evaluará en Frente 8 BLUEPRINT-001 — decisión pendiente sobre inclusión definitiva en v1.0 release.

## [0.23.1] - 2026-05-08
### Added
- **ADR-025**: estrategia dogfooding versionado formalizada (primera ADR sobre el tema).
- **Hook anti-leak** `.githooks/pre-commit` (bash agnóstico): veta items `[A-Z]+-[0-9]+-*.md` en `memsys3_templates/backlog/`. Activación opt-in vía `git config core.hooksPath .githooks`.
- Auditoría PASO 6.5 en `comprobar_alineamiento.md`: capa 2 de defensa anti-leak.
- README raíz: instrucción de activación de hooks para contribuidores.
- ISSUE-028 abierto: CI check anti-leak (futuro pipeline).
### Changed
- Rotación `adr.yaml` → `adr_1.yaml` (1994 líneas, hasta ADR-024).

## [0.23.0] - 2026-05-07
### Added
- **`memory.yaml` agnóstico + bridge `MEMORY.md` opcional Claude** (ADR-020): separa memoria distribuible de instrucciones Claude-específicas.
- **`backlog/docs/` con informe y plan opcionales anti-CDC** (ADR-021): documentación estructurada en backlog para contexto de continuidad.
- **`PRINCIPLES.md` canónico con 10 principios sistémicos** (ADR-022, BLUEPRINT-001 Frente 1): documento fundacional del sistema.
- Auditoría 20 ADRs vs código real (BLUEPRINT-001 Frente 2): 18/20 cumplidas.

## [0.22.0] - 2026-05-06
### Added
- ADR-017: sistema `file_version` por archivo (versionado independiente).
- ADR-018: sustitución diferencial de templates de schema en `actualizar.md`.
- ADR-019: política de evolución de schema (deprecation contextualizada).
- Lógica nueva en `actualizar.md` Paso 6.4 (sustitución diferencial) y 6.4.5 (detección deprecated/huérfanos).
### Fixed
- ISSUE-023: fugas dogfooding en archivos legacy operativos.
### Changed
- Limpieza scaffolds `memsys3_templates/memory/` (4 archivos vaciados a Modelo D).
- `.gitignore`: `docs/` excluido (material local no distribuible).

## [0.21.1] - 2026-05-05
### Added
- Restricción `operaciones_git` en `main-agent`: lectura obligatoria de `github.md` antes de cualquier operación git (defensa anti-firma).
- ISSUE-021, ISSUE-022 (hook pre-commit anti-firma), EXPLORATION-003 (READMEs modulares) abiertos.

## [0.21.0] - 2026-04-16
### Changed
- README reescrito con propuesta de valor diferencial (una carpeta, agnóstico, human in the loop, `@` mentions, límites configurables).
- Wiki GitHub creada: Home, Prompts Reference, Workflow, Agents + sidebar.
### Fixed
- Terminología agnóstica: `Development Agent`/`DevAI` erradicado de templates y docs (15 archivos).
- Restricción infraestructura quitada del `main-agent` dogfooding (deadlock).
- `github.md`: warning obligatorio con `AskUserQuestion` para confirmar tag.

## [0.20.0] - 2026-04-15
### Added
- Sistema `file_version` independiente por archivo (`0.Y.Z` en 21 archivos de infraestructura).
- Restricciones de infraestructura memsys3 en `main-agent.yaml` y `context-agent.yaml`.
### Changed
- `viz/` archivada en `docs/archivo/viz/` y eliminada de producción.
- `mind.md` eliminado.
### Fixed
- Catalán erradicado de keys YAML, templates, prompts y agents (~60 campos).

## [0.19.2] - 2026-04-13
### Added
- Sistema de 5 tiers de ingesta para Context Agent (hasta 150K tokens): memory/full obligatorio, README, backlog completo, docs_contextuales, git log reciente.
- Nuevo paso en `endSession` para referenciar docs importantes al Context Agent.

## [0.19.1] - 2026-03-26
### Added
- `operations.log` en `memory/full/` para trazabilidad de actualizaciones y compilaciones, con rotación estilo sessions (≥1800 líneas).

## [0.19.0] - 2026-03-25
### Added
- Nuevo prompt `git.md` para tracking local sin push.
### Changed
- 7 prompts mejorados: actualizar, adr, backlog, compile-context, endSession, github, newSession.
- Prompts específicos de memsys3 movidos a `memsys3/prompts-dev/`.
### Fixed
- ISSUE-018: `actualizar.md` preserva archivos custom del proyecto.

## [0.18.0–0.18.3] - 2026-03-08 / 2026-03-14
### Added
- `migrate.md`: guía de migración de proyectos preservando historial Claude Code.
- `reference.md`: sección migración en docs técnicos.
### Fixed
- ISSUE-017: `agent_id` guardado en `~/.claude/` (compatible cross-platform) en lugar de `/tmp/`.
- ISSUE-016: `endSession` avisa tras 5+ sesiones sin compilar context.yaml.
- 3 bugs en `actualizar.md`: ruta absoluta `$PROJECT_ROOT`, `mv` con path destino explícito, limpieza preventiva artefactos.
### Changed
- `deploy.md`: recomendación gitignore invertida (incluir memsys3 por defecto); briefing en dos fases con `AskUserQuestion`.

## [0.17.0] - 2026-03-07
### Added
- `meet.md`: checklist obligatorio 3 pasos (ESCRIBIR/RESUMIR/POLLING) con task ID.
### Changed
- `docs/`: 9 archivos individuales fusionados en `reference.md`.

## [0.15.0–0.16.0] - 2026-03-06
### Added
- `endSession`: detecta sesiones sin compilar, recordatorio pasivo desde 5 (ISSUE-016).
- `actualizar.md` Paso 0b: bootstrap clona repo y sobrescribe prompt local antes de continuar.
### Fixed
- Múltiples bugs `actualizar.md`: auto-recursión backup, `docs/` siempre copiado, creación `backlog/`, orden de pasos, verificación activa post-edición.

## [0.13.0–0.14.0] - 2026-03-06
### Added
- `memsys3_templates/docs/` (9 archivos de referencia técnica).
- Prompt `agent-identity.md` para asignación de `agent_id`.
- `agent_id` persistente entre compacts.
### Changed
- `actualizar.md`: detecta archivos eliminados con `--name-status`, backups en `memsys3/docs/backups/`.
- `meet.md`: briefing obligatorio del convocante; convocante propone Decisión.

## [0.12.0–0.12.1] - 2026-02-17 / 2026-03-03
### Added
- `meet.md` v2.0 unificado: fusiona `meet-coord.md` y `meet-research.md`.
- Convención `agent_id` multi-ventana, persistencia en compact.
### Removed
- `meet-coord.md` y `meet-research.md` (reemplazados por `meet.md` unificado).

## [0.11.0–0.11.3] - 2026-02-03 / 2026-02-17
### Added
- Sistema Reuniones Colaborativas completo: `reunion.md` (905 líneas), `docs/reunion/README.md` (836 líneas), filosofía 5 principios.
- Statusline personalizable para Claude Code.
### Fixed
- **Fix crítico `github.md`**: defensa en profundidad 4 capas para prevención firmas Co-Authored-By (margen error: 70% → 5%).
### Changed
- Arquitectura dogfooding: `docs/` → `memsys3/docs/` (14 archivos, consistencia).

## [0.10.0] - 2026-02-03
### Added
- Sistema de clasificación de sesiones por peso (bajo/medio/alto).
- Context Agent con síntesis diferenciada por peso (90%/60%/40%).
- PASO 2.5 en `endSession.md`: evaluación de peso con criterios claros.

## [0.9.0] - 2025-12-30
### Added
- ADR-016: principio agnóstico (memsys3 funciona con cualquier modelo IA).
- ADR-015: terminología unificada `Main Agent` como nomenclatura estándar.
- Sistema de comandos globales auto-actualizantes: `commands.md`, `/deploy-memsys3`, `/actualizar-memsys3`.
### Fixed
- ISSUE-005 (crítico): `actualizar.md` no copiaba `adr.md`, `backlog.md`, `commands.md` — pérdida silenciosa de funcionalidad en actualizaciones.

## [0.8.0–0.8.1] - 2025-12-12 / 2025-12-14
### Added
- Prompt `adr.md`: sistema de gestión ADRs (consultar, crear, actualizar).
- Comando global `/deploy-memsys3` ejecutable desde cualquier proyecto.
- Metadata rica en tags git: sesiones, ADRs, breaking changes.
- ADR-013: consistencia arquitectónica sistema de gestión.

## [0.7.0–0.7.1] - 2025-11-14 / 2025-12-02
### Changed
- Backlog consolidado en `memsys3/backlog/` (dogfooding); `memsys3_templates/backlog/` solo README distribuible.
- `context.yaml` v1.9 compilado: 403 líneas, reducción 76% tokens.

## [0.5.0–0.6.1] - 2025-11-12
### Added
- `actualizar.md` (551 líneas): actualización segura con detección de estructura antigua, backups y testing real.
- Context Agent lee `README.md` del proyecto (FEATURE-002).
- Sistema de tracking de versión memsys3 en deployments.

## [0.2.1–0.4.0] - 2025-10-29 / 2025-11-02
### Added
- Prompt `github.md` para gestión de releases.
- Traducción completa catalán → español al 100%.
### Changed
- Limpieza completa del sistema de rutas: prefijo `memsys3/` unificado; eliminados directorios residuales (-6543 líneas).

[0.24.1]: https://github.com/iv0nis/memsys3/releases/tag/v0.24.1
[0.24.0]: https://github.com/iv0nis/memsys3/releases/tag/v0.24.0
[0.23.1]: https://github.com/iv0nis/memsys3/releases/tag/v0.23.1
[0.23.0]: https://github.com/iv0nis/memsys3/releases/tag/v0.23.0
[0.22.0]: https://github.com/iv0nis/memsys3/releases/tag/v0.22.0
[0.21.1]: https://github.com/iv0nis/memsys3/releases/tag/v0.21.1
[0.21.0]: https://github.com/iv0nis/memsys3/releases/tag/v0.21.0
[0.20.0]: https://github.com/iv0nis/memsys3/releases/tag/v0.20.0
[0.19.2]: https://github.com/iv0nis/memsys3/releases/tag/v0.19.2
[0.19.1]: https://github.com/iv0nis/memsys3/releases/tag/v0.19.1
[0.19.0]: https://github.com/iv0nis/memsys3/releases/tag/v0.19.0
[0.18.3]: https://github.com/iv0nis/memsys3/releases/tag/v0.18.3
[0.17.0]: https://github.com/iv0nis/memsys3/releases/tag/v0.17.0
[0.16.0]: https://github.com/iv0nis/memsys3/releases/tag/v0.16.0
[0.13.0]: https://github.com/iv0nis/memsys3/releases/tag/v0.13.0
[0.12.0]: https://github.com/iv0nis/memsys3/releases/tag/v0.12.0
[0.11.0]: https://github.com/iv0nis/memsys3/releases/tag/v0.11.0
[0.10.0]: https://github.com/iv0nis/memsys3/releases/tag/v0.10.0
[0.9.0]: https://github.com/iv0nis/memsys3/releases/tag/v0.9.0
[0.8.0]: https://github.com/iv0nis/memsys3/releases/tag/v0.8.0
[0.7.0]: https://github.com/iv0nis/memsys3/releases/tag/v0.7.0
[0.5.0]: https://github.com/iv0nis/memsys3/releases/tag/v0.5.0
[0.2.1]: https://github.com/iv0nis/memsys3/releases/tag/v0.2.1
