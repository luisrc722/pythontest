import random
from collections import defaultdict
from typing import Dict, List, Iterable, Optional, Union
try:
    from ..models.question import Question
except Exception:  # Support running without package context (tests)
    from models.question import Question


DIFFICULTY_ORDER = ["basica", "intermedia", "avanzada"]


def _group_by_area(questions: Iterable[Question]) -> Dict[str, List[Question]]:
    buckets: Dict[str, List[Question]] = defaultdict(list)
    for q in questions:
        buckets[q.area].append(q)
    return buckets


def sample_by_area(
    questions: List[Question],
    areas: List[str],
    per_area_min: Union[int, Dict[str, int]] = 5,
    difficulty_mix: Optional[Dict[str, float]] = None,
    seed: Optional[int] = None,
) -> List[Question]:
    """Muestrea preguntas por área con mínimo por área y mezcla de dificultad.

    - Si no hay suficientes preguntas en un área, toma todas las disponibles.
    - La mezcla de dificultad es un objetivo; si no se puede cumplir, rellena con otras dificultades.
    """
    if seed is not None:
        random.seed(seed)

    by_area = _group_by_area(questions)
    selection: List[Question] = []

    # Normaliza mezcla de dificultad si se especifica
    mix = None
    if difficulty_mix:
        total = sum(difficulty_mix.values())
        if total > 0:
            mix = {k: v / total for k, v in difficulty_mix.items()}

    for area in areas:
        pool = list(by_area.get(area, []))
        random.shuffle(pool)
        if not pool:
            continue

        desired = per_area_min.get(area, 0) if isinstance(per_area_min, dict) else per_area_min
        target = min(desired, len(pool)) if desired > 0 else len(pool)

        if not mix:
            selection.extend(pool[:target])
            continue

        # Distribuye por dificultad según mix (objetivo, con relleno)
        buckets: Dict[str, List[Question]] = {d: [] for d in DIFFICULTY_ORDER}
        for q in pool:
            buckets.get(q.difficulty, buckets["basica"]).append(q)
        for b in buckets.values():
            random.shuffle(b)

        picked: List[Question] = []
        # Objetivo por dificultad (redondeo hacia abajo)
        targets = {d: int(target * mix.get(d, 0)) for d in DIFFICULTY_ORDER}
        # Ajuste por residuo para completar hasta target
        while sum(targets.values()) < target:
            for d in DIFFICULTY_ORDER:
                if sum(targets.values()) >= target:
                    break
                if mix.get(d, 0) > 0:
                    targets[d] += 1

        # Selecciona según objetivo
        for d in DIFFICULTY_ORDER:
            need = targets[d]
            take = min(need, len(buckets[d]))
            picked.extend(buckets[d][:take])
            buckets[d] = buckets[d][take:]

        # Rellena si faltan
        missing = target - len(picked)
        if missing > 0:
            leftovers = [q for b in buckets.values() for q in b]
            random.shuffle(leftovers)
            picked.extend(leftovers[:missing])

        selection.extend(picked[:target])

    random.shuffle(selection)
    return selection
