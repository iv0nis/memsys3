# Memory Visualizer

Interfície web per visualitzar la "ment" dels agents - el context, ADRs, sessions i status del projecte.

## 🚀 Ús Ràpid

```bash
cd memory/viz
python serve.py
```

S'obrirà automàticament al navegador a `http://localhost:8080`

## 📊 Què mostra?

### 🤖 Agent View
El context compilat que carreguen els Development Agents:
- Project info
- Features operatives
- ADRs rellevants (filtrades pel CA)
- Última sessió resumida
- Gotchas crítics
- Pendents prioritaris

### 📚 Full History
Tot l'històric complet:
- Totes les ADRs mai escrites
- Totes les sessions de treball

### 📊 Project Status
Estat actual complet del projecte amb features, stack, URLs, etc.

### 📈 Stats
Estadístiques de compilació:
- Quants tokens té el context
- Quantes ADRs s'han filtrat
- Última compilació
- Notes del Context Agent

## 🛠 Requisits

- Python 3.x (ve preinstal·lat a la majoria de sistemes)

## 🔧 Troubleshooting

**Port 8080 ocupat?**
Edita `serve.py` i canvia `PORT = 8080` a un altre port.

**Error "No module named..."?**
El servidor usa només llibreries estàndard de Python, no cal instal·lar res.

**Pestanyes buides?**
- Assegura't que existeixen els fitxers YAMLs/MD a `memory/`
- Comprova la consola del navegador per errors

**"context.yaml not found"?**
Normal si encara no has executat el Context Agent. Executa `@prompts/compile-context.md` primer.

## 📁 Fitxers

- `serve.py` - Servidor HTTP mínim
- `index.html` - Dashboard amb pestanyes
- `style.css` - Dark theme modern
- `viewer.js` - Carrega i renderitza YAMLs
- `README.md` - Aquest fitxer

## 🎨 Personalització

Pots modificar:
- **Colors**: Edita les CSS variables a `style.css`
- **Port**: Canvia `PORT` a `serve.py`
- **Layout**: Modifica `index.html` i `viewer.js`

## 📝 Notes

- El visualitzador llegeix els YAMLs **directament** via fetch()
- **No modifica** cap fitxer, només lectura
- Es refresca automàticament en recarregar la pàgina
- Simple YAML parser integrat (no cal dependències)
