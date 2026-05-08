# New Session - Cargar Contexto del Proyecto

## 0. Identificar tu memsys3 + fecha actual

```bash
# Fecha actual (referencia para fechar entradas, pendientes, deadlines)
date '+%Y-%m-%d %H:%M %Z'

# Localizar memsys3
MEMSYS3_ROOT="$(pwd)/memsys3"
if [ -f "$MEMSYS3_ROOT/memory/project-status.yaml" ]; then
  echo "✅ memsys3: $MEMSYS3_ROOT"
else
  echo "⚠️ memsys3/ no encontrado en $(pwd). Buscando..."
  find . -maxdepth 4 -path "*/memsys3/memory/project-status.yaml" 2>/dev/null | sed 's|/memory/project-status.yaml$||'
fi
```

**Por qué `date`**: el agente NO conoce la fecha actual con fiabilidad (su corte de entrenamiento + ausencia de variable de tiempo) — ejecutar `date` al inicio le da una referencia concreta para datar entradas en sessions.yaml/memory.yaml/ADRs, calcular deadlines relativos ("en 2 semanas"), comparar recencia de archivos, y calendarizar pendientes.

## 1. Cargar contexto

- Lee **README.md** del proyecto para entender su visión general y objetivo
- Lee **@memsys3/PRINCIPLES.md** si existe — referencia canónica de los principios sistémicos de memsys3 (ADR-022)
- Lee **@memsys3/memory/project-status.yaml** para conocer el estado actual (fase, features, pendientes)
- Lee **@memsys3/memory/context.yaml** para cargar la memoria histórica (ADRs, sessions, gotchas)
- Lee **@memsys3/memory/memory.yaml** para conocer al usuario y reglas de comportamiento aprendidas (ADR-020)
- Actúa según las instrucciones en **@memsys3/agents/main-agent.yaml**

## Notas

- README.md contiene la identidad actual del proyecto (siempre actualizada)
- PRINCIPLES.md contiene los principios sistémicos de memsys3 (invariantes; anti-CDC, agnosticismo, etc.)
- context.yaml contiene memoria histórica sintetizada (decisiones, aprendizajes)
- memory.yaml contiene perfil del usuario + feedback (reglas/correcciones aprendidas)
- Juntos proporcionan contexto completo para trabajar efectivamente

<!-- version: 0.2.0 -->

