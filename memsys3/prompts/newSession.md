# New Session - Cargar Contexto del Proyecto

- Lee **README.md** del proyecto para entender su visión general y objetivo
- Lee **@memsys3/memory/project-status.yaml** para conocer el estado actual (fase, features, pendientes)
- Lee **@memsys3/memory/context.yaml** para cargar la memoria histórica (ADRs, sessions, gotchas)
- Actúa según las instrucciones en **@memsys3/agents/main-agent.yaml**

## Notas

- README.md contiene la identidad actual del proyecto (siempre actualizada)
- context.yaml contiene memoria histórica sintetizada (decisiones, aprendizajes)
- Juntos proporcionan contexto completo para trabajar efectivamente

## Contexto Específico: memsys3 (Dog-fooding)

- Este es un **proyecto meta**: usamos memsys3 para desarrollar el mismo memsys3
- **memsys3_templates/** = PRODUCTO FINAL (templates agnósticos que se distribuyen)
- **memsys3/** = Instancia de dog-fooding (desarrollo interno, NO se distribuye)

### Workflow de Desarrollo

Los cambios/mejoras se aplican PRIMERO en `memsys3_templates/` y luego se prueban desplegándolos en `memsys3/`.

**IMPORTANTE: Trabaja en ESPAÑOL siempre**

