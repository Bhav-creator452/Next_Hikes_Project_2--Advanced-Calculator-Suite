"""
Unified history system shared by all calculator modules.

Each entry: {id, module, expression, result, timestamp}
Persisted to data/history.json. Recovers gracefully from corruption.
"""
import json
import uuid
from datetime import datetime
from pathlib import Path
from typing import List, Optional, Dict

from src.config import HISTORY_FILE, ensure_data_dir

MAX_HISTORY_ENTRIES = 500


class HistoryManager:
    def __init__(self, file_path: Path = HISTORY_FILE):
        self.file_path = file_path
        self._entries: List[Dict] = []
        self.load()

    # ---- persistence -----------------------------------------------
    def load(self) -> None:
        ensure_data_dir()
        if not self.file_path.exists():
            self._entries = []
            self._save()
            return
        try:
            raw = self.file_path.read_text(encoding="utf-8")
            data = json.loads(raw) if raw.strip() else []
            if not isinstance(data, list):
                raise ValueError("history.json root must be a list")
            self._entries = data
        except (json.JSONDecodeError, ValueError, OSError):
            # Corrupted file -> recover gracefully, don't crash the app.
            self._entries = []
            self._save()

    def _save(self) -> None:
        ensure_data_dir()
        try:
            self.file_path.write_text(
                json.dumps(self._entries, indent=2, ensure_ascii=False), encoding="utf-8"
            )
        except OSError:
            pass  # Best effort; app should keep working without persistence.

    # ---- API ----------------------------------------------------------
    def add_entry(self, module: str, expression: str, result: str) -> Dict:
        entry = {
            "id": uuid.uuid4().hex,
            "module": module,
            "expression": expression,
            "result": result,
            "timestamp": datetime.now().isoformat(timespec="seconds"),
        }
        self._entries.insert(0, entry)
        self._entries = self._entries[:MAX_HISTORY_ENTRIES]
        self._save()
        return entry

    def get_all(self, module: Optional[str] = None) -> List[Dict]:
        if module is None:
            return list(self._entries)
        return [e for e in self._entries if e.get("module") == module]

    def delete_entry(self, entry_id: str) -> bool:
        before = len(self._entries)
        self._entries = [e for e in self._entries if e.get("id") != entry_id]
        changed = len(self._entries) != before
        if changed:
            self._save()
        return changed

    def clear(self, module: Optional[str] = None) -> None:
        if module is None:
            self._entries = []
        else:
            self._entries = [e for e in self._entries if e.get("module") != module]
        self._save()
