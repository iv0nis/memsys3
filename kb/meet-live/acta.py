#!/usr/bin/env python3
"""Convierte meet_messages.json en el acta .md de la reunión (mismo formato que el transporte
por archivo). El agente completa después el objetivo y la «Decisión (Moderador)».

Uso:  python3 acta.py meet_messages.json "Objetivo en una línea" > memsys3/docs/meets/AAAAMMDD_N.md
"""
import json
import sys


def main():
    if len(sys.argv) < 2:
        sys.exit("uso: acta.py meet_messages.json [objetivo]")
    msgs = json.load(open(sys.argv[1], encoding="utf-8"))
    if not msgs:
        sys.exit("no hay turnos")
    goal = sys.argv[2] if len(sys.argv) > 2 else "[objetivo]"
    day = msgs[0]["ts"][:10]
    agents = sorted({m["agent_id"] for m in msgs if m.get("agent_id")})
    humans = sorted({m["author"] for m in msgs if m.get("author")})
    out = [f"# Reunión {day.replace('-', '')}_N — {goal}", "",
           f"**Fecha:** {day} ({msgs[0]['ts'][11:16]}-{msgs[-1]['ts'][11:16]})",
           f"**Agentes:** {', '.join(agents) or '—'}",
           f"**Humanos:** {', '.join(humans) or '—'}",
           "**Moderador:** [nombre]",
           "**Transporte:** en vivo (meet-live)", "", "---", ""]
    for m in msgs:
        name = m.get("author") or m.get("agent_id") or ("humano" if m["role"] == "user" else "agente")
        if m.get("to"):
            name += f" → {m['to']}"
        out += [f"## {m['ts'][11:16]} · {name}", "", m["text"].rstrip(), ""]
    out += ["---", "", "## Decisión (Moderador)", "", "[Resolución, próximos pasos, quién hace qué]", "",
            f"**Fecha cierre:** {msgs[-1]['ts'][:10]}"]
    print("\n".join(out))


if __name__ == "__main__":
    main()
