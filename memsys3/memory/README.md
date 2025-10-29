# Memory System - Context Management per Agents

> **Sistema replicable per gestionar el context dels AI agents de forma eficient**

Aquest sistema està dissenyat per optimitzar el consum de tokens dels Development Agents (DevAI) proporcionant-los context compacte i rellevant del projecte.

## 🎯 Objectiu

Evitar que els agents llegeixin desenes de fitxers de codi per entendre el projecte. En lloc d'això, carreguen un únic fitxer `context.yaml` (màxim 2000 línies) amb tota la informació crítica.

## ⚡ Quick Start (Replicar en un nou projecte)

```bash
# 1. Copia l'estructura de memsys3/ al teu projecte
cp -r memsys3/ /path/to/nou/projecte/

# 2. Omple el project-status.yaml inicial
# Usa memsys3/memory/templates/project-status-template.yaml com a base

# 3. Comença a documentar decisions i sessions
# Escriu a memsys3/memory/full/adr.yaml i memsys3/memory/full/sessions.yaml seguint els templates

# 4. Compila el context quan calgui
# Executa: @memsys3/prompts/compile-context.md

# 5. Visualitza la "ment" dels agents
cd memsys3/memory/viz
python serve.py
```

## 📁 Estructura

```
memsys3/
├── memory/
│   ├── context.yaml                    # ← DevAI carrega això (compilat)
│   ├── project-status.yaml             # ← Estat actual del projecte
│   ├── README.md                       # ← Aquest fitxer
│   │
│   ├── viz/                            # ← Visualitzador web
│   │   ├── serve.py                    # Servidor mínim
│   │   ├── index.html                  # Dashboard
│   │   ├── style.css                   # Estils
│   │   ├── viewer.js                   # Renderitzador
│   │   └── README.md                   # Instruccions
│   │
│   ├── full/                           # ← Documentació completa (input CA)
│   │   ├── adr.yaml                    # Totes les ADRs històriques
│   │   └── sessions.yaml               # Totes les sessions de treball
│   │
│   └── templates/                      # ← Templates reutilitzables
│       ├── adr-template.yaml
│       ├── context-template.yaml
│       ├── project-status-template.yaml
│       └── sessions-template.yaml
│
├── agents/
│   └── context-agent.yaml              # Configuració formal del Context Agent
│
└── prompts/
    ├── compile-context.md              # Prompt per executar Context Agent
    └── mind.md                         # Slash command /mind per visualitzador
```

## 🔄 Workflow

### 1. Documentar (Humans/DevAI)

Escriu a aquests fitxers durant el desenvolupament:

**`memsys3/memory/full/adr.yaml`** - Decisions arquitectòniques importants
- Quan: Has pres una decisió no òbvia que afecta el projecte
- Format: Usa `memsys3/memory/templates/adr-template.yaml`
- Exemple: "Per què Astro vs React", "Per què jsPDF vs html2canvas"

**`memsys3/memory/full/sessions.yaml`** - Sessions de treball
- Quan: Al final de cada sessió significativa (>1h treball)
- Format: Usa `memsys3/memory/templates/sessions-template.yaml`
- Inclou: features implementades, problemes resolts, decisions, pendents

**`memsys3/memory/project-status.yaml`** - Estat actual
- Quan: Canvia l'estat global (nova feature operativa, nou milestone)
- Format: Ja està creat, només actualitza'l
- No el facis créixer massa, el CA el llegeix sencer

### 2. Compilar (Context Agent)

Quan el context creix massa o després de sessions importants:

```bash
# Executa el Context Agent
@memsys3/prompts/compile-context.md

# O carrega la configuració formal
@memsys3/agents/context-agent.yaml
```

El CA farà:
- Llegir **TOT**: `memsys3/memory/full/adr.yaml`, `memsys3/memory/full/sessions.yaml`, `memsys3/memory/project-status.yaml`
- Si > 150K tokens: arxivar dades irrellevants a `memsys3/memory/history/` (no llegit)
- Filtrar amb criteri intel·ligent (impacte global, rellevància)
- Generar `memsys3/memory/context.yaml` (màxim 2000 línies)

### 3. Desenvolupar (DevAI)

Els Development Agents només han de:

```bash
# Carregar context
@memsys3/memory/context.yaml
```

I ja tenen tot el que necessiten per començar a desenvolupar.

## 📊 Filosofia del Context Agent

El CA té la **visió panoràmica completa** del projecte i decideix amb criteri intel·ligent:

**"Què ha de saber QUALSEVOL agent descontextualitzat per treballar aquí?"**

### Límit ÚNIC
- **Màxim 2000 línies** al `context.yaml` final
- **NO límits arbitraris** per ADRs, sessions, gotchas, etc.
- El CA decideix basant-se en **rellevància i impacte global**

### Pla de Contingència (>150K tokens)
Si les dades a `memsys3/memory/full/` superen 150K tokens:
1. CA identifica ADRs/sessions **irrellevants** amb criteri
2. Les mou a `memsys3/memory/history/` (que **NO es llegeix**)
3. Redueix a ~120K tokens
4. Continua compilació normal

**Resultat:** Estalvi real de tokens, dades preservades, sistema escalable.

### Criteri de Selecció

**Inclou:**
- ADRs amb impacte global (afecten tot el projecte)
- Sessions recents amb canvis significatius
- Gotchas que trenquen desenvolupament
- Decisions no òbvies

