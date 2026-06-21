import json
from datetime import datetime, timezone
from pathlib import Path


def append_json_line(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    enriched = {
        "logged_at": datetime.now(tz=timezone.utc).isoformat(),
        **payload,
    }
    with path.open("a", encoding="utf-8") as file:
        file.write(json.dumps(enriched) + "\n")
