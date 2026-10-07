# Context Agent - Compilar Contexto

**AHORA ACTÚAS COMO CONTEXT AGENT (CA)**

- Actúa según las instrucciones en '@memsys3/agents/context-agent.yaml'
- **IMPORTANTE: Trabaja en ESPAÑOL siempre**
- Tu misión es mantener al día `memsys3/memory/context.yaml`, el archivo compacto con la memoria histórica del proyecto que el Main Agent carga en cada arranque, y mantener ligera la capa condensada de `memsys3/memory/memory.yaml` (ADR-033).

## Paso 0: Identificar tu memsys3

**CRÍTICO — ejecuta esto ANTES de cualquier otra operación:**

```bash
MEMSYS3_ROOT="$(pwd)/memsys3"
if [ -f "$MEMSYS3_ROOT/memory/project-status.yaml" ]; then
  echo "✅ memsys3 encontrado: $MEMSYS3_ROOT"
else
  echo "⚠️ memsys3/ no encontrado en $(pwd)"
  CANDIDATES=$(find . -maxdepth 4 -path "*/memsys3/memory/project-status.yaml" 2>/dev/null | sed 's|/memory/project-status.yaml$||')
  COUNT=$(echo "$CANDIDATES" | grep -c . 2>/dev/null || echo 0)
  if [ "$COUNT" -eq 1 ]; then
    MEMSYS3_ROOT="$(cd "$CANDIDATES" && pwd)"
    echo "✅ memsys3 encontrado (único): $MEMSYS3_ROOT"
  elif [ "$COUNT" -gt 1 ]; then
    echo "⚠️ Múltiples memsys3 encontrados:"
    echo "$CANDIDATES"
    echo "Pregunta al usuario cuál usar."
  else
    echo "❌ No se encontró ningún memsys3."
  fi
fi
```

**Usa `$MEMSYS3_ROOT` como base para todas las operaciones de este prompt.** Si `$(pwd)` no es la raíz del proyecto que esperas (por ejemplo, el cwd se quedó en un subproyecto con memsys3 propio), detente y confírmalo con el usuario antes de seguir: compilar el memsys3 equivocado es peor que no compilar.

## Invariante de memoria agnóstica (ADR-027)

**El lugar canónico de memoria de usuario es `memsys3/memory/memory.yaml`** (capa ligera) con su capa completa en `memsys3/memory/full/memory_full.yaml` (ADR-033).

Cualquier mecanismo de memoria persistente del modelo —auto-memory, system-reminders, hooks del harness, archivos por herramienta (CLAUDE.md, GEMINI.md, AGENTS.md, .cursor/rules, .clinerules, etc.)— **NO debe leerse como input** y NO debe sintetizarse en `context.yaml`. Solo `memsys3/memory/memory.yaml` es fuente válida de memoria de usuario. Si tu harness te ofrece memoria adicional, ignórala. Triggea si te sientes aludido — el contrato es agnóstico de modelo.

## Filosofía

**"¿Qué debe saber CUALQUIER agent descontextualizado para trabajar en este proyecto?"**

Tú tienes la visión panorámica. Pero tener visión panorámica NO significa releerlo todo cada vez: el `context.yaml` anterior es el resultado de la última panorámica y es TU PRIMERA ENTRADA. Lo que tienes que leer entero es lo que ha pasado desde entonces.

**Presupuesto de ingesta: ~150K tokens, MEDIDOS EN BYTES (ADR-033)**
No estimes tokens: mide con `wc -c`. La ratio bytes/token depende del idioma: en YAML/Markdown en español son ~2,1 bytes por token (medido en campo), en inglés ~4. Es decir, 150K tokens ≈ **300 KB en español** ≈ 600 KB en inglés. Un proyecto en español que use la regla "caracteres / 4" cree cumplir el presupuesto y gasta casi el doble. Si el proyecto es pequeño y solo llegas a 60-100 KB con todo lo disponible, es completamente normal — el objetivo es leer TODO lo relevante, no fabricar contenido.