**Exclou (i arxiva si > 150K):**
- ADRs deprecated o massa específiques
- Sessions >6 mesos sense rellevància
- Canvis cosmètics
- Detalls visibles al codi

## 🚀 Quan Executar el CA

**Executa el Context Agent quan:**
- ✅ Has completat una sessió gran (>2h treball)
- ✅ Has afegit 3+ ADRs noves
- ✅ `full/sessions.yaml` té >10 sessions
- ✅ Nota que `context.yaml` està obsolet

**NO cal executar-lo si:**
- ❌ Només has canviat una línia de codi
- ❌ Fixes menors o typos
- ❌ `context.yaml` té menys d'1 setmana

## 💡 Millors Pràctiques

### Per Documentar

**✅ Fer:**
- Documenta decisions no òbvies
- Sigues concís però complet
- Usa el format dels templates
- Afegeix sessions després de treball significatiu
- Linkeja ADRs des de sessions si cal

**❌ Evitar:**
- Documentar cada petit canvi
- Duplicar informació entre fitxers
- Descripcions vagas ("millorat sistema")
- Massa detall tècnic ("canviat padding 10px→12px")

### Per Compilar

**✅ Fer:**
- Executa CA regularment (setmanalment o després sessions grans)
- Revisa que `context.yaml` tingui sentit
- Comprova que no supera 2000 línies
- Deixa que el CA decideixi què arxivar (si >150K tokens)

**❌ Evitar:**
- Editar `context.yaml` manualment (sempre via CA)
- Executar CA després de cada petit canvi
- Ignorar notes de compilació del CA
- Esborrar `history/` (dades arxivades)

## 🔧 Manteniment

### Rotació Automàtica (>1800 línies)

Quan `sessions.yaml` o `adr.yaml` superen 1800 línies:
- **endSession.md** detecta automàticament
- Fa rotació segura: `sessions.yaml` → `sessions_N.yaml`
- Crea nou fitxer buit per continuar
- **No es perden dades**, queden a `sessions_1.yaml`, `sessions_2.yaml`, etc.

**Context Agent llegeix tots els fitxers** (`sessions.yaml` + `sessions_*.yaml`) fins que total >150K tokens, llavors arxiva irrellevants a `history/`.

### Arxivament Intel·ligent (>150K tokens)

Si el CA detecta >150K tokens totals:
- Mou ADRs/sessions irrellevants a `memory/history/`
- `history/` **NO es llegeix** → estalvi real
- Dades preservades, recuperables si cal

### Periodicitat

- **Context Agent**: Executa després de sessions importants
- **Rotació**: Automàtica quan >1800 línies
- **Arxivament**: Automàtic del CA quan >150K tokens
- **Revisió manual**: Opcional cada 6-12 mesos per netejar `history/`

## 📝 Exemples

### Exemple 1: Nova Feature Gran

1. Desenvolupes feature durant 3h
2. Al final, escrius a `memsys3/memory/full/sessions.yaml`:
   ```yaml
   sessions:
     - id: "2025-10-23"
       titol: "Sistema d'Exportació de Documents"
       features_implementades:
         - nom: "Exportació PDF"
           descripcio: "Text real amb Llibreria X, format professional..."
       decisions_preses:
         - decisio: "jsPDF vs html2canvas"
           justificacio: "Millor qualitat de text"
   ```
3. Si vas decidir quelcom arquitectònic, afegeix ADR a `memsys3/memory/full/adr.yaml`
4. Executes `@memsys3/prompts/compile-context.md`
5. `memsys3/memory/context.yaml` s'actualitza amb info nova

### Exemple 2: DevAI Nou

1. Nou agent carrega `@memsys3/memory/context.yaml`
2. En ~1500 tokens entén:
   - Què és el projecte
   - Què funciona i què no
   - Decisions clau preses
   - Última sessió (què es va tocar)
   - Gotchas a vigilar
3. Pot començar a desenvolupar immediatament

## 🆘 Troubleshooting

**P: context.yaml està obsolet**
R: Executa `@memsys3/prompts/compile-context.md`

**P: CA inclou massa/poques ADRs**
R: Ajusta límits i criteris a `memsys3/prompts/compile-context.md`

**P: DevAI diu que li falta context**
R: Potser necessita codi específic. El CA només dona visió general, no substitueix llegir codi quan cal.

**P: memsys3/memory/full/sessions.yaml és immens**
R: Normal després de mesos. El CA només agafa l'última sessió per `memsys3/memory/context.yaml`. Si molesta, pots arxivar sessions antigues.

## 🎨 Visualitzador Web

Interfície visual per veure la "ment" dels agents.

**Executar:**
```bash
# Opció 1: Slash command
/mind

# Opció 2: Prompt directe
@memsys3/prompts/mind.md

# Opció 3: Manual
cd memsys3/memory/viz
python serve.py
```

**Pestanyes disponibles:**
- 🤖 **Agent View**: El que veu DevAI (context compilat)
- 📚 **Full History**: Tot l'històric d'ADRs i sessions
- 📊 **Project Status**: Estat complet del projecte
- 📈 **Stats**: Mètriques de compilació

**Ús:** Ideal per fer revisions visuals del context, detectar gaps, o presentar l'estat del projecte.

**Documentació completa:** Veure `memsys3/memory/viz/README.md`

---

**Creat**: 2025-10-23
**Versió**: 1.0
**Mantenidors**: Sistema automatitzat + humans
