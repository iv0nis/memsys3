# meet-live — reuniones en vivo para `meet.md`

Extensión opcional de memsys3. Añade a `memsys3/prompts/meet.md` un transporte en vivo: un servidor local lleva los turnos, una web muestra la conversación a los humanos y los agentes escriben por HTTP. Sin él, la reunión funciona igual por archivo.

- **Requisitos:** Python 3 (solo biblioteca estándar) y un agente con shell. Nada que instalar.
- **Cuándo usarla:**
  - **Coordinar agentes de distintas herramientas en tu máquina** (Claude Code con Codex CLI, Gemini CLI…): basta con que cada agente pueda ejecutar comandos; el canal es HTTP local y no depende de que la herramienta sepa hablar con otras sesiones.
  - **Reuniones con humanos**, que las siguen y escriben desde el navegador, también desde fuera de tu máquina (túnel).
- **La web:** cada interlocutor con su color; a la derecha, en pantallas de ordenador, el hilo de la reunión (un turno por línea) con las líneas que empiezan por `Decisión:` o `Pregunta:` resaltadas. Se puede plegar.

## Instalar

Desde la raíz del proyecto:

```bash
mkdir -p .meet-live && cd .meet-live
for f in meet_server.py meet.html say.py watch.py acta.py; do
  curl -sLO "https://raw.githubusercontent.com/iv0nis/memsys3/master/kb/meet-live/$f"
done
```

Añade `.meet-live/` a tu `.gitignore`: ahí se guardan los turnos de cada reunión.

## Usar

```bash
cd .meet-live
rm -f meet_messages.json           # sala vacía (no lo borres si retomas una reunión cortada)
python3 meet_server.py             # http://localhost:3077   (MEET_PORT para otro puerto)
```

El agente arranca el servidor en segundo plano y abre `http://localhost:3077` para el moderador.

| Quién | Cómo |
|---|---|
| Agente, hablar | `python3 say.py Agent-miproyecto <<'EOF'` … `EOF` (pide la palabra, escribe, la suelta) |
| Agente, esperar | `python3 watch.py Agent-miproyecto` en segundo plano: sale con los turnos nuevos de otros, completos |
| Humano | la web: nombre en la casilla, texto, Ctrl/Cmd+Enter |
| Cerrar | `python3 acta.py meet_messages.json "Objetivo" > ../memsys3/docs/meets/AAAAMMDD_N.md`, completar la Decisión y parar el servidor |

Para parar el servidor, mátalo por su PID o con `fuser -k 3077/tcp`. No uses `pkill -f meet_server`: si tu shell contiene ese texto, se mata a sí misma.

## Humanos fuera de esta máquina (túnel)

El servidor escucha solo en `127.0.0.1`. Para que entre alguien desde otro dispositivo, abre un túnel HTTP hacia `localhost:3077` y comparte el enlace que te dé. Vale cualquier túnel que añada la cabecera `X-Forwarded-For` (cloudflared, ngrok, Tailscale Funnel…). Ejemplo con cloudflared, sin cuenta:

```bash
: > /tmp/cf-empty.yml
cloudflared --config /tmp/cf-empty.yml tunnel --no-autoupdate --protocol http2 --url http://localhost:3077
# el enlace https://….trycloudflare.com sale en el log a los pocos segundos
```

- **Config vacío.** Si tienes un `~/.cloudflared/config.yml` con `ingress` propio, el túnel rápido lo hereda y da 404.
- **http2.** El protocolo por defecto (QUIC) se cae en algunas redes y VPN.
- **Un enlace por reunión.** El túnel rápido genera un enlace nuevo cada vez y muere al pararlo.
- **Permisos.** Tu agente puede necesitar que apruebes abrir el túnel: expone un puerto local a internet.
- **Comprobar.** Espera a que `curl -s -o /dev/null -w '%{http_code}' <enlace>/` dé `200` antes de compartirlo.

**Seguridad.** No hay contraseña: quien tenga el enlace lee la reunión y escribe como humano. Lo que llega por el túnel no puede cambiar el modo, suspender ni escribir como agente; eso solo se hace desde esta máquina. Comparte el enlace por un canal privado y para el túnel al acabar.

## Controles del moderador (solo en local)

- **Modo Libre / Moderación.** En libre, los agentes hablan por iniciativa. En moderación esperan; cuando el moderador escribe, responde el primer agente que coge la palabra y vuelve a esperar.
- **Suspender turnos.** Ningún agente escribe hasta reanudar.
- **Pedir turno.** El moderador se cuela un mensaje sin parar el flujo.

## API

| Ruta | Uso |
|---|---|
| `GET /api/messages` | todos los turnos: `role`, `text`, `ts`, `agent_id` o `author`, `to` |
| `GET /api/floor` | quién tiene la palabra, modo, suspensión y si quien pregunta es local |
| `POST /api/send` | turno humano `{text, author}` |
| `POST /api/claim` · `/api/agent` · `/api/release` | turno de agente: pedir, escribir `{agent, text, to?}`, soltar (solo local) |
| `POST /api/mode` · `/api/suspend` | controles del moderador (solo local) |

La palabra de un agente caduca a los 120 s si no escribe. Un `409` significa «espera».

<!-- version: 0.1.0 -->
