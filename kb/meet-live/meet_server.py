#!/usr/bin/env python3
"""meet-live: servidor mínimo para reuniones en vivo de memsys3 (meet.md, transporte en vivo).

Solo biblioteca estándar de Python 3. Sirve meet.html y guarda los turnos en meet_messages.json
(en el directorio desde el que se arranca; MEET_MESSAGES para otra ruta). Puerto: MEET_PORT (3077).
Escucha solo en 127.0.0.1 (MEET_HOST para otra interfaz): desde fuera se entra por un túnel.

Acceso:
- LOCAL (navegador o agente en esta máquina): todo, incluidos los controles del moderador.
- REMOTO (por un túnel: la petición trae X-Forwarded-For, CF-Connecting-IP, X-Real-IP o
  Forwarded, o llega desde una IP no local): solo leer y escribir como humano (/api/send).

API:
- GET  /                -> meet.html
- GET  /api/messages    -> lista de turnos (JSON)
- GET  /api/floor       -> {holder, expires_in, hold, suspended, return_to, mode, local}
- POST /api/send        -> turno humano {"text", "author"}            (local y remoto)
- POST /api/claim       -> pedir la palabra {"agent", "hold"?}  200/409  (solo local)
- POST /api/agent       -> turno de agente {"text", "agent", "to"?}   (solo local; exige la palabra)
- POST /api/release     -> soltar la palabra {"agent", "force"?}      (solo local)
- POST /api/suspend     -> suspender/reanudar turnos de agentes {"on"} (solo local)
- POST /api/mode        -> {"mode": "libre"|"moderacion"}             (solo local)
"""
import ipaddress
import json
import os
import threading
import time
from datetime import datetime
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

ROOT = os.path.dirname(os.path.abspath(__file__))
HTML = os.path.join(ROOT, "meet.html")
MESSAGES = os.path.abspath(os.environ.get("MEET_MESSAGES", "meet_messages.json"))
PORT = int(os.environ.get("MEET_PORT", "3077"))
HOST = os.environ.get("MEET_HOST", "127.0.0.1")  # 0.0.0.0 para abrirlo a la red local
MAX_TEXT = 100_000  # caracteres por turno: los humanos pegan documentos enteros
LOCK = threading.Lock()

# --- Turno (floor token) ---
# holder     -> quién tiene la palabra (agent_id o MODERADOR)
# hold=True  -> el moderador retiene la palabra: no expira
# return_to  -> en modo moderación, al escribir un agente la palabra vuelve aquí
# suspended  -> STOP: ningún agente puede pedir la palabra ni escribir
# mode       -> "libre" (los agentes hablan por iniciativa) | "moderacion" (el moderador abre
#               la palabra al enviar; responde el primer agente que la coge y vuelve a él)
FLOOR_TTL = 120  # segundos: si un agente tiene la palabra y no escribe, se libera sola
FLOOR = {"holder": None, "expires": 0.0, "hold": False, "return_to": None,
         "suspended": False, "mode": "libre"}
MOD = "MODERADOR"
PROXY_HEADERS = ("X-Forwarded-For", "CF-Connecting-IP", "X-Real-IP", "Forwarded")


def _floor_now(now):
    """(holder, segundos_restantes|None, hold). Expira la palabra de un agente. Bajo LOCK."""
    if FLOOR["holder"] and not FLOOR["hold"] and now >= FLOOR["expires"]:
        if FLOOR["return_to"]:
            FLOOR.update(holder=FLOOR["return_to"], hold=True, return_to=None, expires=0.0)
        else:
            FLOOR.update(holder=None, hold=False, expires=0.0)
    if not FLOOR["holder"]:
        return None, 0, False
    left = None if FLOOR["hold"] else max(0, int(FLOOR["expires"] - now))
    return FLOOR["holder"], left, FLOOR["hold"]


def _after_agent_post():
    """Tras el turno de un agente: la palabra vuelve al moderador (moderación) o queda libre."""
    if FLOOR["return_to"]:
        FLOOR.update(holder=FLOOR["return_to"], hold=True, return_to=None, expires=0.0)
    else:
        FLOOR.update(holder=None, hold=False, expires=0.0)


def load():
    if not os.path.exists(MESSAGES):
        return []
    with open(MESSAGES, encoding="utf-8") as f:
        return json.load(f)


def _append_nolock(role, text, agent=None, to=None, author=None):
    msgs = load()
    now = datetime.now()
    # Doble envío: mismo texto humano y mismo autor en menos de 5 s -> se ignora.
    if role == "user" and msgs:
        last = msgs[-1]
        try:
            fresh = (now - datetime.strptime(last["ts"], "%Y-%m-%d %H:%M:%S")).total_seconds() < 5
        except (KeyError, ValueError):
            fresh = False
        if fresh and last.get("role") == "user" and last.get("text") == text \
                and last.get("author") == author:
            return
    entry = {"role": role, "text": text, "ts": now.strftime("%Y-%m-%d %H:%M:%S")}
    if agent:
        entry["agent_id"] = agent  # identidad por mensaje: slug de proyecto (Agent-memsys3)
    if to:
        entry["to"] = to
    if author:
        entry["author"] = author
    msgs.append(entry)
    tmp = MESSAGES + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(msgs, f, ensure_ascii=False, indent=2)
    os.replace(tmp, MESSAGES)