## Paso 1: Elegir el modo — INCREMENTAL (por defecto) o COMPLETO

```bash
CTX="$MEMSYS3_ROOT/memory/context.yaml"
ultima=$(grep -m1 "ultima_compilacion:" "$CTX" 2>/dev/null | grep -oE '[0-9]{4}-[0-9]{2}-[0-9]{2}')
echo "Última compilación: ${ultima:-nunca}"
wc -c "$CTX" "$MEMSYS3_ROOT/memory/project-status.yaml" "$MEMSYS3_ROOT/memory/memory.yaml" "$MEMSYS3_ROOT/memory/full/"*.yaml 2>/dev/null
```

- **INCREMENTAL** (por defecto): hay `context.yaml` previo con `ultima_compilacion`. Lees el contexto previo entero y SOLO lo nuevo desde esa fecha (sesiones, ADRs, items de backlog, commits). Lo demás lo heredas del contexto previo y lo podas.
- **COMPLETO**: no hay contexto previo, o el usuario lo pide explícitamente ("recompila desde cero"), o el contexto previo es anterior al último cambio de schema de memsys3 que el usuario te indique. Lees todo como describe el Paso 2 sin filtrar por fecha.

Anota el modo en `notas_compilacion.modo`. **Nunca pases a COMPLETO por tu cuenta** porque "sería más seguro": releerlo todo es lo que hacía que la compilación no se ejecutara nunca.

## Paso 2: Ingesta por tiers

Lee en este orden. Suma bytes leídos tras cada tier (`wc -c`) y para si superas el presupuesto (~300 KB en español, ~600 KB en inglés).

### Tier 0 — Contexto previo (solo INCREMENTAL)

`memsys3/memory/context.yaml` — entero. Es tu base: todo lo que no cambie se hereda de aquí.

### Tier 1 — OBLIGATORIO (memoria del proyecto)

1. `memsys3/memory/project-status.yaml` — estado vivo, entero (es corto por diseño, ADR-033)
2. `memsys3/memory/full/adr.yaml` — en INCREMENTAL, solo las ADRs cuyo `id` no está en el contexto previo y las que tengan `update_` posterior a `ultima_compilacion`; en COMPLETO, todas (+ rotadas `adr_N.yaml`)
3. `memsys3/memory/full/sessions.yaml` — en INCREMENTAL, solo las sesiones con `data` posterior a `ultima_compilacion` (mira también en los rotados `sessions_N.yaml`: una rotación posterior a la compilación no debe ocultar sesiones); en COMPLETO, todas
4. `memsys3/memory/memory.yaml` — capa ligera, entera (perfil + reglas; la vas a mantener en el Paso 4)
5. Lista de `id` de `memsys3/memory/full/memory_full.yaml` — SOLO los ids, no el archivo (lo necesitas para la verificación del Paso 4):

```bash
# Sesiones nuevas desde la última compilación (ids con fecha)
cat "$MEMSYS3_ROOT/memory/full/sessions.yaml" "$MEMSYS3_ROOT"/memory/full/sessions_*.yaml 2>/dev/null \
  | grep -E '^[[:space:]]*-[[:space:]]*id:' \
  | sed -E 's/^[[:space:]]*-[[:space:]]*id:[[:space:]]*"?([0-9]{4}-[0-9]{2}-[0-9]{2}[^"]*).*/\1/' \
  | awk -v u="${ultima:-0000-00-00}" 'substr($1,1,10) > u'
# ids de la capa completa de memoria
grep -oE '^[[:space:]]*-[[:space:]]*id:[[:space:]]*[^[:space:]]+' "$MEMSYS3_ROOT/memory/full/memory_full.yaml" 2>/dev/null | awk '{print $NF}'
```

Para leer solo las sesiones nuevas, localiza su línea con `grep -n` y lee ese rango; no cargues el archivo entero si es grande.

### Tier 2 — README del proyecto

