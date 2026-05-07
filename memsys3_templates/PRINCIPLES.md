# Principios memsys3

> **Documento canónico.** Fuente única de verdad para los principios sistémicos de memsys3.
> Cualquier comportamiento del sistema debe poder justificarse desde uno de estos principios.
> Si una decisión los contradice, o cambian los principios, o cambia la decisión.

Este archivo se distribuye con el sistema. Cuando un agente carga `newSession.md`, también debe leer este documento para conocer las invariantes que rigen memsys3.

---

## 1. Anti-CDC (Casualidad de Contexto)

**Definición.** CDC es la lucidez agéntica generada por la eventualidad del contexto de la sesión actual, y no por archivos canónicos. Es decir: que el agente "acierte" porque ha leído algo justo antes en esta sesión, no porque el sistema lo haya garantizado.

**Rol de memsys3.** memsys3 ES una solución a la CDC. Su propósito es propiciar lucidez agéntica **sostenida** en el tiempo, garantizada por archivos canónicos (`context.yaml`, `memory.yaml`, `project-status.yaml`, `adr.yaml`), no fluctuante según el azar del contexto de cada sesión.

**Test mental anti-CDC.** Para cada decisión de diseño: *"¿esto requiere que un agente fresco adivine, o le doy archivo canónico?"* Si una conducta deseable solo emerge cuando el agente "ha leído X justo antes", entonces X debe estar en un archivo canónico que se lea siempre (newSession, compile-context). Si solo emerge en una sesión específica, es CDC y hay que eliminarla.

**ADRs relacionados:** ADR-008 (compile-context en sesión limpia), ADR-020 (memory.yaml), ADR-021 (backlog docs anti-CDC).

---

## 2. Agnosticismo de modelo de IA

**Definición.** memsys3 funciona con cualquier modelo de IA capaz de leer prompts en Markdown e interpretar YAML (Claude, Gemini, Codex, etc.). Nada del núcleo distribuible debe depender de un modelo concreto.

**Jerarquía fuente de verdad.**
- `memsys3_templates/` (AGNÓSTICO, distribuible) →
- `memsys3/prompts/` (ESPECÍFICO del proyecto desplegado) →
- `.claude/commands/` u otros (LOCAL, opt-in por modelo, opcional).

Las features específicas de un modelo (ej. comandos `/deploy-memsys3` de Claude Code) son **workarounds opt-in**, nunca core. La documentación debe dejarlo explícito.

**ADRs relacionados:** ADR-016 (agnosticismo + commands opcionales).

---

## 3. Una sola carpeta

**Definición.** El sistema completo cabe en `memsys3/` dentro del proyecto del usuario. Sin base de datos, sin servidor, sin dependencias externas obligatorias. Copiar la carpeta y funciona.

**Excepción.** Bridges opcionales (ej. `MEMORY.md` raíz para auto-memory de Claude Code, ADR-020) se permiten **fuera** de `memsys3/` solo si:
- son opt-in,
- son punteros a algo dentro de `memsys3/`,
- el sistema funciona igual sin ellos (graceful degradation).

**Por qué importa.** Portabilidad. Versionable con git como el resto del código. Sin instalación. Sin permisos. Onboarding de un proyecto nuevo es un `cp -r` (o un deploy.md).

---

## 4. Human-in-the-loop

**Definición.** El usuario decide cuándo iniciar sesión, cuándo cerrarla, cuándo compilar contexto, cuándo actualizar memsys3, cuándo crear ADRs, cuándo documentar. El sistema **NUNCA** ejecuta estas acciones por su cuenta.

**Implicaciones.**
- Los prompts (`newSession.md`, `endSession.md`, `compile-context.md`, `actualizar.md`) son ejecutados explícitamente por el usuario.
- Los agents proponen, sugieren o avisan; nunca actúan unilateralmente sobre operaciones destructivas o de sincronización.
- Acciones con confirmación obligatoria: bumps de versión, eliminaciones, sustituciones de schema, commits/tags/push.

**Por qué importa.** El usuario mantiene el control y la responsabilidad sobre la memoria del proyecto. Evita que un agente "ayudante" corrompa o sobrescriba estado canónico sin auditoría humana.

---

## 5. Criterio inteligente vs límites arbitrarios

**Definición.** El Context Agent decide qué entra en `context.yaml` con criterio panorámico ("¿qué debe saber CUALQUIER agent descontextualizado para trabajar aquí?"), no con cuotas rígidas por sección.

**Único límite duro.** 2000 líneas en `context.yaml` (límite del Read tool en Claude). Todo lo demás es criterio.

**Anti-pattern descartado.** "Máximo 7 ADRs", "150 caracteres por gotcha", etc. Se probaron en sistemas anteriores y eran frágiles: proyectos pequeños perdían contexto, grandes no podían expresarse.

**ADRs relacionados:** ADR-001 (criterio inteligente).

---

## 6. Templates como documentación activa permanente

**Definición.** Los archivos en `memsys3/memory/templates/` (`adr-template.yaml`, `sessions-template.yaml`, `memory-template.yaml`, etc.) son **referencia viva** que el Main Agent consulta durante endSession para documentar bien. NO se borran después del deployment.

