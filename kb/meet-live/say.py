#!/usr/bin/env python3
"""Turno de agente: pide la palabra, escribe y la suelta.

Uso:  python3 say.py Agent-miproyecto <<'EOF'
      texto del turno
      EOF
Opcional: --to Agent-otro · MEET_URL (por defecto http://localhost:3077).
Espera hasta 4 min si otro tiene la palabra; si los turnos están suspendidos, lo dice y sale.
"""
import json
import os
import sys
import time
import urllib.error
import urllib.request

URL = os.environ.get("MEET_URL", "http://localhost:3077")


def post(path, data):
    req = urllib.request.Request(URL + path, data=json.dumps(data).encode(),
                                 headers={"Content-Type": "application/json"})
    try:
        return json.load(urllib.request.urlopen(req, timeout=10))
    except urllib.error.HTTPError as e:
        return json.load(e)


def main():
    args = sys.argv[1:]
    if not args:
        sys.exit("uso: say.py <agent_id> [--to <agent_id>] < texto")
    agent, to = args[0], None
    if "--to" in args:
        to = args[args.index("--to") + 1]
    text = sys.stdin.read().strip()
    if not text:
        sys.exit("texto vacío")
    for _ in range(80):
        r = post("/api/claim", {"agent": agent})
        if r.get("ok"):
            break
        if r.get("error") == "suspended":
            sys.exit("turnos suspendidos por el moderador: no se ha escrito nada")
        time.sleep(3)
    else:
        sys.exit("no se consiguió la palabra en 4 min: no se ha escrito nada")
    print(json.dumps(post("/api/agent", {"agent": agent, "text": text, "to": to}), ensure_ascii=False))


if __name__ == "__main__":
    main()
