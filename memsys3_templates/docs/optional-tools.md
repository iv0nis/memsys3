# Herramientas Opcionales

Estas features son específicas de Claude Code. No afectan al funcionamiento core de memsys3.

---

## Statusline

Muestra modelo activo y uso de contexto en tiempo real en la línea de estado de Claude Code.

**Setup:**

1. Crear `~/.claude/statusline.sh` con el script de monitoreo
2. Añadir a `~/.claude/settings.json`:

```json
{
  "statusLine": {
    "type": "command",
    "command": "~/.claude/statusline.sh"
  }
}
```

**Comportamiento:**
- Muestra porcentaje y tokens calculados desde `used_percentage` (no `total_input_tokens` histórico)
- Se alinea con los valores de `/context`
- Se actualiza con cada mensaje regular del usuario — `/compact` y `/context` no disparan actualización

---

## Comandos globales

Instala comandos disponibles en cualquier proyecto desde Claude Code:

```bash
@memsys3/prompts/commands.md
```

**Comandos instalados en `~/.claude/commands/`:**
- `/deploy-memsys3` — deployment inicial
- `/actualizar-memsys3` — actualización de memsys3 en proyecto existente
