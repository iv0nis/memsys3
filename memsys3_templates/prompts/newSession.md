# New Session - Cargar Contexto del Proyecto

## 0. Identificar tu memsys3

```bash
MEMSYS3_ROOT="$(pwd)/memsys3"
if [ -f "$MEMSYS3_ROOT/memory/project-status.yaml" ]; then
  echo "✅ memsys3: $MEMSYS3_ROOT"
else
  echo "⚠️ memsys3/ no encontrado en $(pwd). Buscando..."
  find . -maxdepth 4 -path "*/memsys3/memory/project-status.yaml" 2>/dev/null | sed 's|/memory/project-status.yaml$||'
fi
```

## 1. Cargar contexto

- Lee **README.md** del proyecto para entender su visión general y objetivo
- Lee **@memsys3/memory/project-status.yaml** para conocer el estado actual (fase, features, pendientes)
- Lee **@memsys3/memory/context.yaml** para cargar la memoria histórica (ADRs, sessions, gotchas)
- Actúa según las instrucciones en **@memsys3/agents/main-agent.yaml**

## Notas

- README.md contiene la identidad actual del proyecto (siempre actualizada)
- context.yaml contiene memoria histórica sintetizada (decisiones, aprendizajes)
- Juntos proporcionan contexto completo para trabajar efectivamente

