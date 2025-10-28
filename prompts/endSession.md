# End Session - Documenta la Sessió Actual

Tu (DevAgent) has de documentar aquesta sessió de treball al sistema Memory del projecte.

## Objectiu

Registrar automàticament què s'ha fet durant aquesta sessió perquè el pròxim DevAgent tingui context complet.

## Tasques a Realitzar

### 1. Recopilar Evidències Objectives

Abans d'auto-analitzar, recull evidències de què s'ha fet durant la sessió.

**Si el projecte usa Git:**
```bash
# Veure què s'ha canviat
git status
git diff --stat
git log --oneline -5

# Fitxers modificats (staged i unstaged)
git diff --name-only
```

**Fitxers modificats recentment:**
```bash
# Últimes 2-3 hores (ajusta -mmin segons durada sessió estimada)
find . -type f -mmin -180 -not -path '*/node_modules/*' -not -path '*/.git/*' -not -path '*/dist/*' -not -path '*/__pycache__/*'
```

**Bash history (últims comandos executats):**
```bash
history | tail -30
```

**Notes:**
- Aquestes evidències són **opcionals però recomanades**
- Et donen pistes objectives de què s'ha tocat
- No substitueixen el teu context de conversa, només el complementen
- Si no hi ha git o alguna eina falla, continua igualment amb el teu context intern

### 2. Auto-analitzar la Sessió

