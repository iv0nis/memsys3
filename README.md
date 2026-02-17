# memsys3 - Sistema de Memoria para Agentes de IA

> Sistema replicable de gestión de contexto para optimizar el trabajo con AI Development Agents

**memsys3** es un sistema de gestión de contexto diseñado para optimizar el consumo de tokens de los Development Agents proporcionándoles contexto compacto y relevante del proyecto.

## 🎯 Problema que Resuelve

Cuando trabajas con AI agents en proyectos grandes:
- ❌ Los agents deben leer decenas de archivos de código para entender el proyecto
- ❌ Cada sesión nueva consume miles de tokens repitiendo el mismo contexto
- ❌ Decisiones y aprendizajes se pierden entre sesiones
- ❌ No hay visibilidad de qué "sabe" el agent

## ✨ Solución

**memsys3** proporciona:
- ✅ Context compilado en un único archivo (~2500-3000 tokens)
- ✅ Sistema de documentación estructurado (ADRs, sessions, status)
- ✅ Context Agent que filtra automáticamente la información relevante
- ✅ Visualizador web para ver la "mente" de los agents
- ✅ Prompts reutilizables (newSession, endSession, compile-context, mind, deploy, actualizar, adr, backlog, github)
- ✅ Sistema de rotación automática cuando supera límites (>1800 líneas)
- ✅ Plan de contingencia con archivado inteligente (>150K tokens)
- ✅ Prompt actualizar.md para actualización segura de memsys3 en proyectos existentes (con detección estructura antigua)
- ✅ README opcional: Context Agent acepta proyectos sin README o puede crear automáticamente
- ✅ Consulta .gitignore durante deployment: pregunta si excluir memsys3/ de git (PASO 8, privacidad)
- ✅ Sistema Backlog distribuible: memsys3/backlog/ con README agnóstico + prompt backlog.md (consultar, crear, actualizar)
- ✅ Sistema ADRs gestionable: prompt adr.md para gestionar decisiones arquitectónicas (consultar, crear, actualizar)
- ✅ Sistema sincronización catalana: actualizar_cat.md sincroniza español → catalán (branch catalan GitHub)
- ✅ Context Agent mejorado: análisis profundo README automático (PASO 7, 10 categorías) + integración backlog selectiva
- ✅ Statusline personalizable para Claude Code: monitoreo de uso de contexto activo en tiempo real (tokens/porcentaje alineado con `/context`)

## ⚡ Quick Start

### 1. Deployment

Desde la raíz de tu proyecto, con tu AI agent ejecuta:

```bash
# El agent clonará temporalmente el repo, copiará la estructura,
# te hará un briefing y personalizará el deployment
@memsys3/prompts/deploy.md
```

El workflow es:
1. Clone temporal de memsys3 desde GitHub
2. Copia de estructura a tu proyecto/memsys3/
3. Briefing sobre tu proyecto (stack, objetivos, etc.)
4. Personalización de archivos (project-status.yaml, newSession.md)
5. Limpieza del clone temporal

**Resultado**: Sistema memsys3 completamente funcional y personalizado.

### 2. Primeros Pasos

Una vez desplegado:

```bash
# 1. Compila el contexto inicial
@memsys3/prompts/compile-context.md

# 2. Visualiza la "mente" de los agents
@memsys3/prompts/mind.md

# 3. Comienza a trabajar
@memsys3/prompts/newSession.md
```

### 3. Uso con AI Agents

Una vez desplegado en tu proyecto, usa estos prompts:

**Comenzar sesión:**
```bash
@memsys3/prompts/newSession.md
```

**Acabar sesión:**
```bash
@memsys3/prompts/endSession.md
```

**Recompilar contexto:**
```bash
@memsys3/prompts/compile-context.md
```

**Ver la "mente" del agent:**
```bash
@memsys3/prompts/mind.md
```

## 📁 Estructura del Repositorio

