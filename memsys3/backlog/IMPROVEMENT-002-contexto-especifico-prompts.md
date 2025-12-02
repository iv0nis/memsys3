# IMPROVEMENT-002: Contexto específico por prompt

**Estado:** Propuesto
**Prioridad:** Media
**Tipo:** Improvement
**Plazo:** Medio plazo
**Fecha identificación:** 2025-11-17

---

## Problema / Necesidad

Actualmente, **newSession.md** carga el contexto "general" del proyecto (context.yaml completo, project-status.yaml, main-agent.yaml). Sin embargo, algunos prompts pueden tener necesidades de contexto muy específicas que difieren del contexto general:

- **compile-context.md**: Necesita leer TODO memory/full/ (~50K tokens). Ya se ejecuta en instancia limpia por ADR-008, por lo que NO necesita newSession
- **endSession.md**: Necesita leer sessions-template.yaml, sessions.yaml actual, posiblemente ADRs recientes. Probablemente NO necesita todo context.yaml
- **deploy.md**: Necesita entender estructura templates, workflow. Podría necesitar solo project-status básico
- **actualizar.md**: Necesita entender versiones memsys3, estructuras. Contexto específico de "actualización"
- **backlog.md**: Necesita backlog/README.md + items del backlog (ya hace lectura selectiva)

**Problema detectado:**
- Algunos prompts pueden estar cargando contexto innecesario (desperdicio de tokens)
- Otros prompts pueden carecer de contexto específico que necesitan
- No hay una estrategia clara de "qué contexto necesita cada prompt"

## Propuesta / Opciones

**Opción A: Prompts con "Pre-requisitos" explícitos**
Cada prompt especifica al inicio qué debe leer:
```markdown
# Prerequisitos
- NO ejecutar newSession.md (instancia limpia)
- Leer: memory/full/sessions.yaml, memory/full/adr.yaml, ...
```

**Pros:**
- Explícito y claro
- Flexible por prompt
- No modifica arquitectura existente

**Contras:**
- Cada prompt debe documentar sus necesidades
- Puede generar inconsistencias

---

**Opción B: Diferentes niveles de newSession**
Crear variantes de newSession según necesidad:
- `newSession-light.md`: Solo project-status
- `newSession-full.md`: context.yaml completo (actual)
- `newSession-compile.md`: Para compile-context específicamente

**Pros:**
- Reutilizable entre prompts
- Estandariza niveles de contexto
- Optimización clara de tokens

**Contras:**
- Más archivos que mantener
- User debe saber cuál usar
- Duplicación de lógica

---

**Opción C: Sistema "contexto mínimo + específico"**
newSession carga solo un mínimo común, cada prompt carga adicionales según necesidad:
- newSession.md: Solo project-status.yaml (mínimo)
- Cada prompt: Lee lo específico que necesita

**Pros:**
- Máxima optimización tokens
- Cada prompt autocontenido
- Evita duplicación

**Contras:**
- Prompts más largos
- Más difícil mantener coherencia

---

**Opción D: Prompts completamente autocontenidos**
Algunos prompts incluyen sus instrucciones de carga de contexto completas, sin depender de newSession:

**Pros:**
- Máxima independencia
- Claro qué lee cada prompt
- Fácil de entender

**Contras:**
- Duplicación significativa
- Difícil sincronizar cambios

## Decisiones / Acciones

**Pendiente de análisis detallado:**
1. Revisar cada prompt actual y documentar qué contexto REALMENTE necesita
2. Identificar casos donde se carga contexto innecesario
3. Identificar casos donde falta contexto específico
4. Evaluar opciones con casos reales
5. Decidir aproximación más coherente con filosofía memsys3

**No urgente** - sistema actual funciona correctamente. Es una optimización de eficiencia y claridad.

## Referencias

- Conversación: 2025-11-17 (Session inicio, observación sobre contexto prompts)
- Related: newSession.md, compile-context.md, endSession.md, deploy.md, actualizar.md, backlog.md
- ADR-008: Main-Agent NO debe proponer compile-context (restricción contexto)
