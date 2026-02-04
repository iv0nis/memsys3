# Actualización de memsys3

> Guía para actualizar memsys3 en proyectos que ya lo tienen desplegado

## 🚀 Método Recomendado: Prompt actualizar.md

**La forma más segura de actualizar memsys3 es usar el prompt dedicado:**

```bash
@memsys3/prompts/actualizar.md
```

Este prompt:
- ✅ Detecta automáticamente tu versión actual de memsys3
- ✅ Identifica estructura antigua incompatible (PASO 0 crítico)
- ✅ Crea backups automáticos antes de tocar datos
- ✅ Actualiza solo archivos safe (viz/, templates/, prompts/, agents/)
- ✅ Preserva tus datos (adr.yaml, sessions.yaml, project-status.yaml)
- ✅ Valida la actualización al finalizar

**Si prefieres actualización manual**, continúa con esta guía.

---

## Contexto

Esta guía es para cuando hay **cambios/mejoras en memsys3_templates/** y quieres aplicarlos a tu proyecto que ya tiene memsys3 desplegado.

**IMPORTANTE:** NO sobreescribas archivos con datos específicos de tu proyecto.

## Tipos de Actualización

### 1. Actualización de Sistema (Safe)

Archivos que puedes actualizar sin perder datos:

**Visualizador (viz/):**
```bash
cp -r memsys3/memsys3_templates/viz/* tu-proyecto/memsys3/viz/
```

**Documentación del sistema:**
```bash
cp memsys3/memsys3_templates/memory/README.md tu-proyecto/memsys3/memory/README.md
```

### 2. Actualización de Templates (Safe)

Templates base que no contienen datos específicos:

```bash
cp memsys3/memsys3_templates/memory/templates/*.yaml tu-proyecto/memsys3/memory/templates/
```

### 3. Actualización de Prompts (⚠️ Cuidado)

Los prompts pueden estar personalizados en tu proyecto. Opciones:

**Opción A: Comparar y Merge Manual**
```bash
# Ver diferencias
diff memsys3/memsys3_templates/prompts/compile-context.md tu-proyecto/memsys3/prompts/compile-context.md

# Aplicar cambios manualmente si tiene sentido
```

**Opción B: Sobrescribir (si no has personalizado)**
```bash
cp memsys3/memsys3_templates/prompts/*.md tu-proyecto/memsys3/prompts/
```

### 4. Actualización de Agents (⚠️ Cuidado)

Los agents pueden estar personalizados. Revisa antes de sobrescribir:

```bash
# Ver diferencias
diff memsys3/memsys3_templates/agents/main-agent.yaml tu-proyecto/memsys3/agents/main-agent.yaml

# Aplicar cambios manualmente si tiene sentido
```

## Archivos que NUNCA Debes Sobrescribir

Estos contienen datos específicos de tu proyecto:

- ❌ `memory/context.yaml` (contexto compilado)
- ❌ `memory/project-status.yaml` (estado de tu proyecto)
- ❌ `memory/full/adr.yaml` (tus decisiones)
- ❌ `memory/full/sessions.yaml` (tu historial)
- ❌ `memory/history/*` (archivos archivados)

## Workflow Recomendado

### Paso 1: Backup

```bash
# Crea backup de tu carpeta memsys3 antes de actualizar
cp -r tu-proyecto/memsys3 tu-proyecto/memsys3_backup_$(date +%Y%m%d)
```

### Paso 2: Actualizar Archivos Safe

```bash
cd tu-proyecto

# Visualizador
cp -r path/to/memsys3/memsys3_templates/viz/* memsys3/viz/

# Templates
cp path/to/memsys3/memsys3_templates/memory/templates/*.yaml memsys3/memory/templates/

# Documentación
cp path/to/memsys3/memsys3_templates/memory/README.md memsys3/memory/README.md
```

### Paso 3: Revisar Cambios en Prompts/Agents

```bash
# Ver qué ha cambiado
diff -r path/to/memsys3/memsys3_templates/prompts memsys3/prompts
diff -r path/to/memsys3/memsys3_templates/agents memsys3/agents
```

### Paso 4: Aplicar Cambios Manualmente

Si hay mejoras en prompts/agents que quieres:
- Abre ambos archivos lado a lado
- Copia las mejoras manualmente
- Preserva tus personalizaciones

### Paso 5: Verificar

```bash
# Verifica que el visualizador funciona
cd memsys3/memory
python3 serve.py

# Verifica que puedes compilar contexto
# Con tu AI agent: @memsys3/prompts/compile-context.md
```

## Casos Específicos

### Nuevo Feature en Context Agent

Si hay cambios en `prompts/compile-context.md`:

1. Revisa el changelog de memsys3
2. Compara tu versión con la nueva
3. Aplica cambios manualmente si quieres el nuevo feature
4. Prueba compilando: `@memsys3/prompts/compile-context.md`

### Nueva Funcionalidad en Visualizador

Actualización directa (safe):

```bash
cp -r memsys3/memsys3_templates/viz/* tu-proyecto/memsys3/viz/
```

### Cambios en Templates YAML

Actualización directa (safe):

```bash
cp memsys3/memsys3_templates/memory/templates/*.yaml tu-proyecto/memsys3/memory/templates/
```

## Troubleshooting

### "El visualizador no carga después de actualizar"

```bash
# Verifica permisos
chmod +x memsys3/viz/serve.py

# Verifica paths en viewer.js
# Deben apuntar a tus archivos correctos
```

### "El Context Agent se comporta diferente"

- Revisa cambios en `prompts/compile-context.md`
- Compara con tu versión anterior
- Puede haber nuevas instrucciones o lógica

### "Perdí datos después de actualizar"

- Restaura desde backup: `cp -r memsys3_backup_YYYYMMDD memsys3`
- NUNCA sobrescribas `memory/full/`, `memory/context.yaml`, `memory/project-status.yaml`

## Checklist de Actualización

- [ ] Backup de `memsys3/` completo
- [ ] Actualizar visualizador (`viz/`)
- [ ] Actualizar templates (`memory/templates/`)
- [ ] Actualizar documentación (`memory/README.md`)
- [ ] Revisar diff de prompts
- [ ] Revisar diff de agents
- [ ] Aplicar cambios manualmente en prompts/agents si aplica
- [ ] Verificar visualizador funciona
- [ ] Verificar compilación de contexto funciona
- [ ] Eliminar backup si todo OK

## Notas Importantes

- **memsys3_templates/** es la fuente de verdad para templates
- Tu carpeta **memsys3/** contiene datos específicos de tu proyecto
- Actualiza regularmente para obtener nuevas features y mejoras
- Siempre haz backup antes de actualizar
- Documenta en tus ADRs si personalizas prompts/agents significativamente

---

**¿Dudas?** Consulta el [README principal](../README.md) o abre un issue en GitHub.
