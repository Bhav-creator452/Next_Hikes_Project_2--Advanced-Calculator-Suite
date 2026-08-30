"""
Settings persistence for CalcSuite.

Centralizes user preferences (theme, decimal places, sound, history,
angle mode) so no module hard-codes its own preferences.
"""
import json
from pathlib import Path
from typing import Any, Dict

from src.config import SETTINGS_FILE, DEFAULT_SETTINGS, ensure_data_dir


class SettingsManager:
    def __init__(self, file_path: Path = SETTINGS_FILE):
        self.file_path = file_path
        self._settings: Dict[str, Any] = dict(DEFAULT_SETTINGS)
        self.load()

    def load(self) -> None:
        ensure_data_dir()
        if not self.file_path.exists():
            self._settings = dict(DEFAULT_SETTINGS)
            self._save()
            return
        try:
            raw = self.file_path.read_text(encoding="utf-8")
            data = json.loads(raw) if raw.strip() else {}
            if not isinstance(data, dict):
                raise ValueError("settings.json root must be an object")
            merged = dict(DEFAULT_SETTINGS)
            merged.update(data)
            self._settings = merged
        except (json.JSONDecodeError, ValueError, OSError):
            self._settings = dict(DEFAULT_SETTINGS)
            self._save()

    def _save(self) -> None:
        ensure_data_dir()
        try:
            self.file_path.write_text(
                json.dumps(self._settings, indent=2, ensure_ascii=False), encoding="utf-8"
            )
        except OSError:
            pass

    def get(self, key: str, default: Any = None) -> Any:
        return self._settings.get(key, default)

    def set(self, key: str, value: Any) -> None:
        self._settings[key] = value
        self._save()

    def all(self) -> Dict[str, Any]:
        return dict(self._settings)

    def reset(self) -> None:
        self._settings = dict(DEFAULT_SETTINGS)
        self._save()
