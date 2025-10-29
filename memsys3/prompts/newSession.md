# New Session - Cargar Contexto del Proyecto

- En este proyecto trabajaremos en **memsys3**: sistema de gestión de contexto para AI Development Agents
- Actúa según las instrucciones en 'memsys3/agents/main-agent.yaml'
- Este es un proyecto meta: usamos memsys3 para desarrollar el mismo memsys3 (dog-fooding)
- Lee memsys3/memory/project-status.yaml y memsys3/memory/context.yaml

## Estructura Crítica

- **memsys3_templates/** = PRODUCTO FINAL (templates agnósticos que se distribuyen)
- **memsys3/** = Instancia de dog-fooding (desarrollo interno, NO se distribuye)

## Workflow de Desarrollo

Los cambios/mejoras se aplican PRIMERO en `memsys3_templates/` y luego se prueban desplegándolos en `memsys3/`.
