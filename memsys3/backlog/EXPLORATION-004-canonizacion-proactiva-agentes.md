# EXPLORATION-004: Canonización proactiva — agentes con criterio anti-CDC

**Estado:** Propuesto
**Prioridad:** Media-Alta
**Tipo:** Exploration
**Plazo:** Medio plazo
**Fecha identificación:** 2026-05-07
**Sesión origen:** 2026-05-07 (post-Frente 2 BLUEPRINT-001)

---

## Problema / Necesidad

El principio fundacional **Anti-CDC** (`PRINCIPLES.md` #1) define que memsys3 existe para garantizar lucidez agéntica sostenida via archivos canónicos, no fluctuante según el azar del contexto de cada sesión.

**La paradoja que abre esta exploración:** la canonización misma (acto de mover un insight desde la conversación a un archivo canónico — `memory.yaml`, ADR, `PRINCIPLES.md`, `sessions.yaml`) **depende hoy del azar de la lucidez del agente**. Si el agente no detecta que una conversación produjo material canonizable, ese material muere al cerrar sesión.

Es CDC operando sobre el propio principio anti-CDC. Meta-ironía documentada en sesión 2026-05-07b (incidente real: agente bumpó `file_version` pese a tener la regla escrita en el archivo que estaba editando).

**Síntoma operativo:** durante una sesión emerge una decisión, heurística, principio o pieza de feedback útil. Si no se canoniza antes del `endSession`, se pierde — solo queda en el transcript, que NO es archivo canónico.

**Casos reales observados:**
- Sesión 2026-05-07a: heurística de orquestación de forks articulada en conversación. Habría muerto si el usuario no la hubiera pedido capturar explícitamente. Se canonizó en `memory.yaml` feedback.
- Sesión 2026-05-07a: principio CDC mismo articulado por el usuario en conversación. Habría muerto si no se hubiera anotado. Se canonizó en `memory.yaml`.
- Sesión 2026-05-07b: gotcha bumpeo `file_version` detectado y resuelto, pero requirió que el usuario lo viera. Si pasa desapercibido, se pierde la lección.

## Propuesta / Opciones

Diseñar un **criterio explícito de canonización** que el agente aplique:
1. **Activamente durante la sesión** — detectar candidatos a canonización mientras emergen.
2. **Defensivamente al cerrar** — `endSession.md` revisa la sesión y avisa al usuario: *"⚠️ Estos elementos surgieron en sesión y NO están canonizados. Si no los movemos a archivo canónico, se pierden."*

**Tipos de elementos canonizables a detectar:**

| Tipo | Destino canónico |
|---|---|
| Decisión arquitectónica | ADR (`memory/full/adr.yaml`) |
| Principio sistémico | `PRINCIPLES.md` (vía ADR) |
| Regla de comportamiento aprendida | `memory.yaml` feedback |
| Heurística operativa | `memory.yaml` feedback |
| Preferencia / perfil del usuario | `memory.yaml` usuario |
| Gotcha crítico recurrente | `sessions.yaml` gotchas + posible mención en `PRINCIPLES.md` si es estructural |
| Hito de progreso del proyecto | `sessions.yaml` highlights + `project-status.yaml` |
| Convención de naming / formato | `PRINCIPLES.md` o convención específica en docs |
| Pendiente concreto | `project-status.yaml` `pendientes_prioritarios` o backlog |
| Pattern arquitectónico nuevo | BLUEPRINT en backlog |

**Opciones de diseño** (a explorar):

### Opción A — Criterio en `endSession.md`
Añadir paso al final de `endSession.md`: *"Antes de cerrar, revisa el transcript de la sesión. ¿Hay elementos canonizables que NO están en archivos canónicos? Si sí, lista al usuario con AskUserQuestion: ¿canonizamos ahora o se aceptan perdidos?"*

- **Pro**: simple, una sola intervención.
- **Contra**: reactivo. Si el agente ya está saturado de tokens, su detección será pobre.

### Opción B — Criterio en `main-agent.yaml` (proactivo)
Añadir bloque `criterio_canonizacion` en main-agent.yaml: el agente aplica el criterio durante TODA la sesión, no solo al cierre. Cuando detecta un elemento canonizable, propone capturarlo inmediatamente con AskUserQuestion.

- **Pro**: anti-CDC fuerte. Captura caliente, en el momento de la lucidez.
- **Contra**: ruido conversacional alto si el criterio detecta falsos positivos. Necesita afinación.

### Opción C — Híbrida (proactivo + defensivo)
Combina A y B. Captura caliente durante la sesión + revisión final en `endSession`.

- **Pro**: defensa multi-capa (como las firmas commits — defensa 4 capas funcionó).
- **Contra**: más complejo, más reglas que mantener.

### Opción D — Subagente "canonizador"
Al cerrar, lanzar un fork (`Agent` tool tipo Explore) que lea el transcript de la sesión y extraiga candidatos. Devuelve lista al agente principal.

- **Pro**: descarga del agente principal. Token-efficient.
- **Contra**: Claude Code no expone API directa al transcript propio (limitación técnica a verificar).

## Riesgos conocidos

- **Falsos positivos**: si el criterio es demasiado amplio, cada sesión genera una lista interminable de "candidatos" que satura al usuario y se ignora. Inversión del problema.
- **Falsos negativos**: si el criterio es demasiado estrecho, sigue habiendo CDC porque pierde elementos sutiles (matices conversacionales).
- **Coste cognitivo**: cada AskUserQuestion mid-session interrumpe el flujo. Hay que medir si compensa.
- **Auto-referencia**: el criterio mismo es canonizable. Cuando se establezca, va en `PRINCIPLES.md` o como ADR.

## Refinamiento 2026-05-08: el problema NO es solo detectar

Observación articulada por el usuario al revisar Frente 5 BLUEPRINT-001:

> *"El problema no es que no lo detecte, el problema es que los agentes no tienden a canonizar — es como que olvidáis que olvidáis."*

Esto refina sustancialmente la EXPLORATION:

**Diagnóstico revisado.** Los agentes LLM tienen **metacognición ausente** sobre la efimeridad de su propio contexto. No solo olvidan al cambiar de turno — **NO SABEN que están olvidando**. La conversación se "siente" continua aunque no lo sea. Por eso el comportamiento por defecto NO es canonizar — es proseguir, como si el insight ya estuviera guardado por el simple hecho de haberse pronunciado.

**Implicación para el diseño.** Una regla tipo *"detecta candidatos canonizables"* (Opciones A/B/C originales) **falla en aislamiento** porque presupone una metacognición que el agente no tiene. Detectar requiere sentir la efimeridad — y la disposición por defecto es la opuesta (sentir continuidad).

**Enfoque correcto.** Reformular el **DEFAULT mental**, no añadir una tarea. Una invariante en `main-agent.yaml` del tipo:

> *"Tu estado por defecto es el olvido. Cualquier cosa articulada en esta conversación que no esté en un archivo canónico se está perdiendo en este momento. La continuidad sentida es ilusión del turno actual."*

Esto opera al nivel **disposicional**, no instrumental. No le pides al agente que detecte — le cambias el modelo mental sobre el tiempo de la sesión.

**Nueva opción E (refinamiento de C):**

### Opción E — Disposicional + Defensiva (refinamiento 2026-05-08)

1. **Disposicional**: invariante en `main-agent.yaml` que reformula el default mental sobre la efimeridad del contexto. NO una tarea, una invariante.
2. **Defensiva**: paso en `endSession.md` que revisa explícitamente la sesión buscando candidatos canonizables (red de seguridad).

Esta combinación **ataca causa + síntoma**:
- Disposicional resuelve el "no saber que olvidan".
- Defensiva captura lo que aun así se escape.

Probablemente la opción a prototipar primero. Bajo coste, bajo riesgo, alto retorno potencial.

**Anclaje.** Este refinamiento se canoniza también en `memsys3/memory/memory.yaml` como `principios_fundacionales[id=olvidan-que-olvidan]`, complementando el principio CDC (id=cdc): la CDC es síntoma, la meta-amnesia es la causa agéntica subyacente.

---

## Decisiones / Acciones

Pendiente de exploración. Próximos pasos sugeridos:

1. **Investigar precedentes**: ¿cómo resuelven esto otros sistemas (Engram, gentle-ai)? Comparativa.
2. **Definir criterio inicial mínimo**: lista corta de detectores (ej: usuario dice "principio de X", "regla nueva", "deberíamos siempre Y"). Explorar como heurística inicial.
3. **Prototipar Opción A** (defensiva en endSession) primero — bajo coste, fácil de revertir si no funciona.
4. **Si Opción A funciona**, considerar Opción C (híbrida) como evolución.
5. **Documentar como FEATURE/ADR** una vez la exploración converja.

## Referencias

- **Principio motivador:** `memsys3/PRINCIPLES.md` #1 (Anti-CDC)
- **ADR origen:** ADR-020 (memory.yaml — primer paso de canonización estructurada)
- **Sesión articulación CDC:** 2026-05-07a (sessions.yaml)
- **Incidente meta-CDC:** 2026-05-07b (bumpeo file_version pese a regla escrita)
- **Items relacionados:**
  - FEATURE-010 (checkpoint mid-session) — complementario, captura periódica vs reactiva
  - FEATURE-011 (Main Agent proactivo) — solapamiento parcial: ambos buscan agente que sugiere proactivamente
  - EXPLORATION-001 (consulta historial bajo demanda) — complementario, lectura vs escritura canónica
- **Informe extendido (ADR-021 lo recomienda para EXPLORATIONs):** PENDIENTE. Cuando la exploración avance, crear `docs/informe_EXPLORATION-004.md` con investigación, alternativas profundas, prototipo.

<!-- version: 0.1.0 -->
