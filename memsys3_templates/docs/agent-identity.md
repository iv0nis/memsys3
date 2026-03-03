# Agent Identity

## Qué es

El `agent_id` es el nombre que el moderador asigna a una sesión de Claude Code (u otro modelo) al convocarla: `Agent A`, `Agent B`, etc. No es un ID técnico del sistema — es la identidad conversacional de esa sesión.

## Para qué sirve

- Identificarse en reuniones (`@memsys3/prompts/meet.md`)
- Documentar qué agente hizo qué en sesiones paralelas
- Cualquier contexto donde el usuario trabaje con múltiples sesiones simultáneas

## Cómo asignar

El moderador pasa al agente el prompt `@memsys3/prompts/agent-identity.md` con el ID correspondiente, o lo incluye directamente en el briefing de la reunión.

## Persistencia entre compacts

El `agent_id` vive en el contexto conversacional — un `/compact` lo borra. Para preservarlo:

```bash
echo "Agent B" > /tmp/memsys3_agent_b.md
```

Al hacer `endSession`, el agente verifica que el archivo existe (paso 4.5). Al retomar tras un compact, puede leerlo:

```bash
cat /tmp/memsys3_agent_b.md
```

**Nota:** `/tmp` se borra al reiniciar el sistema. Si el ID se pierde, el moderador simplemente lo reasigna.

## Alcance

El `agent_id` es específico de la sesión, no del proyecto. Si el mismo agente trabaja en dos proyectos distintos, puede tener IDs distintos en cada uno.
