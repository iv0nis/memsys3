# Visualizador Web

## Qué es

Dashboard web para visualizar la memoria del agente. Muestra el contexto compilado, el histórico completo, el estado del proyecto y métricas de compilación.

## Arrancar

```bash
cd memsys3/viz
python3 serve.py
```

Se abre automáticamente en `http://localhost:8080`.

## Pestañas

| Pestaña | Contenido |
|---------|-----------|
| 🤖 Agent View | `context.yaml` — lo que ve el agente al iniciar sesión |
| 📚 Full History | `adr.yaml` + `sessions.yaml` completos |
| 📊 Project Status | `project-status.yaml` |
| 📈 Stats | Métricas de compilación (tokens, ADRs filtradas, sesiones) |

## Características técnicas

- Sin dependencias externas (no npm, no pip)
- YAML parser JavaScript integrado
- CORS habilitado, cache desactivado (refresca YAMLs en cada carga)
- Abre navegador automáticamente (`webbrowser.open()`)

## Requisitos

- Python 3.x

## Archivos

```
memsys3/viz/
├── serve.py      — servidor HTTP con CORS
├── index.html    — dashboard
├── viewer.js     — cargador y renderizador de YAMLs
└── style.css     — dark theme
```
