# memsys3 - Sistema de Memoria para Agentes de IA

> Sistema de gestión de contexto para optimizar el trabajo con AI Agents

## 🎯 ¿Qué es memsys3?

**memsys3** es una sola carpeta que se añade a tu proyecto y gestiona la memoria de tus AI agents entre sesiones.

## 💡 Por qué memsys3

- **Un cerebro, una carpeta** — minimalismo digital: sin base de datos, sin servidor, sin dependencias, sin mecanismos que mantener aparte del propio agente. Copias `memsys3/` y funciona
- **Agnóstico** — funciona con cualquier modelo de IA (Claude, Gemini, Codex, etc.)
- **Workflow sencillo pero flexible** — 3 prompts para el día a día (empezar, trabajar, acabar)
- **Basado en @ mentions** — ejecutas prompts directamente con `@memsys3/prompts/...`, sin CLIs ni herramientas externas (si tu herramienta no tiene `@`, la misma ruta sin arroba funciona igual)
- **Deploy y actualización triviales** — un comando para instalar, un comando para actualizar
- **Human in the loop** — tú decides cuándo empezar y acabar sesión, cuándo compilar contexto, cuándo actualizar. El sistema no hace nada sin ti
- **Todo lo que lee el arranque cabe en una lectura** — memoria en dos capas, estado vivo corto, presupuestos medidos en bytes (ADR-033); rotación y archivado automático cuando crece

## 🚀 Uso Diario

### Iniciar Sesión

Al comenzar a trabajar, carga el contexto del proyecto:

```bash
@memsys3/prompts/newSession.md
```

Esto carga automáticamente:
- Visión general del proyecto (`README.md`)
- Estado actual del proyecto (`memory/project-status.yaml`)
- Memoria histórica compilada (`memory/context.yaml`)
- Instrucciones del Main Agent (`agents/main-agent.yaml`)

### Durante el Desarrollo

Trabaja normalmente. El sistema está diseñado para no interferir en tu workflow.

### Terminar Sesión

Al finalizar, documenta lo realizado:

```bash
@memsys3/prompts/endSession.md
```

Esto:
- Documenta la sesión en `memory/full/sessions.yaml`
- Documenta gotchas encontrados (con criticidad) en la misma sesión
- Crea ADRs si hubo decisiones arquitectónicas
- Actualiza el `memory/project-status.yaml`
- Aplica rotación automática si es necesario

### Compilar Contexto

Cuando quieras actualizar el contexto compilado (en una **nueva instancia limpia**):

```bash
@memsys3/prompts/compile-context.md
```

El Context Agent:
- Compila de forma INCREMENTAL: parte del `context.yaml` anterior y lee solo lo nuevo desde la última compilación (desde cero solo si se lo pides)
- Aplica criterio inteligente de filtrado
- Actualiza `memory/context.yaml` compacto (máx 2000 líneas, cabe en una lectura)
- Mantiene ligera la capa condensada de `memory.yaml` (fusiones trazables, con tu OK)
- Aplica Plan de Contingencia si supera el presupuesto (medido en bytes)

`endSession` te lo ofrece en un agente fresco cuando hay 5 o más sesiones sin compilar.

## 📁 Estructura

```
memsys3/
├── README.md                       # Este archivo
├── agents/
│   ├── main-agent.yaml            # Configuración del Main Agent
│   └── context-agent.yaml         # Configuración del Context Agent
├── memory/
│   ├── context.yaml                # Context compilado (generado por CA)
│   ├── project-status.yaml         # Estado vivo (índice de pendientes, sin histórico)
│   ├── memory.yaml                 # Memoria del usuario, capa ligera (lo que lee el arranque)
│   ├── README.md                   # Documentación detallada del sistema
│   ├── full/                       # Datos completos (NO se leen al arrancar)
│   │   ├── adr.yaml               # Architectural Decision Records
│   │   ├── sessions.yaml          # Historial de sesiones
│   │   ├── memory_full.yaml       # Memoria del usuario, capa completa (mismo id)
│   │   ├── tasks.yaml             # Detalle de tareas sin expediente
│   │   └── (archivos rotados: adr_N.yaml, sessions_N.yaml)
│   ├── templates/                  # Templates YAML reutilizables
│   │   ├── adr-template.yaml
│   │   ├── context-template.yaml
│   │   ├── memory-template.yaml
│   │   ├── project-status-template.yaml
│   │   └── sessions-template.yaml
│   └── history/                    # Archivos archivados (NO se leen)
│       └── (datos antiguos cuando se supera el presupuesto)
└── prompts/
    ├── newSession.md              # Cargar contexto al iniciar
    ├── endSession.md              # Documentar sesión
    └── compile-context.md         # Compilar contexto (Context Agent)
```

