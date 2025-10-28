# memsys3 - Memory System for AI Agents

> Sistema replicable per gestionar el context dels AI agents de forma eficient

**memsys3** és un sistema de gestió de context dissenyat per optimitzar el consum de tokens dels Development Agents proporcionant-los context compacte i rellevant del projecte.

## 🎯 Problema que Resol

Quan treballes amb AI agents en projectes grans:
- ❌ Els agents han de llegir desenes de fitxers de codi per entendre el projecte
- ❌ Cada sessió nova consumeix milers de tokens repetint el mateix context
- ❌ Decisions i aprenentatges es perden entre sessions
- ❌ No hi ha visibilitat de què "sap" l'agent

## ✨ Solució

**memsys3** proporciona:
- ✅ Context compilat en un únic fitxer (~2500-3000 tokens)
- ✅ Sistema de documentació estructurat (ADRs, sessions, status)
- ✅ Context Agent que filtra automàticament la informació rellevant
- ✅ Visualitzador web per veure la "ment" dels agents
- ✅ Prompts reutilitzables per començar/acabar sessions

## ⚡ Quick Start

### 1. Instal·lació

```bash
# Copia memsys3 al teu projecte
cp -r memsys3/ /path/to/your/project/

# O clona aquest repo dins del teu projecte
cd /path/to/your/project
git clone https://github.com/iv0nis/memsys3.git
```

### 2. Configuració Inicial

```bash
# 1. Omple el project-status.yaml inicial
# Edita memory/project-status.yaml amb info del teu projecte

# 2. Comença a documentar
# Afegeix decisions a memory/full/adr.yaml
# Afegeix sessions a memory/full/sessions.yaml

# 3. Compila el context
# Executa: @prompts/compile-context.md (amb el teu AI agent)

# 4. Visualitza
cd memory/viz
python3 serve.py
```

### 3. Ús amb AI Agents

**Començar sessió:**
```bash
@memory/context.yaml
```

**Acabar sessió:**
```bash
@prompts/endSession.md
```

**Recompilar context:**
```bash
@prompts/compile-context.md
```

## 📁 Estructura

```
memsys3/
├── README.md                       # Aquest fitxer
├── memory/
│   ├── context.yaml                # Context compilat (generat pel CA)
│   ├── project-status.yaml         # Estat actual del projecte
│   ├── README.md                   # Documentació detallada
│   ├── full/                       # Documentació completa
│   │   ├── adr.yaml               # Totes les ADRs
│   │   └── sessions.yaml          # Totes les sessions
│   ├── templates/                  # Templates reutilitzables
│   │   ├── adr-template.yaml
│   │   ├── context-template.yaml
│   │   ├── project-status-template.yaml
│   │   └── sessions-template.yaml
│   └── viz/                        # Visualitzador web
│       ├── serve.py
│       ├── index.html
│       ├── style.css
│       ├── viewer.js
│       └── README.md
├── prompts/
│   ├── compile-context.md          # Context Agent prompt
│   ├── endSession.md              # Documentar sessions
│   └── mind.md                    # Obrir visualitzador
└── agents/
    └── context-agent.yaml         # Configuració Context Agent
```

## 🔄 Workflow

### 1. **Documentar** (Humans/DevAI)
- Escriu decisions a `memory/full/adr.yaml`
- Documenta sessions a `memory/full/sessions.yaml`
- Actualitza `memory/project-status.yaml`

### 2. **Compilar** (Context Agent)
- Executa `@prompts/compile-context.md`
- Genera `memory/context.yaml` compacte

### 3. **Desenvolupar** (DevAI)
- Carrega `@memory/context.yaml`
- Desenvolupa amb context complet
- Documenta al acabar amb `@prompts/endSession.md`

## 🎨 Visualitzador Web

Interfície visual per veure la "ment" dels agents:

```bash
cd memory/viz
python3 serve.py
```

O amb prompt:
```bash
@prompts/mind.md
```

**Pestanyes:**
- 🤖 **Agent View**: Context compilat que veu DevAI
- 📚 **Full History**: Totes les ADRs i sessions
- 📊 **Project Status**: Estat complet del projecte
- 📈 **Stats**: Mètriques de compilació

## 📖 Documentació Completa

Veure **[memory/README.md](memory/README.md)** per:
- Criteris de filtratge del Context Agent
- Millors pràctiques
- Troubleshooting
- Exemples detallats

## 🛠 Requisits

- Python 3.x (per al visualitzador web)
- AI agent compatible amb prompts markdown (Claude, etc.)

## 🤝 Contribucions

Aquest sistema està obert a millores! Si tens idees o trobes bugs, obre un issue o PR.

## 📝 Llicència

MIT License - Lliure per usar en qualsevol projecte

## 🙏 Crèdits

Creat per gestionar context en projectes amb AI Development Agents.

---

**Versió**: 1.0
**Repositori**: https://github.com/iv0nis/memsys3
