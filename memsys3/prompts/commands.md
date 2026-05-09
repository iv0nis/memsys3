# Instalar Comandos Globales de memsys3

> **⚠️ OPCIONAL - Solo Claude Code**
>
> Este prompt es **ESPECÍFICO de Claude Code**. Si usas otro modelo de IA (Gemini, Codex, etc.), puedes **IGNORAR completamente** este archivo.
>
> Los prompts en `memsys3/prompts/` funcionan universalmente en cualquier modelo. Los comandos locales son un workaround opcional para usuarios de Claude Code con .gitignore.

---

**Tu tarea:** Configurar comandos globales de memsys3 en este sistema para que el usuario pueda ejecutarlos desde cualquier proyecto.

## ¿Qué son los comandos globales?

Comandos que funcionan desde **cualquier proyecto** sin necesidad de tener memsys3 desplegado localmente:

- **`/deploy-memsys3`** — Desplegar memsys3 en proyecto nuevo. Crea scaffold canónico (ADR-023): agents, prompts, templates, memory/full vacíos, backlog, `PRINCIPLES.md` (ADR-022), bridge `MEMORY.md` opcional para Claude Code (ADR-020), `.gitignore` con consulta interactiva.
- **`/actualizar-memsys3`** — Actualizar memsys3 en proyecto desplegado. Sustitución diferencial de templates schema (ADR-018, Paso 6.4) + deprecation contextualizada (ADR-019, Paso 6.4.5) + sincronización `PRINCIPLES.md` (Paso 6.6) + preservación de archivos custom del usuario.

Se instalan en `~/.claude/commands/` y Claude Code los reconoce automáticamente.

---

## Paso 1: Verificar y preparar directorio

```bash
# Crear directorio si no existe
mkdir -p "$HOME/.claude/commands"

# Verificar que funciona
ls -lh "$HOME/.claude/commands/" 2>/dev/null || echo "Directorio creado correctamente"
```

---

## Paso 2: Detectar comandos existentes

Lista de comandos que se van a instalar:

1. **deploy-memsys3.md** - Deployment inicial de memsys3
2. **actualizar-memsys3.md** - Actualización de memsys3 existente

Verifica si ya existen:

```bash
echo "Comandos actuales en ~/.claude/commands/:"
ls -1 "$HOME/.claude/commands/" | grep -E "deploy-memsys3|actualizar-memsys3" || echo "  (ninguno instalado)"
```

**Si alguno ya existe:**
- Pregunta al usuario: **"¿Quieres sobrescribir los comandos existentes? (sí/no)"**
- Si responde "no" → DETENTE, no instales nada
- Si responde "sí" → Continúa al Paso 3

**Si ninguno existe:**
- Continúa al Paso 3 directamente

---

## Paso 3: Crear comandos globales

### 3.1 Crear /deploy-memsys3

```bash
cat > "$HOME/.claude/commands/deploy-memsys3.md" <<'EOF'
---
description: Deploy memsys3 system from GitHub to current project
---

# Deploy memsys3

**AHORA ACTÚAS COMO MAIN AGENT desplegando memsys3 en este proyecto por primera vez**

Ejecuta los siguientes pasos:

## 1. Clonar repositorio temporalmente

```bash
git clone https://github.com/iv0nis/memsys3 memsys3_temp
```

## 2. Cargar prompt de deployment del repositorio clonado

Ejecuta: `@memsys3_temp/memsys3_templates/prompts/deploy.md`

El prompt cubre el deployment completo:
- Scaffold canónico (ADR-023): agents, prompts, templates, memory/full vacíos, backlog scaffold
- Propagación de `PRINCIPLES.md` (ADR-022)
- Bridge `MEMORY.md` opcional para usuarios Claude Code (ADR-020)
- Configuración `.gitignore` con AskUserQuestion (incluir/excluir memsys3/)
- Briefing del proyecto (nombre, stack, fase, idioma) y personalización de project-status.yaml
- Verificación del inventario canónico post-deploy

## 3. Limpieza temporal (EJECUTAR AL TERMINAR deployment)

```bash
rm -rf memsys3_temp
```

---

**Nota:** Este comando descarga la última versión de memsys3 y ejecuta el prompt de deployment, garantizando que siempre uses las instrucciones más actuales.
EOF

echo "✅ /deploy-memsys3 creado"
```

