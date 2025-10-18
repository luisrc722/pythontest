from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any


@dataclass
class Question:
    id: Optional[str]
    text: str
    options: List[str]
    correct: str
    area: str
    difficulty: str = "basica"  # basica | intermedia | avanzada
    domain: str = "python"  # e.g., python | numpy | cuda
    tags: List[str] = field(default_factory=list)
    source: Optional[str] = None
    explanation: Optional[str] = None
    cognitive_level: Optional[str] = None  # bloom: remember|understand|apply|analyze|evaluate|create
    outcomes: List[str] = field(default_factory=list)  # learning outcomes codes

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> "Question":
        # Backwards compatibility: allow "category" or "topic" as alias for area
        area = data.get("area") or data.get("topic") or data.get("category") or "fundamentos"
        difficulty = data.get("difficulty", "basica")
        domain = data.get("domain", "python")
        options = data.get("options", [])
        return Question(
            id=data.get("id"),
            text=data["text"],
            options=options,
            correct=data["correct"],
            area=str(area).strip().lower(),
            difficulty=str(difficulty).strip().lower(),
            domain=str(domain).strip().lower(),
            tags=data.get("tags", []) or [],
            source=data.get("source"),
            explanation=data.get("explanation") or data.get("why") or None,
            cognitive_level=(data.get("cognitive_level") or data.get("bloom") or None),
            outcomes=data.get("outcomes", []) or [],
        )

    def is_correct(self, answer: str) -> bool:
        return answer.strip().lower() == self.correct.strip().lower()
