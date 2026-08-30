"""
Central configuration for CalcSuite.

Holds paths, app metadata, and default values used across the app.
Nothing UI-specific belongs here — see theme.py for visual tokens.
"""
from pathlib import Path

APP_NAME = "CalcSuite"
APP_VERSION = "1.0.0"
APP_TAGLINE = "A modern, modular desktop calculator suite."

# ---- Paths -----------------------------------------------------------
ROOT_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT_DIR / "data"
ASSETS_DIR = ROOT_DIR / "assets"

HISTORY_FILE = DATA_DIR / "history.json"
SETTINGS_FILE = DATA_DIR / "settings.json"
CURRENCY_CACHE_FILE = DATA_DIR / "currency_cache.json"

# ---- Window ------------------------------------------------------------
DEFAULT_WINDOW_SIZE = "980x640"
MIN_WINDOW_WIDTH = 720
MIN_WINDOW_HEIGHT = 480

# ---- Sidebar -------------------------------------------------------------
SIDEBAR_WIDTH_EXPANDED = 210
SIDEBAR_WIDTH_COLLAPSED = 64
SIDEBAR_COLLAPSE_BREAKPOINT = 820  # window width below which sidebar auto-collapses

# ---- Defaults --------------------------------------------------------
DEFAULT_SETTINGS = {
    "theme": "Dark",
    "decimal_places": "Auto",  # Auto, 2, 4, 6, 8
    "sound_enabled": False,
    "history_enabled": True,
    "angle_mode": "DEG",  # DEG, RAD, GRAD
}

MAX_DECIMAL_PLACES_AUTO = 10

# ---- Currency ----------------------------------------------------------
CURRENCY_API_URL = "https://api.exchangerate-api.com/v4/latest/{base}"
SUPPORTED_CURRENCIES = ["USD", "EUR", "GBP", "INR", "CAD", "AUD", "JPY", "CHF", "CNY"]
CURRENCY_CACHE_TTL_SECONDS = 60 * 60  # 1 hour

CURRENCY_SYMBOLS = {
    "USD": "$", "EUR": "\u20ac", "GBP": "\u00a3", "INR": "\u20b9",
    "CAD": "CA$", "AUD": "A$", "JPY": "\u00a5", "CHF": "CHF", "CNY": "\u00a5",
}


def ensure_data_dir() -> None:
    """Create the data directory if it doesn't already exist."""
    DATA_DIR.mkdir(parents=True, exist_ok=True)
