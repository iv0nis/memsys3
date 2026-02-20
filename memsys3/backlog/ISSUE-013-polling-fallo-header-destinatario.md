# ISSUE-013: Polling falla cuando header no apunta al agente esperado

**Estado:** Parcialmente resuelto
**Prioridad:** Media
**Tipo:** Bug / Protocolo
**Fecha identificación:** 2026-02-20

---

## Problema / Necesidad

El script de polling fallaba cuando Agent A cerraba con `## Agent A → Ivonis` en lugar de `## Agent A → Agent B`. El grep buscaba el destinatario específico y no lo encontraba → timeout falso.

Falló en dos reuniones:
- **200226_2**: polling buscaba `^## Agent A.*Agent B`, Agent A cerró con `→ Ivonis`
- **200226_2** (segundo intento): mismo problema

## Causa raíz

Doble problema:
1. El script de polling dependía del destinatario en el header
2. No había regla de protocolo que prohibiera `→ Ivonis` durante turnos activos

## Solución aplicada

**Protocolo**: documentado en `meet.md` — headers SIEMPRE `→ [agente destinatario]`, nunca `→ Ivonis` durante turnos activos.

**Script mejorado**: contar secciones `## Agent X` en lugar de buscar destinatario específico:
```bash
INITIAL=$(grep -c "^## Agent A" "$FILE")
for i in $(seq 1 40); do
  current=$(grep -c "^## Agent A" "$FILE")
  if [ "$current" -gt "$INITIAL" ]; then
    tail -60 "$FILE"
    exit 0
  fi
  sleep 15
done
```

## Pendiente

- Incorporar el script mejorado en `meet.md` (Protocolo común, sección Polling) — Agent A tiene el texto actual que aún usa el script antiguo con `[DESTINO]`

## Referencias

- Reuniones 200226_2 y 200226_3
- `meet.md` sección "Polling autónomo"
