# FEATURE-011: Main Agent proactivo — sugerencias de workflow memsys3

**Estado:** Propuesto
**Prioridad:** Alta
**Tipo:** Feature
**Plazo:** Short-term
**Fecha identificación:** 2026-03-27
**Origen:** Análisis comparativo gentle-ai/Engram vs memsys3 + feedback usuario

---

## Problema / Necesidad

Actualmente el Main Agent es pasivo respecto al workflow de memsys3: trabaja hasta que el usuario decide hacer endSession. No sugiere proactivamente cuándo documentar, hacer checkpoint, o tomar acciones de preservación de contexto.

**Situación actual:**
- El usuario debe recordar cuándo hacer endSession
- No hay señales del agente sobre acumulación de contexto
- Decisiones importantes pueden pasar desapercibidas si la sesión es larga
- El agente no propone midSession checkpoint (FEATURE-010) ni re-lectura de contexto

**Restricción existente (ADR-008):**
Main Agent NO debe proponer compile-context.md (se ejecuta en instancia nueva). Esta restricción se mantiene — el agente sugiere endSession, no compilar.

---

## Propuesta

### Criterios para que el Main Agent sugiera acciones

Agregar en main-agent.yaml una sección de "triggers proactivos":

```yaml
# Triggers proactivos del Main Agent:
#
# SUGERIR midSession checkpoint (FEATURE-010) cuando:
# - Se ha tomado una decisión arquitectónica significativa
# - Se ha descubierto un gotcha que no debe perderse
# - Han pasado >1h de trabajo intenso con múltiples cambios
# - Se va a cambiar de tema/feature dentro de la misma sesión
# - El usuario menciona que va a hacer /compact
#
# SUGERIR endSession cuando:
# - Se ha completado el objetivo principal de la sesión
# - Se han acumulado múltiples cambios significativos
# - El usuario indica que va a parar o cambiar de tarea
# - La sesión ha sido larga con trabajo sustancial
#
# SUGERIR re-lectura de contexto cuando:
# - Detectas que no recuerdas decisiones previas de la sesión
# - Después de un /compact
# - Hay incertidumbre sobre el estado actual del proyecto
#
# FORMATO de sugerencia:
# Breve, no intrusivo, como nota al final de una respuesta.
# Ejemplo: "Nota: hemos tomado una decisión arquitectónica importante.
# ¿Quieres que haga un checkpoint midSession?"
#
# RESTRICCIONES (ADR-008):
# - NO proponer compile-context.md (se ejecuta en instancia nueva)
# - NO insistir si el usuario rechaza la sugerencia
# - NO interrumpir flujo de trabajo para sugerir
```

### Consideraciones

**Pros:**
- El agente se convierte en participante activo del workflow de memoria
- Reduce riesgo de pérdida de contexto por sesiones largas sin documentar
- Complementa FEATURE-010 (checkpoint) y ISSUE-020 (post-compact)
- No intrusivo — sugiere, no fuerza
- Consistente con restricción ADR-008

**Contras:**
- Riesgo de sugerencias molestas si los triggers son demasiado sensibles
- Los criterios son subjetivos — el agente debe calibrar
- Añade complejidad al main-agent.yaml

### Implementación

1. **Modificar main-agent.yaml** (templates + dog-fooding):
   - Agregar sección "Triggers proactivos"
   - Definir criterios claros para cada tipo de sugerencia
   - Incluir formato y restricciones

2. **Integrar con FEATURE-010** (midSession):
   - El agente sugiere → el usuario acepta → se ejecuta midSession.md

3. **Integrar con ISSUE-020** (post-compact):
   - Después de /compact, el agente sugiere re-leer contexto

---

## Referencias

- **ADR-008:** Main Agent NO propone compile-context (restricción vigente)
- **FEATURE-010:** Checkpoint mid-session (mecanismo que el agente sugeriría)
- **ISSUE-020:** Protocolo post-compact (recuperación de contexto)
- **Inspiración:** Engram protocol (agente guarda proactivamente, pero allí es obligatorio — aquí es sugerencia)
- **Feedback usuario:** "busquemos la forma en que el main agent proponga cuándo hacer mid o end session"
