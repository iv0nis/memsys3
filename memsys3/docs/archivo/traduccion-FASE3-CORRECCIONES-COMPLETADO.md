# Correcciones FASE 3 - Valores Descriptivos en Catalán

## ⚠️ HALLAZGOS DE AUDITORÍA

La FASE 3 tradujo correctamente los **keys YAML**, **código JS** y **CSS**, pero **NO tradujo los valores descriptivos** dentro de los archivos YAML.

**Errores encontrados:** ~101 instancias de catalán residual

---

## 📊 Resumen de Errores

| Archivo | Líneas con catalán | Criticidad |
|---|---|---|
| `memsys3/memory/full/adr.yaml` | ~45 | 🚨 ALTA |
| `memsys3/memory/full/sessions.yaml` | ~30 | 🚨 ALTA |
| `memsys3/memory/templates/context-template.yaml` | ~10 | 🔴 ALTA |
| `memsys3/memory/templates/project-status-template.yaml` | ~5 | 🔴 ALTA |
| `memsys3/memory/context.yaml` | 3 | 🟡 MEDIA |
| `memsys3/memory/project-status.yaml` | 2 | 🟡 MEDIA |
| `memsys3/prompts/endSession.md` | 2 | 🟡 MEDIA |
| `memsys3/prompts/deploy.md` | 1 | 🟡 MEDIA |

**Total:** 8 archivos × 2 (memsys3/ + memsys3_templates/) = **16 archivos a corregir**

---

## 🎯 Palabras Catalanas a Traducir

### Grupo A: Palabras con acento
```
automàtica     → automática
automàticament → automáticamente
rotació        → rotación
intel·ligent   → inteligente
línies         → líneas
únics          → únicos
àrees          → áreas
específic      → específico
màxim          → máximo
```

### Grupo B: Palabras comunes
```
Pla            → Plan
però           → pero
això           → esto
només          → solo
fa             → hace
Fa             → Hace
Fins i tot     → Incluso
Neteja         → Limpieza
criteri        → criterio
arxivament     → archivado
irrellevants   → irrelevantes
massa          → demasiados/muchos
basant-se      → basándose
```

---

## 📝 Instrucciones de Corrección

### PASO 1: Corregir Archivos YAML (Valores Descriptivos)

**Método:** Usar Edit tool con find & replace en cada archivo.

#### 1.1 - `memsys3/memory/context.yaml` (3 instancias)

Leer archivo completo y traducir:

- **Línea 279**: `"Sistema de rotació automàtica >1800 línies"` → `"Sistema de rotación automática >1800 líneas"`
- **Línea 301**: `"Validar rotació automàtica en projecte real"` → `"Validar rotación automática en proyecto real"`
- **Línea 388**: `"Aquest fitxer és COMPILAT automàticament, no editar manualment"` → `"Este archivo es COMPILADO automáticamente, no editar manualmente"`

#### 1.2 - `memsys3/memory/project-status.yaml` (2 instancias)

- **Línea 73**: `"Validar rotació automàtica en projecte real"` → `"Validar rotación automática en proyecto real"`
- **Línea 77**: `"Validar Pla Contingència (>150K tokens)"` → `"Validar Plan Contingencia (>150K tokens)"`

#### 1.3 - `memsys3/memory/full/adr.yaml` (~45 instancias) 🚨 CRÍTICO

**Estrategia:** Leer archivo completo, usar Edit tool con múltiples reemplazos.

