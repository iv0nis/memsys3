# Actualizar Versión Catalana - Sincronización memsys3 → memsys3_CAT

⚠️ **EJECUTAR DESDE:** `/mnt/c/PROYECTOS/memsys3` (repositorio español)

Este prompt sincroniza los cambios de templates desde el repo español al repo catalán que está en un directorio completamente separado.

## Objetivo

Sincronizar cambios desde `/mnt/c/PROYECTOS/memsys3/memsys3_templates/` (versión española) hacia `/mnt/c/PROYECTOS/memsys3_CAT/memsys3_templates/` (versión catalana), traduciendo al catalán todos los archivos distribuibles.

## Contexto

**IMPORTANTE - Rutas Absolutas:**

- **Repositorio principal (español - ORIGEN):**
  - Ruta: `/mnt/c/PROYECTOS/memsys3`
  - Branch: `master`
  - Directorio templates: `/mnt/c/PROYECTOS/memsys3/memsys3_templates/`

- **Repositorio catalán (català - DESTINO):**
  - Ruta: `/mnt/c/PROYECTOS/memsys3_CAT`
  - Branch: `catalan`
  - Directorio templates: `/mnt/c/PROYECTOS/memsys3_CAT/memsys3_templates/`

- **Ambos apuntan al mismo repo GitHub** con branches diferentes:
  - `master` → versión español
  - `catalan` → versión catalán

- **Solo se traducen templates** (`memsys3_templates/`), NO el dog-fooding

## Workflow de Sincronización

### PASO 1: Verificar Directorios

Verifica que ambos directorios existen y están limpios:

```bash
# Verificar memsys3 (español - origen)
cd /mnt/c/PROYECTOS/memsys3
git status
echo "Branch actual:"
git branch --show-current

# Verificar memsys3_CAT (catalán - destino)
cd /mnt/c/PROYECTOS/memsys3_CAT
git status
echo "Branch actual:"
git branch --show-current
```

Ambos deben estar en working tree limpio. Si hay cambios pendientes, pregunta al usuario qué hacer.

### PASO 2: Obtener Última Versión de Master

```bash
cd /mnt/c/PROYECTOS/memsys3
git pull origin master
```

### PASO 3: Identificar Cambios en Templates

Compara los archivos que han cambiado desde el último sync:

```bash
cd /mnt/c/PROYECTOS/memsys3
git log --oneline --since="2 weeks ago" -- memsys3_templates/
```

Muestra al usuario qué commits afectan a templates.

### PASO 4: Copiar Archivos de Templates (Español)

Copia toda la estructura de `memsys3_templates/` al directorio catalán:

```bash
# Desde memsys3 (origen)
cd /mnt/c/PROYECTOS/memsys3

# Copiar a memsys3_CAT (destino)
cp -r memsys3_templates/* /mnt/c/PROYECTOS/memsys3_CAT/memsys3_templates/
```

### PASO 5: Traducir Archivos al Catalán

Ahora debes traducir TODOS los archivos copiados de español a catalán.

**IMPORTANTE:** Traduce TODO el contenido (textos, comentarios, instrucciones), pero mantén:
- Nombres de archivos (NO traducir)
- Nombres de keys YAML (NO traducir)
- Rutas y paths (NO traducir)
- Código (variables, funciones)

#### Archivos a Traducir (por orden de prioridad):

**1. Prompts (9 archivos):**
- `prompts/newSession.md`
- `prompts/endSession.md`
- `prompts/compile-context.md`
- `prompts/deploy.md`
- `prompts/actualizar.md`
- `prompts/mind.md`
- `prompts/backlog.md`
- `prompts/github.md`
- `prompts/actualizar_cat.md` (este mismo archivo, ¡irónico!)

**2. Templates YAML (4 archivos):**
- `memory/templates/project-status-template.yaml`
- `memory/templates/sessions-template.yaml`
- `memory/templates/adr-template.yaml`
- `memory/templates/context-template.yaml`

**3. Agents (2 archivos):**
- `agents/main-agent.yaml`
- `agents/context-agent.yaml`

**4. Visualizador (3 archivos):**
- `viz/index.html`
- `viz/viewer.js`
- `viz/README.md`

**5. READMEs (1 archivo):**
- `memory/README.md`

**NO traducir:**
- `README.md` (templates root) - se crea en proyecto destino
- `memory/full/*.yaml` - ejemplos vacíos
- `memory/project-status.yaml` - se crea en proyecto destino
- `memory/context.yaml` - se crea en proyecto destino

#### Estrategia de Traducción

Para CADA archivo:

1. Lee el archivo en español
2. Traduce al catalán manteniendo:
   - Estructura YAML/Markdown intacta
   - Keys YAML sin traducir (ej: `metadata:`, `ultima_actualizacion:`)
   - Rutas sin traducir (ej: `memsys3/memory/context.yaml`)
   - Nombres de archivos sin traducir
3. Usa Edit tool para reemplazar contenido español → catalán

**Tabla de Traducciones Comunes:**