### 3.2 Crear /actualizar-memsys3

```bash
cat > "$HOME/.claude/commands/actualizar-memsys3.md" <<'EOF'
---
description: Update memsys3 system from GitHub in existing project
---

# Actualizar memsys3

**AHORA ACTÚAS COMO MAIN AGENT actualizando memsys3 en este proyecto**

Ejecuta los siguientes pasos:

## 1. Clonar repositorio temporalmente

```bash
git clone https://github.com/iv0nis/memsys3 memsys3_update_temp
```

## 2. Cargar prompt de actualización del repositorio clonado

Ejecuta: `@memsys3_update_temp/memsys3_templates/prompts/actualizar.md`

El prompt cubre actualización segura completa:
- Detección de estructura antigua incompatible (PASO 0)
- Backups automáticos antes de tocar nada
- **Sustitución diferencial de templates schema** (Paso 6.4, ADR-018): compara `file_version` upstream vs destino, sustituye condicionalmente
- **Detección de campos deprecated y huérfanos** (Paso 6.4.5, ADR-019, modo Extendido)
- **Sincronización `PRINCIPLES.md`** vía sustitución diferencial (Paso 6.6, ADR-022)
- **Preservación de archivos custom** del usuario (no sobrescribe sus edits, ISSUE-018)
- Bumping de `file_version` solo aquí (regla dura, ADR-017)
- Validaciones finales: archivos existen, schemas íntegros, hooks operativos

## 3. Limpieza temporal (EJECUTAR AL TERMINAR actualización)

```bash
rm -rf memsys3_update_temp
```

---

**Nota:** Este comando descarga la última versión de memsys3 y ejecuta el prompt de actualización, garantizando que siempre uses las instrucciones más actuales.
EOF

echo "✅ /actualizar-memsys3 creado"
```

---

## Paso 4: Verificar instalación

```bash
echo ""
echo "📋 Comandos globales instalados:"
ls -lh "$HOME/.claude/commands/" | grep -E "deploy-memsys3|actualizar-memsys3"

echo ""
echo "✅ Instalación completada"
echo ""
echo "Comandos disponibles desde cualquier proyecto:"
echo "  /deploy-memsys3      - Desplegar memsys3 en proyecto nuevo"
echo "  /actualizar-memsys3  - Actualizar memsys3 existente"
```

---

## Troubleshooting

### "mkdir: permission denied"
**Causa:** Sin permisos de escritura en `~/.claude/commands/`

**Solución alternativa (instalación manual):**
1. Copia el contenido de los comandos (Paso 3.1 y 3.2)
2. Crea los archivos manualmente:
   - `~/.claude/commands/deploy-memsys3.md`
   - `~/.claude/commands/actualizar-memsys3.md`
3. Pega el contenido en cada archivo

### "Comando no aparece en Claude Code"
**Causa:** Claude Code puede necesitar reinicio

**Solución:**
1. Cierra y vuelve a abrir Claude Code
2. Verifica que los archivos existen: `ls ~/.claude/commands/`

### "No quiero usar comandos globales"
**Alternativa:** Puedes usar los prompts directamente:
- Deployment: Clonar repo y ejecutar `@memsys3_temp/memsys3_templates/prompts/deploy.md`
- Actualización: Clonar repo y ejecutar `@memsys3_update_temp/memsys3_templates/prompts/actualizar.md`

---

**Instalación completada.** Los comandos globales están listos para usar en cualquier proyecto.
<!-- version: 0.1.0 -->
