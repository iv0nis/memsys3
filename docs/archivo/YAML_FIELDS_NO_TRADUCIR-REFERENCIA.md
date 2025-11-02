# Campos YAML - NO TRADUCIR

**CRÍTICO:** Esta es la lista de referencia para traducciones catalán → español.

**Regla general:** Los NOMBRES DE CAMPOS YAML (keys) NO se traducen. Solo se traducen VALORES de contenido descriptivo (values).

---

## TIER 1 - NUNCA TRADUCIR (Estructura del sistema)

### Contenedores principales
```yaml
metadata
features
adrs
sessions
stack
stack_tecnologic
urls
gotchas
pendents
pendents_prioritaris
decisions_clau
historic_sessions
sessions_recents
visio_general
estat_actual
convencions_codi
comandos_utils
```

### Subcampos de metadata
```yaml
compilat_per
ultima_compilacio
ultima_actualitzacio
actualitzat_per
versio_context
fase
```

### Subcampos de sesiones
```yaml
features_implementades
problemes_resolts
decisions_preses
tecnologies_afegides
deployments
proxims_passos
notes_addicionals
gotchas_documentats
archivos_criticos_modificados
highlights
highlights_sintetitzats
```

### Subcampos de compilación
```yaml
notes_compilacio
adrs_totals
adrs_incloses
adrs_filtrades  # OJO: usar adrs_incloses (estandarizado)
sessions_totals
sessions_incloses
gotchas_extrets
tokens_inicials
tokens_finals
arxivament
criteris_filtratge
linies_totals
justificacio_adrs
justificacio_sessions
justificacio_gotchas
observacions
```

### Subcampos de ADRs
```yaml
alternatives
consequencies
positives
negatives
pros
contras
per_que_descartada
```

### Subcampos técnicos
```yaml
inputs
inputs.obligatoris
inputs.opcionals
output
limits
instruccions
regles
exemples
responsabilitats
restriccions
path
base_template
estructura
maxim
linies_per_adr
total_caracters
criteris_seleccio
pas_1_llegir
pas_2_extreure
pas_N_*
obligatories
qualitat
com_executar
frequencia
ordre
concisio
adr_links
consistencia
bo
massa_detallat
massa_vague
gotchas_bons
gotchas_dolents
```

### Stack y tecnología
```yaml
frontend
backend
database
deploy
llenguatge_docs
framework
runtime
auth
ci_cd
platform
env_vars
styling
patrons
llibreries_clau
us
```

### URLs y referencias
```yaml
repository
production
staging
produccio  # Considerar: es catalán pero es nombre de campo
url
servei
adr_relacionada
sessio
nota
```

---

## VALORES FIJOS - NUNCA TRADUCIR

### Estados (estat)
```yaml
operatiu
desenvolupament
pendent
deprecated
accepted
superseded_by
```

### Áreas (area)
```yaml
arquitectura
frontend
backend
process
infraestructura
documentació
escalabilitat
format
usabilitat
workflow
```

### Criticidad (criticitat)
```yaml
alta
mitjana
baixa
```

### Tipos (tipus)
```yaml
warning
error
gotcha
issue
SPA
SSR
MPA
```

### Roles (rol)
```yaml
Development Agent
Context Agent
Main-Agent
```

---

## TIER 2 - SÍ TRADUCIR (Solo valores, no keys)

Estos son CAMPOS (keys) que NO se traducen, pero sus VALORES (values) SÍ:

### Contenido descriptivo
```yaml
nom: "Sistema de gestió..."  # KEY no traducir, VALUE sí
descripcio: "Agent que compila..."  # KEY no traducir, VALUE sí
objectiu: "Optimitzar consum..."  # KEY no traducir, VALUE sí
context: "Durant el desenvolupament..."  # KEY no traducir, VALUE sí
decisio: "TODAS las rutas..."  # KEY no traducir, VALUE sí
problema: "Confusión sobre rutas..."  # KEY no traducir, VALUE sí
solucio: "Sistemáticamente actualizado..."  # KEY no traducir, VALUE sí
motiu: "Durante el desarrollo..."  # KEY no traducir, VALUE sí
impacte: "Claridad total..."  # KEY no traducir, VALUE sí
titol: "Limpieza Completa..."  # KEY no traducir, VALUE sí
detall: "Ejecutar deployment..."  # KEY no traducir, VALUE sí
tasca: "Probar deployment..."  # KEY no traducir, VALUE sí
justificacio: "Contienen info crítica..."  # KEY no traducir, VALUE sí
cambio: "Rutas con memsys3/"  # KEY no traducir, VALUE sí
ruta: "memsys3/agents/..."  # KEY no traducir, VALUE puede ser path técnico
que_es: "Sistema de gestió..."  # KEY no traducir, VALUE sí
client: "Open Source..."  # KEY no traducir, VALUE sí
ultima_feature: "Sistema preparado..."  # KEY no traducir, VALUE sí
seguent_milestone: "Testing deployment..."  # KEY no traducir, VALUE sí
```

