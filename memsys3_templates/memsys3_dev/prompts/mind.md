# Mind - Visualitza la Memòria dels Agents

Executa el Memory Visualizer per veure la "ment" dels agents de forma visual.

## Tasca

1. Navega al directori del visualitzador
2. Executa el servidor Python
3. El navegador s'obrirà automàticament mostrant el dashboard

## Instruccions

Executa el següent comando:

```bash
cd memory/viz && python3 serve.py
```

**Important:**
- El servidor quedarà en execució (background)
- S'obrirà automàticament http://localhost:8080
- Mostra missatge a l'usuari confirmant que el visualitzador està obert
- Per aturar-lo, l'usuari pot fer Ctrl+C al terminal

## Què veurà l'usuari

El dashboard amb 4 pestanyes:
- 🤖 **Agent View**: Context compilat que veu DevAI
- 📚 **Full History**: Tot l'històric d'ADRs i sessions
- 📊 **Project Status**: Estat complet del projecte
- 📈 **Stats**: Mètriques de compilació i tokens

## Notes

- Si el port 8080 està ocupat, el servidor fallarà
- Si `context.yaml` no existeix, Agent View mostrarà error (normal si CA encara no s'ha executat)
- El visualitzador llegeix els YAMLs en temps real, refresca la pàgina per actualitzar
