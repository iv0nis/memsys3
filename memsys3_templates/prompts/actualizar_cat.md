# Actualitzar Versió Catalana - Sincronització memsys3 → memsys3_CAT

⚠️ **EXECUTAR DES DE:** `/mnt/c/PROYECTOS/memsys3` (repositori espanyol)

Aquest prompt sincronitza els canvis de templates des del repo espanyol al repo català que està en un directori completament separat.

## Objectiu

Sincronitzar canvis des de `/mnt/c/PROYECTOS/memsys3/memsys3_templates/` (versió espanyola) cap a `/mnt/c/PROYECTOS/memsys3_CAT/memsys3_templates/` (versió catalana), traduint al català tots els arxius distribuïbles.

## Context

**IMPORTANT - Rutes Absolutes:**

- **Repositori principal (espanyol - ORIGEN):**
  - Ruta: `/mnt/c/PROYECTOS/memsys3`
  - Branch: `master`
  - Directori templates: `/mnt/c/PROYECTOS/memsys3/memsys3_templates/`

- **Repositori català (DESTÍ):**
  - Ruta: `/mnt/c/PROYECTOS/memsys3_CAT`
  - Branch: `catalan`
  - Directori templates: `/mnt/c/PROYECTOS/memsys3_CAT/memsys3_templates/`

- **Tots dos apunten al mateix repo GitHub** amb branches diferents:
  - `master` → versió espanyol
  - `catalan` → versió català

- **Només es tradueixen templates** (`memsys3_templates/`), NO el dog-fooding

## Workflow de Sincronització

### PAS 1: Verificar Directoris

Verifica que tots dos directoris existeixen i estan nets:

```bash
# Verificar memsys3 (espanyol - origen)
cd /mnt/c/PROYECTOS/memsys3
git status
echo "Branch actual:"
git branch --show-current

# Verificar memsys3_CAT (català - destí)
cd /mnt/c/PROYECTOS/memsys3_CAT
git status
echo "Branch actual:"
git branch --show-current
```

Tots dos han d'estar en working tree net. Si hi ha canvis pendents, pregunta a l'usuari què fer.

### PAS 2: Obtenir Última Versió de Master

```bash
cd /mnt/c/PROYECTOS/memsys3
git pull origin master
```

### PAS 3: Identificar Canvis en Templates

Compara els arxius que han canviat des de l'última sincronització:

```bash
cd /mnt/c/PROYECTOS/memsys3
git log --oneline --since="2 weeks ago" -- memsys3_templates/
```

Mostra a l'usuari quins commits afecten a templates.

### PAS 4: Copiar Arxius de Templates (Espanyol)

Copia tota l'estructura de `memsys3_templates/` al directori català:

```bash
# Des de memsys3 (origen)
cd /mnt/c/PROYECTOS/memsys3

# Copiar a memsys3_CAT (destí)
cp -r memsys3_templates/* /mnt/c/PROYECTOS/memsys3_CAT/memsys3_templates/
```

### PAS 5: Traduir Arxius al Català

Ara has de traduir TOTS els arxius copiats d'espanyol a català.

**IMPORTANT:** Tradueix TOT el contingut (textos, comentaris, instruccions), però mantén:
- Noms d'arxius (NO traduir)
- Noms de keys YAML (NO traduir)
- Rutes i paths (NO traduir)
- Codi (variables, funcions)

#### Arxius a Traduir (per ordre de prioritat):

**1. Prompts (9 arxius):**
- `prompts/newSession.md`
- `prompts/endSession.md`
- `prompts/compile-context.md`
- `prompts/deploy.md`
- `prompts/actualizar.md`
- `prompts/mind.md`
- `prompts/backlog.md`
- `prompts/github.md`
- `prompts/actualizar_cat.md` (aquest mateix arxiu, irònic!)

**2. Templates YAML (4 arxius):**
- `memory/templates/project-status-template.yaml`
- `memory/templates/sessions-template.yaml`
- `memory/templates/adr-template.yaml`
- `memory/templates/context-template.yaml`

**3. Agents (2 arxius):**
- `agents/main-agent.yaml`
- `agents/context-agent.yaml`

