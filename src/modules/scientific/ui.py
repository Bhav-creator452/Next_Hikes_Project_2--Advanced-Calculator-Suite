"""Scientific Calculator UI, built on top of the safe expression engine."""
import customtkinter as ctk

from src.modules.scientific.calculator import evaluate, ExpressionError, ScientificMathError
from src.components.display import Display
from src.components.buttons import CalculatorButton
from src.theme import theme_manager, BUTTON_SPACING
from src.utils.formatting import format_number

FUNCTION_ROWS = [
    [("DEG", "utility"), ("sin", "utility"), ("cos", "utility"), ("tan", "utility"), ("(", "utility"), (")", "utility")],
    [("\u03c0", "utility"), ("e", "utility"), ("x\u00b2", "utility"), ("x^y", "utility"), ("\u221a", "utility"), ("1/x", "utility")],
    [("log", "utility"), ("ln", "utility"), ("n!", "utility"), ("%", "utility"), ("+/-", "utility"), ("\u232b", "utility")],
]

MAIN_ROWS = [
    [("AC", "utility"), ("7", "number"), ("8", "number"), ("9", "number"), ("\u00f7", "operator")],
    [("", "spacer"), ("4", "number"), ("5", "number"), ("6", "number"), ("\u00d7", "operator")],
    [("", "spacer"), ("1", "number"), ("2", "number"), ("3", "number"), ("-", "operator")],
    [("", "spacer"), ("0", "number"), (".", "number"), ("=", "equals"), ("+", "operator")],
]


class ScientificCalculatorUI(ctk.CTkFrame):
    def __init__(self, master, on_result=None, angle_mode: str = "DEG", **kwargs):
        colors = theme_manager.colors
        super().__init__(master, fg_color=colors.bg, **kwargs)

        self.on_result = on_result
        self.angle_mode = angle_mode
        self.expression = ""
        self.last_result = None
        self.error = None

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=0, minsize=120)
        self.grid_rowconfigure(1, weight=1)

        self.display = Display(self)
        self.display.grid(row=0, column=0, sticky="nsew")

        self.pad = ctk.CTkFrame(self, fg_color="transparent")
        self.pad.grid(row=1, column=0, sticky="nsew", padx=16, pady=(0, 16))
        self._build_pad()
        self._refresh_display()

    def _build_pad(self):
        n_cols = 6
        for c in range(n_cols):
            self.pad.grid_columnconfigure(c, weight=1, uniform="col")
        total_rows = len(FUNCTION_ROWS) + len(MAIN_ROWS)
        for r in range(total_rows):
            self.pad.grid_rowconfigure(r, weight=1, uniform="row")

        r = 0
        self.deg_button = None
        for row in FUNCTION_ROWS:
            for c, (label, role) in enumerate(row):
                btn = CalculatorButton(self.pad, text=label, role=role, font_key="button_small",
                                        command=lambda l=label: self._handle_function(l))
                btn.grid(row=r, column=c, sticky="nsew", padx=BUTTON_SPACING // 2, pady=BUTTON_SPACING // 2)
                if label == "DEG":
                    self.deg_button = btn
            r += 1

        for row in MAIN_ROWS:
            col = 0
            for label, role in row:
                if role == "spacer":
                    col += 1
                    continue
                colspan = 1
                btn = CalculatorButton(self.pad, text=label, role=role,
                                        command=lambda l=label: self._handle_main(l))
                btn.grid(row=r, column=col, sticky="nsew", padx=BUTTON_SPACING // 2, pady=BUTTON_SPACING // 2)
                col += colspan
            r += 1

    # ---- input handling -------------------------------------------------
    def _append(self, text: str):
        if self.last_result is not None and not self.error:
            # start fresh unless continuing with an operator
            if text and (text[0].isdigit() or text[0] in "(\u03c0e" or text in ("sin", "cos", "tan", "log", "ln", "\u221a")):
                self.expression = ""
        self.expression += text
        self.last_result = None
        self.error = None
        self._refresh_display()

    def _handle_main(self, label: str):
        if label == "AC":
            self.expression = ""
            self.last_result = None
            self.error = None
        elif label == "\u232b":
            self.expression = self.expression[:-1]
            self.last_result = None
        elif label == "=":
            self._do_equals()
            return
        elif label.isdigit() or label == ".":
            self._append(label)
        elif label in ("+", "-"):
            self._append(label)
        elif label == "\u00d7":
            self._append("*")
        elif label == "\u00f7":
            self._append("/")
        self._refresh_display()

    def _handle_function(self, label: str):
        if label == "DEG":
            order = ["DEG", "RAD", "GRAD"]
            idx = (order.index(self.angle_mode) + 1) % len(order)
            self.angle_mode = order[idx]
            self.deg_button.configure(text=self.angle_mode)
            return
        mapping = {
            "sin": "sin(", "cos": "cos(", "tan": "tan(",
            "\u03c0": "pi", "e": "e",
            "x\u00b2": "^2", "x^y": "^",
            "\u221a": "sqrt(", "1/x": "1/",
            "log": "log(", "ln": "ln(",
            "n!": "!", "%": "%",
            "(": "(", ")": ")",
        }
        if label == "+/-":
            if self.expression.startswith("-"):
                self.expression = self.expression[1:]
            else:
                self.expression = "-" + self.expression
            self._refresh_display()
            return
        if label == "\u232b":
            self.expression = self.expression[:-1]
            self._refresh_display()
            return
        text = mapping.get(label, "")
        self._append(text)

    def _do_equals(self):
        if not self.expression.strip():
            return
        try:
            result = evaluate(self.expression, self.angle_mode)
            formatted = format_number(result)
            if self.on_result:
                self.on_result(self.expression, formatted)
            self.last_result = result
            self.error = None
            self._refresh_display(result_override=formatted)
            self.expression = self._num_to_str(result)
        except ScientificMathError as e:
            self.error = str(e)
            self._refresh_display()
        except ExpressionError:
            self.error = "Invalid Expression"
            self._refresh_display()
        except ZeroDivisionError:
            self.error = "Division by Zero"
            self._refresh_display()
        except Exception:
            self.error = "Invalid Expression"
            self._refresh_display()

    @staticmethod
    def _num_to_str(value: float) -> str:
        if value == int(value):
            return str(int(value))
        return repr(round(value, 10))

    def _refresh_display(self, result_override=None):
        self.display.set_expression(self.expression or " ")
        if self.error:
            self.display.set_result(self.error, is_error=True)
            return
        if result_override is not None:
            self.display.set_result(result_override)
            return
        try:
            preview = evaluate(self.expression, self.angle_mode) if self.expression.strip() else None
            self.display.set_result(format_number(preview) if preview is not None else "0")
        except Exception:
            self.display.set_result(self.expression.split("(")[-1] or "0")
