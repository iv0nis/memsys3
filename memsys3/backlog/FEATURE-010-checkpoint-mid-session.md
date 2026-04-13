# FEATURE-010: Checkpoint mid-session

**Estado:** Propuesto
**Prioridad:** Media-Alta
**Tipo:** Feature
**Plazo:** Short-term
**Fecha identificación:** 2026-03-27
**Origen:** Análisis comparativo gentle-ai/Engram vs memsys3

---

## Problema / Necesidad

memsys3 documenta todo al final de la sesión (endSession). Si la sesión se corta inesperadamente, se pierde el contexto de lo trabajado. Además, en sesiones largas se acumulan decisiones y gotchas que podrían olvidarse al documentar al final.

**Situación actual:**
- endSession es el único punto de documentación
- Si el agente compacta (/compact) a mitad de sesión, pierde contexto de lo que pasó antes
- Engram guarda insights durante la sesión conforme ocurren — concepto valioso aunque su implementación (depender de que el agente "se acuerde" de guardar) es frágil

**Escenarios donde mid-session checkpoint ayudaría:**
1. Sesión larga (>2h) con múltiples cambios significativos
2. Decisión arquitectónica importante tomada a mitad de sesión
3. Gotcha crítico descubierto que no debe perderse
4. Antes de un /compact para preservar lo trabajado
5. Cambio de tema/feature dentro de la misma sesión

---

## Propuesta

### Prompt midSession.md (o checkpoint.md)

Mecanismo ligero para guardar estado parcial sin cerrar la sesión:

```markdown
# midSession checkpoint
1. Documenta en sessions.yaml una entrada parcial marcada como "checkpoint"
2. Incluye: decisiones tomadas, gotchas descubiertos, archivos modificados hasta ahora
3. NO cierra la sesión — el agente sigue trabajando
4. endSession al final consolida los checkpoints en la entrada final de sesión
```

**Formato en sessions.yaml:**
```yaml
- data: "2026-03-27"
  tipo: "checkpoint"  # Marca especial — no es sesión completa
  hora: "14:30"
  contexto: "Mid-session: implementando FEATURE-010"
  decisions:
    - "Decidido usar midSession.md como prompt separado"
  gotchas:
    - "grep -c en WSL requiere tr -d para limpiar output"
  archivos_modificados:
    - "src/auth/middleware.ts"
```

**endSession consolidación:**
```markdown
# Al hacer endSession, si hay checkpoints previos:
1. Leer checkpoints de la sesión actual
2. Consolidar en una única entrada de sesión
3. Eliminar entradas tipo "checkpoint"
```

### Consideraciones

**Pros:**
- Protege contra pérdida de contexto en sesiones largas
- Ligero — no requiere infraestructura, solo un prompt corto
- Determinista — no depende de que el agente "se acuerde" (como Engram)
- Compatible con workflow actual (endSession sigue siendo el cierre)

**Contras:**
- Riesgo de checkpoints huérfanos si no se hace endSession
- Más entradas temporales en sessions.yaml
- Requiere que endSession sepa consolidar checkpoints

---

## Relación con FEATURE-011

FEATURE-011 (Main Agent proactivo) complementa esta feature: el Main Agent sugeriría cuándo hacer un checkpoint, y este prompt sería el mecanismo para ejecutarlo.

---

## Referencias

- **Inspiración:** Engram mem_save (guardar insights en tiempo real)
- **Prompt afectado:** endSession.md (consolidación de checkpoints)
- **ADR relacionado:** ADR-009 (gotchas en sessions)
- **Feature relacionada:** FEATURE-011 (Main Agent proactivo)
