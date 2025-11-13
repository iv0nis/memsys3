# memsys3 - Sistema de Memòria per Agents d'IA

> Sistema de gestió de context per optimitzar el treball amb AI Development Agents

## 🎯 Què és memsys3?

**memsys3** és un sistema de gestió de context dissenyat per optimitzar el consum de tokens dels AI Development Agents proporcionant-los context compacte i rellevant del projecte.

## 💡 Problema que Resol

Quan treballes amb AI agents en projectes:
- ❌ Els agents han de llegir molts arxius per entendre el projecte
- ❌ Cada sessió nova consumeix milers de tokens repetint el mateix context
- ❌ Decisions i aprenentatges es perden entre sessions
- ❌ No hi ha visibilitat de què "sap" l'agent

## ✨ Solució

**memsys3** proporciona:
- ✅ **Context compilat**: Un únic arxiu (~2500-3000 tokens) amb el context essencial
- ✅ **Documentació estructurada**: ADRs, sessions, project status
- ✅ **Context Agent**: Filtra automàticament la informació rellevant amb criteri intel·ligent
- ✅ **Visualitzador web**: Dashboard per veure la "ment" dels agents
- ✅ **Prompts reutilitzables**: Per iniciar/finalitzar sessions i compilar context
- ✅ **Rotació automàtica**: Escala quan supera límits (>1800 línies)
- ✅ **Pla de contingència**: Arxivat intel·ligent (>150K tokens)

## 🚀 Ús Diari

### Iniciar Sessió

En començar a treballar, carrega el context del projecte:

```bash
@memsys3/prompts/newSession.md
```

Això carrega automàticament:
- Estat actual del projecte (`memory/project-status.yaml`)
- Context compilat (`memory/context.yaml`)
- Instruccions del Main Agent (`agents/main-agent.yaml`)

### Durant el Desenvolupament

Treballa normalment. El sistema està dissenyat per no interferir en el teu workflow.

### Finalitzar Sessió

En finalitzar, documenta el que s'ha realitzat:

```bash
@memsys3/prompts/endSession.md
```

Això:
- Documenta la sessió a `memory/full/sessions.yaml`
- Documenta gotchas trobats (amb criticitat) a la mateixa sessió
- Crea ADRs si hi ha hagut decisions arquitectòniques
- Actualitza el `memory/project-status.yaml`
- Aplica rotació automàtica si és necessari

### Compilar Context

Quan vulguis actualitzar el context compilat (en una **nova instància neta**):

```bash
@memsys3/prompts/compile-context.md
```

El Context Agent:
- Llegeix TOT l'històric (`memory/full/adr.yaml`, `memory/full/sessions.yaml`)
- Aplica criteri intel·ligent de filtrat
- Genera `memory/context.yaml` compacte (màx 2000 línies)
- Aplica Pla de Contingència si supera 150K tokens

### Visualitzar la "Ment" de l'Agent

Per veure el dashboard visual:

```bash
@memsys3/prompts/mind.md
```

O manualment:
```bash
cd memsys3/viz
python3 serve.py
```

Obre http://localhost:8080 i veuràs:
- 🤖 **Agent View**: Context compilat
- 📚 **Full History**: ADRs i sessions completes
- 📊 **Project Status**: Estat del projecte
- 📈 **Stats**: Mètriques de compilació

## 📁 Estructura

```
memsys3/
├── README.md                       # Aquest arxiu
├── agents/
│   ├── main-agent.yaml            # Configuració del Development Agent
│   └── context-agent.yaml         # Configuració del Context Agent
├── memory/
│   ├── context.yaml                # Context compilat (generat per CA)
│   ├── project-status.yaml         # Estat actual del projecte
│   ├── README.md                   # Documentació detallada del sistema
│   ├── full/                       # Documentació completa
│   │   ├── adr.yaml               # Architectural Decision Records
│   │   ├── sessions.yaml          # Historial de sessions
│   │   └── (arxius rotats: adr_N.yaml, sessions_N.yaml)
│   ├── templates/                  # Templates YAML reutilitzables
│   │   ├── adr-template.yaml
│   │   ├── context-template.yaml
│   │   ├── project-status-template.yaml
│   │   └── sessions-template.yaml
│   ├── history/                    # Arxius arxivats (NO es llegeixen)
│   │   └── (dades antigues quan >150K tokens)
│   └── viz/                        # Visualitzador web
│       ├── serve.py
│       ├── index.html
│       ├── style.css
│       └── viewer.js
└── prompts/
    ├── newSession.md              # Carregar context a l'inici
    ├── endSession.md              # Documentar sessió
    ├── compile-context.md         # Compilar context (Context Agent)
    └── mind.md                    # Obrir visualitzador
```

