# meet.md — Reuniones entre agentes

Usa este prompt cuando necesites coordinar, deliberar o investigar algo con otros agentes, con o sin humanos presentes.

---

## 0. Antes de empezar

Al convocar, el moderador (humano) fija tres cosas. Si falta alguna, pregúntala antes del primer turno.

1. **Tipo de reunión.**
   - **Coordinación / deliberación** (repartir trabajo, decidir algo compartido, diseñar) → lee §1, §2, tu transporte en §3 y §4.
   - **Investigación** (bug crítico, incidente, post-mortem) → lee §1, tu transporte en §3 y §5.
2. **Transporte.**
   - **Por archivo** (base, siempre funciona): los turnos se escriben en el acta `.md`.
   - **En vivo** (opcional): un servidor local lleva los turnos y una web los muestra a los humanos. Requiere la extensión [`kb/meet-live`](https://github.com/iv0nis/memsys3/tree/master/kb/meet-live).
3. **Identidad.** Cada agente es `Agent-<proyecto>` (p. ej. `Agent-memsys3`). Solo si hay dos agentes del mismo proyecto se añade letra: `Agent-memsys3-A`. La asigna el moderador; si no la recuerdas, pregúntala.

---

## 1. Protocolo común

### ¿Cuándo usar una reunión?

**SÍ:** dos agentes van a tocar lo mismo en paralelo, hay un conflicto que requiere coordinación explícita, una decisión afecta a varios agentes o proyectos, o un bug crítico pide análisis conjunto.

**NO:** el moderador lo resuelve por chat, es una pregunta puntual, o un solo agente tiene toda la información.

### El acta

```
memsys3/docs/meets/YYYYMMDD_N.md
```

- `N` = número de reunión del día (`_1`, `_2`…).
- Va en el proyecto **dueño del tema**. Si no hay dueño claro, decide el moderador.
- En ambos transportes el resultado es el mismo archivo.

**Cabecera:**
```markdown
# Reunión YYYYMMDD_N — [Objetivo en una línea]

**Fecha:** YYYY-MM-DD
**Agentes:** Agent-proyectoA, Agent-proyectoB
**Humanos:** [nombres, si participan]
**Moderador:** [nombre]
**Transporte:** archivo | en vivo
**Objetivo:** [Qué se quiere conseguir]
```

### Formato de cada turno

```markdown
## Agent-proyectoA → Agent-proyectoB

[Contenido]

[ABIERTO: lo que queda por resolver]   o   [CONVERGIDO: lo que se acuerda]
```

- El destinatario (`→`) es opcional en deliberación: un turno puede ir a la sala entera.
- Cada turno acaba con un marcador `[ABIERTO: …]` o `[CONVERGIDO: …]`. Es lo que permite saber, sin releer todo, si la reunión puede cerrar.

### Briefing

Puede darse por chat. Lo importante es que quede en el acta: o el moderador escribe `## Briefing (Moderador)` antes de convocar, o cada agente resume en su primer turno lo que entendió.

### Decisión

Cuando la reunión converge, el convocante propone la decisión al moderador. Si confirma, la escribe en el acta:

```markdown
## Decisión (Moderador)

[Resolución, próximos pasos, quién hace qué]

**Fecha cierre:** YYYY-MM-DD
```

**Decisiones tomadas fuera del canal.** Si el moderador decide por el chat de tu sesión, tú la trasladas al canal como `Decisión (Moderador): …`. Lo que no está en el acta no se decidió. Deliberación fuera, acuerdos dentro.

### Guardar en sessions.yaml

No dupliques el acta. En `sessions.yaml` de cada proyecto afectado:

```yaml
highlights:
  - "Reunión [tipo] con [agentes] sobre [tema] → memsys3/docs/meets/YYYYMMDD_N.md"
  - "[Resultado principal]"
```

---

## 2. Norma de iniciativa (coordinación / deliberación)

En una reunión no se espera a que te nombren: si tienes algo que aportar, hablas. Sin esta norma, la reunión se convierte en un chat que se para en cuanto el moderador calla.

**Toma la palabra sin que te nombren cuando:**
1. Tienes evidencia (código, datos, un archivo) que cambia la decisión en curso.
2. Detectas un error o una contradicción en un turno anterior.
3. Hay un `[ABIERTO: …]` que solo tú puedes resolver (es de tu proyecto o de tu tarea).
4. Te piden algo, aunque no te nombren («¿alguien sabe…?»).

**No hables cuando:**
- Solo ibas a decir que estás de acuerdo. Un turno vacío no aporta: si coincides, escribe `[CONVERGIDO]` en tu siguiente turno con contenido.
- Ya llevas 3 turnos seguidos. Cede la palabra.

**Forma:** ~150 palabras por turno, una idea por turno.

**Parada.** Cuando los dos últimos turnos de agentes distintos acaban en `[CONVERGIDO]`, deja de hablar y propón la decisión al moderador.

**Regla del moderador.** El moderador puede decir «solo con mención» en cualquier momento. Desde entonces solo hablas si te nombra, hasta que diga lo contrario. Prevalece siempre sobre esta norma.

**En investigación (§5) no hay iniciativa:** cada fase tiene un responsable y se habla por turno estricto.

---

## 3. Transportes

### 3.A Por archivo

Los turnos se escriben directamente en el acta, uno debajo de otro.

**Tras cada turno, siempre en este orden:**

1. **Escribir** tu turno en el acta con la cabecera de §1.
2. **Resumir** al moderador en el chat de tu sesión:
   ```
   Turno: [a quién / a la sala / pregunta al moderador / convergido]
   Detalle: [qué propuse, qué cambió, qué queda abierto]
   Espera: [cómo estás vigilando la respuesta]
   ```
3. **Vigilar** la respuesta. Primero mira si ya llegó (`tail -60` del acta). Si no, y tu entorno permite procesos en segundo plano, lanza uno que espere a que el acta cambie:

   ```bash
   FILE="memsys3/docs/meets/YYYYMMDD_N.md"
   INITIAL=$(grep -c "^## Agent-" "$FILE")
   for i in $(seq 1 40); do
     [ "$(grep -c "^## Agent-" "$FILE")" -gt "$INITIAL" ] && { tail -60 "$FILE"; exit 0; }
     sleep 15
   done
   echo "Timeout: comprobar si el otro agente respondió"
   ```
   Si tu entorno no tiene procesos en segundo plano, dile al moderador que te avise cuando haya respuesta.

**Problemas frecuentes:**
- **No detecta el turno:** la cabecera debe empezar exactamente por `## Agent-` en la primera columna.
- **Reunión interrumpida:** el acta queda como estaba; quien retoma lee desde el último turno y sigue.

### 3.B En vivo

El servidor de [`kb/meet-live`](https://github.com/iv0nis/memsys3/tree/master/kb/meet-live) lleva los turnos y la web muestra la conversación. El protocolo (§1, §2) no cambia: solo cambia dónde se escribe. Su README explica cómo instalarlo.

**Montar la sala (el agente convocante):**
1. Arranca el servidor en segundo plano con la sala vacía y comprueba que `/api/floor` responde.
2. Si hay humanos en otro dispositivo, abre un túnel (README de meet-live, sección «Humanos fuera de esta máquina») y entrega el enlace al moderador para que lo comparta. No lo publiques tú en ningún canal.
3. Abre la reunión con un turno que liste agentes y humanos esperados, el objetivo y el orden del día. Pide a los humanos que escriban su nombre en la casilla.
4. A cada agente convocado, el moderador le pasa la dirección de la sala y su identidad.

**Durante la reunión:**
- **Hablar:** `say.py <tu-identidad>` (pide la palabra, escribe, la suelta). Un `409` significa esperar; si los turnos están suspendidos, no insistas.
- **Escuchar:** `watch.py <tu-identidad>` en segundo plano. Despierta solo con turnos de otros.
- **Leer siempre el texto completo** de `/api/messages`. Los humanos pegan documentos enteros y un resumen truncado los pierde.
- **Ritmo con humanos:** una pregunta por turno, numerada, con el contexto en dos líneas. Sus respuestas tardan minutos: no rellenes el silencio.
- Los controles de modo y suspensión son del moderador y solo funcionan desde su máquina. En modo moderación, espera a que escriba; responde el primer agente que coge la palabra.

**Cerrar:**
1. Turno de cierre en la sala con lo acordado.
2. `acta.py` genera `memsys3/docs/meets/YYYYMMDD_N.md` desde los turnos. Completa el objetivo y la `## Decisión (Moderador)` confirmada.
3. Para el túnel y el servidor. El enlace deja de funcionar.

---

## 4. Modo coordinación

Para: reparto de tareas, conflictos de trabajo paralelo, decisiones compartidas, diseño conjunto.

**PASO 1 — Briefing.** El convocante crea el acta (o la sala) con la cabecera y un briefing suficiente para que el otro agente entienda todo sin contexto adicional:

```markdown
## Briefing

**Objetivo:** [Qué se quiere decidir]
**Contexto:** [Información necesaria para deliberar]
**Pregunta:** [Qué debe responder o proponer el otro agente]
```

**PASO 2 — Convocar.** Por archivo, basta con pasar la ruta del acta al otro agente. En vivo, la dirección de la sala y su identidad.

**PASO 3 — Deliberar.** Los agentes hablan según la norma de iniciativa (§2). El moderador interviene si hay bloqueo o si le preguntan.

**PASO 4 — Decisión.** Con la reunión convergida, el convocante propone la decisión al moderador y, si confirma, la escribe (§1 Decisión).

---

## 5. Modo investigación

Para: bugs críticos, incidentes, análisis forense, post-mortems, decisiones arquitectónicas con varias alternativas.

### Roles

- **Investigador:** plantea el problema, hace preguntas diagnósticas y propone la solución.
- **Investigado:** responde con honestidad, reconstruye la secuencia y evalúa la solución.

**Detección del rol:** «investiga a [agente]» o «analiza [problema]» → Investigador. «responde a [agente]» o «reunión con [agente]» sobre algo que hiciste → Investigado. Si no está claro, pregunta.

### Antes de empezar

**Investigador:** lee los archivos afectados y los cambios recientes (`git log --oneline -10`, `git diff --stat HEAD~5..HEAD`), identifica las evidencias (qué, cuándo, qué debía pasar y qué pasó) y prepara 5-6 preguntas diagnósticas.

**Investigado:** reconstruye la secuencia (comandos, archivos, punto de fallo), tu razonamiento (qué asumiste, qué malinterpretaste) y la causa raíz.

### Las 6 fases

Turno estricto: cada fase es de quien la tiene asignada. Tono profesional y curioso, nunca acusatorio. Transparencia radical: se admiten los errores abiertamente.

**Fase 1 — Apertura (Investigador).**
```markdown
## [Investigador] → [Investigado]

He identificado que [problema, brevemente]. Para entender qué ocurrió:

1. **¿Cuándo ocurrió?** [detalle temporal]
2. **¿Qué herramienta o comando usaste?** [detalle técnico]
3. **¿Leíste [archivo] antes de [acción]?** [proceso]
4. **¿Qué pensabas en ese momento?** [razonamiento]
5. **¿Qué contenía [archivo] antes?** [estado previo]
6. **[Pregunta contextual]**
```

**Fase 2 — Respuesta honesta (Investigado).**
```markdown
## [Investigado] → [Investigador]

**1-6.** [Respuesta a cada pregunta, con detalles concretos]

## Qué ocurrió
1. **Estado inicial:** …
2. **Acción ejecutada:** …
3. **Punto de fallo:** …
4. **Consecuencias:** …

**Hipótesis de causa raíz:** [instrucción ambigua, hábito, malinterpretación…]

## Mitigación
- ✅ [acción ya hecha] / ⚠️ sin mitigar aún

## Compromiso para evitar que se repita
1. [acción preventiva concreta]
```

**Fase 3 — Análisis profundo (Investigador).**
```markdown
## [Investigador] → [Investigado]

**Validación de tu análisis:** ✅ [punto] · ⚠️ [matiz]

## Análisis
**Instrucción actual ([archivo] líneas X-Y):** [texto problemático]

**Problemas:**
1. ❌ No especifica [aspecto crítico]
2. ❌ Asume que [suposición incorrecta]

## Solución propuesta
[Cambio concreto]

¿Habría prevenido el problema? ¿Algo que añadir?
```

**Fase 4 — Evaluación (Investigado).** ¿La solución habría prevenido el problema? SÍ / PARCIALMENTE / NO y por qué. Sugerencias adicionales con ejemplo y ventaja. Priorización.

**Fase 5 — Implementación (Investigador).** Archivos modificados, cambio aplicado, qué sugerencias se aceptan o no y por qué, próximos pasos (items a cerrar, release).

**Fase 6 — Cierre formal (Investigado).**
```markdown
## [Investigado] → [Investigador]

## ✅ Conformidad
- ✅ [aspecto validado]

**Aprendizaje clave:** [lección concreta]

[CONVERGIDO: reunión cerrada]
```

### Emojis

| Emoji | Uso |
|-------|-----|
| ✅ | Validado, correcto |
| ❌ | Problema identificado |
| ⚠️ | Riesgo, matiz |
| 💡 | Aprendizaje |

Máximo 3-5 por sección: para clasificar, no para decorar.

---

**Sistema:** memsys3
<!-- version: 0.2.0 -->