**4. Visualitzador (3 arxius):**
- `viz/index.html`
- `viz/viewer.js`
- `viz/README.md`

**5. READMEs (1 arxiu):**
- `memory/README.md`

**NO traduir:**
- `README.md` (templates root) - es crea en projecte destí
- `memory/full/*.yaml` - exemples buits
- `memory/project-status.yaml` - es crea en projecte destí
- `memory/context.yaml` - es crea en projecte destí

#### Estratègia de Traducció

Per a CADA arxiu:

1. Llegeix l'arxiu en espanyol
2. Tradueix al català mantenint:
   - Estructura YAML/Markdown intacta
   - Keys YAML sense traduir (ex: `metadata:`, `ultima_actualizacion:`)
   - Rutes sense traduir (ex: `memsys3/memory/context.yaml`)
   - Noms d'arxius sense traduir
3. Usa Edit tool per reemplaçar contingut espanyol → català

**Taula de Traduccions Comunes:**

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

### PAS 6: Verificar Traducció

Després de traduir, verifica que:
- Keys YAML NO es van traduir
- Rutes mantenen format original
- Estructura d'arxius intacta
- NO hi ha barreja espanyol/català

```bash
cd /mnt/c/PROYECTOS/memsys3_CAT

# Verificar que NO hi ha paraules espanyoles residuals
grep -r "sesión\|descripción\|decisión" memsys3_templates/ --include="*.yaml" --include="*.md" || echo "✅ Sense espanyol residual"
```

### PAS 7: Commit i Push a Branch Catalan

```bash
cd /mnt/c/PROYECTOS/memsys3_CAT

# Verificar branch
git branch --show-current  # Ha de ser 'catalan'

# Si no està en catalan, canviar
git checkout catalan

# Afegir canvis
git add memsys3_templates/

# Veure què es commitarà
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

### PAS 8: Verificar en GitHub

Confirma que els canvis es van pujar correctament:

```bash
cd /mnt/c/PROYECTOS/memsys3_CAT
git log --oneline -3
```

Informa a l'usuari:
- Commit ID creat
- Arxius sincronitzats i traduïts
- Branch actualitzada (catalan)
- URL de GitHub per verificar

## Notes Importants

1. **NO tocar dog-fooding:** Només sincronitzes `memsys3_templates/`, NO `memsys3/memory/full/` ni altres carpetes de desenvolupament.

2. **Keys YAML romanen en espanyol:**
   - ✅ `ultima_actualizacion:` (NO traduir key)
   - ✅ `"2025-11-13"` (valor, traduir si és text)

3. **Rutes NO es tradueixen:**
   - ✅ `memsys3/memory/context.yaml` (sempre igual)
   - ✅ `@memsys3/prompts/newSession.md` (sempre igual)

4. **Contingut SÍ es tradueix:**
   - Instruccions en prompts
   - Comentaris en YAML
   - Textos d'interfície (HTML)
   - Missatges d'usuari

5. **Aquest prompt (actualizar_cat.md) també s'ha de traduir** quan estigui a `memsys3_templates/` català.

## Troubleshooting

**"Branch catalan no existeix a memsys3_CAT":**
```bash
cd /mnt/c/PROYECTOS/memsys3_CAT
git checkout -b catalan
git push -u origin catalan
```

**"Hi ha conflictes de merge":**
- Revisar quins arxius tenen conflicte
- Resoldre manualment prioritzant versió catalana més recent
- Tornar a traduir si és necessari

**"Keys YAML es van traduir accidentalment":**
- Revertir canvis: `git checkout -- memsys3_templates/`
- Tornar a PAS 4 amb més cura

## Verificació Final

Abans de finalitzar, confirma amb l'usuari:
- ✅ Arxius sincronitzats des de master
- ✅ TOT traduït al català (contingut)
- ✅ Keys YAML i rutes sense traduir
- ✅ Commit i push a branch `catalan` exitós
- ✅ Sense espanyol residual en templates

---

**Sincronització completada. memsys3_CAT branch `catalan` actualitzada.**
