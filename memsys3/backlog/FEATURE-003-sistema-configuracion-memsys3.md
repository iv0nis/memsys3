# FEATURE-003: Sistema de configuración centralizada para memsys3

**Estado:** Propuesto
**Prioridad:** Alta
**Tipo:** Feature
**Plazo:** Corto plazo
**Fecha identificación:** 2025-12-16

---

## Problema / Necesidad

memsys3 actualmente tiene **valores hardcodeados** en múltiples archivos que asumen límites específicos de contexto y tokens:

- **Límites de líneas:** sessions.yaml/adr.yaml rotan en 1800-2000 líneas (asume Read tool límite 2000)
- **Context Agent:** context.yaml máximo 2000 líneas (~2000-3000 tokens)
- **Rotación flexible:** umbrales 1800 (Escenario A) vs 2000 (Escenario B)
- **Plan de Contingencia:** activa archivado cuando >150K tokens

**Problema:** Diferentes modelos y planes de LLM tienen capacidades distintas:
- Claude Sonnet 4.5: 200K tokens de contexto
- Claude Haiku: 100K tokens de contexto (menor)
- Otros modelos: pueden variar significativamente

**Consecuencia:** memsys3 no es fácilmente adaptable a diferentes entornos sin modificar manualmente múltiples archivos.

**Necesidad:** Sistema de configuración centralizada que permita ajustar memsys3 según las capacidades del modelo/plan utilizado.

---

## Propuesta / Opciones

### Opción A: Archivo de configuración YAML (config.yaml)

Crear `memsys3/config/memsys3-config.yaml` con todos los parámetros configurables:

```yaml
# Configuración memsys3
modelo: "Claude Sonnet 4.5"
contexto_maximo: 200000  # tokens

limites_documentos:
  sessions_yaml_rotacion_minimo: 1800
  sessions_yaml_rotacion_maximo: 2000
  adr_yaml_rotacion_minimo: 1800
  adr_yaml_rotacion_maximo: 2000

context_agent:
  context_yaml_lineas_maximo: 2000
  context_yaml_tokens_estimado: 3000
  readme_lineas_maximo: 300
  adrs_maximo: 7
  gotchas_maximo: 5
  pendientes_maximo: 5

plan_contingencia:
  threshold_tokens: 150000
  target_reduction_tokens: 120000

newSession:
  tokens_carga_inicial_estimado: 12000  # context.yaml + project-status + README
```

**Pros:**
- Configuración centralizada en un solo lugar
- Fácil de ajustar sin modificar código
- Puede incluir perfiles predefinidos (small, medium, large)

**Contras:**
- Todos los prompts/agents deben leer este archivo
- Requiere modificar lógica existente para usar config

### Opción B: Prompt interactivo config-memsys3.md

Crear `memsys3/prompts/config-memsys3.md` que:
1. Pregunta al usuario sobre su modelo/plan
2. Calcula límites apropiados según capacidad
3. Actualiza archivos relevantes (context-agent.yaml, etc.)

**Pros:**
- Más simple de implementar inicialmente
- Guiado para usuarios no técnicos
- No requiere lógica de lectura de config en todos los prompts

**Contras:**
- Configuración dispersa en múltiples archivos
- Requiere re-ejecutar si cambias de modelo

### Opción C: Sistema de perfiles predefinidos

Crear múltiples versiones de configuración:
- `memsys3/config/profiles/small.yaml` (modelos 50-100K tokens)
- `memsys3/config/profiles/medium.yaml` (modelos 100-200K tokens)
- `memsys3/config/profiles/large.yaml` (modelos 200K+ tokens)

Prompt `config-memsys3.md` copia el perfil apropiado.

**Pros:**
- Balance entre flexibilidad y simplicidad
- Perfiles testeados y validados
- Fácil de elegir

**Contras:**
- Menos flexible para casos específicos
- Requiere mantener múltiples perfiles

---

## Parámetros Configurables Identificados

### 1. Límites de Documentos (full/)
- `sessions.yaml` rotación: min/max líneas
- `adr.yaml` rotación: min/max líneas

### 2. Context Agent (context-agent.yaml)
- `context.yaml` máximo líneas
- README máximo líneas en contexto
- Máximo ADRs incluidas
- Máximo gotchas incluidos
- Máximo pendientes incluidos

### 3. Plan de Contingencia
- Threshold para activar archivado (tokens)
- Target de reducción (tokens)

### 4. newSession.md
- Tokens estimados de carga inicial
- Advertencias si modelo tiene poco contexto

### 5. Rotación Automática (ADR-002)
- Escenario A: umbral mínimo (actualmente 1800)
- Escenario B: umbral máximo (actualmente 2000)

---

## Aproximación Recomendada (Fase 1)

**Implementar Opción B (Prompt interactivo) como testeo:**

1. Crear `memsys3/prompts/config-memsys3.md` (prompt guiado)
2. Pregunta:
   - ¿Qué modelo/plan usas?
   - ¿Cuál es tu límite de contexto? (ej: 200K, 100K)
3. Calcula y ajusta:
   - Límites en `context-agent.yaml`
   - Umbrales de rotación en documentación (endSession.md)
   - Advertencias en newSession.md
4. Genera reporte de configuración aplicada

**Testing:**
- Validar con Claude Sonnet 4.5 (200K tokens)
- Validar con Claude Haiku (100K tokens)
- Documentar en ADR si funciona correctamente

**Fase 2 (futuro):**
Si funciona bien, evolucionar a Opción C (perfiles predefinidos) para distribución.

---

## Decisiones / Acciones

**Pendiente de implementación.**

Plan propuesto:
1. Crear prompt `config-memsys3.md` como prueba de concepto
2. Testear ajustando configuración para modelo pequeño (ej: Haiku)
3. Validar que memsys3 funciona correctamente con límites reducidos
4. Documentar en ADR si se aprueba la aproximación
5. Considerar evolución a sistema de perfiles (Opción C) si testing exitoso

---

## Referencias

- **Context Agent:** `memsys3/agents/context-agent.yaml` (límites hardcodeados)
- **ADR-002:** Rotación automática (umbrales 1800-2000 líneas)
- **ADR-003:** Plan de Contingencia (threshold 150K tokens)
- **endSession.md:** Referencias a escenarios de rotación
- **Sesión propuesta:** 2025-12-16

---

## Archivos Afectados

Archivos que contienen valores hardcodeados a actualizar:

1. `memsys3/agents/context-agent.yaml` (líneas 40, 58-124)
2. `memsys3/prompts/endSession.md` (referencias a 1800/2000 líneas)
3. `memsys3/prompts/compile-context.md` (referencias a límites)
4. `memsys3_templates/` (mismos archivos en versión distribuible)

---

## Casos de Uso

### Caso 1: Usuario con Claude Haiku (100K contexto)
- Reducir `context.yaml` a ~1000 líneas (~1500 tokens)
- Rotación a 900-1000 líneas (vs 1800-2000)
- Plan Contingencia a 75K tokens (vs 150K)

### Caso 2: Usuario con modelo grande (500K contexto)
- Aumentar `context.yaml` a ~5000 líneas (~7500 tokens)
- Rotación a 4500-5000 líneas
- Plan Contingencia a 350K tokens

### Caso 3: Proyecto pequeño vs grande
- Proyecto pequeño: límites más altos (mantener todo en memoria)
- Proyecto grande: límites más estrictos (filtrar agresivamente)
