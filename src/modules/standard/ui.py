"""Standard Calculator UI. Wraps StandardCalculator, keeps UI code separate from logic."""
import customtkinter as ctk

from src.modules.standard.calculator import StandardCalculator, CalculatorState
from src.components.display import Display
from src.components.buttons import CalculatorButton
from src.theme import theme_manager, BUTTON_SPACING
from src.utils.formatting import format_number

# rows of (label, role, handler_key)
BUTTON_LAYOUT = [
    [("AC", "utility"), ("(", "utility"), (")", "utility"), ("\u00f7", "operator")],
    [("7", "number"), ("8", "number"), ("9", "number"), ("\u00d7", "operator")],
    [("4", "number"), ("5", "number"), ("6", "number"), ("-", "operator")],
    [("1", "number"), ("2", "number"), ("3", "number"), ("+", "operator")],
    [("+/-", "utility"), ("0", "number"), (".", "number"), ("=", "equals")],
    [("%", "utility"), ("\u232b", "utility")],
]


class StandardCalculatorUI(ctk.CTkFrame):
    def __init__(self, master, on_result=None, **kwargs):
        colors = theme_manager.colors
        super().__init__(master, fg_color=colors.bg, **kwargs)

        self.engine = StandardCalculator()
        self.on_result = on_result  # callback(expression, result) for history

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=0, minsize=140)
        self.grid_rowconfigure(1, weight=1)

        self.display = Display(self)
        self.display.grid(row=0, column=0, sticky="nsew")

        self.keypad = ctk.CTkFrame(self, fg_color="transparent")
        self.keypad.grid(row=1, column=0, sticky="nsew", padx=16, pady=(0, 16))
        self._build_keypad()

        self._bind_keyboard()
        self._refresh_display()

    # ---- layout -------------------------------------------------------
    def _build_keypad(self):
        n_cols = 4
        for c in range(n_cols):
            self.keypad.grid_columnconfigure(c, weight=1, uniform="col")
        n_rows = len(BUTTON_LAYOUT)
        for r in range(n_rows):
            self.keypad.grid_rowconfigure(r, weight=1, uniform="row")

        self._buttons = []
        for r, row in enumerate(BUTTON_LAYOUT):
            col = 0
            for label, role in row:
                colspan = 1
                if label == "=" and len(row) < 4:
                    colspan = 4 - col
                if label == "\u232b" and len(row) < 4:
                    colspan = 4 - col
                btn = CalculatorButton(self.keypad, text=label, role=role,
                                        command=lambda l=label: self._handle_input(l))
                btn.grid(row=r, column=col, columnspan=colspan, sticky="nsew",
                         padx=BUTTON_SPACING // 2, pady=BUTTON_SPACING // 2)
                self._buttons.append(btn)
                col += colspan

    # ---- input handling -------------------------------------------------
    def _handle_input(self, label: str):
        if label.isdigit():
            self.engine.input_digit(label)
        elif label == ".":
            self.engine.input_decimal()
        elif label in ("+", "-", "\u00d7", "\u00f7"):
            self.engine.input_operator(label)
        elif label == "(":
            self.engine.input_open_paren()
        elif label == ")":
            self.engine.input_close_paren()
        elif label == "AC":
            self.engine.clear()
        elif label == "\u232b":
            self.engine.backspace()
        elif label == "+/-":
            self.engine.toggle_sign()
        elif label == "%":
            self.engine.input_percent()
        elif label == "=":
            self._do_equals()
        self._refresh_display()

    def _do_equals(self):
        expr_before = self.engine.get_expression_display()
        result = self.engine.equals()
        if result is not None and self.on_result:
            self.on_result(expr_before, format_number(result))

    def _refresh_display(self):
        state = self.engine.state
        if state == CalculatorState.ERROR:
            self.display.set_expression(self.engine.get_expression_display())
            self.display.set_result(self.engine.error or "Error", is_error=True)
            return

        self.display.set_expression(self.engine.get_expression_display())
        if state == CalculatorState.SHOWING_RESULT:
            self.display.set_result(format_number(self.engine.last_result))
        else:
            preview = self.engine.get_result_preview()
            current_text = self.engine.tokens[-1]
            self.display.set_result(preview if preview is not None else current_text)

    # ---- keyboard ---------------------------------------------------
    def _bind_keyboard(self):
        # CTk widgets disallow bind_all (undefined behavior across CTk internals),
        # so bind on the toplevel window instead and clean up on destroy.
        self._toplevel = self.winfo_toplevel()
        self._key_bind_id = self._toplevel.bind("<Key>", self._on_key, add="+")
        self.bind("<Destroy>", self._on_destroy, add="+")

    def _on_destroy(self, event=None):
        try:
            self._toplevel.unbind("<Key>", self._key_bind_id)
        except Exception:
            pass

    def _on_key(self, event):
        try:
            if not self.winfo_exists() or not self.winfo_ismapped():
                return
        except Exception:
            return
        key = event.keysym
        char = event.char

        if char and char.isdigit():
            self._handle_input(char)
        elif char == ".":
            self._handle_input(".")
        elif char == "+":
            self._handle_input("+")
        elif char == "-":
            self._handle_input("-")
        elif char == "*":
            self._handle_input("\u00d7")
        elif char == "/":
            self._handle_input("\u00f7")
        elif char == "%":
            self._handle_input("%")
        elif char == "(":
            self._handle_input("(")
        elif char == ")":
            self._handle_input(")")
        elif key in ("Return", "KP_Enter"):
            self._handle_input("=")
        elif key == "Escape":
            self._handle_input("AC")
        elif key == "BackSpace":
            self._handle_input("\u232b")

    def load_expression(self, expression: str):
        """Used by History: load a past expression as the fresh current input."""
        self.engine.reset()
        # Rehydrate tokens directly from the stored expression string.
        self.engine.tokens = expression.split(" ") if expression else ["0"]
        self.engine.state = CalculatorState.ENTERING_NUMBER
        self._refresh_display()
