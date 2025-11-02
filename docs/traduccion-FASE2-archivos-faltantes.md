# Traducción FASE 2 - Archivos Faltantes

## Contexto

Durante la FASE 1 se tradujeron 18 archivos YAML y agents. Sin embargo, **faltaron 14 archivos** con contenido significativo en catalán que NO estaban en el checklist original.

## Objetivo

Traducir TODOS los archivos .md, .py, .html, .js que contienen catalán.

---

## Instrucciones

**REGLAS:**

1. **Documentación (.md):**
   - Traducir TODO el contenido en catalán → español
   - Preservar bloques de código (bash, yaml, etc.) sin cambios
   - Preservar rutas, comandos, nombres técnicos

2. **Código (.py, .js, .html):**
   - Traducir SOLO comentarios y docstrings
   - Traducir strings de UI/mensajes de usuario
   - NO traducir nombres de variables, funciones, clases
   - NO traducir atributos HTML técnicos (lang="ca" puede cambiarse a lang="es")

3. **Verificación:**
   - Mantener formato original (Markdown, sintaxis de código)
   - Verificar que no se rompe funcionalidad
   - Tachar items completados: `- [x] ~~archivo~~`

---

## Archivos Pendientes (14 archivos)

### Fase 2A: Documentación (.md) - 8 archivos

**Prioridad ALTA - Documentación de usuario:**

- [ ] `memsys3/viz/README.md` (85 líneas, ~95% catalán)
  - **Traducir:** TODO el contenido excepto bloques de código
  - **Preservar:** Comandos bash, nombres de archivos

- [ ] `memsys3/memory/README.md` (297 líneas, ~98% catalán)
  - **Traducir:** TODO el contenido excepto bloques de código
  - **Preservar:** Comandos bash, nombres de archivos, ejemplos YAML

- [ ] `memsys3/prompts/deploy.md` (232 líneas, ~85% catalán)
  - **Traducir:** TODO el texto de instrucciones
  - **Preservar:** Bloques de código bash, YAML, nombres técnicos

- [ ] `memsys3/prompts/mind.md` (38 líneas, ~90% catalán)
  - **Traducir:** TODO el texto de instrucciones
  - **Preservar:** Comandos bash

**Templates distribuibles (copias):**

- [ ] `memsys3_templates/viz/README.md`
  - **Acción:** Copiar desde `memsys3/viz/README.md` ya traducido

- [ ] `memsys3_templates/memory/README.md`
  - **Acción:** Copiar desde `memsys3/memory/README.md` ya traducido

- [ ] `memsys3_templates/prompts/deploy.md`
  - **Acción:** Copiar desde `memsys3/prompts/deploy.md` ya traducido

- [ ] `memsys3_templates/prompts/mind.md`
  - **Acción:** Copiar desde `memsys3/prompts/mind.md` ya traducido

### Fase 2B: Código (.py, .html, .js) - 6 archivos

**Código Python:**

- [ ] `memsys3/viz/serve.py` (39 líneas, ~20% catalán en comentarios)
  - **Traducir:**
    - Línea 3: docstring "Minimal HTTP server per visualitzar..." → "Servidor HTTP mínimo para visualizar..."
    - Línea 4: "Ús: python serve.py" → "Uso: python serve.py"
    - Línea 22: comentario "Servir des del directori..." → "Servir desde el directorio..."
    - Línea 32: comentario "Auto-obre navegador" → "Auto-abre navegador"
  - **NO traducir:** Nombres de variables, funciones, imports

- [ ] `memsys3_templates/viz/serve.py`
  - **Acción:** Copiar desde `memsys3/viz/serve.py` ya traducido

**HTML:**

