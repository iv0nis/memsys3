# Comprobar Alineamiento - Dog-fooding ↔ Templates

**CONTEXTO:** Este prompt es ESPECÍFICO del proyecto memsys3 (desarrollo del sistema).

**OBJETIVO:** Verificar sincronización bidireccional entre:
- `memsys3/` (instancia dog-fooding, desarrollo interno)
- `memsys3_templates/` (producto final distribuible)

---

## ¿Por qué es necesario?

Durante el desarrollo de memsys3, pueden ocurrir **desincronizaciones**:

### Escenario A: Mejoras en dog-fooding NO aplicadas a producción
```
memsys3/ → [MEJORA IMPLEMENTADA] ✅
memsys3_templates/ → [DESACTUALIZADO] ❌
```

**Ejemplo real:**
- Main Agent implementa mejora en `memsys3/prompts/compile-context.md`
- Olvida actualizar `memsys3_templates/prompts/compile-context.md`
- **Resultado:** Próximo deployment usa versión antigua sin la mejora

### Escenario B: Templates actualizados NO sincronizados a dog-fooding
```
memsys3_templates/ → [ACTUALIZADO] ✅
memsys3/ → [DESACTUALIZADO] ❌
```

**Ejemplo real:**
- Se actualiza `memsys3_templates/agents/context-agent.yaml`
- `memsys3/agents/context-agent.yaml` queda con versión antigua
- **Resultado:** Dog-fooding usa código desactualizado, testing incorrecto

---

## Workflow de Verificación

### PASO 1: Verificar Estructura de Directorios

```bash
# Verificar que ambos directorios existen
ls -la memsys3/ | head -10
ls -la memsys3_templates/ | head -10
```

Ambos deben tener estructura similar:
- `prompts/`
- `memory/templates/`
- `agents/`
- `viz/`

### PASO 2: Identificar Archivos Agnósticos

**Archivos que DEBEN estar sincronizados** (distribuibles):

**Prompts (8 archivos):**
- `prompts/newSession.md`
- `prompts/endSession.md`
- `prompts/compile-context.md`
- `prompts/deploy.md`
- `prompts/actualizar.md`
- `prompts/mind.md`
- `prompts/backlog.md`
- `prompts/github.md`

**Templates YAML (4 archivos):**
- `memory/templates/project-status-template.yaml`
- `memory/templates/sessions-template.yaml`
- `memory/templates/adr-template.yaml`
- `memory/templates/context-template.yaml`

**Agents (2 archivos):**
- `agents/main-agent.yaml`
- `agents/context-agent.yaml`

**Visualizador (4 archivos):**
- `viz/index.html`
- `viz/viewer.js`
- `viz/styles.css`
- `viz/serve.py`

**Documentación sistema (2 archivos):**
- `memory/README.md`
- `viz/README.md`

**Total:** 20 archivos agnósticos distribuibles

### PASO 3: Comparar Archivos (Diff Completo)

Para CADA archivo agnóstico, ejecuta diff:

```bash
# Ejemplo para compile-context.md
diff memsys3/prompts/compile-context.md memsys3_templates/prompts/compile-context.md

# Si hay diferencias, mostrará output
# Si NO hay diferencias, no mostrará nada (silent)
```

**Automatizar verificación de todos los archivos:**

