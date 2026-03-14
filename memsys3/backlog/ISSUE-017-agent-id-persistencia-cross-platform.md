# ISSUE-017 - agent_id: persistencia cross-platform (macOS, Linux, WSL, Windows)

**Estado**: Resuelto
**Prioridad**: Media
**Tipo**: Bug/Improvement
**Fecha**: 2026-03-14

## Problema

El archivo de identidad del agente se guarda en `/tmp/memsys3_agent_X.md`, que **no persiste** entre sesiones en WSL (se borra al reiniciar o tras `/compact`). Tampoco es portable a Windows nativo.

## Impacto

- Tras `/compact` o reinicio de WSL, el agente pierde su `agent_id`
- El agente no puede recuperar su identidad sin que el usuario se la indique manualmente
- En Windows nativo, `/tmp/` no existe

## Solución

Cambiar la ubicación de persistencia a `~/.claude/memsys3_agent_id`:

- **macOS/Linux/WSL**: `~/.claude/memsys3_agent_id` — directorio siempre presente (Claude Code lo crea)
- **Windows nativo**: `%USERPROFILE%\.claude\memsys3_agent_id` — equivalente en cmd/powershell

El directorio `~/.claude/` es gestionado por Claude Code y existe en todos los entornos soportados.

## Archivos a modificar

- `memsys3/prompts/agent-identity.md`
- `memsys3/prompts/endSession.md` (paso 4.5)
- `memsys3_templates/prompts/agent-identity.md`
- `memsys3_templates/prompts/endSession.md` (paso 4.5)

## Implementación

```bash
# Guardar
echo "Agent C" > ~/.claude/memsys3_agent_id

# Leer
cat ~/.claude/memsys3_agent_id 2>/dev/null || echo "Sin agent_id asignado"
```
