#!/usr/bin/env python3
import json
import sys
from collections import Counter, defaultdict
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from utils.loader import load_questions  # type: ignore
from utils.taxonomy import load_taxonomy, taxonomy_leaf_topics  # type: ignore
from utils.blueprint import load_blueprint  # type: ignore


ALLOWED_DIFFICULTY = {"basica", "intermedia", "avanzada"}
ALLOWED_COGNITIVE = {"remember", "understand", "apply", "analyze", "evaluate", "create"}


def main() -> int:
    strict_coverage = "--strict-coverage" in sys.argv
    taxonomy = load_taxonomy()
    leaves = set(taxonomy_leaf_topics(taxonomy)) if taxonomy else set()
    questions = load_questions()

    problems = []
    warnings = []
    deficits = []

    # Unicidad de IDs
    ids = [q.id for q in questions if q.id]
    counts = Counter(ids)
    dupes = [i for i, c in counts.items() if c > 1]
    if dupes:
        problems.append(f"IDs duplicados: {dupes}")

    # Validaciones por pregunta
    for i, q in enumerate(questions):
        ctx = f"(idx={i}, id={q.id})"
        if not q.text or not isinstance(q.text, str):
            problems.append(f"Texto inválido {ctx}")
        if not isinstance(q.options, list) or len(q.options) < 2:
            problems.append(f"Opciones insuficientes {ctx}")
        if q.correct not in q.options:
            problems.append(f"Correct no está en options {ctx}")
        if q.difficulty not in ALLOWED_DIFFICULTY:
            problems.append(f"Dificultad inválida {ctx}: {q.difficulty}")
        if q.cognitive_level and q.cognitive_level not in ALLOWED_COGNITIVE:
            warnings.append(f"cognitive_level no reconocido {ctx}: {q.cognitive_level}")
        if q.outcomes and not isinstance(q.outcomes, list):
            problems.append(f"outcomes debe ser lista {ctx}")
        if leaves and q.area not in leaves:
            warnings.append(f"Área no presente en taxonomy {ctx}: {q.area}")

    # Cobertura por leaf vs blueprint
    default_min, overrides, _mix, _rubric = load_blueprint()
    per_leaf = defaultdict(int)
    for q in questions:
        per_leaf[q.area] += 1

    print("Cobertura por leaf (preguntas disponibles):")
    all_leaves = sorted(leaves) if leaves else sorted(per_leaf.keys())
    for leaf in all_leaves:
        have = per_leaf.get(leaf, 0)
        need = overrides.get(leaf, default_min)
        status = "OK" if have >= need else "FALTA"
        print(f" - {leaf}: {have}/{need} {status}")
        if have < need:
            deficits.append((leaf, have, need))

    if warnings:
        print("\nWARNINGS:")
        for w in warnings:
            print(" -", w)
    if strict_coverage and deficits:
        problems.append("Cobertura insuficiente en uno o más leaves (modo estricto)")
    if problems:
        print("\nERRORES:")
        for p in problems:
            print(" -", p)
        if strict_coverage and deficits:
            print(" Detalle de cobertura insuficiente:")
            for leaf, have, need in deficits:
                print(f"  · {leaf}: {have}/{need}")
        return 1
    print("\nValidación OK ✅")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