```bash
echo "=== VERIFICANDO ALINEAMIENTO memsys3/ ↔ memsys3_templates/ ==="
echo ""

# Prompts
for file in newSession.md endSession.md compile-context.md deploy.md actualizar.md mind.md backlog.md github.md; do
  echo "Comparando prompts/$file..."
  diff memsys3/prompts/$file memsys3_templates/prompts/$file > /dev/null 2>&1
  if [ $? -eq 0 ]; then
    echo "✅ prompts/$file - SINCRONIZADO"
  else
    echo "❌ prompts/$file - DESINCRONIZADO"
  fi
done

echo ""

# Templates YAML
for file in project-status-template.yaml sessions-template.yaml adr-template.yaml context-template.yaml; do
  echo "Comparando memory/templates/$file..."
  diff memsys3/memory/templates/$file memsys3_templates/memory/templates/$file > /dev/null 2>&1
  if [ $? -eq 0 ]; then
    echo "✅ memory/templates/$file - SINCRONIZADO"
  else
    echo "❌ memory/templates/$file - DESINCRONIZADO"
  fi
done

echo ""

# Agents
for file in main-agent.yaml context-agent.yaml; do
  echo "Comparando agents/$file..."
  diff memsys3/agents/$file memsys3_templates/agents/$file > /dev/null 2>&1
  if [ $? -eq 0 ]; then
    echo "✅ agents/$file - SINCRONIZADO"
  else
    echo "❌ agents/$file - DESINCRONIZADO"
  fi
done

echo ""

# Visualizador
for file in index.html viewer.js styles.css serve.py README.md; do
  echo "Comparando viz/$file..."
  diff memsys3/viz/$file memsys3_templates/viz/$file > /dev/null 2>&1
  if [ $? -eq 0 ]; then
    echo "✅ viz/$file - SINCRONIZADO"
  else
    echo "❌ viz/$file - DESINCRONIZADO"
  fi
done

echo ""

# Documentación
echo "Comparando memory/README.md..."
diff memsys3/memory/README.md memsys3_templates/memory/README.md > /dev/null 2>&1
if [ $? -eq 0 ]; then
  echo "✅ memory/README.md - SINCRONIZADO"
else
  echo "❌ memory/README.md - DESINCRONIZADO"
fi

echo ""
echo "=== VERIFICACIÓN COMPLETADA ==="
```

### PASO 4: Analizar Diferencias (Archivos Desincronizados)

Para cada archivo marcado como ❌ DESINCRONIZADO:

```bash
# Ver diferencias específicas
diff memsys3/prompts/[ARCHIVO] memsys3_templates/prompts/[ARCHIVO]
```

**Determinar dirección correcta de sincronización:**

1. **Lee ambas versiones completas** (usa Read tool)
2. **Compara fechas de modificación:**
   ```bash
   ls -l memsys3/prompts/[ARCHIVO]
   ls -l memsys3_templates/prompts/[ARCHIVO]
   ```
3. **Analiza el contexto:**
   - ¿La mejora es lógica del sistema? → Debe estar en templates
   - ¿Cuál versión es más completa/reciente?
   - ¿Hay commits recientes que documenten cambios?

### PASO 5: Sincronizar (Según Dirección Correcta)

**Opción A: Dog-fooding → Templates** (mejora implementada en memsys3 debe ir a producción)

```bash
# Copiar de memsys3/ a memsys3_templates/
cp memsys3/[RUTA_ARCHIVO] memsys3_templates/[RUTA_ARCHIVO]

# Ejemplo:
cp memsys3/prompts/compile-context.md memsys3_templates/prompts/compile-context.md
```

**Opción B: Templates → Dog-fooding** (templates tiene versión más actualizada)

```bash
# Copiar de memsys3_templates/ a memsys3/
cp memsys3_templates/[RUTA_ARCHIVO] memsys3/[RUTA_ARCHIVO]

# Ejemplo:
cp memsys3_templates/agents/context-agent.yaml memsys3/agents/context-agent.yaml
```

### PASO 6: Re-verificar Alineamiento

Después de sincronizar, ejecuta de nuevo el script del PASO 3 para confirmar:

```bash
# Ejecutar de nuevo el script de verificación completo
# Todos los archivos deben mostrar ✅ SINCRONIZADO
```

### PASO 7: Documentar en sessions.yaml

Documenta la sincronización realizada:

