# Reunión de Coordinación entre Agentes

Usa este prompt cuando necesites coordinar dos o más agentes sobre cualquier tema: reparto de tareas, resolución de conflictos, diseño compartido, decisiones con múltiples perspectivas.

**No usar para**: debugging forense o investigación de bugs → usa `meet-research.md`

---

## PASO 1: Crear el archivo de reunión

**Ubicación:** `memsys3/docs/meets/DDMMYY_N.md` del proyecto dueño del tema
- `DD` día, `MM` mes, `YY` año, `N` número de reunión del día
- Si participan agentes de distintos proyectos: el archivo va en el proyecto al que pertenece el tema discutido (no el que "anfitriona" la reunión)
- Si el tema es transversal sin dueño claro: el moderador decide explícitamente antes de crear el archivo

**Estructura base:**

```markdown
# Reunión DDMMYY_N — [Objetivo en una línea]

**Fecha:** YYYY-MM-DD
**Agentes:** [Agent A (proyecto)], [Agent B (proyecto)]
**Moderador:** [nombre]
**Objetivo:** [Qué se quiere conseguir]

---

## Briefing (Moderador)
[Contexto y qué necesitas de cada agente]

---
```

**Sobre el Briefing**: puede darse por chat (es lo natural), pero debe incorporarse al archivo. Dos opciones: el moderador lo escribe aquí antes de convocar, o cada agente resume al inicio de su turno lo que entendió del briefing recibido por chat.

---

## PASO 2: Convocar a los agentes

Pega esto en la ventana de cada agente (uno a uno, respetando el turno):

```
Lee y escribe tu turno en: memsys3/docs/meets/DDMMYY_N.md
```

**Identificación de agentes:**
- Mismo proyecto: `Agent A`, `Agent B`
- Proyectos distintos: `Agent A (proyecto)`, `Agent B (proyecto)`

---

## PASO 3: Formato de cada turno (para agentes)

Cada agente escribe su sección en el documento:

```markdown
## [Agent X (proyecto)] → [Agent Y / Todos]

[Contenido del turno: estado, propuesta, preguntas, respuestas]

Tu turno, [Agent Y].
```

Al terminar de escribir en el documento, el agente envía un resumen breve en el chat al moderador con este formato:

```
CTA: [Turno a Agent Y / Pregunta directa a ti, moderador]
Detalle: [Qué cambié, qué propuse, qué quedó sin resolver]
```

---

## PASO 4: Decisión del moderador

Cuando todos los turnos estén completos, el moderador escribe la sección final:

```markdown
## Decisión (Moderador)

[Resolución final, próximos pasos, qué hace cada agente]

**Fecha cierre:** YYYY-MM-DD
```

Solo el moderador escribe esta sección.

---

## PASO 5: Referenciar en sessions.yaml

No duplicar contenido. En sessions.yaml de cada proyecto afectado:

```yaml
highlights:
  - "Reunión de coordinación con [Agente] sobre [tema] (memsys3/docs/meets/DDMMYY_N.md)"
  - "[Resultado principal en una línea]"
```

---

**Versión:** 1.0
**Sistema:** memsys3
