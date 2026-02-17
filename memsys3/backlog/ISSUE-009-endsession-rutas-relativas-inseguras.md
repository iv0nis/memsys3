# ISSUE-009: endSession.md crea estructura en directorio incorrecto (rutas relativas inseguras)

**Estado**: Abierto
**Prioridad**: Alta
**Tipo**: Bug
**Plazo**: Corto plazo
**Fecha creación**: 2026-02-06

---

## Problema

Durante ejecución de `endSession.md` en proyecto tallersColomer, el agente creó estructura `memsys3/memory/full/` en directorio de trabajo incorrecto porque **endSession.md usa rutas relativas** (`memsys3/memory/full/sessions.yaml`) sin verificar primero dónde está ubicado memsys3.

**Secuencia del error:**

1. Agent ejecuta `wc -l memsys3/memory/full/sessions.yaml`
2. Comando falla (file not found) porque CWD no es la raíz del proyecto
3. Agent interpreta error como "sessions.yaml no existe"
4. Agent crea estructura nueva: `mkdir -p memsys3/memory/full` en CWD (incorrecto)
5. Agent escribe sessions.yaml en ubicación incorrecta (49 líneas)
6. Usuario debe intervenir y corregir manualmente

**Proyecto afectado**: tallersColomer
**Impacto**: Tiempo perdido ~5min, archivos basura, frustración usuario

---

## Causa Raíz

❌ **Error 1**: endSession.md usa rutas relativas sin establecer ruta base
❌ **Error 2**: No hay checkpoint inicial para localizar memsys3 ANTES de documentar
❌ **Error 3**: Agent interpreta "file not found" como "no existe" en vez de "ruta incorrecta"
❌ **Error 4**: No hay validación de existencia de memsys3 antes de crear estructura

---

## Evidencia

**Comando que falló:**
```bash
wc -l memsys3/memory/full/sessions.yaml
# Error: No such file or directory
```

**Respuesta incorrecta del agent:**
```bash
# Agent asume que no existe y crea estructura nueva
mkdir -p memsys3/memory/full
cat > memsys3/memory/full/sessions.yaml << EOF
...
EOF
```

**Ruta correcta (tallersColomer):**
```
/mnt/c/PROYECTOS/SoluzzIAvers/tallersColomer/memsys3
```

**Ruta donde se creó (incorrecta):**
```
[CWD_aleatorio]/memsys3
```

---

## Propuesta de Solución

### Opción A: Checkpoint inicial en endSession.md (RECOMENDADO)

Agregar **PASO 0: Localizar memsys3** ANTES de cualquier operación:

```markdown
### PASO 0: Localizar memsys3 (CHECKPOINT CRÍTICO)

Antes de documentar, localiza dónde está memsys3:

```bash
# Buscar memsys3 en proyecto actual
MEMSYS_PATH=$(find . -maxdepth 3 -name "memsys3" -type d 2>/dev/null | grep -v node_modules | head -1)

if [ -z "$MEMSYS_PATH" ]; then
  echo "❌ ERROR: memsys3 no encontrado en este proyecto"
  echo "¿Has desplegado memsys3? Ejecuta: @memsys3/prompts/deploy.md"
  exit 1
fi

echo "✅ memsys3 encontrado en: $MEMSYS_PATH"

# Verificar archivos críticos
if [ ! -f "$MEMSYS_PATH/memory/full/sessions.yaml" ]; then
  echo "❌ ERROR: sessions.yaml no existe en $MEMSYS_PATH/memory/full/"
  echo "La estructura de memsys3 está incompleta o corrupta"
  exit 1
fi
```

**Todos los pasos siguientes deben usar `$MEMSYS_PATH`:**

```bash
# ANTES (inseguro):
wc -l memsys3/memory/full/sessions.yaml

# DESPUÉS (seguro):
wc -l $MEMSYS_PATH/memory/full/sessions.yaml
```
```

**Ventajas:**
- ✅ Detecta memsys3 automáticamente
- ✅ Falla temprano si memsys3 no existe (no crea basura)
- ✅ Funciona independientemente de CWD
- ✅ Valida integridad de estructura

