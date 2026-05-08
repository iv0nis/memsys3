# Informe BLUEPRINT-001 Frente 7 — Smoke tests deploy/actualizar/commands

**Fecha:** 2026-05-08
**Sesión:** BLUEPRINT-001 Frente 7
**Scope:** validación end-to-end de los flujos críticos (deploy, actualizar, commands, hook anti-leak) antes de cierre release v1.0 (Frente 8).
**Metodología:** ejecución literal de los bloques bash de los Pasos críticos contra escenarios sintéticos en `mktemp -d`. Hook anti-leak en repo real con cleanup garantizado. Lectura crítica adicional para los pasos no automatizables (gitignore, MEMORY.md bridge, deprecation lógica posterior, commands.md).

---

## Resultados

| Test | Pasos cubiertos | Estado | Observaciones |
|------|-----------------|--------|----------------|
| 1. Deploy inventario canónico | deploy.md Paso 2 (ADR-023) | ✓ | 31 archivos en inventario, coincide 100% con ADR-023. Headers de version intactos en todos los templates / agents / PRINCIPLES.md. Vacíos canónicos correctos en `memory/full/`. |
| 1.5. Deploy Pasos 8/9 (estático) | gitignore + MEMORY.md bridge | ✓ | Estructura coherente, branches A/B bien definidas, AskUserQuestion correctamente especificado, graceful degradation en Paso 9 (ADR-020). |
| 2. Actualizar Paso 6.4 — sustitución diferencial | ADR-018 | ✓ | 3 casos validados con outputs esperados (ver detalle abajo). |
| 3. Actualizar Paso 6.6 — PRINCIPLES.md sync | ADR-022 + ADR-018 | ✓ | 4 casos validados (no existe / sin version / igual / mayor). Helper `extract_md_version` extrae correctamente desde `<!-- version: X.Y.Z -->`. |
| 4. Actualizar Paso 6.4.5 — deprecation | ADR-019 | ✓ | Grep detecta DEPRECATED inyectado. Lógica posterior (comparación claves top-level) correctamente expresa criterio human-in-the-loop. Side-finding documentado abajo. |
| 5. Hook anti-leak | ADR-025 | ✓ | `git commit` con archivo en `memsys3_templates/backlog/[A-Z]+-[0-9]+-*.md` retorna exit=1. Cleanup OK. |
| 6. commands.md (estático) | ADR-014 | ✓ con notas | Launcher pattern OK. 1 ISSUE-029 menor abierto (descripciones internas no mencionan features post-Frentes 1-6). |

**Conclusión:** los 3 flujos críticos funcionan correctamente. 0 bugs bloqueantes. 1 ISSUE menor (ISSUE-029, prioridad baja).

---

## Detalle Test 2 — Sustitución diferencial Paso 6.4

Setup en `$TMPDIR/test-actualizar/`:

- Caso A — `project-status-template.yaml` con línea `# version:` eliminada (legacy pre-ADR-017).
- Caso B — `adr-template.yaml`, `context-template.yaml`, `memory-template.yaml` con misma versión que upstream (0.1.0).
- Caso C — `sessions-template.yaml` con header bumpado manualmente a `99.0.0`.

Output literal de la ejecución:

```
✅ adr-template.yaml — versiones iguales (0.1.0), no se toca
✅ context-template.yaml — versiones iguales (0.1.0), no se toca
✅ memory-template.yaml — versiones iguales (0.1.0), no se toca
⚠️ project-status-template.yaml — destino sin file_version (legacy pre-ADR-017). Sustituyendo (v_up=0.1.0)
🚨 sessions-template.yaml — destino 99.0.0 > upstream 0.1.0. Estado anómalo.
```

Post-estado destino:

- `project-status-template.yaml` → ahora tiene `# version: 0.1.0` (sustituido). ✓
- `sessions-template.yaml` → sigue con `# version: 99.0.0` (NO sobrescrito; en agente real entraría a `AskUserQuestion`). ✓
- Los 3 templates iguales → intactos. ✓

**Helpers** (`extract_version`, `compare_versions`) correctos. `sort -V` resuelve comparación semver; el case `lt` se mapea a 🚨.

---

## Detalle Test 3 — PRINCIPLES.md sync Paso 6.6

Casos cubiertos:

- **N (no existe)** → `🆕 PRINCIPLES.md — no existe en destino, copiando (v=0.1.0)` ✓
- **A (sin version)** → `⚠️ destino sin file_version (legacy). Sustituyendo (v_up=0.1.0)` ✓
- **B (igual)** → `✅ versiones iguales (0.1.0), no se toca` ✓
- **C (destino mayor)** → `🚨 destino 99.0.0 > upstream 0.1.0. Estado anómalo.` (preserva 99.0.0) ✓

Helper `extract_md_version` filtra correctamente. PRINCIPLES.md contiene texto que menciona la sintaxis `<!-- version: 0.Y.Z -->` literalmente, pero el regex `^\s*<!--\s*version:` requiere la línea empezar con `<!--`, así que solo coincide la línea de comentario real. Confirmed con `head -1`.

---

## Detalle Test 4 — Deprecation Paso 6.4.5

Inyección controlada en `project-status-template.yaml`:

```
# DEPRECATED v0.X.Y — motivo: campo legacy de prueba (smoke test Frente 7)
campo_obsoleto: "test"
```

Resultado del grep (línea 585 actualizar.md):

```
.../project-status-template.yaml:153:# DEPRECATED v0.X.Y — motivo: campo legacy de prueba (smoke test Frente 7)
```

✓ Detección funcional.

