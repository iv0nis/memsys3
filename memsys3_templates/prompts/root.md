# root — Volver a la raíz de la sesión

> Ejecútalo con `memsys3/prompts/root.md` (o `@memsys3/prompts/root.md` / `/root` en harnesses con atajos).

**Problema que resuelve.** Un `cd` dentro de un comando persiste y mueve el directorio de trabajo de la sesión. A partir de ahí, las rutas relativas fallan, el autocompletado de `@` muestra rutas raras (`../../memsys3/...`) y los prompts de memsys3 no se encuentran. Este prompt lo deshace.

**Haz AHORA, en este orden:**

1. Identifica el directorio con el que **arrancó esta sesión**. Tu harness te lo dio al inicio (directorio de trabajo principal) y te avisa cuando cambia. Ese es el destino: **no** el `memsys3/` más cercano (en monorepos hay memsys3 anidados y el más cercano puede ser el de otro proyecto).
2. Ejecuta un `cd` real a ese directorio y confirma:

   ```bash
   cd "<directorio de arranque>" && pwd
   ```

3. Si no sabes cuál era (compact, sesión larga): sube directorios hasta el primero que contenga `memsys3/memory/project-status.yaml` y **pregunta al usuario** si es el correcto antes de darlo por bueno.

Responde solo con el `pwd` resultante.

**Prevención.** En adelante no cambies de directorio con `cd` en los comandos: usa rutas absolutas o guarda la raíz una vez (`R=$(pwd)`) y trabaja con `$R/...`.

<!-- version: 0.1.0 -->