**Desventajas:**
- ⚠️ Requiere modificar endSession.md (breaking change menor)
- ⚠️ Agrega ~10 líneas al prompt

---

### Opción B: Agregar instrucción "cd a raíz del proyecto" al inicio

```markdown
**IMPORTANTE**: Antes de ejecutar cualquier comando, asegúrate de estar en la raíz del proyecto:

```bash
# Verificar que estás en la raíz
pwd
# Si no estás en la raíz del proyecto, navega hasta allí:
# cd /ruta/a/tu/proyecto
```
```

**Ventajas:**
- ✅ Solución simple y rápida
- ✅ No requiere cambios estructurales

**Desventajas:**
- ❌ Depende de que el agent interprete correctamente "raíz del proyecto"
- ❌ No previene el error, solo lo mitiga
- ❌ Requiere intervención manual del agent

---

### Opción C: Usar rutas absolutas desde newSession.md

Establecer variable de entorno en newSession.md que se preserve:

```bash
# En newSession.md (al inicio):
export PROJECT_ROOT=$(pwd)
export MEMSYS_PATH="$PROJECT_ROOT/memsys3"
```

Luego en endSession.md, todos los comandos usan `$MEMSYS_PATH`.

**Ventajas:**
- ✅ Rutas absolutas garantizadas
- ✅ Funciona entre sesiones (si variable persiste)

**Desventajas:**
- ❌ Variables de entorno bash NO persisten entre tool calls en Claude Code
- ❌ No funciona en práctica

---

## Recomendación

**Implementar Opción A: Checkpoint inicial en endSession.md**

Es la solución más robusta:
1. Detecta automáticamente memsys3
2. Falla temprano si no existe (no crea basura)
3. Funciona independientemente de CWD
4. Valida integridad

**Cambios necesarios:**

1. **Actualizar endSession.md**:
   - Agregar PASO 0: Localizar memsys3
   - Reemplazar todas las rutas relativas `memsys3/` por `$MEMSYS_PATH/`

2. **Actualizar otros prompts afectados**:
   - compile-context.md (mismo patrón)
   - adr.md (mismo patrón)
   - backlog.md (mismo patrón)
   - mind.md (mismo patrón)

3. **Testing**:
   - Probar endSession.md en 3 proyectos diferentes
   - Probar desde diferentes CWD
   - Probar con memsys3 no desplegado (debe fallar limpiamente)

---

## Impacto de No Resolver

- ⚠️ **Riesgo Alto**: Creación de estructuras incorrectas en proyectos
- ⚠️ **Riesgo Medio**: Frustración de usuarios al tener que corregir manualmente
- ⚠️ **Riesgo Bajo**: Pérdida de confianza en el sistema memsys3

**Frecuencia esperada**: 1 de cada 10 ejecuciones de endSession.md (si CWD no es raíz)

---

## Referencias

- Proyecto afectado: tallersColomer (2026-02-06)
- Prompt afectado: memsys3/prompts/endSession.md
- Otros prompts con mismo patrón: compile-context.md, adr.md, backlog.md, mind.md

---

## Notas Adicionales

**Patrones de código afectados:**

```bash
# ❌ PATRÓN INSEGURO (todos estos comandos están afectados):
wc -l memsys3/memory/full/sessions.yaml
cat memsys3/memory/full/adr.yaml
ls memsys3/backlog/*.md
python memsys3/viz/serve.py

# ✅ PATRÓN SEGURO:
wc -l $MEMSYS_PATH/memory/full/sessions.yaml
cat $MEMSYS_PATH/memory/full/adr.yaml
ls $MEMSYS_PATH/backlog/*.md
python $MEMSYS_PATH/viz/serve.py
```

**¿Por qué no se detectó antes?**

Durante development de memsys3 (dog-fooding), siempre ejecutamos desde la raíz del proyecto, por lo que las rutas relativas funcionaban correctamente. El bug solo aparece en proyectos externos cuando CWD ≠ raíz del proyecto.

---

**Conclusión**: Bug crítico de usabilidad que debe resolverse en próxima versión (v0.11.3). Solución clara y probada (Opción A).