## 🔄 Workflow

### 1. Documentar (Developers + Main Agent)
- Desarrolla features normalmente
- Al final de sesión: `@memsys3/prompts/endSession.md`
- Se documenta en `memory/full/sessions.yaml`
- Se crean ADRs si hay decisiones arquitectónicas importantes

### 2. Compilar (Context Agent)
- En instancia limpia o agente fresco (endSession lo ofrece): `memsys3/prompts/compile-context.md`
- Incremental: contexto anterior + lo nuevo
- Aplica criterio inteligente
- Actualiza `memory/context.yaml` compacto y mantiene ligera `memory.yaml`

### 3. Desarrollar (Main Agent)
- Nueva sesión: `@memsys3/prompts/newSession.md`
- Carga contexto compilado
- Desarrolla con visión completa del proyecto
- Al terminar: `@memsys3/prompts/endSession.md`

## 🧠 Filosofía del Context Agent

El Context Agent tiene **visión panorámica completa** y decide basándose en:

**"¿Qué debe saber CUALQUIER agent descontextualizado para trabajar en este proyecto?"**

**Incluye:**
- Decisiones con impacto global
- Decisiones no obvias leyendo el código
- Trade-offs importantes
- Problemas resueltos que pueden repetirse
- Configuraciones críticas

**Excluye:**
- Cambios cosméticos
- ADRs obsoletas
- Sessions muy antiguas sin relevancia
- Detalles de implementación evidentes

## 🔁 Escalabilidad

### Rotación Automática (>1800 líneas)

Cuando `sessions.yaml` o `adr.yaml` superan 1800 líneas:
- `endSession.md` detecta automáticamente
- Rotación segura: copia → verifica → crea nuevo
- `sessions.yaml` → `sessions_1.yaml`
- `adr.yaml` → `adr_1.yaml`
- Context Agent lee TODOS los archivos rotados

### Plan de Contingencia (presupuesto en bytes)

Cuando lo que el Context Agent tiene que leer supera su presupuesto (~300 KB en español / ~600 KB en inglés ≈ 150K tokens, medido con `wc -c`):
- Context Agent identifica datos irrelevantes
- Los mueve a `memory/history/` (NO se lee → ahorro real)
- Reduce a ~80% del presupuesto
- Datos preservados, no perdidos, recuperables

### Todo lo que lee el arranque cabe en una lectura (ADR-033)

- `memory.yaml` en dos capas: ligera (id + regla + fecha) y `full/memory_full.yaml` (contexto y origen, mismo id)
- `project-status.yaml` = solo estado vivo: sin histórico, `pendientes_prioritarios` como índice de líneas ≤300 caracteres con `→ puntero`
- `endSession` limpia sin preguntar; `newSession` agrupa los pendientes vencidos en una sola pregunta

## 📖 Documentación Detallada

Ver **[memory/README.md](memory/README.md)** para:
- Criterios detallados del Context Agent
- Mejores prácticas de documentación
- Troubleshooting
- Ejemplos de ADRs y sessions

## 🛠 Requisitos

- AI agent compatible con prompts markdown

## 💡 Tips

### Para Main-Agent
- NO ejecutes `compile-context.md` tú mismo (ADR-008); con ≥5 sesiones sin compilar, endSession ofrece lanzarlo en un agente fresco
- Sugiere `endSession.md` al finalizar sesión
- El user decide cuándo compilar el contexto

### Para Context-Agent
- Lee TODO primero, filtra después
- Confía en tu criterio inteligente
- Límite único: 2000 líneas en `context.yaml`

### Para Developers
- Documenta decisiones arquitectónicas importantes como ADRs
- Usa `endSession.md` al finalizar cada sesión significativa
- Compila contexto en nueva instancia limpia cuando sea necesario
- Revisa `memory/context.yaml` para entender qué saben los agents

## 🔧 Personalización

Este sistema es altamente personalizable:

- **agents/main-agent.yaml**: Personaliza comportamiento del Main Agent
- **memory/project-status.yaml**: Mantén actualizado el estado de tu proyecto
- **memory/templates/**: Ajusta los templates según tus necesidades

---

**Sistema memsys3** - Gestión inteligente de contexto para AI Agents
