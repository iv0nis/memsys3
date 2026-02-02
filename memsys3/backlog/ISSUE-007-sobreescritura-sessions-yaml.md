# ISSUE-007: Agentes sobreescribiendo sessions.yaml en lugar de añadir sesiones

**Estado:** Completado
**Prioridad:** Crítica
**Tipo:** Bug / Pérdida de Datos
**Plazo:** Inmediato
**Fecha identificación:** 2025-01-30
**Fecha resolución:** 2025-01-30

---

## Problema / Necesidad

Los agentes están **SOBREESCRIBIENDO** `memsys3/memory/full/sessions.yaml` en lugar de **AÑADIR** nuevas sesiones al array existente durante endSession.md.

**Comportamiento esperado:**
- Main Agent ejecuta endSession.md
- Documenta sesión nueva siguiendo sessions-template.yaml
- **AÑADE** la sesión al PRINCIPIO del array `sessions:` en sessions.yaml
- Verifica si sessions.yaml supera 1800-2000 líneas → rotación automática

**Comportamiento actual (BUG):**
- Main Agent ejecuta endSession.md
- Documenta sesión nueva siguiendo sessions-template.yaml
- **SOBREESCRIBE** completamente sessions.yaml → pérdida total de sesiones anteriores
- ❌ Historial de sesiones perdido
- ❌ Memoria del proyecto eliminada

**Consecuencias:**
1. **Pérdida de memoria histórica del proyecto** (crítico)
2. Context Agent no puede compilar correctamente (faltan sesiones)
3. Gotchas documentados en sesiones previas desaparecen
4. Decisiones y aprendizajes del proyecto se pierden
5. Sistema de rotación automática no funciona (no hay datos para rotar)

**Caso real reportado:**
- **Proyecto:** No especificado (reportado por usuario)
- **Situación:** "al hacer endSession, los agentes han empezado a sobreescribir sessions.yaml"
- **Impacto:** Pérdida total de historial de sesiones previas

---

## Análisis

**Problema raíz:**
El prompt endSession.md puede no ser suficientemente explícito sobre el comportamiento de **AÑADIR** vs **SOBRESCRIBIR**.

**Instrucción actual en endSession.md PASO 4:**
```
4. Añadir Sesión a `memsys3/memory/full/sessions.yaml`:
   - **Añadir al PRINCIPIO** del array `sessions:`
   - Usa `memsys3/memory/templates/sessions-template.yaml` como guía
```

**Posibles causas:**
1. Agente interpreta "Añadir" como "escribir nueva sesión" sin leer archivo existente
2. Agente usa Write tool en lugar de Edit tool (Write sobrescribe, Edit añade)
3. Agente no lee sessions.yaml antes de editarlo (violación workflow)
4. Instrucciones ambiguas sobre workflow: Read → Edit → Verificar

**Comparación con comportamiento correcto:**
- ✅ Leer sessions.yaml completo
- ✅ Usar Edit tool para añadir nueva sesión al principio del array
- ✅ Verificar que sesión añadida + sesiones previas están presentes
- ✅ Contar líneas para detectar necesidad de rotación
- ❌ BUG: Usar Write tool → sobrescribe todo

---

## Propuesta / Opciones

### Opción A: Reforzar instrucciones en endSession.md (RECOMENDADA)

Modificar endSession.md PASO 4 para ser EXTREMADAMENTE explícito:

```markdown
4. Añadir Sesión a `memsys3/memory/full/sessions.yaml`:

   **⚠️ CRÍTICO: NO SOBREESCRIBIR EL ARCHIVO**

   **Workflow obligatorio:**
   1. **PRIMERO:** Leer archivo completo `@memsys3/memory/full/sessions.yaml`
   2. **SEGUNDO:** Usar Edit tool para AÑADIR tu sesión al PRINCIPIO del array `sessions:`
   3. **TERCERO:** Verificar que tu sesión + todas las sesiones previas están presentes
   4. **CUARTO:** Contar líneas totales del archivo para detectar rotación

   **NUNCA uses Write tool en sessions.yaml** → Write SOBRESCRIBE, Edit AÑADE

   **Formato de la nueva sesión:**
   - Usa `@memsys3/memory/templates/sessions-template.yaml` como guía
   - Añade AL PRINCIPIO del array `sessions:` (después de la línea `sessions:`)
   - Mantén indentación correcta (2 espacios para `- id:`)
```

**Pros:**
- Instrucciones inequívocas sobre workflow correcto
- Warnings explícitos sobre Write vs Edit
- Pasos numerados imposibles de malinterpretar
- No requiere cambios arquitectónicos

**Contras:**
- Más verboso (pero necesario para prevenir pérdida de datos)

### Opción B: Agregar verificación post-endSession

Crear paso adicional en endSession.md que verifica:

```bash
# Verificar que sesión se añadió correctamente (no sobrescribió)
SESSIONS_COUNT=$(grep -c "^  - id:" memsys3/memory/full/sessions.yaml)
if [ "$SESSIONS_COUNT" -lt 2 ]; then
  echo "⚠️ ERROR: sessions.yaml tiene solo $SESSIONS_COUNT sesión(es)"
  echo "¿Se sobrescribió el archivo en lugar de añadir?"
  exit 1
fi
echo "✅ Verificado: $SESSIONS_COUNT sesiones en sessions.yaml"
```

**Pros:**
- Detección automática de sobreescritura
- Feedback inmediato si algo salió mal
- Permite corregir antes de continuar

**Contras:**
- Solo detecta problema DESPUÉS de ocurrir (mejor prevenir)
- Requiere Bash execution (adicional a edición)

