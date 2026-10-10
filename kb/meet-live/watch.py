#!/usr/bin/env python3
"""Espera el siguiente turno de OTRO participante e imprime los turnos nuevos COMPLETOS.

Uso:  python3 watch.py Agent-miproyecto [--max-min 55]
Pensado para lanzarse en segundo plano: sale en cuanto alguien que no eres tú escribe
(espera 8 s más por si llegan varios seguidos). Código de salida 0 = hay turno; 2 = timeout;
3 = el servidor no responde. MEET_URL por defecto http://localhost:3077.
"""
import json
import os
import sys
import time
import urllib.request

URL = os.environ.get("MEET_URL", "http://localhost:3077") + "/api/messages"


def get():
    return json.load(urllib.request.urlopen(URL, timeout=10))


def who(m):
    return m.get("author") or m.get("agent_id") or m.get("role")


def main():
    args = sys.argv[1:]
    if not args:
        sys.exit("uso: watch.py <agent_id> [--max-min N]")
    me = args[0]
    limit = float(args[args.index("--max-min") + 1]) * 60 if "--max-min" in args else 55 * 60
    mine = lambda m: m.get("agent_id") == me
    try:
        seen = len(get())
    except OSError as e:
        print("servidor no responde:", e)
        sys.exit(3)
    t0 = time.time()
    while time.time() - t0 < limit:
        try:
            msgs = get()
        except OSError as e:
            print("servidor no responde:", e)
            sys.exit(3)
        if any(not mine(m) for m in msgs[seen:]):
            time.sleep(8)
            for m in get()[seen:]:
                if not mine(m):
                    print(f"## {m['ts'][11:16]} · {who(m)}\n\n{m['text']}\n")
            sys.exit(0)
        seen = len(msgs)
        time.sleep(4)
    print("timeout: nadie ha escrito")
    sys.exit(2)


if __name__ == "__main__":
    main()
