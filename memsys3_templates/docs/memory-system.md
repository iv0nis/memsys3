# Sistema de Memoria

## Cómo funciona

El Context Agent lee todo el histórico (`sessions.yaml`, `adr.yaml`, `project-status.yaml`, `README.md`) y genera `context.yaml` — un archivo compacto con lo que cualquier agente descontextualizado necesita para trabajar.

**Límite único:** 2000 líneas (~2500-3000 tokens). Sin límites arbitrarios por ADRs o sesiones individuales.

## Archivos clave

```
memsys3/memory/
├── context.yaml          — contexto compilado (lo que lee el agente)
├── project-status.yaml   — estado actual del proyecto
└── full/
    ├── sessions.yaml     — histórico de sesiones
    ├── adr.yaml          — decisiones arquitectónicas
    └── sessions_N.yaml   — rotaciones anteriores
```

## Flujo

1. **Desarrollar** — el agente trabaja y documenta con `endSession.md`
2. **Compilar** — el Context Agent ejecuta `compile-context.md` y genera `context.yaml`
3. **Iniciar** — el agente carga `newSession.md` que lee `context.yaml`

## Rotación automática (>1800 líneas)

Cuando `sessions.yaml` o `adr.yaml` superan 1800 líneas, se rotan automáticamente:

- **Escenario A (1800-2000 líneas):** documentar primero, rotar después
  - `sessions.yaml` → `sessions_N.yaml` (copia completa)
  - Crear nuevo `sessions.yaml` vacío
- **Escenario B (>2000 líneas):** rotar antes de documentar

El Context Agent lee todos los archivos rotados hasta detectar >150K tokens.

## Plan de Contingencia (>150K tokens)

Cuando el histórico total supera 150K tokens, el Context Agent archiva datos irrelevantes a `memory/history/` (que no se lee), reduciendo a ~120K tokens. Los datos se preservan, no se pierden.

## Sistema de pesos

Cada sesión tiene un peso que determina cuánto contexto ocupa en `context.yaml`:

| Peso | Líneas orientativas | Cuándo |
|------|-------------------|--------|
| 🔴 ALTO | ~140 líneas → ~35 en context | ADRs, decisiones arquitectónicas, features críticas |
| 🟡 MEDIO | ~95 líneas → ~20 en context | Features normales, refactorings |
| 🟢 BAJO | ~70 líneas → ~8 en context | Fixes menores, mantenimiento |

**Retrocompatibilidad:** sesiones sin campo `peso` se tratan como peso medio.

## Metadata en context.yaml

El Context Agent incluye automáticamente:
- `compilado_por`, `ultima_compilacion`, `version_context`
- `notas_compilacion`: ADRs totales vs incluidas, sesiones totales, criterios de filtrado