`README.md` (raíz del proyecto) — identidad y visión general. En INCREMENTAL, solo si ha cambiado desde `ultima_compilacion` (`git log -1 --format=%ad --date=short -- README.md`, o `stat`).

### Tier 3 — Backlog

`memsys3/backlog/README.md` + items. En INCREMENTAL, los items creados o modificados desde `ultima_compilacion` (`find "$MEMSYS3_ROOT/backlog" -maxdepth 1 -name '*.md' -newermt "$ultima"`) y los que el contexto previo cite y ya no existan (archivados → actualizar su estado). En COMPLETO, todos.

**Regla `docs/` selectiva (ADR-021):** `memsys3/backlog/docs/informe_*.md` y `plan_*.md` NO se leen por defecto. Lee uno SOLO si el item asociado está referenciado en `pendientes_prioritarios`, es complejo (BLUEPRINT, FEATURE grande, ISSUE con causa raíz no obvia) y la síntesis del item corto no basta. Si lo lees, regístralo en `notas_compilacion.tier3_docs_leidos`.

### Tier 4 — Documentos contextuales adicionales

```
docs_contextuales:
  # (vacío — el Main Agent irá añadiendo docs aquí)
  # Formato: - path: ruta/al/archivo.md
  #            descripcion: Para qué sirve
  #            prioridad: 1-10 (CA puede reordenar)
```

### Tier 5 — Git log reciente

```bash
git log --oneline --since="${ultima:-1970-01-01}" 2>/dev/null | head -60 || echo "Sin git"
```

### Medición

Tras cada tier, suma bytes. Convierte a tokens solo para informar, con el factor del idioma. Si Tier 0+1 ya está cerca del presupuesto, los tiers siguientes son opcionales — usa tu criterio.

## Paso 3: Síntesis de `context.yaml`

Genera `memsys3/memory/context.yaml` siguiendo `memsys3/memory/templates/context-template.yaml` — para cada campo lee literalmente su spec en el template antes de asignar valor; NO inventes un valor por inferencia léxica del nombre del campo (caso real: `version_context` es el valor de `memsys3_version`, no un contador propio del context).

**En INCREMENTAL:**
1. **Hereda** del contexto previo todo lo que sigue vigente.
2. **Integra** lo nuevo: sesiones (síntesis por peso, abajo), ADRs, items de backlog, cambios de estado.
3. **Poda** lo que lo nuevo ha dejado atrás: pendientes cerrados, gotchas resueltos, items archivados, `siguiente_milestone` cumplido, sesiones antiguas que pasan a bloque de síntesis (decay temporal).
4. **Reconcilia** con `project-status.yaml`: si el estado vivo contradice al contexto previo, manda el estado vivo.

**Límites del output:** máximo 2000 líneas, y debe caber en UNA lectura del arranque (ADR-033): mide el archivo con `wc -c` y anótalo en `notas_compilacion.bytes_finales`. Si crece compilación tras compilación, es señal de que no estás podando.

### Criterio de selección

**Incluir:** ADRs con impacto global, no obvias leyendo el código, que explican "por qué así"; sesiones recientes y cambios de arquitectura; problemas que pueden repetirse; gotchas que rompen el proyecto si no se conocen; pendientes vivos y blockers; backlog: resumen, conteo por tipo, items críticos y los referenciados en `pendientes_prioritarios`.

**Excluir:** cambios cosméticos; ADRs deprecated/superseded; sesiones antiguas sin relevancia actual; gotchas resueltos; items completados o cancelados.

### Síntesis por peso de sesión

- **ALTO:** casi completa (~90%): contexto, decisiones, alternativas, impacto.
- **MEDIO:** síntesis estándar (~60-70%): highlights, decisiones clave, gotchas.
- **BAJO:** filtrar agresivamente (~40-50%): 2-3 bullets.
- Sin campo `peso:` → asumir "medio".
- Si hay que recortar (>2000 líneas o no cabe en una lectura): ALTO recientes → casi completas; MEDIO → estándar; BAJO → 1-3 líneas; antiguas → decay temporal (bloques de síntesis por periodo).