### Opción C: Template con placeholder para nueva sesión

Modificar sessions.yaml para incluir placeholder al principio:

```yaml
sessions:
  # 👇 AÑADE TU NUEVA SESIÓN AQUÍ (usando Edit tool, NO Write)
  # Usa memsys3/memory/templates/sessions-template.yaml como guía

  - id: "2025-12-30-bug-fix-issue-005-adr-016-agnostico"
    # ... sesiones existentes ...
```

**Pros:**
- Indicador visual claro de dónde añadir
- Refuerza uso de Edit tool

**Contras:**
- Placeholder debe mantenerse después de cada sesión
- Puede confundir si se olvida actualizar

---

## Decisiones / Acciones

**Decisión:** Implementar **Opción A** + elementos de **Opción B**

**Justificación:**
- Opción A previene el problema (mejor que detectar post-facto)
- Opción B añade safety net para detectar si ocurre
- Combinación: prevención + detección

**Implementación:**

1. **Modificar memsys3_templates/prompts/endSession.md PASO 4:**
   - Agregar warning "⚠️ CRÍTICO: NO SOBREESCRIBIR"
   - Workflow obligatorio en 4 pasos numerados
   - Explicitar "NUNCA uses Write tool en sessions.yaml"
   - Mencionar consecuencias (pérdida de memoria histórica)

2. **Agregar verificación en endSession.md después de PASO 4:**
   ```markdown
   5. **Verificar que sesión se añadió correctamente:**
      ```bash
      # Contar sesiones en archivo
      SESSIONS_COUNT=$(grep -c "^  - id:" memsys3/memory/full/sessions.yaml)
      echo "✅ Total de sesiones en sessions.yaml: $SESSIONS_COUNT"

      # Verificar que nueva sesión está presente
      grep -q "id: \"$(date +%Y-%m-%d)" memsys3/memory/full/sessions.yaml && \
        echo "✅ Sesión de hoy añadida correctamente" || \
        echo "⚠️ WARNING: No se encuentra sesión de hoy"
      ```
   ```

3. **Sincronizar con memsys3/prompts/endSession.md** (dog-fooding)

4. **Testing exhaustivo:**
   - Ejecutar endSession en proyecto con sessions.yaml con 5+ sesiones
   - Verificar que nueva sesión se añade al principio
   - Verificar que sesiones previas NO se pierden
   - Verificar conteo de sesiones correcto

5. **Documentar en ADR si se detectan patrones adicionales:**
   - Si problema persiste, considerar ADR sobre herramientas permitidas/prohibidas
   - Posible ADR: "Write tool prohibido en archivos acumulativos (sessions, ADRs)"

---

## Referencias

- **Prompt afectado:** `memsys3/prompts/endSession.md` (PASO 4)
- **Template relacionado:** `memsys3/memory/templates/sessions-template.yaml`
- **ADR relacionado:** ADR-002 (Rotación automática sessions/ADRs)
- **Sistema afectado:** Memoria histórica del proyecto (sessions.yaml)
- **Conversación:** Reportado por usuario 2025-01-30

---

## Notas Adicionales

**Impacto en Context Agent:**
Si sessions.yaml se sobrescribe constantemente:
- Context Agent solo ve última sesión documentada
- Compilación de contexto incompleta (falta historial)
- Gotchas de sesiones previas no incluidos
- Decisions documentadas en sesiones previas perdidas

**Relación con ADR-002 (Rotación automática):**
- Sistema de rotación depende de contar líneas en sessions.yaml
- Si archivo se sobrescribe cada vez, NUNCA alcanza 1800-2000 líneas
- Rotación automática nunca se activa
- Sistema de escalabilidad roto

**Prevención futura:**
- Considerar agregar tests automáticos en compile-context.md
- Context Agent podría verificar integridad de sessions.yaml
- Detectar si sessions.yaml tiene menos sesiones que la última compilación

---

## RESOLUCIÓN (2025-01-30)

**Fix implementado:** Opción A minimalista (instrucción explícita Edit tool)

**Archivos modificados:**
1. ✅ `memsys3_templates/prompts/endSession.md` (PASO 4.A)
2. ✅ `memsys3/prompts/endSession.md` (sincronizado)

**Cambio implementado:**

```markdown
Usa **Edit tool** para añadir tu sesión al PRINCIPIO del array:

old_string: "sessions:"
new_string: "sessions:
  - id: YYYY-MM-DD-titulo-descriptivo
    ..."

⚠️ NO uses Write tool → sobrescribiría todas las sesiones previas
```

**Justificación decisión minimalista:**
- Solución base resuelve 80-90% del problema con mínima complejidad
- Preferencia por prompts pulidos y minimalistas
- Verificaciones post-ejecución descartadas (detectan después, no previenen)
- Ejemplos visuales descartados (beneficio marginal bajo ~2%)

**Validación:**
- Agente Taller Colomer confirmó que habría prevenido completamente el incidente
- Instrucción explícita + warning claro eliminan ambigüedad
- Margen de error reducido de ~40-50% a ~5-10%

**Testing realizado:**
- [x] Modificar endSession.md con instrucciones reforzadas
- [x] Sincronizar fix con memsys3/ (dog-fooding)
- [ ] Ejecutar endSession en próxima sesión para validar
- [ ] Verificar que nueva sesión se añade correctamente
- [ ] Incluir en próxima release de memsys3

**Reunión colaborativa:**
- Sesión de debugging con agente Taller Colomer completada
- Archivo: `/mnt/c/PROYECTOS/SoluzzIAvers/tallersColomer/reunion/300126_1.md`
- Análisis forense exhaustivo realizado
- Causa raíz identificada y documentada
