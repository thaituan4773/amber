import json
from pathlib import Path

STATE_FILE = Path("state.json")

def load_state():
    if not STATE_FILE.exists():
        return {}
    return json.loads(STATE_FILE.read_text())

def save_state(state: dict):
    STATE_FILE.write_text(json.dumps(state, indent=2))

# Check if an article has changed based on its ID and updated_at timestamp
def has_changed(article: dict, state: dict) -> bool:
    article_id = str(article["id"])
    return state.get(article_id) != article["updated_at"]