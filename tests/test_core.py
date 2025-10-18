import random
import sys
from pathlib import Path

# Ensure src/ is on sys.path for imports
ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from models.question import Question
from utils.sampler import sample_by_area


def _q(area: str, difficulty: str, i: int) -> Question:
    return Question(
        id=f"t.{area}.{i}",
        text=f"q{i}",
        options=["a", "b"],
        correct="a",
        area=area,
        difficulty=difficulty,
        domain="python",
        tags=[],
        source=None,
    )


def test_sample_by_area_minimum_counts():
    data = []
    for i in range(4):
        data.append(_q("fundamentos", "basica", i))
    for i in range(10):
        data.append(_q("numpy", random.choice(["basica", "intermedia", "avanzada"]), i))

    selection = sample_by_area(
        data,
        areas=["fundamentos", "numpy"],
        per_area_min=5,
        difficulty_mix={"basica": 0.5, "intermedia": 0.3, "avanzada": 0.2},
        seed=42,
    )

    # fundamentos solo tiene 4 -> toma 4
    assert sum(1 for q in selection if q.area == "fundamentos") == 4
    # numpy tiene 10 -> toma 5
    assert sum(1 for q in selection if q.area == "numpy") == 5
    assert len(selection) == 9
