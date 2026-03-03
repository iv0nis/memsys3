# Deployment y Actualización

## Instalación inicial (proyecto nuevo)

```bash
@memsys3/prompts/deploy.md
```

**Pasos que ejecuta el agente:**
1. Clona memsys3 temporalmente desde GitHub
2. Copia la estructura a `memsys3/` en tu proyecto
3. Briefing con el usuario (nombre, stack, fase, URLs, convenciones)
4. Personaliza `project-status.yaml` y `newSession.md`
5. Consulta `.gitignore` (ver Privacidad)
6. Limpia el clone temporal

**Resultado:** memsys3 funcional y personalizado en tu proyecto.

## Actualización (proyecto existente)

```bash
@memsys3/prompts/actualizar.md
```

**PASO 0 crítico — detección de estructura:**
- Solo `/memory` (estructura antigua pre-ADR-006) → migración automática
- `/memory` + `/memsys3` coexistiendo → migración con backups
- `/memsys3` correcto → proceder normalmente

Hace backups automáticos antes de tocar datos y preserva el histórico completo.

## Privacidad (.gitignore)

Durante el deployment, el agente pregunta si excluir `memsys3/` de git:

**Opción A — Excluir (recomendado):** contexto local privado. Sesiones, decisiones y gotchas no se suben al repo.
⚠️ Con esta opción, los `@mentions` de Claude Code no funcionan — usar instrucciones directas ("Ejecuta memsys3/prompts/newSession.md").

**Opción B — Incluir:** para equipos que quieran compartir contexto entre desarrolladores.

## Primeros pasos tras instalar

```bash
# 1. Compila el contexto inicial
@memsys3/prompts/compile-context.md

# 2. Inicia tu primera sesión
@memsys3/prompts/newSession.md
```