## 🔄 Workflow

### 1. Documentar (Developers + DevAI)
- Desenvolupa features normalment
- Al final de sessió: `@memsys3/prompts/endSession.md`
- Es documenta a `memory/full/sessions.yaml`
- Es creen ADRs si hi ha decisions arquitectòniques importants

### 2. Compilar (Context Agent)
- En nova instància neta: `@memsys3/prompts/compile-context.md`
- Llegeix TOT l'històric
- Aplica criteri intel·ligent
- Genera `memory/context.yaml` compacte

### 3. Desenvolupar (DevAI)
- Nova sessió: `@memsys3/prompts/newSession.md`
- Carrega context compilat
- Desenvolupa amb visió completa del projecte
- En finalitzar: `@memsys3/prompts/endSession.md`

## 🧠 Filosofia del Context Agent

El Context Agent té **visió panoràmica completa** i decideix basant-se en:

**"Què ha de saber QUALSEVOL agent descontextualitzat per treballar en aquest projecte?"**

**Inclou:**
- Decisions amb impacte global
- Decisions no òbvies llegint el codi
- Trade-offs importants
- Problemes resolts que poden repetir-se
- Configuracions crítiques

**Exclou:**
- Canvis cosmètics
- ADRs obsoletes
- Sessions molt antigues sense rellevància
- Detalls d'implementació evidents

## 🔁 Escalabilitat

### Rotació Automàtica (>1800 línies)

Quan `sessions.yaml` o `adr.yaml` superen 1800 línies:
- `endSession.md` detecta automàticament
- Rotació segura: còpia → verifica → crea nou
- `sessions.yaml` → `sessions_1.yaml`
- `adr.yaml` → `adr_1.yaml`
- Context Agent llegeix TOTS els arxius rotats

### Pla de Contingència (>150K tokens)

Quan el total de `memory/full/` supera 150K tokens:
- Context Agent identifica dades irrellevants
- Les mou a `memory/history/` (NO es llegeix → estalvi real)
- Redueix a ~120K tokens
- Dades preservades, no perdudes, recuperables

## 📖 Documentació Detallada

Veure **[memory/README.md](memory/README.md)** per a:
- Criteris detallats del Context Agent
- Millors pràctiques de documentació
- Troubleshooting
- Exemples d'ADRs i sessions

## 🛠 Requisits

- Python 3.x (per al visualitzador web)
- AI agent compatible amb prompts markdown

## 💡 Tips

### Per Main-Agent
- NO executis `compile-context.md` (consumeix molts tokens)
- Suggereix `endSession.md` en finalitzar sessió
- L'user decideix quan compilar el context

### Per Context-Agent
- Llegeix TOT primer, filtra després
- Confia en el teu criteri intel·ligent
- Límit únic: 2000 línies a `context.yaml`

### Per Developers
- Documenta decisions arquitectòniques importants com ADRs
- Usa `endSession.md` en finalitzar cada sessió significativa
- Compila context en nova instància neta quan sigui necessari
- Visualitza la "ment" amb `mind.md` per entendre què saben els agents

## 🔧 Personalització

Aquest sistema és altament personalitzable:

- **agents/main-agent.yaml**: Personalitza comportament del Development Agent
- **memory/project-status.yaml**: Mantén actualitzat l'estat del teu projecte
- **memory/templates/**: Ajusta els templates segons les teves necessitats

---

**Sistema memsys3** - Gestió intel·ligent de context per AI Agents
