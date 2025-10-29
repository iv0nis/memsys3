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
- ✅ Prompts reutilizables para comenzar/terminar sesiones
- ✅ Sistema de rotación automática cuando supera límites (>1800 líneas)
- ✅ Plan de contingencia con archivado inteligente (>150K tokens)

## ⚡ Quick Start

### 1. Instalación

```bash
# Clona el repositorio
git clone https://github.com/iv0nis/memsys3.git

# Copia memsys3_templates a la raíz de tu proyecto como 'memsys3/'
cp -r memsys3/memsys3_templates /path/to/your/project/memsys3
```

### 2. Configuración Inicial

**Opción A: Deployment Guiado (Recomendado)**
```bash
# Con tu AI agent, ejecuta el prompt de deploy
@memsys3/prompts/deploy.md
```

El agent te hará un briefing y personalizará el deployment según tu proyecto.

**Opción B: Manual**
```bash
cd /path/to/your/project/memsys3

# 1. Personaliza el project-status.yaml inicial
# Edita memory/project-status.yaml con info de tu proyecto

# 2. Personaliza el agent (opcional)
# Edita agents/main-agent.yaml según tu workflow

# 3. Compila el contexto inicial
# Ejecuta con tu AI agent: @prompts/compile-context.md

# 4. Visualiza
cd memory
python3 serve.py
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
│   │   ├── templates/         # Templates YAML base
│   │   │   ├── adr-template.yaml
│   │   │   ├── context-template.yaml
│   │   │   ├── project-status-template.yaml
│   │   │   └── sessions-template.yaml
│   │   └── viz/              # Visualizador web
│   │       ├── serve.py
│   │       ├── index.html
│   │       ├── style.css
│   │       ├── viewer.js
│   │       └── README.md
│   └── prompts/
│       ├── newSession.md      # Template de prompt para iniciar sesión
│       ├── endSession.md      # Template de prompt para documentar
│       ├── compile-context.md # Template de prompt del Context Agent
│       ├── mind.md           # Template de prompt para visualizador
│       └── deploy.md         # Guía de deployment
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
cd memsys3/memory/viz
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
- AI agent compatible con prompts markdown
- Git (opcional, para versionado)

## 🎓 Dog-fooding

Este proyecto usa **memsys3** para desarrollarse a sí mismo.

- `memsys3_templates/` = PRODUCTO FINAL (lo que se distribuye)
- `memsys3/` = Instancia de dog-fooding (desarrollo interno, NO se distribuye)

Los cambios/mejoras se aplican primero en `memsys3_templates/` y luego se prueban desplegándolos en `memsys3/`.

## 🤝 Contribuciones

Este sistema está abierto a mejoras. Si tienes ideas o encuentras bugs, abre un issue o PR en GitHub.

## 📝 Licencia

MIT License - Libre para usar en cualquier proyecto

---

**Versión**: 1.0
**Repositorio**: https://github.com/iv0nis/memsys3
**Documentación**: [memsys3_templates/memory/README.md](memsys3_templates/memory/README.md)
