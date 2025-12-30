# IMPROVEMENT-005: Detectar versión memsys3 desde project-status.yaml como primera opción

**Estado:** Propuesto
**Prioridad:** Baja
**Tipo:** Improvement (UX)
**Plazo:** Medio plazo
**Fecha identificación:** 2025-12-15

---

## Problema / Necesidad

Durante el testing de `/actualizar-memsys3` en proyecto UOC (sesión 2025-12-15), se detectó que Claude intentó detectar la versión actual de memsys3 usando `git describe` antes de consultar `project-status.yaml`.

### Comportamiento Actual

1. Claude ejecuta `git describe --tags --always --dirty` en el directorio de trabajo
2. Intenta varios comandos git buscando la versión
3. **Después de varios intentos**, el usuario le indica que mire `project-status.yaml`
4. Claude finalmente encuentra la versión correcta en `memsys3_version: "v0.6.1-2-g181742f"`

### Problemas Identificados

1. **Ineficiencia:** Múltiples comandos git innecesarios antes de ir a la fuente de verdad
2. **Confusión:** `git describe` puede devolver versión del proyecto principal, no de memsys3
3. **UX subóptima:** Usuario debe intervenir para indicar dónde está la información
4. **Inconsistencia:** `project-status.yaml` es la fuente de verdad del deployment de memsys3, no git

### Contexto

- **project-status.yaml** contiene `metadata.memsys3_version` y `metadata.memsys3_deployed`
- Estos campos se actualizan durante deployment (`/deploy-memsys3`) y actualización (`/actualizar-memsys3`)
- Es la **fuente de verdad oficial** del sistema memsys3 desplegado en un proyecto

## Propuesta / Opciones

### ✅ Opción Recomendada: project-status.yaml como fuente primaria

**Cambio en prompts/actualizar.md (PASO 1):**

```markdown
PASO 1: Detectar Versión Actual

Detecta la versión de memsys3 instalada:

1. **PRIMERO: Consultar project-status.yaml**
   ```bash
   grep "memsys3_version:" memsys3/memory/project-status.yaml
   grep "memsys3_deployed:" memsys3/memory/project-status.yaml
   ```
   - Si existe: usar esta versión (es la fuente de verdad oficial)

2. **FALLBACK: Si project-status.yaml no existe o no tiene memsys3_version:**
   ```bash
   cd memsys3 && git describe --tags --always --dirty 2>/dev/null || echo "Sin información de versión"
   ```
   - Útil solo para deployments muy antiguos (pre-v0.6.0)

**Reportar:**
- Versión detectada: vX.X.X
- Fuente: project-status.yaml (o fallback git si aplica)
- Fecha deployment: YYYY-MM-DD
```

### Ventajas

1. **Más eficiente:** Un solo grep en lugar de múltiples intentos git
2. **Más confiable:** project-status.yaml es fuente de verdad, no puede estar desactualizado
3. **Mejor UX:** Encuentra versión en primer intento, sin intervención usuario
4. **Consistente:** Refuerza que project-status.yaml es metadato oficial
5. **Menos errores:** Evita confusión con versiones git del proyecto principal

### Desventajas

1. **Deployments muy antiguos:** Si proyecto tiene memsys3 desplegado antes de que existiera `memsys3_version` en metadata
   - Mitigación: Fallback a git describe si no encuentra field
2. **Archivo corrupto:** Si project-status.yaml está mal formado
   - Mitigación: Fallback a git describe

---

### Alternativa A: git describe como primera opción (status quo)

**Pros:**
- Ya implementado
- Funciona en cualquier deployment con .git

**Contras:**
- ⚠️ Ineficiente (múltiples comandos)
- ⚠️ Puede devolver versión incorrecta (proyecto principal)
- ⚠️ Requiere intervención usuario en algunos casos

---

### Alternativa B: Hybrid approach (git + project-status)

Consultar ambos y comparar:

**Pros:**
- Validación cruzada
- Detecta inconsistencias

**Contras:**
- Más complejo
- Overhead innecesario (project-status.yaml ES la verdad)

## Decisiones / Acciones

### Archivos a Modificar

Si se implementa Opción Recomendada:

1. **memsys3_templates/prompts/actualizar.md**
   - PASO 1: Cambiar orden (project-status primero, git fallback)
   - Documentar que project-status.yaml es fuente de verdad

2. **Posiblemente: memsys3_templates/prompts/deploy.md**
   - Si también tiene lógica de detección de versión (verificar)
   - Aplicar mismo patrón por consistencia

3. **ADR nueva (opcional, baja prioridad):**
   - Si se considera decisión arquitectónica
   - Título: "project-status.yaml como fuente de verdad para metadata memsys3"
   - Justificación: consistencia, eficiencia, UX

### Testing

Antes de implementar:
- [ ] Verificar si deploy.md también intenta detectar versión
- [ ] Validar comportamiento con deployments antiguos (pre-v0.6.0)
- [ ] Confirmar que fallback a git describe funciona si no hay memsys3_version

Después de implementar:
- [ ] Testear actualización en proyecto con project-status.yaml válido
- [ ] Testear actualización en proyecto sin memsys3_version (simular antiguo)
- [ ] Verificar que no hay múltiples comandos git innecesarios

### Prioridad: Baja

- **NO bloqueante:** Sistema actual funciona (con intervención usuario)
- **Mejora UX:** Reduce friction y comandos innecesarios
- **Relativamente simple:** ~10-20 líneas modificadas en actualizar.md
- **Impacto:** Solo afecta PASO 1 de actualizar.md, resto del flujo igual

## Referencias

- **Conversación:** 2025-12-15 (Testing /actualizar-memsys3 en proyecto UOC)
- **Sesión documentada:** sessions.yaml "2025-12-15-testing-actualizar-memsys3"
- **Problema observado:** Claude intentó git describe antes de consultar project-status.yaml
- **Solución sugerida:** Usuario indicó "solo te hace falta mirar @memsys3/memory/project-status.yaml para saber la version"
- **Meta-aprendizaje:** "project-status.yaml debería ser primera fuente consultada para detectar versión, no git describe"
- **ADRs relacionadas:** ADR-014 (sistema comandos globales), potencial nueva ADR sobre metadata
- **Archivos afectados:** actualizar.md, posiblemente deploy.md

---

## Notas Adicionales

### Campos Relevantes en project-status.yaml

```yaml
metadata:
  memsys3_version: "v0.8.1"      # ← Fuente de verdad de versión instalada
  memsys3_deployed: "2025-10-28"  # ← Fecha deployment original
```

Estos campos se actualizan automáticamente en:
- **PASO 7 de actualizar.md:** Actualiza memsys3_version y memsys3_deployed
- **deploy.md:** Inicializa memsys3_version y memsys3_deployed en primer deployment

### Evolución Histórica

- **Pre-v0.6.0:** project-status.yaml no tenía campos memsys3_version/memsys3_deployed
- **v0.6.0+:** Campos añadidos, se actualizan durante deploy/actualizar
- **v0.8.1:** Testing reveló que git describe se consulta antes que project-status.yaml

Por tanto, la mejora tiene sentido: reforzar que project-status.yaml es la fuente oficial desde v0.6.0 en adelante.
