#!/usr/bin/env python3
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
QUESTIONS_DIR = ROOT / "src/data/questions"
OUTPUT_FILE = ROOT / "src/data/questions.json"


def iter_leaf_files(base: Path):
    for p in base.rglob("*.json"):
        # Skip the unified file and any non-leaf helpers
        if p.name == "questions.json":
            continue
        yield p


def main() -> int:
    if not QUESTIONS_DIR.exists():
        print(f"No existe {QUESTIONS_DIR}")
        return 1

    combined = []
    for p in iter_leaf_files(QUESTIONS_DIR):
        try:
            data = json.loads(p.read_text(encoding="utf-8"))
            if not isinstance(data, list):
                print(f"[warn] {p} no contiene una lista; se omite")
                continue
        except Exception as e:
            print(f"[warn] No se pudo leer {p}: {e}")
            continue

        # Inferir área desde la ruta si falta
        # Ej.: src/data/questions/functions/definitions.json -> functions/definitions
        rel = p.relative_to(QUESTIONS_DIR)
        if rel.name.endswith(".json"):
            area_path = rel.with_suffix("").as_posix()
        else:
            area_path = rel.as_posix()

        for q in data:
            if "area" not in q or not q["area"]:
                q["area"] = area_path
            combined.append(q)

    # Ordenar por area + id si existe
    def _key(q):
        return (q.get("area", ""), q.get("id", ""))

    combined.sort(key=_key)
    OUTPUT_FILE.write_text(json.dumps(combined, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Escrito {len(combined)} preguntas en {OUTPUT_FILE}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