**Ejemplos de errores encontrados:**
```yaml
# Línea 186
titulo: "Criteri intel·ligent del Context Agent vs límits arbitraris"
# Debe ser:
titulo: "Criterio inteligente del Context Agent vs límites arbitrarios"

# Línea 197
El Context Agent usa criteri intel·ligent basant-se en la pregunta:
# Debe ser:
El Context Agent usa criterio inteligente basándose en la pregunta:

# Línea 233
titulo: "Rotació automàtica de sessions/ADRs (>1800 línies)"
# Debe ser:
titulo: "Rotación automática de sessions/ADRs (>1800 líneas)"

# Línea 244-245
- endSession.md detecta automàticament
- Fa rotació segura: copia → verifica → crea nou
# Debe ser:
- endSession.md detecta automáticamente
- Hace rotación segura: copia → verifica → crea nuevo

# Línea 279
titulo: "Pla de Contingència amb arxivament intel·ligent (>150K tokens)"
# Debe ser:
titulo: "Plan de Contingencia con archivado inteligente (>150K tokens)"

# Línea 285
Fins i tot amb rotació, projectes molt grans poden acumular massa dades.
# Debe ser:
Incluso con rotación, proyectos muy grandes pueden acumular demasiados datos.

# Línea 291
CA identifica ADRs/sessions irrellevants amb criteri intel·ligent
# Debe ser:
CA identifica ADRs/sessions irrelevantes con criterio inteligente

# Línea 301
Neteja automàtica
# Debe ser:
Limpieza automática

# Línea 399
per_que_descartada: "Prompt amb agent és més intel·ligent i flexible"
# Debe ser:
per_que_descartada: "Prompt con agent es más inteligente y flexible"

# Línea 411
- "Deployment guiat i intel·ligent"
# Debe ser:
- "Deployment guiado e inteligente"
```

**Palabras a reemplazar en adr.yaml:**
- `automàtica` → `automática`
- `automàticament` → `automáticamente`
- `rotació` → `rotación`
- `intel·ligent` → `inteligente`
- `línies` → `líneas`
- `Pla` → `Plan`
- `Fa ` → `Hace `
- `fa ` → `hace `
- `Fins i tot` → `Incluso`
- `massa` → `demasiados` o `muchos` (contextual)
- `irrellevants` → `irrelevantes`
- `criteri` → `criterio`
- `arxivament` → `archivado`
- `basant-se` → `basándose`
- `però` → `pero`
- `això` → `esto`
- `només` → `solo`
- `amb` → `con`
- `guiat i` → `guiado e`
- `més` → `más`
- `projectes` → `proyectos`
- `grans` → `grandes`
- `poden` → `pueden`
- `nou` → `nuevo`

#### 1.4 - `memsys3/memory/full/sessions.yaml` (~30 instancias) 🚨 CRÍTICO

**Estrategia:** Similar a adr.yaml, leer completo y aplicar mismas palabras.

Usar las mismas traducciones del Grupo A y B mencionadas arriba.

#### 1.5 - `memsys3/memory/templates/context-template.yaml` (~10 instancias)

Leer y traducir valores descriptivos usando las mismas palabras.

#### 1.6 - `memsys3/memory/templates/project-status-template.yaml` (~5 instancias)

Leer y traducir valores descriptivos usando las mismas palabras.

---

### PASO 2: Corregir Prompts (Field Names Incorrectos)

#### 2.1 - `memsys3/prompts/endSession.md`

**Corrección 1 - Línea 69:**
```markdown
# ANTES:
- Incluir: `tipus`, `problema`, `solucio`, `criticitat` (alta|mitjana|baixa)

# DESPUÉS:
- Incluir: `tipus`, `problema`, `solucio`, `criticitat` (alta|media|baja)
```

**Corrección 2 - Línea 98:**
```markdown
# ANTES:
- `pendents_prioritaris`: Actualizar según próximos pasos

# DESPUÉS:
- `pendientes_prioritarios`: Actualizar según próximos pasos
```

#### 2.2 - `memsys3/prompts/deploy.md`

**Corrección - Línea 143:**
```yaml
# ANTES:
pendents_prioritaris:

# DESPUÉS:
pendientes_prioritarios:
```

---

### PASO 3: Sincronizar Templates

Una vez corregidos los 8 archivos en `memsys3/`, copiar a `memsys3_templates/`:

