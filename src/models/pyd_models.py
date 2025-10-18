from typing import List, Optional, Literal
from pydantic import BaseModel, field_validator, model_validator


Difficulty = Literal["basica", "intermedia", "avanzada"]


class QuestionModel(BaseModel):
    id: Optional[str] = None
    text: str
    options: List[str]
    correct: str
    area: str
    difficulty: Difficulty = "basica"
    domain: str = "python"
    tags: List[str] = []
    source: Optional[str] = None
    explanation: Optional[str] = None
    cognitive_level: Optional[Literal[
        "remember",
        "understand",
        "apply",
        "analyze",
        "evaluate",
        "create",
    ]] = None
    outcomes: List[str] = []

    @field_validator("area")
    @classmethod
    def normalize_area(cls, v: str) -> str:
        return str(v).strip().lower()

    @field_validator("difficulty")
    @classmethod
    def normalize_difficulty(cls, v: str) -> str:
        return str(v).strip().lower()

    @field_validator("options")
    @classmethod
    def options_min_len(cls, v: List[str]) -> List[str]:
        if not isinstance(v, list) or len(v) < 2:
            raise ValueError("options debe contener al menos 2 elementos")
        return v

    @model_validator(mode="after")
    def check_correct_in_options(self):
        if self.correct not in self.options:
            raise ValueError("'correct' debe estar presente en 'options'")
        return self
