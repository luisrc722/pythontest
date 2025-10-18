from __future__ import annotations

import json
from pathlib import Path
from typing import Dict, List, Optional, Tuple


def _load_toml(p: Path) -> dict:
    try:
        import toml  # type: ignore
    except Exception as e:
        raise RuntimeError("Para módulos .toml instala 'toml' o usa JSON") from e
    return toml.loads(p.read_text(encoding="utf-8"))


def _normalize_min(v) -> int:
    if isinstance(v, str) and v.lower() in {"all", "todo", "full"}:
        return 0  # 0 significa 'tomar todas las preguntas disponibles'
    return int(v)


def load_module_profile(path: str) -> Tuple[List[str], Dict[str, int], Dict[str, float], Optional[int]]:
    """Carga un perfil de módulo educativo.

    Retorna (areas, per_leaf_map, difficulty_mix, max_total).

    Formato soportado (TOML o JSON):
    {
      "areas": ["functions/definitions", "control_flow/loops"],
      "per_leaf_min": 3,
      "overrides": {"functions/definitions": 5},
      "difficulty_mix": {"basica":0.6, "intermedia":0.3, "avanzada":0.1},
      "max_total": 20
    }
    """
    p = Path(path)
    if not p.exists():
        raise FileNotFoundError(f"No se encontró el módulo: {path}")
    if p.suffix.lower() == ".toml":
        data = _load_toml(p)
    else:
        data = json.loads(p.read_text(encoding="utf-8"))

    areas = list(data.get("areas") or [])
    default_min = _normalize_min(data.get("per_leaf_min", 0))
    overrides = {k: _normalize_min(v) for k, v in (data.get("overrides", {}) or {}).items()}
    per_leaf_map = {a: overrides.get(a, default_min) for a in areas}
    mix = data.get("difficulty_mix") or {}
    max_total = data.get("max_total")
    return areas, per_leaf_map, mix, max_total
