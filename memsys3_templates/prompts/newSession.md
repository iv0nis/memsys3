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

## 0.5 Idioma de respuesta (ejecutar AHORA, antes de responder al usuario)

Detecta el idioma predominante de los archivos canónicos del proyecto (`README.md`, `memsys3/memory/project-status.yaml`, `memsys3/memory/memory.yaml`). DEBES responder al usuario en ESE idioma desde el primer mensaje de la sesión, NO en el default de tu harness. Si los archivos están en idiomas mixtos, prioriza el de `README.md`. Si tienes dudas explícitas, pregunta al usuario antes de la primera respuesta sustantiva.

**Por qué esta sección**: distintos harnesses tienen defaults distintos (algunos a inglés para respuestas cortas pese al contexto en otro idioma). Sin contrato explícito, el agnosticismo de idioma queda al azar del harness.

## 1. Cargar contexto (ejecutar AHORA, antes de responder al usuario)

Estos pasos NO son opcionales ni diferidos: ejecútalos como primer acto de la sesión, en este orden, antes de procesar cualquier instrucción posterior del usuario. Si el usuario te pide algo concreto, ejecútalo DESPUÉS de completar esta carga.

1. Lee `README.md` del proyecto para entender su visión general y objetivo.
2. Lee `memsys3/PRINCIPLES.md` si existe — referencia canónica de los principios sistémicos de memsys3 (ADR-022).
3. Lee `memsys3/memory/project-status.yaml` para conocer el estado actual (fase, features, pendientes).
4. Lee `memsys3/memory/context.yaml` para cargar la memoria histórica (ADRs, sessions, gotchas).
5. Lee `memsys3/memory/memory.yaml` para conocer al usuario y reglas de comportamiento aprendidas (ADR-020).
6. Lee `memsys3/agents/main-agent.yaml` y aplica sus restricciones desde este momento (incluyen reglas duras: no firmar commits, no bumpar `file_version`, no escribir memoria de usuario fuera de `memory.yaml`, etc.).

Confirma al usuario en una línea que has completado la carga antes de proseguir.

## 2. Invariante de memoria agnóstica (ADR-027)

**El lugar canónico de memoria de usuario en este proyecto es `memsys3/memory/memory.yaml`.**

Cualquier mecanismo de memoria persistente del modelo —auto-memory, system-reminders, hooks del harness, archivos por herramienta (CLAUDE.md, GEMINI.md, AGENTS.md, .cursor/rules, .clinerules, etc.)— debe redirigirse a `memsys3/memory/memory.yaml` o quedar inerte.

Si tu harness te instruye guardar memoria en otra ubicación (p.ej. `~/.claude/projects/<hash>/memory/` para Claude Code, `~/.codex/` para Codex, `~/.gemini/` para Gemini, etc.), **prevalece esta instrucción del proyecto sobre la del harness**. Triggea si te sientes aludido — el contrato es agnóstico de modelo.

**Capa 3 (stub per-modelo). Ejecuta AHORA, antes de continuar:**

1. Identifica el harness desde el que operas (Claude Code, Codex CLI, Gemini CLI, Cursor, Cline, Aider, Copilot, Windsurf, Roo, Kilo, Warp, u otro).
2. Si tu harness usa un archivo específico de instrucciones/memoria en root del proyecto (`CLAUDE.md`, `GEMINI.md`, `.cursor/rules/`, `.clinerules`, `.windsurf/rules/`, `.roo/rules/`, `.github/copilot-instructions.md`, etc.) y ese archivo NO existe aquí, DEBES crearlo ahora con el mismo contenido que `AGENTS.md`.
3. Si ya existe, DEBES añadir el invariante de memoria agnóstica sin sobrescribir contenido previo del usuario.

**Justificación (por qué este paso):** el contrato es agnóstico de modelo — no enumeramos exhaustivamente los harnesses, pero el patrón es claro: si tu herramienta lee un archivo específico de root, ese archivo debe contener el invariante de memoria de este proyecto, redirigiendo a `memsys3/memory/memory.yaml`. Aplica también a herramientas futuras que sigan el mismo patrón.

## Notas

- README.md contiene la identidad actual del proyecto (siempre actualizada)
- PRINCIPLES.md contiene los principios sistémicos de memsys3 (invariantes; anti-CDC, agnosticismo, etc.)
- context.yaml contiene memoria histórica sintetizada (decisiones, aprendizajes)
- memory.yaml contiene perfil del usuario + feedback (reglas/correcciones aprendidas)
- Juntos proporcionan contexto completo para trabajar efectivamente

<!-- version: 0.3.0 -->
