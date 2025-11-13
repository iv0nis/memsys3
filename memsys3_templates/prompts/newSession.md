# Nova Sessió - Carregar Context del Projecte

- En aquest projecte treballarem en **memsys3**: sistema de gestió de context per a AI Development Agents
- Actua segons les instruccions a '@memsys3/agents/main-agent.yaml'
- Aquest és un projecte meta: fem servir memsys3 per desenvolupar el mateix memsys3 (dog-fooding)
- Llegeix @memsys3/memory/project-status.yaml i @memsys3/memory/context.yaml
- **IMPORTANT: Treballa en CATALÀ sempre**

## Estructura Crítica

- **memsys3_templates/** = PRODUCTE FINAL (templates agnòstics que es distribueixen)
- **memsys3/** = Instància de dog-fooding (desenvolupament intern, NO es distribueix)

## Workflow de Desenvolupament

Els canvis/millores s'apliquen PRIMER a `memsys3_templates/` i després es proven desplegant-los a `memsys3/`.
