"""
Currency service layer.

Responsible for:
  * requesting live exchange rates from a reputable API
  * parsing the response
  * caching rates locally (data/currency_cache.json)
  * handling network / API failures gracefully
  * recording last-updated time and clearly labeling cached vs live data

UI code should never talk to the network or the cache file directly —
everything goes through CurrencyService.
"""
import json
import time
from pathlib import Path
from typing import Dict, Optional, Tuple

from src.config import CURRENCY_API_URL, CURRENCY_CACHE_FILE, SUPPORTED_CURRENCIES, ensure_data_dir

try:
    import requests
except ImportError:  # pragma: no cover - requests is a declared dependency
    requests = None


class CurrencyServiceError(Exception):
    pass


class CurrencyService:
    def __init__(self, cache_file: Path = CURRENCY_CACHE_FILE, timeout: float = 6.0):
        self.cache_file = cache_file
        self.timeout = timeout

    # ---- cache ------------------------------------------------------
    def _read_cache(self) -> Optional[dict]:
        if not self.cache_file.exists():
            return None
        try:
            raw = self.cache_file.read_text(encoding="utf-8")
            data = json.loads(raw) if raw.strip() else None
            if not isinstance(data, dict) or "rates" not in data or "base" not in data:
                return None
            return data
        except (json.JSONDecodeError, OSError, ValueError):
            return None

    def _write_cache(self, base: str, rates: Dict[str, float]) -> None:
        ensure_data_dir()
        payload = {"base": base, "rates": rates, "fetched_at": time.time()}
        try:
            self.cache_file.write_text(json.dumps(payload, indent=2), encoding="utf-8")
        except OSError:
            pass

    # ---- public API ---------------------------------------------------
    def get_rates(self, base: str) -> Tuple[Dict[str, float], bool, Optional[str]]:
        """
        Returns (rates, is_live, last_updated_label).

        Tries the live API first; on any failure, falls back to the
        cache for the same base currency if available. Never pretends
        cached rates are live.
        """
        if requests is not None:
            try:
                url = CURRENCY_API_URL.format(base=base)
                resp = requests.get(url, timeout=self.timeout)
                resp.raise_for_status()
                data = resp.json()
                rates = data.get("rates")
                if not isinstance(rates, dict) or not rates:
                    raise CurrencyServiceError("Malformed API response.")
                self._write_cache(base, rates)
                return rates, True, "Live rates"
            except Exception:
                pass  # fall through to cache

        cached = self._read_cache()
        if cached and cached.get("base") == base:
            fetched_at = cached.get("fetched_at")
            label = self._format_cache_label(fetched_at)
            return cached["rates"], False, label

        raise CurrencyServiceError(
            "Unable to fetch latest rates. No cached rates are available for this currency."
        )

    def convert(self, amount: float, from_currency: str, to_currency: str) -> Tuple[float, bool, Optional[str]]:
        if from_currency == to_currency:
            return amount, True, "Same currency"

        rates, is_live, label = self.get_rates(from_currency)
        if to_currency not in rates:
            raise CurrencyServiceError(f"No rate available for {to_currency}.")

        converted = amount * rates[to_currency]
        return converted, is_live, label

    @staticmethod
    def _format_cache_label(fetched_at: Optional[float]) -> str:
        if not fetched_at:
            return "Using last available rates (unknown time)"
        try:
            import datetime
            dt = datetime.datetime.fromtimestamp(fetched_at)
            return f"Using last available rates (updated {dt.strftime('%Y-%m-%d %H:%M')})"
        except Exception:
            return "Using last available rates"
