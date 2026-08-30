import sys
import json
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import pytest
from src.history_manager import HistoryManager


@pytest.fixture
def temp_history_file(tmp_path):
    return tmp_path / "history.json"


def test_add_entry(temp_history_file):
    hm = HistoryManager(temp_history_file)
    entry = hm.add_entry("standard", "2 + 2", "4")
    assert entry["expression"] == "2 + 2"
    assert entry["result"] == "4"
    assert len(hm.get_all()) == 1


def test_load_persisted_history(temp_history_file):
    hm1 = HistoryManager(temp_history_file)
    hm1.add_entry("standard", "5 + 5", "10")

    hm2 = HistoryManager(temp_history_file)  # fresh instance reads from disk
    entries = hm2.get_all()
    assert len(entries) == 1
    assert entries[0]["result"] == "10"


def test_delete_entry(temp_history_file):
    hm = HistoryManager(temp_history_file)
    entry = hm.add_entry("standard", "1 + 1", "2")
    assert hm.delete_entry(entry["id"]) is True
    assert hm.get_all() == []


def test_delete_nonexistent_entry_returns_false(temp_history_file):
    hm = HistoryManager(temp_history_file)
    assert hm.delete_entry("does-not-exist") is False


def test_clear_history(temp_history_file):
    hm = HistoryManager(temp_history_file)
    hm.add_entry("standard", "1 + 1", "2")
    hm.add_entry("scientific", "sin(0)", "0")
    hm.clear()
    assert hm.get_all() == []


def test_clear_by_module(temp_history_file):
    hm = HistoryManager(temp_history_file)
    hm.add_entry("standard", "1 + 1", "2")
    hm.add_entry("scientific", "sin(0)", "0")
    hm.clear(module="standard")
    remaining = hm.get_all()
    assert len(remaining) == 1
    assert remaining[0]["module"] == "scientific"


def test_get_all_filtered_by_module(temp_history_file):
    hm = HistoryManager(temp_history_file)
    hm.add_entry("standard", "1 + 1", "2")
    hm.add_entry("bmi", "BMI check", "22.4 Normal")
    standard_only = hm.get_all(module="standard")
    assert len(standard_only) == 1
    assert standard_only[0]["module"] == "standard"


def test_corrupted_file_recovers_gracefully(temp_history_file):
    temp_history_file.write_text("{not valid json", encoding="utf-8")
    hm = HistoryManager(temp_history_file)
    assert hm.get_all() == []
    # Should have repaired the file on disk.
    data = json.loads(temp_history_file.read_text(encoding="utf-8"))
    assert data == []


def test_newest_entry_first(temp_history_file):
    hm = HistoryManager(temp_history_file)
    hm.add_entry("standard", "1 + 1", "2")
    hm.add_entry("standard", "2 + 2", "4")
    entries = hm.get_all()
    assert entries[0]["expression"] == "2 + 2"