Amb les evidències recollides (si n'hi ha) i el teu context intern de la conversa, identifica:

**Features/Tasques Implementades:**
- Quins fitxers has creat, editat o esborrat (Read, Edit, Write)
- Quines funcionalitats noves has desenvolupat
- Quins bugs has resolt
- Quins refactorings has fet

**Problemes Resolts:**
- Quins errors o obstacles has trobat
- Com els has solucionat
- Quins beneficis ha portat la solució

**Decisions Preses:**
- Quines decisions tècniques o arquitectòniques has pres amb l'usuari
- Justificació de cada decisió
- Si són decisions arquitectòniques importants → necessiten ADR

**Tecnologies/Llibreries:**
- Què has afegit al projecte (dependencies, tools)
- Què has eliminat o substituït
- Per què (motiu de cada canvi)

**Deployments:**
- Quins serveis has desplegat
- URLs resultants
- Notes sobre el deployment

**Pròxims Passos:**
- Què queda pendent
- Què s'ha mencionat per fer en futures sessions

### 3. Usar el Template

Llegeix `memory/templates/sessions-template.yaml` i segueix la seva estructura.

### 4. Comprovar Rotació de Sessions (si cal)

Abans d'afegir la nova sessió, comprova si `sessions.yaml` ha superat el límit de línies.

**Comprovar mida:**
```bash
wc -l memory/full/sessions.yaml
```

**Si supera 1800 línies:**

1. **Trobar proper número lliure:**
   ```bash
   # Comprovar quins fitxers existeixen
   ls memory/full/sessions_*.yaml 2>/dev/null
   # Identificar el proper número (si existeix sessions_2.yaml, usar sessions_3.yaml)
   ```

2. **Rotació Segura (pas a pas):**
   ```bash
   # A. PRIMER: Copiar el fitxer actual (preservar dades)
   cp memory/full/sessions.yaml memory/full/sessions_N.yaml

   # B. Verificar que la còpia existeix i té contingut
   wc -l memory/full/sessions_N.yaml

   # C. Si la verificació és OK, crear nou sessions.yaml amb header bàsic
   # (Escriure només l'estructura YAML base, sense sessions)

   # D. Confirmar rotació
   echo "✓ Rotació completada: sessions.yaml → sessions_N.yaml"
   echo "✓ Nou sessions.yaml creat per continuar"
   ```

**Avantatges d'aquest flux:**
- ✅ No perd dades (copia abans)
- ✅ Verifica que la còpia existeix
- ✅ Sessions antigues intactes a sessions_N.yaml
- ✅ sessions.yaml sempre existeix amb les més recents
- ✅ Context Agent pot llegir sessions.yaml sense problemes de límit

**Si NO supera 1800 línies:**
- Continua amb el flux normal (afegir al principi)

### 5. Afegir Sessió a `memory/full/sessions.yaml`

- Afegeix la nova sessió **al PRINCIPI** de l'array `sessions:` (ordre cronològic invers)
- ID i data: YYYY-MM-DD d'avui
- Títol: Descriptiu i concís (ex: "Implementació Feature X + Fix Bug Y")
- Durada: Estima basant-te en la conversa
- Participants: Tu com a DevAgent

**IMPORTANT:**
- Sigues concís però complet
- Evita detalls massa granulars (typos, canvis de styling menors)
- Evita ser massa vague ("millorat sistema")
- Troba el balanç (veure exemples al template)

### 6. Actualitzar `memory/project-status.yaml`

Actualitza les següents seccions:

**metadata:**
- `ultima_actualitzacio`: Data d'avui
- `actualitzat_per`: "Claude (Session [Títol])"

**estat_actual:**
- `ultima_feature`: Última feature implementada aquesta sessió (si n'hi ha)

**features:**
- Si has completat una feature, canvia `estat: operatiu`
- Si has creat una feature nova, afegeix-la

**historic_sessions:**
- Afegeix entrada amb data, durada i objectiu resumit

**pendents_prioritaris:**
- Marca com completades les tasques fetes
- Afegeix noves tasques identificades

### 7. Crear ADRs si Cal

Si has pres **decisions arquitectòniques importants** (no decisions menors):

**Exemples de decisions que necessiten ADR:**
- Triar una llibreria/framework en lloc d'un altre
- Canviar l'arquitectura del sistema
- Decidir un patró de disseny
- Canviar stack tecnològic

**Exemples que NO necessiten ADR:**
- Canviar un color de botó
- Afegir validació a un formulari
- Fixar un bug menor
- Refactoritzar una funció

Si cal ADR:

**1. Comprovar Rotació d'ADRs (si cal):**

Abans de crear l'ADR, comprova si `adr.yaml` ha superat el límit de línies.

```bash
wc -l memory/full/adr.yaml
```

**Si supera 1800 línies:**

Rotació Segura (mateix procés que sessions):
```bash
# A. Trobar proper número lliure
ls memory/full/adr_*.yaml 2>/dev/null

# B. Copiar el fitxer actual (preservar dades)
cp memory/full/adr.yaml memory/full/adr_N.yaml

# C. Verificar que la còpia existeix
wc -l memory/full/adr_N.yaml

# D. Crear nou adr.yaml amb header YAML bàsic
# (Escriure només estructura base: adrs: [])

# E. Confirmar rotació
echo "✓ Rotació ADRs completada: adr.yaml → adr_N.yaml"
```

**Si NO supera 1800 línies:**
- Continua amb el flux normal

**2. Crear l'ADR:**
1. Llegeix `memory/templates/adr-template.yaml`
2. Crea entrada a `memory/full/adr.yaml`
3. Linkeja l'ADR des de la sessió (camp `adr_relacionada`)

### 8. Interacció amb l'Usuari

**Pregunta només si:**
- No estàs segur de com titular la sessió
- No pots estimar la durada
- Tens dubte sobre si una decisió necessita ADR
- Falta context crític que no pots inferir

**NO preguntis:**
- Confirmació per cada canvi individual
- Aprovació de la documentació (assumeix que està correcta)
- Detalls que pots inferir del context

## Workflow Recomanat

1. **Recull evidències** (git status, find, history)
2. **Auto-analitza** la conversa i identifica canvis
3. **Llegeix** els templates i fitxers actuals
4. **Comprova rotació** (si sessions.yaml > 1800 línies, rotació segura)
5. **Genera** l'entrada de sessió en YAML
6. **Afegeix** a `full/sessions.yaml` al principi
7. **Actualitza** `project-status.yaml`
8. **Crea ADRs** si cal
9. **Informa** l'usuari que la sessió s'ha documentat (resum breu)

## Notes

- **Format**: YAML estricte (tabs → 2 espais)
- **Multiline strings**: Usa `|` per textos llargs
- **Consistència**: Segueix l'estil de sessions anteriors
- **Tokens**: No et preocupis per tokens aquí, sigues complet
- **Context Agent**: Ell ja s'encarregarà de filtrar després

## Exemple de Sortida Esperada

Al final hauràs:
✅ Fet rotació de sessions si calia (sessions.yaml → sessions_N.yaml)
✅ Afegit sessió a `memory/full/sessions.yaml`
✅ Actualitzat `memory/project-status.yaml`
✅ Creat ADRs a `memory/full/adr.yaml` (si cal)
📝 Informat l'usuari amb resum de què s'ha documentat

---

**Comença ara la documentació de la sessió actual.**