**Implicaciones.**
- Los templates son agnósticos: ningún proyecto debe modificarlos. Son contrato.
- Bumpear su `file_version` solo lo hace `/actualizar-memsys3`, vía sustitución diferencial (ADR-018).
- Los gotchas se documentan en `sessions.yaml` (contextualizados temporalmente), NO en `project-status.yaml`.

**ADRs relacionados:** ADR-009 (templates permanentes), ADR-018 (sustitución diferencial), ADR-019 (deprecation contextualizada).

---

## 7. file_version inmutable salvo `/actualizar-memsys3`

**Definición.** Cada archivo de infraestructura (prompts, agents, templates, principios) lleva una versión independiente (`<!-- version: 0.Y.Z -->` en `.md`, `file_version: "X.Y.Z"` en `.yaml` agents, `# version: X.Y.Z` en templates). Bumpear esa versión es **operación exclusiva** de `/actualizar-memsys3`.

**Regla dura.** Aunque un agente añada contenido a un archivo de infraestructura, **NO debe tocar su `file_version`**. El reflejo automático "modifico → bumpo" es incorrecto y rompe el sistema de versionado independiente. Esto está formalizado como restricción dura en `agents/main-agent.yaml`.

**Excepción documentada.** En el repo dogfooting de memsys3 mismo, la restricción se levanta para evitar deadlock (el desarrollador del sistema necesita poder editar la infraestructura).

**ADRs relacionados:** ADR-017 (file_version), ADR-018 (sustitución diferencial).

---

## 8. Datos siempre preservados

**Definición.** memsys3 nunca borra datos del usuario (sesiones, ADRs, decisiones, history). Cuando el volumen supera límites operativos, **mueve** en lugar de borrar.

**Mecanismos.**
- **Rotación automática** (>1800–2000 líneas): `sessions.yaml` → `sessions_N.yaml`, `adr.yaml` → `adr_N.yaml`. Histórico íntegro.
- **Plan de Contingencia** (>150K tokens al compilar): el Context Agent archiva ADRs/sesiones irrelevantes a `memsys3/memory/history/` (que NO se lee). Reduce a ~120K. Datos recuperables.
- **Backups en `actualizar.md`**: snapshot de `memsys3/` antes de tocar nada. Borrado solo tras validación.

**Por qué importa.** Pérdida histórica = pérdida del razonamiento detrás del proyecto. Lo importante puede no parecerlo en el momento de comprimir.

**ADRs relacionados:** ADR-002 (rotación), ADR-003 (Plan de Contingencia).

---

## 9. Separation of Concerns

**Definición.** Cada archivo del sistema cubre una preocupación distinta. No hay duplicaciones. Cuando dos archivos podrían contener lo mismo, uno se convierte en lectura directa y el otro en compilación.

**Mapa.**
- `README.md` (raíz proyecto) → identidad **actual** del proyecto. Lectura directa en newSession (ADR-012).
- `memsys3/memory/project-status.yaml` → estado operativo: fase, features, pendientes.
- `memsys3/memory/context.yaml` → memoria histórica **compilada** (ADRs, sessions sintetizados, gotchas). Generado por Context Agent.
- `memsys3/memory/full/sessions.yaml` → bitácora detallada (input del CA).
- `memsys3/memory/full/adr.yaml` → ADRs completas (input del CA).
- `memsys3/memory/memory.yaml` → perfil del usuario + feedback aprendido (ADR-020).
- `memsys3/PRINCIPLES.md` → invariantes del sistema (este documento).

**Por qué importa.** Imposible desincronización. Cada archivo es responsable de una sola cosa, lo que también limita su crecimiento natural.

**ADRs relacionados:** ADR-007 (meta-niveles READMEs), ADR-012 (README lectura directa), ADR-020 (memory.yaml).

---

## 10. Restricciones de infraestructura en agents

**Definición.** El Main Agent y el Context Agent tienen prohibido modificar archivos de infraestructura (`prompts/`, `agents/`, `memory/templates/`) en proyectos desplegados. Pueden leer, no escribir.

**Quién sí puede modificar infraestructura.**
- `/actualizar-memsys3` (operación explícita del usuario).
- En el repo dogfooting de memsys3 (excepción documentada — sin esta excepción, el desarrollador del sistema no podría iterar).

**Datos vs infraestructura.**
- **Datos** (escribibles por agents): `memory/full/sessions.yaml`, `memory/full/adr.yaml`, `memory/project-status.yaml`, `memory/memory.yaml`, `memory/context.yaml`, `backlog/`.
- **Infraestructura** (read-only para agents): `prompts/`, `agents/`, `memory/templates/`, `PRINCIPLES.md`.

**Por qué importa.** La infraestructura define cómo opera memsys3. Si los agents la modifican silenciosamente, el sistema deriva impredeciblemente y se rompe la promesa anti-CDC.

**ADRs relacionados:** ADR-017 (file_version + restricciones), ADR-018 (sustitución diferencial vía actualizar.md).

---

## Cómo evolucionan estos principios

Estos principios son la spina dorsal del sistema, pero no son inmutables. Cuando un patrón nuevo emerge y desafía un principio:

1. Se discute con el usuario.
2. Si se acepta, se crea/actualiza una ADR que justifique el cambio.
3. Se actualiza este `PRINCIPLES.md`.
4. Se bumpa `file_version` (vía `/actualizar-memsys3`).

No hay cambios silenciosos. La trazabilidad histórica vive en `memory/full/adr.yaml`.

<!-- version: 0.1.0 -->