```
memsys3/                          # Repositorio GitHub
├── README.md                    # Este archivo
├── memsys3_templates/           # PRODUCTO FINAL (templates agnósticos)
│   ├── README.md               # Documentación del sistema
│   ├── agents/
│   │   ├── main-agent.yaml    # Template del Development Agent
│   │   └── context-agent.yaml # Template del Context Agent
│   ├── memory/
│   │   ├── context.yaml        # Template de contexto (vacío)
│   │   ├── project-status.yaml # Template de estado (genérico)
│   │   ├── README.md          # Documentación detallada
│   │   ├── full/              # Templates de documentación
│   │   │   ├── adr.yaml      # Template de ADRs (vacío)
│   │   │   └── sessions.yaml # Template de sessions (vacío)
│   │   └── templates/         # Templates YAML base
│   │       ├── adr-template.yaml
│   │       ├── context-template.yaml
│   │       ├── project-status-template.yaml
│   │       └── sessions-template.yaml
│   ├── viz/                  # Visualizador web
│   │   ├── serve.py
│   │   ├── index.html
│   │   ├── style.css
│   │   ├── viewer.js
│   │   └── README.md
│   └── prompts/
│       ├── newSession.md      # Template de prompt para iniciar sesión
│       ├── endSession.md      # Template de prompt para documentar
│       ├── compile-context.md # Template de prompt del Context Agent
│       ├── mind.md           # Template de prompt para visualizador
│       ├── deploy.md         # Guía de deployment inicial
│       ├── actualizar.md      # Guía de actualización segura de memsys3
│       ├── adr.md            # Template para gestionar ADRs
│       ├── backlog.md        # Template para gestionar backlog
│       └── github.md         # Template para commits/push a GitHub
└── memsys3/                     # Dog-fooding (desarrollo de memsys3)
    └── (Instancia específica, NO se distribuye)
```

## 🔄 Workflow

### 1. **Documentar** (Humans/DevAI)
- Escribe decisiones en `memsys3/memory/full/adr.yaml`
- Documenta sesiones en `memsys3/memory/full/sessions.yaml`
- Actualiza `memsys3/memory/project-status.yaml`

### 2. **Compilar** (Context Agent)
- Ejecuta `@memsys3/prompts/compile-context.md`
- Genera `memsys3/memory/context.yaml` compacto con criterio inteligente
- Aplica rotación automática si supera 1800 líneas
- Aplica Plan de Contingencia si supera 150K tokens

### 3. **Desarrollar** (DevAI)
- Carga `@memsys3/prompts/newSession.md`
- Desarrolla con contexto completo
- Documenta al acabar con `@memsys3/prompts/endSession.md`

## 🎨 Visualizador Web

Interfaz visual para ver la "mente" de los agents:

```bash
cd memsys3/viz
python3 serve.py
```

**Pestañas:**
- 🤖 **Agent View**: Context compilado que ve el DevAI
- 📚 **Full History**: Todas las ADRs y sessions
- 📊 **Project Status**: Estado completo del proyecto
- 📈 **Stats**: Métricas de compilación

## 🚀 Features Principales

### Context Agent con Criterio Inteligente
- Filosofía: "¿Qué debe saber CUALQUIER agent descontextualizado para trabajar aquí?"
- Límite único: máx 2000 líneas en context.yaml
- NO límites arbitrarios por ADRs/sessions
- Lee TODO primero, después filtra con criterio
- **README opcional**: acepta proyectos sin README o puede crear automáticamente desde project-status

### Rotación Automática (>1800 líneas)
- Detecta automáticamente cuando sessions.yaml o adr.yaml superan 1800 líneas
- Rotación segura: copia → verifica → crea nuevo
- sessions.yaml → sessions_N.yaml
- adr.yaml → adr_N.yaml
- CA lee todos los archivos rotados hasta detectar >150K tokens

### Plan de Contingencia (>150K tokens)
- Cuando contexto supera 150K tokens, CA archiva datos irrelevantes
- Mueve a memsys3/memory/history/ (que NO se lee → ahorro real)
- Reduce a ~120K tokens
- Datos preservados, no perdidos

### Sistema de Templates YAML
- Templates agnósticos reutilizables
- Consistencia total del sistema
- ~30% ahorro tokens vs Markdown
- Mejor para LLMs (estructura clara)

### Sistema de Actualización
- **Prompt actualizar.md**: actualización segura de memsys3 en proyectos existentes
- PASO 0: detección inteligente de estructura antigua incompatible (3 escenarios)
- Backups automáticos antes de tocar datos
- Preserva histórico completo durante migración

