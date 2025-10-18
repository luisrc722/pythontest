#!/usr/bin/env python3
import json
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
UNIFIED = ROOT / "src/data/questions.json"
OUT_DIR = ROOT / "src/data/questions"


def main() -> int:
    if not UNIFIED.exists():
        print(f"No existe {UNIFIED}; nada que dividir")
        return 1
    data = json.loads(UNIFIED.read_text(encoding="utf-8"))
    buckets = defaultdict(list)
    for q in data:
        area = (q.get("area") or q.get("topic") or q.get("category") or "uncategorized").strip().lower()
        buckets[area].append(q)

    for area, items in buckets.items():
        # Map area path to file path: functions/definitions -> functions/definitions.json
        p = OUT_DIR / (area + ".json")
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(json.dumps(items, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        print(f"Escrito {len(items):3d} en {p}")
    print(f"Leaves: {len(buckets)}  Total: {sum(len(v) for v in buckets.values())}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