```yaml
- id: "YYYY-MM-DD-alineamiento-memsys3-templates"
  data: "[FECHA_HOY]"
  duracion: "~30min"
  titulo: "Verificación y sincronización dog-fooding ↔ templates"

  que_es_va_fer:
    - "Ejecutado prompts/comprobar_alineamiento.md"
    - "Detectados [X] archivos desincronizados"
    - "[LISTA_ARCHIVOS_SINCRONIZADOS]"

  problemas_resueltos:
    - "[EXPLICAR_DESINCRONIZACIÓN_DETECTADA]"

  decisiones_tomadas:
    - "Dirección de sincronización: [memsys3 → templates / templates → memsys3]"
    - "Justificación: [MOTIVO]"

  proximos_pasos:
    - "Ejecutar comprobar_alineamiento.md periódicamente (cada 2-3 sesiones)"
```

### PASO 8: Commit (Opcional)

Si hiciste sincronizaciones:

```bash
# Si sincronizaste memsys3/ → memsys3_templates/
git add memsys3_templates/
git commit -m "sync: actualizar templates desde dog-fooding

Archivos sincronizados:
- [LISTA_ARCHIVOS]

Mejoras aplicadas a producción."

# Si sincronizaste memsys3_templates/ → memsys3/
git add memsys3/
git commit -m "sync: actualizar dog-fooding desde templates

Archivos sincronizados:
- [LISTA_ARCHIVOS]

Dog-fooding actualizado con versión producción."
```

---

## Archivos ESPECÍFICOS (NO sincronizar)

Estos archivos son únicos del desarrollo de memsys3 y **NO deben sincronizarse**:

**En `/prompts/` (raíz):**
- ❌ `prompts/comprobar_alineamiento.md` (este archivo)
- ❌ `prompts/actualizar_cat.md` (sincronización versión catalana)

**En `memsys3/` (dog-fooding):**
- ❌ `memsys3/memory/full/*.yaml` (sessions, adr del desarrollo memsys3)
- ❌ `memsys3/memory/project-status.yaml` (estado del proyecto memsys3)
- ❌ `memsys3/memory/context.yaml` (contexto compilado memsys3)
- ❌ `memsys3/memory/history/*` (archivos archivados)
- ❌ `memsys3/backlog/*` (backlog del desarrollo memsys3)

**En raíz:**
- ❌ `README.md` (documentación del repositorio)
- ❌ `docs/DEVELOPMENT.md` (guía desarrollo memsys3)
- ❌ `docs/UPDATE.md` (guía actualización memsys3)
- ❌ `.gitignore`, `.git/`, etc.

---

## Frecuencia Recomendada

**Ejecutar este prompt:**
- ✅ Al finalizar cada sesión de desarrollo (antes de endSession)
- ✅ Antes de hacer deployment a nuevo proyecto
- ✅ Después de implementar features significativas
- ✅ Cada 2-3 sesiones como mínimo

**Prevención > Corrección**

Es mejor detectar desincronizaciones temprano que descubrirlas después de deployment.

---

## Troubleshooting

### "Todos los archivos desincronizados"

**Causa probable:** Ejecutaste el script desde directorio incorrecto.

**Solución:**
```bash
# Asegúrate de estar en /mnt/c/PROYECTOS/memsys3
pwd
# Debe mostrar: /mnt/c/PROYECTOS/memsys3
```

### "Archivo existe en memsys3/ pero NO en memsys3_templates/"

**Causa:** Archivo nuevo creado solo en dog-fooding.

**Acción:**
1. Verifica si es agnóstico (debe distribuirse) o específico (solo dog-fooding)
2. Si es agnóstico → copiarlo a templates
3. Si es específico → documentar en ADR separación archivos

### "Diferencias solo en comentarios/whitespace"

**Acción:** Sincronizar igualmente para mantener consistencia perfecta.

---

## Resumen

Este prompt garantiza que:
- ✅ `memsys3_templates/` siempre tiene las mejoras más recientes
- ✅ `memsys3/` usa versión actualizada para testing correcto
- ✅ Deployments futuros usan código más reciente
- ✅ NO hay pérdida de mejoras implementadas
- ✅ Sistema de producción refleja estado real del desarrollo

**Alineamiento = Calidad del producto distribuible**