class Handler(BaseHTTPRequestHandler):
    def _reply(self, code, body, ctype="application/json"):
        data = body.encode("utf-8") if isinstance(body, str) else body
        self.send_response(code)
        self.send_header("Content-Type", ctype + "; charset=utf-8")
        self.send_header("Cache-Control", "no-store")
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def _json(self, code, obj):
        self._reply(code, json.dumps(obj, ensure_ascii=False))

    def _is_local(self):
        if any(self.headers.get(h) for h in PROXY_HEADERS):
            return False  # llega por un túnel o proxy
        try:
            return ipaddress.ip_address(self.client_address[0]).is_loopback
        except ValueError:
            return False

    def do_GET(self):
        if self.path == "/" or self.path.startswith("/index"):
            with open(HTML, encoding="utf-8") as f:
                self._reply(200, f.read(), "text/html")
        elif self.path.startswith("/api/messages"):
            with LOCK:
                msgs = load()
            self._json(200, msgs)
        elif self.path.startswith("/api/floor"):
            with LOCK:
                holder, left, hold = _floor_now(time.time())
                state = {"holder": holder, "expires_in": left, "hold": hold,
                         "suspended": FLOOR["suspended"], "return_to": FLOOR["return_to"],
                         "mode": FLOOR["mode"]}
            state["local"] = self._is_local()
            self._json(200, state)
        else:
            self._json(404, {"error": "not found"})

    def do_POST(self):
        length = int(self.headers.get("Content-Length", 0) or 0)
        raw = self.rfile.read(length).decode("utf-8", "replace") if length else "{}"
        try:
            data = json.loads(raw)
        except json.JSONDecodeError:
            data = {}
        text = (data.get("text") or "").strip()[:MAX_TEXT]
        agent = (data.get("agent") or "").strip()[:60]
        to = (data.get("to") or "").strip()[:60] or None

        if self.path.startswith("/api/send"):
            if not text:
                return self._json(400, {"error": "empty"})
            author = (data.get("author") or "").strip()[:40] or None
            if not author:
                ua = self.headers.get("User-Agent", "")
                dev = "móvil" if any(k in ua for k in ("Android", "iPhone", "Mobile")) else "ordenador"
                ip = self.headers.get("CF-Connecting-IP") or self.client_address[0]
                author = f"Sin nombre ({dev} …{ip[-4:]})"
            with LOCK:
                _append_nolock("user", text, author=author)
                if FLOOR["mode"] == "moderacion":
                    # El moderador acaba de hablar: abre la palabra a los agentes para UNA respuesta.
                    FLOOR.update(holder=None, hold=False, expires=0.0, return_to=MOD)
            return self._json(200, {"ok": True})

        if not self._is_local():
            return self._json(403, {"error": "solo local: controles y turnos de agente"})

        if self.path.startswith("/api/suspend"):
            on = bool(data.get("on"))
            with LOCK:
                FLOOR["suspended"] = on
                if on:
                    FLOOR["return_to"] = None
            self._json(200, {"ok": True, "suspended": on})

        elif self.path.startswith("/api/mode"):
            mode = data.get("mode")
            if mode not in ("libre", "moderacion"):
                return self._json(400, {"error": "mode inválido"})
            with LOCK:
                FLOOR.update(mode=mode, return_to=None, expires=0.0)
                if mode == "moderacion":
                    FLOOR.update(holder=MOD, hold=True)   # agentes en espera hasta que hable
                else:
                    FLOOR.update(holder=None, hold=False)
            self._json(200, {"ok": True, "mode": mode})

        elif self.path.startswith("/api/claim"):
            if not agent:
                return self._json(400, {"error": "agent requerido"})
            with LOCK:
                now = time.time()
                holder, left, _ = _floor_now(now)
                if data.get("hold"):
                    FLOOR.update(holder=agent, expires=now + FLOOR_TTL, hold=True)
                    self._json(200, {"ok": True, "holder": agent, "hold": True})
                elif FLOOR["suspended"]:
                    self._json(409, {"ok": False, "error": "suspended"})
                elif holder is None or holder == agent:
                    FLOOR.update(holder=agent, expires=now + FLOOR_TTL, hold=False)
                    self._json(200, {"ok": True, "holder": agent, "ttl": FLOOR_TTL})
                else:
                    self._json(409, {"ok": False, "holder": holder, "hold": FLOOR["hold"],
                                     "expires_in": left})

        elif self.path.startswith("/api/release"):
            with LOCK:
                holder, _, _ = _floor_now(time.time())
                if holder == agent or data.get("force"):
                    FLOOR.update(holder=None, expires=0.0, hold=False, return_to=None)
                    self._json(200, {"ok": True})
                else:
                    self._json(409, {"ok": False, "holder": holder})

        elif self.path.startswith("/api/agent"):
            if not agent or not text:
                return self._json(400, {"error": "agent y text requeridos"})
            with LOCK:
                if FLOOR["suspended"]:
                    return self._json(409, {"ok": False, "error": "suspended"})
                holder, left, _ = _floor_now(time.time())
                if holder != agent:
                    return self._json(409, {"ok": False, "error": "no-floor", "holder": holder,
                                            "expires_in": left})
                _append_nolock("agent", text, agent=agent, to=to)
                _after_agent_post()
            self._json(200, {"ok": True, "released": True})

        else:
            self._json(404, {"error": "not found"})

    def log_message(self, *args):
        pass


if __name__ == "__main__":
    print(f"meet-live en http://localhost:{PORT}  ·  turnos en {MESSAGES}", flush=True)
    ThreadingHTTPServer((HOST, PORT), Handler).serve_forever()