### Metadatos temporales (valores sí traducir)
```yaml
data: "2025-10-31"  # KEY no traducir, VALUE es fecha (mantener formato)
durada: "~3h"  # KEY no traducir, VALUE mantener
participants: ["Claude (Development Agent)", "User"]  # KEY no traducir, VALUES mantener formato
```

---

## COMENTARIOS YAML - SÍ TRADUCIR

Todos los comentarios (# ...) deben traducirse:

```yaml
# ANTES (catalán):
# Aquest és el fitxer que carrega DevAI per entendre el projecte
# És compilat pel Context Agent (CA) des de memory/full/

# DESPUÉS (español):
# Este es el archivo que carga DevAI para entender el proyecto
# Es compilado por el Context Agent (CA) desde memory/full/
```

---

## INSTRUCCIONES EN VALORES - SÍ TRADUCIR

Cuando los valores contienen instrucciones, tradúcelas:

```yaml
# ANTES:
instruccions:
  ordre: "Omple en aquest ordre cronològic invers..."
  concisio: "Sigues concís però complet..."

# DESPUÉS:
instruccions:
  ordre: "Rellena en este orden cronológico inverso..."
  concisio: "Sé conciso pero completo..."
```

---

## PLACEHOLDERS - MANTENER FORMATO

Preserva los placeholders y su formato:

```yaml
# MANTENER:
nom: "[NOM_PROJECTE]"
descripcio: "[DESCRIPCIÓ_1_LÍNIA]"
fase: "[FASE_ACTUAL]"

# NO CAMBIAR A:
nom: "[NOMBRE_PROYECTO]"  # ❌ INCORRECTO
```

---

## CASOS ESPECIALES

### 1. Campos con contenido mixto
```yaml
# El KEY no se traduce, el VALUE sí si es texto descriptivo:
highlights:
  - "viz/ movido a raíz (memsys3/viz/) según DEVELOPMENT.md"  # ✅ Traducir
  - "Análisis exhaustivo identificó 26 issues"  # ✅ Traducir
```

### 2. Campos técnicos en valores
```yaml
# Preservar nombres técnicos, rutas, comandos:
path: "memsys3/memory/full/adr.yaml"  # ✅ NO traducir (es ruta técnica)
comando: "git status"  # ✅ NO traducir (es comando)
```

### 3. Nombres de archivos
```yaml
# NO traducir nombres de archivos:
"memsys3/memory/context.yaml"  # ✅ Mantener
"sessions-template.yaml"  # ✅ Mantener
"compile-context.md"  # ✅ Mantener
```

---

## WORKFLOW DE TRADUCCIÓN SEGURA

1. **Leer archivo completo**
2. **Identificar estructura:**
   - ¿Es comentario (#)? → Traducir
   - ¿Es KEY de campo? → NO traducir (consultar lista TIER 1)
   - ¿Es VALUE descriptivo? → Traducir (consultar lista TIER 2)
   - ¿Es VALUE técnico (ruta, comando, nombre archivo)? → NO traducir
3. **Traducir solo lo permitido**
4. **Verificar sintaxis YAML** (indentación, comillas, etc.)
5. **Guardar y probar**

---

## REFERENCIA RÁPIDA: QUÉ TRADUCIR

✅ **SÍ TRADUCIR:**
- Comentarios YAML (# ...)
- Valores de campos descriptivos (descripcio, objectiu, problema, solucio, etc.)
- Instrucciones en templates
- Texto explicativo en valores multiline (|)

❌ **NO TRADUCIR:**
- Nombres de campos YAML (keys)
- Valores técnicos (estados, áreas, tipos, roles)
- Rutas de archivos
- Comandos
- Nombres de archivos
- Placeholders entre []
- Referencias técnicas (adrs_incloses, notes_compilacio, etc.)

---

## EN CASO DE DUDA

**Regla de oro:** Si no estás 100% seguro, **NO TRADUCIR**.

Es mejor mantener catalán que romper referencias cruzadas o estructura del sistema.

Consulta este documento antes de cada traducción.
