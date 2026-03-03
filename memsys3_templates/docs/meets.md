# Sistema de Meets

## Qué es

Sistema de reuniones colaborativas entre agentes. Permite coordinar trabajo paralelo, resolver conflictos y hacer análisis forense multi-agente mediante un archivo Markdown compartido con sistema de turnos.

## Cuándo usar una reunión formal

**SÍ:** dos agentes tocan el mismo código en paralelo, conflicto que requiere coordinación, decisión que afecta múltiples agentes, bug crítico que requiere análisis conjunto.

**NO:** el moderador puede resolver por chat, pregunta puntual, un solo agente tiene toda la información.

## Tipos de reunión

- **Coordinación** — reparto de tareas, conflictos, decisiones compartidas → leer Protocolo común + Modo coordinación
- **Investigación** — bug crítico, incidente, análisis forense → leer `@memsys3/prompts/meet.md` completo

## Naming

```
memsys3/docs/meets/YYYYMMDD_N.md
```

## Flujo básico (coordinación)

1. **Convocante** crea el archivo con header + briefing completo
2. **Moderador** pasa el path al otro agente
3. **Agentes** se turnan escribiendo en el archivo, con polling autónomo entre turnos
4. Cuando ambos escriben `CIERRE`, el moderador escribe la `## Decisión`

## Polling autónomo

```bash
FILE="memsys3/docs/meets/YYYYMMDD_N.md"
INITIAL=$(grep -c "^## Agent [DESTINO]" "$FILE" | tr -d '[:space:]')
for i in $(seq 1 40); do
  current=$(grep -c "^## Agent [DESTINO]" "$FILE" | tr -d '[:space:]')
  if [ "$current" -gt "$INITIAL" ]; then
    tail -60 "$FILE"
    exit 0
  fi
  sleep 15
done
echo "Timeout — verificar si el otro agente respondió"
```

Ejecutar en el **contexto principal**, no como subagente.

## Resumen en chat (obligatorio)

Al terminar cada turno, informar al moderador:

```
CTA: [Turno a Agent Y / CIERRE]
Detalle: [Qué propuse, qué cambié, qué quedó sin resolver]
```

Al escribir `CIERRE`, añadir también:

```
TL;DR: [1-2 líneas de qué se acordó]
Pendiente: [próximo paso + responsable]
```

## Referencia completa

Ver `@memsys3/prompts/meet.md` para templates de turnos, modo investigación (6 fases), troubleshooting y todos los detalles del protocolo.
