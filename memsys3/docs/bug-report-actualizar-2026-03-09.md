# Bug Report — actualizar.md (2026-03-09)

**Detectado en:** proyecto real ejecutando actualización v0.12.0 → v0.18.0
**Severidad:** Media

---

## BUG-1: `memsys3_update_temp` no se elimina al finalizar

**Descripción:**
El Paso 8 ejecuta `rm -rf memsys3_update_temp` con ruta relativa. Si el working directory del agente cambió durante la sesión (ej: por un `cd` en el Paso 3), el comando falla silenciosamente y el directorio queda huérfano en la raíz del proyecto.

**Reproducción:**
```bash
cd memsys3_update_temp   # Paso 3 — cambia el cwd
# ... pasos intermedios ...
rm -rf memsys3_update_temp  # Paso 8 — falla sin error visible
# → memsys3_update_temp/ sigue en la raíz del proyecto
```

**Fix sugerido:**
Usar ruta absoluta resuelta al inicio del proceso:
```bash
PROJECT_ROOT=$(pwd)
# ... al final (Paso 8):
rm -rf "$PROJECT_ROOT/memsys3_update_temp"
```
O evitar `cd` en el Paso 3 usando `git -C memsys3_update_temp` (ya se hace en el Paso 6.1).

---

## BUG-2: Backup antiguo en raíz se mezcla al mover a `backups/`

**Descripción:**
Si existe un backup antiguo en la raíz (`memsys3_backup_YYYYMMDD_HHMMSS/`) y se intenta mover a `memsys3/docs/backups/`, el comando `mv` mezcla el contenido dentro del directorio destino en lugar de crear un subdirectorio nombrado — porque el destino ya existe.

**Reproducción:**
```bash
# memsys3/docs/backups/ ya existe con contenido
mv memsys3_backup_20260224_201214 memsys3/docs/backups/
# → memsys3/docs/backups/agents/
# → memsys3/docs/backups/memory/
# → memsys3/docs/backups/prompts/  (mezclado, sin nombre identificable)
```

**Impacto:** Pérdida de trazabilidad del backup. Contenido mezclado con otros backups.

**Fix sugerido:**
Especificar el nombre destino explícitamente en el bloque de migración del Paso 5:
```bash
for old_backup in memsys3_backup_*/; do
  [ -d "$old_backup" ] && mv "$old_backup" "memsys3/docs/backups/$old_backup" && echo "Migrado: $old_backup"
done
```

---

## BUG-3 (menor): Artefacto `memsys3_templates/` no detectado ni limpiado

**Descripción:**
Un directorio `memsys3_templates/` estaba presente en la raíz del proyecto como artefacto de una ejecución anterior (probablemente del deployment inicial). El prompt no incluye verificación de artefactos huérfanos al inicio, lo que puede causar confusión o conflictos con el clone nuevo.

**Fix sugerido:**
Añadir al Paso 0a una limpieza preventiva:
```bash
# Limpiar artefactos de ejecuciones anteriores
rm -rf memsys3_update_temp memsys3_templates 2>/dev/null
echo "Artefactos previos limpiados"
```

---

## Contexto

- OS: Linux (WSL2 sobre Windows)
- Shell: bash
- Working directory: `/mnt/c/PROYECTOS/soluzzia`
- BUG-1 y BUG-3 probablemente se reproducen en cualquier entorno donde el agente ejecute `cd` durante el proceso
