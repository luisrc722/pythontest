# src/utils/loader.py
import json
from pathlib import Path
try:
    from ..models.question import Question
except Exception:
    from models.question import Question

DEFAULT_DATA_FILE = Path("src/data/questions.json")


def load_questions(file_path: str | None = None):
    """Carga preguntas desde un archivo JSON unificado.

    Fallback: si no existe el unificado, intenta cargar desde `python_basics.json`.
    """
    path = Path(file_path) if file_path else DEFAULT_DATA_FILE
    if path.exists():
        with open(path, "r", encoding="utf-8") as f:
            raw = json.load(f)
    else:
        legacy = Path("src/data/python_basics.json")
        if legacy.exists():
            with open(legacy, "r", encoding="utf-8") as f:
                raw = json.load(f)
        else:
            raw = []

    # Intentar validación con Pydantic si está disponible
    try:
        from ..models.pyd_models import QuestionModel  # type: ignore
        use_pydantic = True
    except Exception:
        use_pydantic = False

    normalized = []
    for item in raw:
        if "area" not in item:
            if "topic" in item:
                item["area"] = item["topic"]
            elif "category" in item:
                item["area"] = item["category"]
        if use_pydantic:
            qm = QuestionModel.model_validate(item)  # type: ignore
            normalized.append(
                Question(
                    id=qm.id,
                    text=qm.text,
                    options=qm.options,
                    correct=qm.correct,
                    area=qm.area,
                    difficulty=qm.difficulty,
                    domain=qm.domain,
                    tags=qm.tags,
                    source=qm.source,
                    explanation=qm.explanation,
                )
            )
        else:
            normalized.append(Question.from_dict(item))

    return normalized