**Lectura crítica de la lógica posterior** (sub-paso 1 deprecations + sub-paso 2 huérfanos):

- Sub-paso 1: para cada DEPRECATED encontrado, agente lee datos vivos (`project-status.yaml` + sessions, etc.), evalúa uso real, y dispara `AskUserQuestion` con 3 opciones (mantener / migrar / eliminar). Coherente con ADR-019 (human-in-the-loop). NO automatiza decisión.
- Sub-paso 2: tabla de mapeo template ↔ datos vivos clara. Comparación de claves top-level se hace por agente (no script automatizado), lo cual es consistente con la filosofía pero exige criterio.

**Side-finding (no bloqueante):** comparando upstream vs dogfooting actual, `historico_sesiones` está en `project-status.yaml` (datos vivos) pero NO en `project-status-template.yaml` (upstream). Esto es un huérfano legítimo que el Paso 6.4.5 detectaría correctamente y elevaría a `AskUserQuestion`. NO es un bug — es exactamente el caso de uso que la sustitución diferencial preserva (campo añadido por agentes en su flujo natural, no descartar silenciosamente).

**Gap potencial menor:** la descripción del sub-paso 2 dice "Lee cada template ... y compara sus claves top-level con las del archivo operativo correspondiente" sin precisar cómo extraer claves top-level (grep simple funciona pero falla con keys nested al mismo nivel de indentación). En modo Extendido el agente tiene contexto para juzgar; no es necesario refactorizar.

---

## Detalle Test 5 — Hook anti-leak (ADR-025)

Repo real `***/WORKSPACE_Y/PROYECTOS/memsys3`:

```bash
$ git config core.hooksPath
.githooks
$ touch memsys3_templates/backlog/TEST-999-leak.md
$ git add memsys3_templates/backlog/TEST-999-leak.md
$ git commit -m "test smoke 2"
❌ ANTI-LEAK (ADR-025): items de backlog filtrados a memsys3_templates/backlog/:
    memsys3_templates/backlog/TEST-999-leak.md

Permitido en memsys3_templates/backlog/: solo README.md + docs/.gitkeep
Si el commit es intencional, usa --no-verify (queda anotable en sessions.yaml).
$ echo $?
1
```

✓ Hook bloquea commit. Cleanup verificado: `git reset HEAD ...` + `rm` deja working tree limpio respecto al estado pre-test (solo `agent7_prompt_frente7.txt` untracked, que ya estaba antes del Frente 7).

---

## Detalle Test 6 — commands.md (inspección estática)

Checklist:

| Item | Estado | Nota |
|------|--------|------|
| Launcher pattern (clone temporal + ejecutar prompt + cleanup) | ✓ | Coherente ADR-014. `/deploy-memsys3` clona a `memsys3_temp/`, `/actualizar-memsys3` clona a `memsys3_update_temp/`. Cleanup en Paso 3 de cada heredoc. |
| Sincronización con Frentes 1-6 | ⚠️ | Las descripciones internas de los comandos generados NO mencionan las features nuevas (sustitución diferencial templates, PRINCIPLES.md sync, deprecation contextualizada). Funcionalidad intacta porque solo carga el prompt completo. → **ISSUE-029** (prioridad baja). |
| Permisos de instalación en `~/.claude/commands/` | ✓ | Paso 1 hace `mkdir -p`. Troubleshooting cubre "permission denied" con instalación manual. |
| Sobreescritura sin pérdida de customización | ⚠️ leve | Pregunta "sobrescribir? sí/no", si "no" detiene. NO hace backup del comando previo. Riesgo bajo (los .md son thin launchers, ~30 líneas, customización rara). NO se abre ISSUE — se documenta aquí para visibilidad. |

---

## ISSUEs abiertos por este Frente

- **ISSUE-029** — `commands.md` descripción desactualizada respecto a Frentes 1-6. Prioridad baja. Decisión A/B (actualizar ahora vs diferir a Frente 8) en sesión próxima.

## Pendientes prioritarios cubiertos

- ✓ Pendiente prioritario 2 (project-status.yaml): smoke test actualizar.md con lógica nueva (Pasos 6.4 + 6.4.5 + 6.6).
- ✓ Pendiente prioritario 4: testear deployment con consulta `.gitignore` (Paso 8 inspección estática).
- ✓ Pendiente prioritario 6: testear `.gitignore` PASO 8 (mismo).

## Sub-tareas incluidas

- ✓ EXPLORATION-004 Opción A: paso 2.7 defensivo añadido a `endSession.md` (ambos sitios sincronizados, file_version intacta). Cierra el bucle anti-CDC operativo. Disposicional reminder explícito (PRINCIPLES.md #1 corolario meta-amnesia).

## Sub-tareas diferidas

- ISSUE-027 (migrar `principios_fundacionales` de memory.yaml → PRINCIPLES.md) → Frente 8 cleanup.

## Anclaje principios

- **#1 Anti-CDC**: smoke tests previenen CDC en agentes futuros que ejecutarán deploy/actualizar a ciegas.
- **#4 Human-in-the-loop**: validado en Paso 6.4 (caso 🚨) y Paso 6.4.5 (deprecation/huérfanos).
- **#7 file_version inmutable**: respetado durante edición de `endSession.md` (sigue en 0.1.0).
- **#8 Datos siempre preservados**: caso C del Paso 6.4 demuestra que destino > upstream NO se sobrescribe automáticamente.

## Estado BLUEPRINT-001

- Frentes 1-7 completados.
- Frente 8 (cierre release v1.0.0) pendiente: README final + CHANGELOG + web .org + tag v1.0.0 + cleanup multi-work + anuncio.
