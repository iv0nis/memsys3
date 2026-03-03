# memsys3 — Overview

## Qué es

memsys3 es un sistema de gestión de contexto para agentes de IA. Proporciona memoria persistente entre sesiones, documentación estructurada y protocolos de colaboración multi-agente.

## Problema que resuelve

Los agentes de IA pierden contexto entre sesiones. Sin memsys3, cada sesión nueva consume miles de tokens repitiendo el mismo contexto, las decisiones se pierden y no hay visibilidad de qué "sabe" el agente.

## Solución

Un conjunto de archivos YAML + prompts Markdown que el agente lee al iniciar cada sesión. El Context Agent compila el histórico completo en un archivo compacto (~2500-3000 tokens) que cualquier agente puede cargar en segundos.

## Agnóstico de modelo

memsys3 funciona con cualquier modelo de IA que entienda Markdown: Claude, Gemini, Codex, etc. Los prompts son archivos `.md` estándar. Las features específicas de herramientas (statusline de Claude Code, comandos globales) son opcionales.

## Componentes principales

| Componente | Descripción | Doc |
|-----------|-------------|-----|
| Sistema de memoria | Compilación, rotación, plan contingencia | [memory-system.md](memory-system.md) |
| Documentación | Sessions, ADRs, gotchas, project-status | [sessions-adrs.md](sessions-adrs.md) |
| Backlog | Gestión de trabajo futuro | [backlog.md](backlog.md) |
| Meets | Reuniones colaborativas entre agentes | [meets.md](meets.md) |
| Agent identity | Identidad de sesión persistente | [agent-identity.md](agent-identity.md) |
| Visualizador | Dashboard web de la memoria | [visualizer.md](visualizer.md) |
| Deployment | Instalación y actualización | [deployment.md](deployment.md) |
| Herramientas opcionales | Statusline, comandos Claude Code | [optional-tools.md](optional-tools.md) |

## Filosofía

- **Contexto mínimo, máxima relevancia** — el Context Agent filtra con criterio, no acumula todo
- **YAML sobre Markdown** — ~30% ahorro de tokens, estructura más clara para LLMs
- **Agnóstico primero** — cualquier mejora que no sea específica de una herramienta va en `memsys3_templates/`
- **Dog-fooding** — memsys3 se desarrolla usando memsys3