### Sistema Backlog Distribuible
- **memsys3/backlog/**: gestión de trabajo futuro estructurado
- README agnóstico (315 líneas) con 3 ejemplos ilustrativos (ISSUE, FEATURE, IMPROVEMENT)
- **Prompt backlog.md**: 3 operaciones (consultar, crear, actualizar)
- Sistema de prefijos: ISSUE-XXX, FEATURE-XXX, IMPROVEMENT-XXX, SPEC-XXX, BLUEPRINT-XXX, EXPLORATION-XXX

### Deployment con Privacidad
- **Consulta .gitignore** (PASO 8 en deploy.md): pregunta si excluir memsys3/ de git
- Opción A (RECOMENDADO): Excluir - contexto local privado
- Opción B: Incluir - para equipos que compartan contexto
- Previene subida accidental de información sensible (sessions, decisiones, gotchas)
- **⚠️ Workaround @ mentions**: Si eliges Opción A (excluir), @ mentions NO funcionan (limitación Claude Code). Solución: usar instrucciones directas ("Ejecuta memsys3/prompts/newSession.md")

### Statusline para Claude Code
- Script `~/.claude/statusline.sh` que muestra modelo y uso de contexto activo en tiempo real
- Muestra porcentaje y tokens calculados desde `used_percentage` (no `total_input_tokens` histórico)
- Esto alinea los valores con los que muestra `/context`, evitando confusión por tokens acumulados
- **Nota**: `/compact` y `/context` no disparan actualización del statusline — enviar cualquier mensaje regular sí lo actualiza

## 🛠 Stack Tecnológico

- **Frontend**: HTML/CSS/JS (visualizador web)
- **Backend**: Python 3.x (servidor visualizador)
- **Database**: Ninguno (YAML files como almacenamiento)
- **Deploy**: GitHub + clonado local
- **Lenguaje Docs**: YAML + Markdown
- **Compatibilidad**: Agnóstico de modelo de IA (funciona con Claude, Gemini, Codex, etc.)

## 📖 Documentación Completa

Ver **[memsys3_templates/memory/README.md](memsys3_templates/memory/README.md)** para:
- Criterios de filtraje del Context Agent
- Mejores prácticas
- Troubleshooting
- Ejemplos detallados

## 📦 Guías de Deployment

### Deployment Inicial (Nuevo Proyecto)
Para desplegar memsys3 en un proyecto nuevo, ver la guía en `memsys3_templates/prompts/deploy.md`

### Actualización (Proyecto Existente)
Para actualizar memsys3 en un proyecto que ya lo tiene desplegado, ver la guía en `docs/UPDATE.md`

## 🛠 Requisitos

- Python 3.x (para el visualizador web)
- **Cualquier modelo de IA** compatible con prompts markdown (Claude, Gemini, Codex, etc.)
- Git (opcional, para versionado)

**Nota:** memsys3 es **agnóstico de modelo de IA**. Los prompts (.md) y archivos YAML funcionan universalmente. Features específicas de herramientas (como comandos locales de Claude Code) son opcionales.

## 🎓 Dog-fooding

Este proyecto usa **memsys3** para desarrollarse a sí mismo.

- `memsys3_templates/` = PRODUCTO FINAL (lo que se distribuye)
- `memsys3/` = Instancia de dog-fooding (desarrollo interno, NO se distribuye)

Los cambios/mejoras se aplican primero en `memsys3_templates/` y luego se prueban desplegándolos en `memsys3/`.

**Separación Agnóstico/Específico (ADR-011):**

Al crear nuevos archivos, pregúntate: **"¿Tiene sentido esto en CUALQUIER proyecto con memsys3?"**
- **SI SÍ** → Agnóstico: va en `memsys3_templates/` (se distribuye a otros proyectos)
- **SI NO** → Específico: va en `/prompts/` raíz (solo desarrollo memsys3, NO se distribuye)

**Ejemplos de archivos específicos (NO se distribuyen):**
- `prompts/actualizar_cat.md` - Solo memsys3 tiene versión catalana
- `prompts/comprobar_alineamiento.md` - Solo memsys3 tiene dog-fooding

**Práctica recomendada:**

Al finalizar sesiones donde modificaste archivos agnósticos (prompts, agents, viz, templates), ejecutar `@prompts/comprobar_alineamiento.md` ANTES de endSession para verificar sincronización dog-fooding ↔ templates.

## 🤝 Contribuciones

Este sistema está abierto a mejoras. Si tienes ideas o encuentras bugs, abre un issue o PR en GitHub.

## 📝 Licencia

MIT License - Libre para usar en cualquier proyecto

---

**Repositorio**: https://github.com/iv0nis/memsys3
**Releases**: [Ver versiones en GitHub](https://github.com/iv0nis/memsys3/releases)
**Documentación**: [memsys3_templates/memory/README.md](memsys3_templates/memory/README.md)