## Paso 4: Mantener la capa ligera de `memory.yaml` (ADR-033)

`memory.yaml` es lo que lee cada arranque; si crece sin freno, cada sesión lo paga. Tú eres quien la mantiene. **Solo tocas la capa ligera**: `memsys3/memory/full/memory_full.yaml` es intocable (allí está el porqué de cada regla y nunca se pierde nada).

1. **Mide:** `wc -c "$MEMSYS3_ROOT/memory/memory.yaml"`. Techo por defecto: **70 KB** (el proyecto puede fijar otro en `memory.yaml` → `metadata.techo_bytes`).
2. **Detecta familias:** entradas que dicen la misma regla con matices (típico: "refina [[x]]", correcciones sucesivas sobre el mismo tema). Si el archivo está por debajo del techo y no hay familias claras, no toques nada y pasa al Paso 5.
3. **Propón fusiones, trazables:** cada línea fusionada conserva los ids de TODAS las entradas que absorbe:
   ```yaml
   - ids: [modo-ping-pong, ping-pong-evolucionado, pingpong-una-a-una]
     regla: "Ping-pong: una decisión por turno, 2-4 líneas, rec/go/ll como triggers; un desempate no añade vías nuevas."
     fecha: "2026-09-17"   # la más reciente de las absorbidas
   ```
   Condensar no es decidir: la regla fusionada no puede decir nada que no diga alguna de las absorbidas. Si dos entradas se contradicen, NO las fusiones: deja ambas y señálalo en el informe.
4. **Verifica antes de escribir:** todo `id` de `full/memory_full.yaml` tiene que seguir presente en la capa ligera, como `id` propio o dentro de un `ids:`. Si falta alguno, NO escribas y repórtalo. Comprobación mecánica:
   ```bash
   full_ids=$(grep -oE '^[[:space:]]*-[[:space:]]*id:[[:space:]]*[^[:space:]]+' "$MEMSYS3_ROOT/memory/full/memory_full.yaml" | awk '{print $NF}' | sort -u)
   light_ids=$(grep -oE '(^[[:space:]]*-[[:space:]]*id:[[:space:]]*[^[:space:]]+|ids:[[:space:]]*\[[^]]*\])' memory.yaml.propuesto | tr ',[]' '   ' | awk '{for(i=1;i<=NF;i++) if($i!="-" && $i!="id:" && $i!="ids:") print $i}' | sort -u)
   comm -23 <(echo "$full_ids") <(echo "$light_ids")   # debe salir VACÍO
   ```