```bash
# YAML
cp memsys3/memory/context.yaml memsys3_templates/memory/context.yaml
cp memsys3/memory/project-status.yaml memsys3_templates/memory/project-status.yaml
cp memsys3/memory/full/sessions.yaml memsys3_templates/memory/full/sessions.yaml
cp memsys3/memory/full/adr.yaml memsys3_templates/memory/full/adr.yaml
cp memsys3/memory/templates/context-template.yaml memsys3_templates/memory/templates/context-template.yaml
cp memsys3/memory/templates/project-status-template.yaml memsys3_templates/memory/templates/project-status-template.yaml

# Prompts
cp memsys3/prompts/endSession.md memsys3_templates/prompts/endSession.md
cp memsys3/prompts/deploy.md memsys3_templates/prompts/deploy.md
```

---

## ✅ Verificación Final

Después de las correcciones, ejecutar:

```bash
# Verificar 0 resultados para catalán técnico
grep -r "automàtica\|rotació\|Pla\|intel·ligent\|línies\|Fins i tot\|Neteja\|però\|això\|només\|mitjana\|baixa\|pendents_prioritaris" \
  memsys3/ memsys3_templates/ \
  --include="*.yaml" --include="*.md" \
  --exclude-dir=".git" --exclude-dir="docs"

# Debe devolver 0 resultados (excepto docs/YAML_FIELDS_NO_TRADUCIR.md)
```

**Si devuelve 0 resultados:** ✅ FASE 3 COMPLETADA

---

## 📋 Checklist de Ejecución

### Archivos YAML (valores descriptivos)

**memsys3/**
- [ ] `memory/context.yaml` (3 líneas)
- [ ] `memory/project-status.yaml` (2 líneas)
- [ ] `memory/full/adr.yaml` (~45 líneas) 🚨
- [ ] `memory/full/sessions.yaml` (~30 líneas) 🚨
- [ ] `memory/templates/context-template.yaml` (~10 líneas)
- [ ] `memory/templates/project-status-template.yaml` (~5 líneas)

### Prompts (field names)

**memsys3/**
- [ ] `prompts/endSession.md` (2 correcciones)
- [ ] `prompts/deploy.md` (1 corrección)

### Sincronización

**memsys3_templates/**
- [ ] Copiar 6 archivos YAML corregidos
- [ ] Copiar 2 archivos .md corregidos

### Verificación

- [ ] Ejecutar grep de verificación (0 resultados)
- [ ] Probar visualizador (`cd memsys3/viz && python3 serve.py`)
- [ ] Verificar que no hay errores en consola del navegador

---

## 🎯 Resultado Esperado

Después de estas correcciones:

✅ **Keys YAML:** 100% español (ya completado)
✅ **Valores YAML:** 100% español (correcciones aplicadas)
✅ **Código JS/CSS:** 100% español (ya completado)
✅ **Prompts:** 100% español (correcciones aplicadas)

**Sistema memsys3 completamente en español sin ningún residuo catalán visual.**

---

## ⏱️ Tiempo Estimado

- **Corrección archivos YAML:** 1.5-2 horas (por volumen de texto)
- **Corrección prompts:** 10 minutos
- **Sincronización:** 5 minutos
- **Verificación:** 10 minutos

**Total:** ~2-2.5 horas

---

## 🚨 Notas Críticas

1. **NO traducir en docs/**: El archivo `docs/YAML_FIELDS_NO_TRADUCIR.md` es documental, debe mantener ejemplos catalanes.

2. **Contexto importa**: Algunas palabras como `massa` pueden ser "demasiados" o "muchos" según contexto.

3. **Preservar formato YAML**: Mantener indentación, estructura, comentarios `#`.

4. **Commit strategy**: Hacer commits incrementales:
   - Commit 1: Corregir archivos YAML en memsys3/
   - Commit 2: Corregir prompts en memsys3/
   - Commit 3: Sincronizar templates
   - Commit 4: Verificación final

5. **Testing obligatorio**: Después de cada archivo YAML grande (adr.yaml, sessions.yaml), verificar que no se rompió la sintaxis YAML:
   ```bash
   python3 -c "import yaml; yaml.safe_load(open('memsys3/memory/full/adr.yaml'))"
   ```
