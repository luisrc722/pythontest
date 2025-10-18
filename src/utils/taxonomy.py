import json
from pathlib import Path
from typing import Dict, List


DEFAULT_TAXONOMY = Path("src/data/taxonomy.json")


def load_taxonomy(path: str | None = None) -> Dict:
    p = Path(path) if path else DEFAULT_TAXONOMY
    if not p.exists():
        return {}
    with open(p, "r", encoding="utf-8") as f:
        return json.load(f)


def taxonomy_leaf_topics(taxonomy: Dict) -> List[str]:
    """Return the list of leaf topic paths (e.g., fundamentals/data_structures)."""
    leaves: List[str] = []
    # Expect structure: { category: { subcategories... } } or a dict with arrays
    # We'll support a simple structure:
    # {
    #   "fundamentals": ["data_structures", "operators", ...],
    #   "control_flow": ["conditionals", ...],
    #   ...
    # }
    for group, subs in taxonomy.items():
        if isinstance(subs, list):
            for leaf in subs:
                leaves.append(f"{group}/{leaf}")
        elif isinstance(subs, dict):
            # Flatten 2-level dicts
            for sub, inner in subs.items():
                if isinstance(inner, list):
                    for leaf in inner:
                        leaves.append(f"{group}/{sub}/{leaf}")
                else:
                    leaves.append(f"{group}/{sub}")
        else:
            leaves.append(str(group))
    return leaves

