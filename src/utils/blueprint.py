import json
from pathlib import Path
from typing import Dict, Tuple


DEFAULT_BLUEPRINT = Path("src/data/blueprint.json")


def load_blueprint(path: str | None = None) -> Tuple[int, Dict[str, int], dict, dict]:
    """Return (per_leaf_min_default, overrides_map, difficulty_mix, rubric).

    If no blueprint exists, returns defaults and empty rubric.
    """
    p = Path(path) if path else DEFAULT_BLUEPRINT
    if not p.exists():
        return 5, {}, {"basica": 0.5, "intermedia": 0.35, "avanzada": 0.15}, {}
    with open(p, "r", encoding="utf-8") as f:
        data = json.load(f)
    per_leaf_min = int(data.get("per_leaf_min", 5))
    overrides = {k: int(v) for k, v in (data.get("overrides", {}) or {}).items()}
    mix = data.get("difficulty_mix", {"basica": 0.5, "intermedia": 0.35, "avanzada": 0.15})
    rubric = data.get("rubric", {}) or {}
    return per_leaf_min, overrides, mix, rubric
