# CalcSuite

A modern, modular desktop calculator suite built with Python and CustomTkinter.

## Overview

CalcSuite is a single desktop application that brings together five calculation
tools — Standard, Scientific, BMI, Unit Converter, and Currency Converter —
behind one consistent, dark-themed interface. Instead of five disconnected
scripts, everything shares the same sidebar navigation, visual language,
history system, and settings, so it feels like one coherent product rather
than a collection of classroom exercises.

## Features

- **Standard Calculator** — two-level display (expression + result), chained
  calculations, sensible post-equals behavior, negative numbers, decimals,
  parentheses, percentage, backspace, and full keyboard support. Expressions
  are evaluated with a restricted AST-based evaluator — never Python's raw
  `eval()`.
- **Scientific Calculator** — trigonometric functions with DEG/RAD/GRAD
  switching, π/e constants, powers, roots, logarithms, factorial, and
  reciprocal. Powered by a hand-written tokenizer/parser, so calculator
  input can never execute arbitrary code.
- **BMI Calculator** — supports cm/ft-in and kg/lb units, calculates BMI
  against standard WHO thresholds, and shows a healthy weight range for
  the entered height.
- **Unit Converter** — Length, Weight, Area, Volume, Time, Speed, and Data,
  plus Temperature with proper (non-linear) conversion formulas. Swap
  button flips From/To instantly.
- **Currency Converter** — live exchange rates via a currency API, with
  local caching and a clearly labeled offline fallback when the network
  is unavailable. Never presents cached rates as if they were live.
- **Unified History** — every calculation, conversion, and BMI check is
  recorded with a timestamp, viewable in a dedicated History screen (it
  never eats into the calculator's own layout), and can be tapped to
  reload into the Standard calculator.
- **Settings** — theme (Dark/Light/System), decimal precision, button
  sound, history toggle, and a keyboard shortcut reference. All settings
  persist across launches.
- **Responsive layout** — the sidebar auto-collapses on narrow windows,
  and every module is designed to remain usable at small, default, and
  maximized window sizes.

## Tech Stack

- Python 3
- [CustomTkinter](https://github.com/TomSchimansky/CustomTkinter) for the UI
- `requests` for the currency exchange-rate API
- `pytest` for automated testing
- Standard library: `math`, `decimal`, `datetime`, `json`, `pathlib`, `ast`

## Project Structure

```text
CalcSuite/
├── main.py                  # entry point
├── requirements.txt
├── src/
│   ├── app.py                # main window, sidebar + module router
│   ├── theme.py               # centralized colors/fonts (Dark & Light)
│   ├── config.py              # paths, defaults, window/app constants
│   ├── history_manager.py     # unified, persisted calculation history
│   ├── settings_manager.py    # persisted user preferences
│   ├── modules/
│   │   ├── standard/          # calculator.py (logic) + ui.py
│   │   ├── scientific/        # safe expression engine + ui.py
│   │   ├── bmi/                # BMI formulas + ui.py
│   │   ├── converter/          # unit conversion tables + ui.py
│   │   └── currency/           # currency service (API/cache) + ui.py
│   ├── views/                  # history_view.py, settings_view.py, about_view.py
│   ├── components/             # reusable buttons, display, sidebar, dialogs
│   └── utils/                  # formatting.py, validation.py
├── data/                       # history.json, settings.json, currency_cache.json
└── tests/                      # pytest suite for all calculation logic
```

UI code, calculation logic, persistence, and utilities are kept in separate
files throughout, so each calculation engine can be tested (and reused)
completely independently of the GUI.

## Installation

```bash
git clone <repository>
cd CalcSuite
pip install -r requirements.txt
```

CustomTkinter requires a working Tk installation. On most systems this is
already bundled with Python; on some Linux distributions you may need:

```bash
sudo apt install python3-tk
```

## Running

```bash
python main.py
```

The app opens directly into the Standard Calculator. Use the sidebar (or
the collapse toggle on narrow windows) to switch between modules.

## Testing

```bash
pytest
```

The suite covers the Standard and Scientific engines, BMI calculations,
unit/temperature conversions, and history persistence (including recovery
from a corrupted history file) — 70 tests in total, all UI-independent.

## Screenshots

_Add screenshots here once you've run the app locally, e.g.:_

- `assets/screenshots/standard.png`
- `assets/screenshots/scientific.png`
- `assets/screenshots/bmi.png`
- `assets/screenshots/converter.png`
- `assets/screenshots/currency.png`
- `assets/screenshots/history.png`

## Future Improvements

The architecture is designed so new modules can be dropped in without
touching existing ones (each module is just a `calculator.py` + `ui.py`
pair, registered in `app.py`'s module map). Natural next additions:

- Date / Time calculators
- Loan / GST / Discount / Tip calculators
- Age calculator
- Statistics calculator
- Programmer calculator (bin/oct/hex)
- Matrix calculator
- Equation solver

## Notes on Security

Neither the Standard nor Scientific calculator ever passes user input to
Python's `eval()`. The Standard calculator builds a restricted AST from
tokenized input; the Scientific calculator uses a hand-written
tokenizer + recursive-descent parser over a fixed whitelist of operators,
functions, and constants. Malformed or malicious input fails safely with
a user-facing error message instead of executing code.
