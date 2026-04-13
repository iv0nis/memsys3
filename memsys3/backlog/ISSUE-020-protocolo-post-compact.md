# ISSUE-020: Protocolo post-compact para recuperación de contexto

**Estado:** Propuesto
**Prioridad:** Media
**Tipo:** Issue
**Plazo:** Short-term
**Fecha identificación:** 2026-03-27
**Origen:** Análisis comparativo gentle-ai/Engram vs memsys3

---

## Problema

Cuando el usuario ejecuta `/compact` durante una sesión, el agente pierde parte del contexto conversacional. memsys3 sobrevive mejor que Engram (porque context.yaml es un archivo que se puede releer), pero no hay protocolo explícito que guíe al agente sobre qué hacer después de un compact.

**Situación actual:**
- Después de /compact, el agente tiene contexto reducido
- No hay instrucción en main-agent.yaml ni newSession.md sobre qué hacer post-compact
- El agente puede continuar trabajando con contexto incompleto sin darse cuenta
- Engram intenta resolver esto con un "compact prompt" inyectado — pero es frágil (depende de que el agente lo vea y lo siga)

**Ventaja actual de memsys3:**
- context.yaml y project-status.yaml son archivos — el agente puede releerlos en cualquier momento
- Esto ya es más robusto que Engram, pero no está documentado ni automatizado

---

## Propuesta

### Opción A: Instrucción en main-agent.yaml (RECOMENDADA)

Agregar al main-agent.yaml una sección sobre recuperación post-compact:

```yaml
# Recuperación post-compact:
# Si detectas que has perdido contexto (no recuerdas decisiones previas,
# archivos modificados, o el objetivo de la sesión):
# 1. Relee memsys3/memory/context.yaml
# 2. Relee memsys3/memory/project-status.yaml
# 3. Si hay checkpoints mid-session (FEATURE-010), reléelos
# 4. Continúa desde donde estabas
```

**Pros:** Simple, sin prompts adicionales, funciona en cualquier agente
**Contras:** Depende de que el agente detecte que perdió contexto

### Opción B: Hook post-compact (solo Claude Code)

Configurar un hook que automáticamente re-inyecte contexto después de /compact.

**Pros:** Automático, no depende del agente
**Contras:** Específico de Claude Code, rompe principio agnóstico (ADR-016)

### Opción C: Instrucción en CLAUDE.md del proyecto

Agregar instrucción en CLAUDE.md (si existe) sobre post-compact.

**Pros:** Claude Code lo lee automáticamente
**Contras:** Específico de Claude Code

---

## Decisión Recomendada

**Opción A** como base (agnóstico) + documentar Opción B como opcional para usuarios de Claude Code.

---

## Referencias

- **Inspiración:** Engram compact-prompt (engram-compact-prompt.md)
- **ADR relacionado:** ADR-016 (memsys3 agnóstico de modelo)
- **Feature relacionada:** FEATURE-010 (checkpoint mid-session — complementario)
- **Archivo afectado:** memsys3/agents/main-agent.yaml