| Español | Català |
|---------|--------|
| Agente | Agent |
| Sesión | Sessió |
| Decisión | Decisió |
| Descripción | Descripció |
| Último/a | Últim/a |
| Actualizado | Actualitzat |
| Compilado | Compilat |
| Siguiente | Següent |
| Estado | Estat |
| Título | Títol |
| Motivo | Motiu |
| Impacto | Impacte |
| Duración | Durada |
| Objetivo | Objectiu |
| Participantes | Participants |
| Implementadas | Implementades |
| Resueltos | Resolts |
| Decisiones | Decisions |
| Tecnologías | Tecnologies |
| Agregadas | Afegides |
| Próximos pasos | Propers passos |
| Notas adicionales | Notes addicionals |
| Documentados | Documentats |
| Criticidad | Criticitat |
| Solución | Solució |
| Justificación | Justificació |
| Operativo | Operatiu |
| Desarrollo | Desenvolupament |
| Pendiente | Pendent |
| Aceptado | Acceptat |
| Obsoleto | Deprecat |
| Alta/Media/Baja | Alta/Mitjana/Baixa |
| Actualización | Actualització |
| Lenguaje | Llenguatge |
| Sesiones recientes | Sessions recents |
| Última sesión | Última sessió |
| Incluidas | Incloses |
| Totales | Totals |
| Extraídos | Extrets |
| Criterios | Criteris |
| Filtrado | Filtratge |
| Archivamiento | Arxivament |
| Líneas | Línies |
| Observaciones | Observacions |
| Iniciales | Inicials |
| Finales | Finals |
| Sintetizados | Sintetitzats |
| Pendientes prioritarios | Pendents prioritaris |
| Rotación automática | Rotació automàtica |
| Escalabilidad | Escalabilitat |
| Histórico | Històric |
| Mantenimiento | Manteniment |
| Depende | Depèn |
| Archivar | Arxivar |
| Ilimitado | Il·limitat |
| Irrelevante | Irrellevant |
| Incluye | Inclou |
| Cualquier/Cualquiera | Qualsevol |
| Qué | Què |
| Listo | Llest |
| Usado | Usat |

### PASO 6: Verificar Traducción

Después de traducir, verifica que:
- Keys YAML NO se tradujeron
- Rutas mantienen formato original
- Estructura de archivos intacta
- NO hay mezcla español/catalán

```bash
cd /mnt/c/PROYECTOS/memsys3_CAT

# Verificar que NO hay palabras españolas residuales
grep -r "sesión\|descripción\|decisión" memsys3_templates/ --include="*.yaml" --include="*.md" || echo "✅ Sin español residual"
```

### PASO 7: Commit y Push a Branch Catalan

```bash
cd /mnt/c/PROYECTOS/memsys3_CAT

# Verificar branch
git branch --show-current  # Debe ser 'catalan'

# Si no está en catalan, cambiar
git checkout catalan

# Añadir cambios
git add memsys3_templates/

# Ver qué se va a commitear
git status

# Commit
git commit -m "sync: actualitzar templates des de master (versió espanyola)

Sincronitzats canvis de memsys3_templates/ des de la branca master.
Tots els arxius traduïts al català.

Arxius actualitzats:
- prompts/*.md
- memory/templates/*.yaml
- agents/*.yaml
- viz/*

Generated with Claude Code
https://claude.com/claude-code

Co-Authored-By: Claude <noreply@anthropic.com>"

# Push a branch catalan
git push origin catalan
```

### PASO 8: Verificar en GitHub

Confirma que los cambios se subieron correctamente:

```bash
cd /mnt/c/PROYECTOS/memsys3_CAT
git log --oneline -3
```

Informa al usuario:
- Commit ID creado
- Archivos sincronizados y traducidos
- Branch actualizada (catalan)
- URL de GitHub para verificar

## Notas Importantes

1. **NO tocar dog-fooding:** Solo sincronizas `memsys3_templates/`, NO `memsys3/memory/full/` ni otras carpetas de desarrollo.

2. **Keys YAML permanecen en español:**
   - ✅ `ultima_actualizacion:` (NO traducir key)
   - ✅ `"2025-11-13"` (valor, traducir si es texto)

3. **Rutas NO se traducen:**
   - ✅ `memsys3/memory/context.yaml` (siempre igual)
   - ✅ `@memsys3/prompts/newSession.md` (siempre igual)

4. **Contenido SÍ se traduce:**
   - Instrucciones en prompts
   - Comentarios en YAML
   - Textos de interfaz (HTML)
   - Mensajes de usuario

5. **Este prompt (actualizar_cat.md) también debe traducirse** cuando esté en `memsys3_templates/` catalán.

## Troubleshooting

**"Branch catalan no existe en memsys3_CAT":**
```bash
cd /mnt/c/PROYECTOS/memsys3_CAT
git checkout -b catalan
git push -u origin catalan
```

**"Hay conflictos de merge":**
- Revisar qué archivos tienen conflicto
- Resolver manualmente priorizando versión catalana más reciente
- Volver a traducir si es necesario

**"Keys YAML se tradujeron accidentalmente":**
- Revertir cambios: `git checkout -- memsys3_templates/`
- Volver a PASO 4 con más cuidado

## Verificación Final

Antes de terminar, confirma con el usuario:
- ✅ Archivos sincronizados desde master
- ✅ TODO traducido al catalán (contenido)
- ✅ Keys YAML y rutas sin traducir
- ✅ Commit y push a branch `catalan` exitoso
- ✅ Sin español residual en templates

---

**Sincronización completada. memsys3_CAT branch `catalan` actualizada.**
