# EXPLORATION-003: READMEs modulares por carpeta como memoria lazy-loaded

**Estado:** Propuesto
**Prioridad:** Media
**Tipo:** Exploration
**Plazo:** Long-term
**Fecha identificación:** 2026-04-20
**Origen:** Práctica personal del usuario en agente de productividad con muchas carpetas

---

## Observación

El usuario está probando con buenos resultados un patrón en un agente de productividad con múltiples carpetas:

- Cada carpeta tiene su propio `README.md`
- El agente **no** carga contexto completo de toda la estructura al arrancar
- Cuando entra a una carpeta concreta, lee el README de esa carpeta
- Ese README puede referenciar otros docs dentro de la misma carpeta (profundidad mayor bajo demanda)

**Resultado reportado por el usuario:** funciona muy bien para modularizar la memoria.

---

## Por qué es interesante para memsys3

memsys3 actualmente opera con un modelo **centralizado**:
- `context.yaml` compilado (todo el contexto histórico relevante)
- `project-status.yaml` (estado global)
- `README.md` raíz (identidad actual)

Esto funciona muy bien en proyectos pequeños/medianos, pero:
- En proyectos con muchas áreas/módulos/carpetas, el context.yaml compilado tiene que sintetizar todo en 2000 líneas
- Áreas que el agente no toca esa sesión siguen ocupando tokens
- No hay lazy loading: todo se carga al inicio de sesión vía newSession.md

El patrón que describe el usuario es **memoria lazy-loaded por proximidad**: la carpeta en la que estás trabajando te da contexto, sin imponer contexto de carpetas que no tocas.

---

## Paralelismo con otros sistemas

- **CLAUDE.md anidados de Claude Code:** Claude Code ya soporta múltiples `CLAUDE.md` en subcarpetas y los carga según el scope de trabajo. El patrón del usuario es la versión agnóstica y más rica.
- **Documentación cercana al código** (principio clásico): el doc vive donde vive lo que documenta.
- **Engram / graph-based memory:** nodos conectados, navegación bajo demanda. Este patrón es la versión plana basada en filesystem.

---

## Preguntas a explorar

1. **¿Encaja en memsys3 core o es un patrón que memsys3 debería recomendar sin imponer?**
   - Si core: cambio significativo en filosofía (centralizado → distribuido)
   - Si recomendación: doc en `memsys3/docs/` explicando cuándo aplicarlo

2. **¿Cómo convive con context.yaml?**
   - Opción a) context.yaml sigue siendo el "índice global" y READMEs locales son profundización bajo demanda
   - Opción b) context.yaml se simplifica a solo metadata del proyecto + referencias a READMEs locales
   - Opción c) coexisten sin integración formal — el agente decide qué leer según la carpeta activa

3. **¿Cómo sabe el agente qué README leer?**
   - Por `pwd` al arrancar sesión
   - Por tarea explícita del usuario ("trabajamos en la carpeta X")
   - Por convención: newSession.md lee README raíz, y ese README tiene "mapa" de subcarpetas

4. **¿Requiere prompt nuevo o solo instrucción en newSession.md / main-agent.yaml?**

5. **¿Hay umbral de tamaño/complejidad a partir del cual tiene sentido?**
   - En proyectos pequeños probablemente es overhead
   - En agentes de productividad con muchas áreas (trabajo, personal, proyectos paralelos) parece ganar

---

## Caso real (a documentar con más detalle)

Usuario lo usa en su agente de productividad con múltiples carpetas, cada una con su README y posibles docs referenciados desde ahí. Pendiente: recopilar ejemplo concreto (estructura, README de ejemplo, cómo referencian docs internos) para tener caso de estudio real antes de decidir si integrarlo.

---

## Relación con otros items

- **ISSUE-021 (auto-memory vs memsys3) + Opción D (MEMORY_memsys3.yaml):** ambos comparten la pregunta "¿cómo estructuramos la memoria más allá de context.yaml?". Si se implementan juntos, hay que diseñar la integración.
- **IMPROVEMENT-001 (docs críticos en contexto):** este patrón es una forma de resolverlo sin inflar context.yaml.
- **ADR-012 (README lectura directa):** ya estableció que README se lee directamente. Este exploration extiende el principio a READMEs anidados.

---

## Próximos pasos

1. Recopilar ejemplo real del agente de productividad del usuario (estructura + READMEs de muestra)
2. Evaluar si pilotarlo en un proyecto memsys3 concreto (dog-fooding en el propio memsys3 o en otro proyecto desplegado)
3. Decidir si se integra en el core, se queda como patrón recomendado en docs, o se descarta
