# Traducción Catalán → Español - memsys3

## Objetivo
Traducir archivos con contenido en catalán al español para consistencia del proyecto.

## Instrucciones

**PASO 0 - Preparación (solo primera vez):**
- Lee `@docs/YAML_FIELDS_NO_TRADUCIR.md` para conocer qué NO traducir

**PASO 1 - Por cada archivo NO tachado:**
1. Lee el archivo completo
2. Traduce SOLO:
   - ✅ Comentarios YAML (`# ...`)
   - ✅ Valores descriptivos (el texto DESPUÉS de `:` en campos como descripcio, objectiu, problema, etc.)
   - ✅ Instrucciones en templates
3. NO traduzcas:
   - ❌ Nombres de campos YAML (keys antes de `:`)
   - ❌ Estados técnicos (operatiu, alta, mitjana, etc.)
   - ❌ Rutas, comandos, placeholders
4. Verifica sintaxis YAML
5. Guarda el archivo
6. Tacha el item: `- [x] ~~archivo~~`

**PASO 2 - Al terminar todos:**
- Mueve este archivo a `docs/archivo/traduccion-catalan-espanol-COMPLETADO.md`

**Regla de oro:** Si dudas, NO traduzcas. Consulta `YAML_FIELDS_NO_TRADUCIR.md`.

---

## Archivos Pendientes

### Fase 1: Archivos Originales (memsys3/)

**Memoria:**
- [x] ~~`memsys3/memory/context.yaml` - Solo comentarios~~
- [x] ~~`memsys3/memory/project-status.yaml` - Solo comentarios~~
- [x] ~~`memsys3/memory/full/sessions.yaml` - Solo comentarios encabezado~~
- [x] ~~`memsys3/memory/full/adr.yaml` - Solo comentarios encabezado~~

**Templates:**
- [x] ~~`memsys3/memory/templates/context-template.yaml` - Comentarios + instrucciones~~
- [x] ~~`memsys3/memory/templates/sessions-template.yaml` - Comentarios + instrucciones~~
- [x] ~~`memsys3/memory/templates/adr-template.yaml` - Comentarios + instrucciones~~
- [x] ~~`memsys3/memory/templates/project-status-template.yaml` - Comentarios + instrucciones~~

**Agents:**
- [x] ~~`memsys3/agents/context-agent.yaml` - Valores descripcio, objectiu, instrucciones~~
- [x] ~~`memsys3/agents/main-agent.yaml` - Valor descripcio~~

### Fase 2: Templates Distribuibles (memsys3_templates/)

**Copiar archivos ya traducidos:**
- [x] ~~`memsys3_templates/memory/templates/context-template.yaml`~~
- [x] ~~`memsys3_templates/memory/templates/sessions-template.yaml`~~
- [x] ~~`memsys3_templates/memory/templates/adr-template.yaml`~~
- [x] ~~`memsys3_templates/memory/templates/project-status-template.yaml`~~
- [x] ~~`memsys3_templates/agents/context-agent.yaml`~~
- [x] ~~`memsys3_templates/memory/context.yaml`~~

**Traducir comentarios:**
- [x] ~~`memsys3_templates/memory/full/adr.yaml` - Comentarios encabezado~~
- [x] ~~`memsys3_templates/memory/full/sessions.yaml` - Comentarios encabezado~~

**Progreso:** 18/18 archivos (100%) ✅ COMPLETADO

---

## Ejemplo de Traducción Correcta

```yaml
# ANTES (catalán):
# Aquest és el fitxer que carrega DevAI
descripcio: "Agent que compila context complet amb criteri intel·ligent"

# DESPUÉS (español):
# Este es el archivo que carga DevAI
descripcio: "Agente que compila contexto completo con criterio inteligente"
#            ↑ KEY (descripcio) NO cambia
#                   ↑ VALUE sí se traduce
```

## Verificación Final

Cuando termines todos los archivos:

1. Ejecutar `@memsys3/prompts/compile-context.md` para validar
2. Verificar que no hay errores de sintaxis YAML
3. Archivar este documento:
   ```bash
   mv docs/traduccion-catalan-espanol.md docs/archivo/traduccion-catalan-espanol-COMPLETADO.md
   ```
