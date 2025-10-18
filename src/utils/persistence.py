from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path
from typing import Any, Dict


def save_attempt(result_obj, meta: Dict[str, Any], results_dir: str | Path = "src/data/results") -> Path:
    out_dir = Path(results_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    record = {
        "timestamp": datetime.now().isoformat(timespec="seconds"),
        "title": getattr(result_obj, "title", None),
        "total": getattr(result_obj, "total", None),
        "score": getattr(result_obj, "score", None),
        "level": result_obj.level() if hasattr(result_obj, "level") else None,
        "by_area_total": getattr(result_obj, "by_area_total", {}),
        "by_area_correct": getattr(result_obj, "by_area_correct", {}),
        "by_diff_total": getattr(result_obj, "by_diff_total", {}),
        "by_diff_correct": getattr(result_obj, "by_diff_correct", {}),
        "by_out_total": getattr(result_obj, "by_out_total", {}),
        "by_out_correct": getattr(result_obj, "by_out_correct", {}),
        "rubric": getattr(result_obj, "rubric_eval", {}),
        "meta": meta,
    }

    line = json.dumps(record, ensure_ascii=False)
    out_file = out_dir / f"attempts.jsonl"
    with out_file.open("a", encoding="utf-8") as f:
        f.write(line + "\n")
    return out_file