- [ ] `memsys3/viz/index.html` (150 líneas, ~15% catalán en UI)
  - **Traducir:**
    - Línea 2: `lang="ca"` → `lang="es"`
    - Líneas 37-40: "Context Compilat", "Aquest és el context...", "Màxim ~2500-3000 tokens..." → español
    - Líneas 54, 59, 64, 69: "ADRs Rellevants", "Última Sessió", "Gotchas Crítics", "Pendents Prioritaris" → español
    - Líneas 78-79: "Històric Complet", "Tot l'històric..." → español
    - Líneas 84, 89: "Totes les ADRs", "Sessions Històriques" → español
    - Líneas 122-130: Labels "Total ADRs", "ADRs Filtrades", "Última Compilació" → español
    - Línea 139: "Notes de Compilació" → español
  - **NO traducir:** Clases CSS, IDs, nombres de funciones JS

- [ ] `memsys3_templates/viz/index.html`
  - **Acción:** Copiar desde `memsys3/viz/index.html` ya traducido

**JavaScript:**

- [ ] `memsys3/viz/viewer.js` (338 líneas, ~5% catalán en comentarios)
  - **Traducir:**
    - Línea 1: comentario "Memory Visualizer - Carrega i renderitza YAMLs" → "Carga y renderiza YAMLs"
    - Línea 3: comentario "Utilitzem js-yaml..." → "Utilizamos js-yaml..."
    - Línea 259: comentario "Helper per renderitzar..." → "Helper para renderizar..."
  - **NO traducir:** Nombres de funciones, variables, referencias a campos YAML (ultima_sessio, notes_compilacio, etc.)

- [ ] `memsys3_templates/viz/viewer.js`
  - **Acción:** Copiar desde `memsys3/viz/viewer.js` ya traducido

**Progreso:** 0/14 archivos (0%)

---

## Orden Recomendado de Ejecución

**PASO 1:** Traducir originales en `memsys3/` (7 archivos únicos)
1. memsys3/viz/README.md
2. memsys3/memory/README.md
3. memsys3/prompts/deploy.md
4. memsys3/prompts/mind.md
5. memsys3/viz/serve.py
6. memsys3/viz/index.html
7. memsys3/viz/viewer.js

**PASO 2:** Copiar a `memsys3_templates/` (7 archivos)
```bash
# Después de traducir cada archivo, copiarlo:
cp memsys3/viz/README.md memsys3_templates/viz/README.md
cp memsys3/memory/README.md memsys3_templates/memory/README.md
cp memsys3/prompts/deploy.md memsys3_templates/prompts/deploy.md
cp memsys3/prompts/mind.md memsys3_templates/prompts/mind.md
cp memsys3/viz/serve.py memsys3_templates/viz/serve.py
cp memsys3/viz/index.html memsys3_templates/viz/index.html
cp memsys3/viz/viewer.js memsys3_templates/viz/viewer.js
```

---

## Verificación Final

Cuando termines todos los archivos:

1. **Buscar catalán residual:**
   ```bash
   grep -r "això\|només\|també\|però" memsys3/ --include="*.md" --include="*.py" --include="*.html" --include="*.js"
   ```

2. **Verificar funcionalidad:**
   - Probar visualizador: `cd memsys3/viz && python3 serve.py`
   - Verificar que carga correctamente

3. **Archivar este documento:**
   ```bash
   mv docs/traduccion-FASE2-archivos-faltantes.md docs/archivo/traduccion-FASE2-COMPLETADO.md
   ```

---

## Notas Importantes

**Por qué faltaron estos archivos:**
- El checklist FASE 1 solo buscó archivos YAML con catalán
- NO se incluyeron archivos .md, .py, .html, .js en la búsqueda inicial
- Esto es un complemento para completar la traducción al 100%

**Impacto si no se traducen:**
- Documentación de usuario en catalán (README.md)
- Prompts de instrucciones en catalán (deploy.md, mind.md)
- UI del visualizador en catalán (index.html)
- Comentarios de código en catalán (serve.py, viewer.js)

**Resultado esperado:**
- 100% del proyecto memsys3 en español
- Documentación, prompts, UI y comentarios consistentes
- Sistema profesional y accesible