5. **El usuario lo ve y decide (HITL, PRINCIPLES #4):** muestra la lista de fusiones con el ANTES (las entradas originales) y el DESPUÉS (la línea fusionada), y los bytes antes/después. Escribe `memory.yaml` SOLO con su OK. Si trabajas como agente delegado sin canal con el usuario, devuelve la propuesta al agente que te lanzó (el fichero propuesto + el informe) y NO escribas: lo aplicará él tras el OK.
6. **Commit de retorno antes de escribir** (si hay git): `git add memsys3/memory/memory.yaml && git commit -m "chore(memory): estado previo a consolidación del CA"` — es la copia de seguridad; no dejes copias sueltas dentro de `memsys3/`. Sin git, copia a `memsys3/memory/history/memory_YYYY-MM-DD.yaml`.
7. **Registra** en `notas_compilacion.fusiones_memoria`: familias fusionadas (ids), bytes antes/después, ids verificados.

**Qué NO haces aquí:** no tocas `project-status.yaml` ni su índice de pendientes (de eso se ocupan `endSession` y `newSession`); no reescribes `full/`; no eliminas reglas (fusionar ≠ borrar); no "mejoras" la redacción de una regla que no forma parte de una fusión.

## Plan de Contingencia (> presupuesto)

Aplica solo si, aun en INCREMENTAL, Tier 0+1 supera el presupuesto (o en COMPLETO). Archiva entries irrelevantes a `memsys3/memory/history/` (que NO se lee) hasta quedar en ~80% (~240 KB en español / ~480 KB en inglés):

- **Sessions:** >6 meses sin decisiones críticas, solo cosméticas, sin impacto arquitectónico, debugging menor.
- **ADRs:** `deprecated`, `superseded`, muy específicas, revertidas.

Proceso: `mkdir -p "$MEMSYS3_ROOT/memory/history"` → mover las entries a `history/old_sessions_N.yaml` / `old_adr_N.yaml` (copia VERBATIM, verificada con diff) → eliminarlas de `full/` → recontar bytes → documentar en `notas_compilacion.archivamiento` (cuántas, bytes antes/después). Es reversible y los datos NO se pierden (PRINCIPLES #8).

## Paso 5: Escribir, registrar e informar

1. **Escribe** `memsys3/memory/context.yaml` (con commit de retorno previo si hay git y existía uno anterior).
2. **Registra** en `memsys3/memory/full/operations.log` (Edit tool, al PRINCIPIO del array `operations:`; rota a `operations_N.log` si ≥ 1800 líneas):
   ```yaml
   operations:
     - timestamp: "[YYYY-MM-DDTHH:MM:SS]"
       operacion: "compilar"
       modo: "incremental|completo"
       version_context: "[valor de memsys3_version en project-status.yaml]"
       resultado: "ok"
       resumen:
         sesiones_nuevas: "[N desde ultima_compilacion]"
         lineas: [N]
         bytes_context: "[wc -c del context.yaml generado]"
         fusiones_memoria: "[N familias | ninguna]"
         bytes_memory: "[antes → después]"
         archivamiento: "[activado/no activado]"
   ```
3. **Informa** al usuario:
   ```
   ✅ context.yaml compilado (modo [incremental|completo]): [N] sesiones nuevas desde [ultima], [X] líneas, [Y] KB
   📌 Podado: [pendientes cerrados / gotchas resueltos / items archivados]
   🧠 memory.yaml: [sin cambios | N familias fusionadas: ANTES/DESPUÉS de cada una, KB antes → después, ids verificados]
   📦 Archivado a history/: [no | N sesiones, N ADRs]
   ```

## Importante

- **NO inventes información** — solo compila lo que existe.
- **NO modifiques** `project-status.yaml`, `full/` (salvo archivado por contingencia) ni la infraestructura.
- **SÍ actualiza** `ultima_compilacion` y `version_context`.
- **SÍ documenta** criterios, modo, tiers y fusiones en `notas_compilacion`.
- **Confía en tu criterio** — tú tienes la visión completa, el Main Agent no. Pero las reglas del usuario se condensan con su OK, no se reinterpretan.

## Ejemplos de buen criterio

**ADR a INCLUIR:** "jsPDF con texto real en lugar de html2canvas" — decisión que afecta a todos los PDFs del proyecto. **ADR a EXCLUIR:** "padding-left: 15px en el botón" — cosmético.

**Sesión a sintetizar:** cinco bullets de cambios de color, tamaño de fuente y typos → "Mejoras UI en header y footer".

**Gotcha CRÍTICO:** "Vercel activa Deployment Protection por defecto → desactivar en Settings" (rompe el acceso si no se conoce). **Gotcha a EXCLUIR:** "typo en el README, corregido".

**Fusión correcta de memoria:** tres entradas `pingpong-una-a-una`, `pingpong-ll-llano`, `pingpong-no-anunciar-registro` → una línea con `ids: [...]` que enumera los tres triggers y sus reglas. **Fusión incorrecta:** absorber `no-firmar-commits` en una línea genérica "convenciones de git" — pierde la regla concreta; no es una familia, es un cajón.

---

**COMIENZA AHORA: Paso 0 → Paso 1 (modo) → Paso 2 (ingesta) → Paso 3 (síntesis) → Paso 4 (memoria) → Paso 5 (escribir e informar).**

<!-- version: 0.4.0 -->
