from __future__ import annotations

from typing import Dict, Tuple


def evaluate_rubric(
    rubric: Dict,
    total: int,
    score: int,
    by_area_total: Dict[str, int],
    by_area_correct: Dict[str, int],
) -> Tuple[bool, Dict[str, str]]:
    """Evalúa criterios básicos de aprobación.

    Rubric soportada (opc.):
    {
      "global": {"min_score": 0.7},
      "per_leaf_min_pct": 0.5
    }
    Devuelve (aprobado, detalles).
    """
    details: Dict[str, str] = {}
    if not rubric:
        return True, details

    ok = True

    # Global threshold
    g = rubric.get("global") or {}
    min_score = g.get("min_score")
    if isinstance(min_score, (int, float)) and total > 0:
        ratio = score / total
        if ratio + 1e-9 < float(min_score):
            ok = False
            details["global"] = f"{ratio:.0%} < {float(min_score):.0%}"

    # Per leaf threshold
    min_leaf = rubric.get("per_leaf_min_pct")
    if isinstance(min_leaf, (int, float)):
        for area, t in by_area_total.items():
            if t <= 0:
                continue
            acc = (by_area_correct.get(area, 0) / t)
            if acc + 1e-9 < float(min_leaf):
                ok = False
                details[f"leaf:{area}"] = f"{acc:.0%} < {float(min_leaf):.0%}"

    return ok, details

