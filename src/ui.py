import tkinter as tk

from src.calculator import Calculator

from src.constants import (
    BACKGROUND_COLOR,
    TEXT_COLOR,
    SECONDARY_TEXT,
    EXPRESSION_FONT,
    RESULT_FONT,
    WINDOW_PADDING,
    DISPLAY_TOP_PADDING,
    DISPLAY_BOTTOM_PADDING,
    DISPLAY_HEIGHT,
    BUTTON_LAYOUT,
    NUMBER_BUTTON,
    FUNCTION_BUTTON,
    OPERATOR_BUTTON,
    BUTTON_TEXT,
    BUTTON_FONT,
)

class CalculatorUI:

    def __init__(self, root):

        self.root = root

        self.root.minsize(650, 700)

        self.root.bind_all("<KeyPress>", self.handle_keypress)

        self.current_value = "0"

        self.first_number = None
        self.operator = None

        self.expression = ""

        self.display_expression = ""

        self.just_calculated = False

        self.percent_used = False

        self.scientific_mode = False

        self.create_layout()
        self.create_display()
        self.create_buttons()


    def handle_keypress(self, event):
        key = event.keysym
        char = event.char

         # Ignore Windows / system modifier keys.
        system_keys = {
        "Super_L",
        "Super_R",
        "Win_L",
        "Win_R",
        "Meta_L",
        "Meta_R",
        "Control_L",
        "Control_R",
        "Alt_L",
        "Alt_R",
        "Shift_L",
        "Shift_R",
    }

        if key in system_keys:
            return "break"

    # Numbers
        if char in "0123456789":
            self.handle_button({
            "text": char,
            "type": "number"
        })
            return "break"

    # Decimal
        if char == ".":
            self.handle_button({
            "text": ".",
            "type": "number"
        })
            return "break"

    # Operators
        operator_map = {
            "+": "+",
            "-": "-",
            "*": "×",
            "/": "÷"
    }

        if char in operator_map:
            self.handle_button({
            "text": operator_map[char],
            "type": "operator"
        })
            return "break"

    # Percentage
        if char == "%":
            self.handle_button({
            "text": "%",
            "type": "function"
        })
            return "break"

    # Equals / Enter
        if char == "=" or key == "Return":
            self.handle_button({
            "text": "=",
            "type": "equals"
        })
            return "break"

    # Backspace
        if key == "BackSpace":
            self.handle_button({
            "text": "⌫",
            "type": "function"
        })
            return "break"

    # Escape / AC
        if key == "Escape":
            self.handle_button({
            "text": "AC",
            "type": "function"
        })
            return "break"

    # Every other key is ignored.
        return "break"

    def create_layout(self):
        """Create the main desktop calculator layout."""

        # Main container
        self.main_frame = tk.Frame(
            self.root,
            bg=BACKGROUND_COLOR
        )

        self.main_frame.pack(
            fill="both",
            expand=True
        )

        # Allow the three sections to resize.
        self.main_frame.grid_columnconfigure(
            0,
            weight=0
        )

        self.main_frame.grid_columnconfigure(
            1,
            weight=1
        )

        self.main_frame.grid_columnconfigure(
            2,
            weight=0
        )

        self.main_frame.grid_rowconfigure(
            0,
            weight=1
        )

    # -------------------------------------------------
    # LEFT SIDEBAR
    # -------------------------------------------------

        self.sidebar_frame = tk.Frame(
            self.main_frame,
            bg="#242426",
            width=170
        )

        self.sidebar_frame.grid(
            row=0,
            column=0,
            sticky="nsew"
        )

        self.sidebar_frame.grid_propagate(False)

    # -------------------------------------------------
    # CENTER CALCULATOR AREA
    # -------------------------------------------------

        self.calculator_frame = tk.Frame(
            self.main_frame,
            bg=BACKGROUND_COLOR
        )

        self.calculator_frame.grid(
            row=0,
            column=1,
            sticky="nsew"
        )

        self.calculator_frame.grid_rowconfigure(
            0,
            weight=1
        )

        self.calculator_frame.grid_columnconfigure(
            0,
            weight=1
    )

    # -------------------------------------------------
    # RIGHT HISTORY PANEL
    # -------------------------------------------------

        self.history_frame = tk.Frame(
            self.main_frame,
            bg="#242426",
            width=230
    )

        self.history_frame.grid(
            row=0,
            column=2,
            sticky="nsew"
    )

        self.history_frame.grid_propagate(False)

        # Temporary sidebar content
        sidebar_title = tk.Label(
            self.sidebar_frame,
            text="Calculator",
            bg="#242426",
            fg=TEXT_COLOR,
            font=("Segoe UI", 16, "bold")
        )

        sidebar_title.pack(
            anchor="w",
            padx=20,
            pady=(30, 20)
        )

        basic_label = tk.Label(
            self.sidebar_frame,
            text="▣  Basic",
            bg="#242426",
            fg=TEXT_COLOR,
            font=("Segoe UI", 12)
        )

        basic_label.pack(
            anchor="w",
            padx=20,
            pady=8
        )

        scientific_label = tk.Label(
            self.sidebar_frame,
            text="⚗  Scientific",
            bg="#242426",
            fg=TEXT_COLOR,
            font=("Segoe UI", 12)
        )

        scientific_label.pack(
            anchor="w",
            padx=20,
            pady=8
        )

    # Temporary history content
        history_title = tk.Label(
            self.history_frame,
            text="History",
            bg="#242426",
            fg=TEXT_COLOR,
            font=("Segoe UI", 16, "bold")
    )

        history_title.pack(
            anchor="w",
            padx=20,
            pady=(30, 20)
    )

    def create_display(self):

        display_frame = tk.Frame(
            self.calculator_frame,
            bg=BACKGROUND_COLOR,
            height=DISPLAY_HEIGHT
        )
        display_frame.pack_propagate(False)

        display_frame.pack(
        fill="x",
        padx=WINDOW_PADDING,
        pady=(DISPLAY_TOP_PADDING, DISPLAY_BOTTOM_PADDING)
)

        self.expression_label = tk.Label(
            display_frame,
            text=" ",
            anchor="e",
            bg=BACKGROUND_COLOR,
            fg=SECONDARY_TEXT,
            font=EXPRESSION_FONT
        )

        self.expression_label.pack(
            fill="x"
        )

        self.result_label = tk.Label(
            display_frame,
            text="0",
            anchor="e",
            bg=BACKGROUND_COLOR,
            fg=TEXT_COLOR,
            font=RESULT_FONT
        )

        self.result_label.pack(
            fill="x",
            pady=(0, 10)
        )

        divider = tk.Frame(
        self.root,
        height=1,
        bg="#2C2C2E"
    )

        divider.pack(
        fill="x",
        padx=20,
        pady=(5, 0)
    )

    def create_mode_selector(self):
        """Create the Basic / Scientific mode selector."""

        self.mode_frame = tk.Frame(
            self.root,
            bg=BACKGROUND_COLOR
        )

        self.mode_frame.pack(
            fill="x",
            padx=20,
            pady=(5, 0)
        )

        self.mode_button = tk.Button(
            self.mode_frame,
            text="Basic",
            bg=BACKGROUND_COLOR,
            fg=TEXT_COLOR,
            activebackground=BACKGROUND_COLOR,
            activeforeground=TEXT_COLOR,
            relief="flat",
            bd=0,
            font=("Arial", 12),
            command=self.toggle_scientific_mode
        )

        self.mode_button.pack(
            anchor="w"
    )

    def toggle_scientific_mode(self):
        """Switch between Basic and Scientific calculator modes."""

        self.scientific_mode = not self.scientific_mode

        if self.scientific_mode:
            self.mode_button.config(text="Scientific")
            self.show_scientific_buttons()
        else:
            self.mode_button.config(text="Basic")
            self.hide_scientific_buttons()

    def create_buttons(self):

        button_frame = tk.Frame(
        self.calculator_frame,
        bg=BACKGROUND_COLOR
)

        button_frame.pack(
            fill="both",
            expand=True,
            padx=20,
            pady=(10, 20)
        )

        button_frame.pack_propagate(False)

        for row_index, row in enumerate(BUTTON_LAYOUT):

            for column_index, button in enumerate(row):

                if button["type"] == "number":
                    background = NUMBER_BUTTON

                elif button["type"] == "function":
                    background = FUNCTION_BUTTON

                elif button["type"] == "operator":
                    background = OPERATOR_BUTTON

                else:
                    background = OPERATOR_BUTTON

                btn = tk.Button(
                button_frame,
                text=button["text"],
                bg=background,
                fg=BUTTON_TEXT,
                font=BUTTON_FONT,
                command=lambda b=button: self.handle_button(b)
        )
                btn.grid(
                row=row_index,
                column=column_index,
                sticky="nsew",
                padx=5,
                pady=5
)
    # Make all columns expand equally
        for column in range(len(BUTTON_LAYOUT[0])):
            button_frame.grid_columnconfigure(
            column, 
            weight=1)

# Make all rows expand equally
        for row in range(len(BUTTON_LAYOUT)):
            button_frame.grid_rowconfigure(
            row,
            weight=1,
            minsize=55
    )

    def format_result(self, result):
        if result == int(result):
            return str(int(result))

        return str(result)

    def create_scientific_buttons(self):
        """Create the scientific calculator controls."""

        self.scientific_frame = tk.Frame(
            self.root,
            bg=BACKGROUND_COLOR
        )

        scientific_buttons = [
            {"text": "x²", "type": "scientific", "action": "square"},
            {"text": "xʸ", "type": "scientific", "action": "power"},
            {"text": "√x", "type": "scientific", "action": "sqrt"},
            {"text": "1/x", "type": "scientific", "action": "reciprocal"},
        ]

        for column, button in enumerate(scientific_buttons):

            btn = tk.Button(
                self.scientific_frame,
                text=button["text"],
                bg=FUNCTION_BUTTON,
                fg=BUTTON_TEXT,
                activebackground=FUNCTION_BUTTON,
                activeforeground=BUTTON_TEXT,
                font=BUTTON_FONT,
                relief="flat",
                command=lambda b=button: self.handle_scientific_button(b)
            )

            btn.grid(
                row=0,
                column=column,
                sticky="nsew",
                padx=5,
                pady=5
            )

            self.scientific_frame.grid_columnconfigure(
                column,
                weight=1
            )

    def show_scientific_buttons(self):
        """Show the scientific controls."""

        if not hasattr(self, "scientific_frame"):
            self.create_scientific_buttons()

        self.scientific_frame.pack(
            fill="x",
            padx=20,
            pady=(5, 0)
        )


    def hide_scientific_buttons(self):
        """Hide the scientific controls."""

        if hasattr(self, "scientific_frame"):
            self.scientific_frame.pack_forget()

    def handle_scientific_button(self, button):
        """Handle scientific calculator operations."""

        action = button["action"]

        if self.current_value in ("", "Error"):
            return

        try:
            value = float(self.current_value)

            if action == "square":
                result = value ** 2

            elif action == "sqrt":
                if value < 0:
                    raise ValueError(
                        "Cannot take square root of a negative number"
                    )

                result = value ** 0.5

            elif action == "reciprocal":
                if value == 0:
                    raise ZeroDivisionError(
                        "Cannot divide by zero"
                    )

                result = 1 / value

            elif action == "power":
                # xʸ needs a second number.
                self.expression = self.current_value + "^"
                self.current_value = ""

                self.result_label.config(
                    text=self.expression
                )

                return

            else:
                return

            self.current_value = self.format_result(result)

            self.result_label.config(
                text=self.current_value
            )

            self.just_calculated = True

        except ZeroDivisionError:
            self.current_value = "Error"
            self.result_label.config(text="Error")

        except ValueError:
            self.current_value = "Error"
            self.result_label.config(text="Error")

    def handle_button(self, button):

        if button["type"] == "number":

            if self.just_calculated:
                self.current_value = button["text"]
                self.expression = ""
                self.first_number = None
                self.operator = None
                self.just_calculated = False

                self.expression_label.config(
                    text=""
)
            elif self.current_value in ("0", ""):
                self.current_value = button["text"]
            else:
                self.current_value += button["text"]

            if self.expression:
                self.result_label.config(
                    text=self.expression + self.current_value
                )
            else:
                self.result_label.config(
                    text=self.current_value
                )

        elif button["type"] == "decimal":
            if "." not in self.current_value:
                if self.current_value == "":
                    self.current_value = "0."
                else:
                    self.current_value += "."

                if self.expression:
                    self.result_label.config(
                        text=self.expression + self.current_value
                    )
                else:
                    self.result_label.config(
                        text=self.current_value
                    )

        elif button["type"] == "function":
            if button["text"] == "AC":
                self.current_value = "0"
                self.first_number = None
                self.operator = None
                self.expression = ""
                self.expression_label.config(text="")
                self.result_label.config(text="0")


            elif button["text"] == "+/-":

                # No second number has been entered yet.
                # Allow the user to start it as negative.
                if self.current_value == "":
                    self.current_value = "-"

                # Toggle an existing negative number back to positive.
                elif self.current_value.startswith("-"):
                    self.current_value = self.current_value[1:]

                # Make a positive number negative.
                else:
                    self.current_value = "-" + self.current_value

                # Update the display.
                if self.expression:
                    self.result_label.config(
                        text=self.expression + self.current_value
                    )
                else:
                    self.result_label.config(
                        text=self.current_value
                    )

            elif button["text"] == "%":
                if self.current_value in ("", "-"):
                    return

                try:
                    value = float(self.current_value)

                    # Preserve the original expression only when
                    # percentage is being used as part of an expression.
                    if self.expression:
                        self.display_expression = self.expression + self.current_value + "%"
                    else:
                        self.display_expression = ""

                    # Percentage used inside an expression
                    if self.operator is not None and self.first_number is not None:

                        if self.operator in ("+", "-"):
                            # 10% of the first number
                            percentage = self.first_number * (value / 100)

                            self.current_value = self.format_result(percentage)

                        else:
                            # For × and ÷, percentage is simply value / 100
                            percentage = value / 100

                            self.current_value = self.format_result(percentage)

                        self.percent_used = True

                    # Standalone percentage
                    else:
                        value = value / 100

                        self.current_value = self.format_result(value)

                        self.percent_used = True

                    # Show the original expression only when
                    # percentage is part of an expression.
                    if self.expression:
                        self.result_label.config(
                            text=self.display_expression
                        )
                    else:
                        self.result_label.config(
                            text=self.current_value
                        )

                except ValueError:
                    self.current_value = "Error"

                    self.result_label.config(
                        text="Error"
                    )
                return


            elif button["text"] == "⌫":

                # Delete from the number currently being entered.
                if self.current_value != "":

                    if len(self.current_value) > 1:
                        self.current_value = self.current_value[:-1]

                    elif self.expression:
                        # We are deleting the last digit of the second number.
                        # Leave it empty so the operator remains visible.
                        self.current_value = ""

                    else:
                        # We are deleting the last digit of a standalone number.
                        # Calculator should show 0 instead of becoming empty.
                        self.current_value = "0"

                # If the current number becomes empty,
                # the next backspace should remove the operator.
                elif self.expression:
                    self.expression = self.expression[:-1]

                    # The remaining expression is the first number.
                    if self.expression:
                        self.current_value = self.expression
                        self.expression = ""
                        self.first_number = None
                        self.operator = None
                    else:
                        self.current_value = "0"

                else:
                    self.current_value = "0"

                # Update the display.
                if self.expression:
                    self.result_label.config(
                        text=self.expression + self.current_value
                    )
                else:
                    self.result_label.config(
                        text=self.current_value
                    )

        elif button["type"] == "operator":
            self._handle_operator(button["text"])
            
        elif button["type"] == "equals":
            try:
                # Percentage calculations still use the existing
                # two-number logic for now.
                if self.percent_used:
                    second_number = float(self.current_value)
                    result = Calculator.calculate(
                        self.first_number,
                        self.operator,
                        second_number
                    )
                    self.expression = self.display_expression
                else:
                    # Normal expressions use the new expression engine.
                    self.expression += self.current_value
                    result = Calculator.evaluate_expression(self.expression)

                self.current_value = self.format_result(result)
                self.expression_label.config(text=self.expression)
                self.result_label.config(text=self.current_value)
                self.just_calculated = True
                self.percent_used = False
                self.display_expression = ""

            except ZeroDivisionError:
                self.expression_label.config(
                    text=self.expression + self.current_value
                )
                self.current_value = "Error"
                self.result_label.config(text="Error")

            except ValueError:
                self.expression_label.config(
                    text=self.expression + self.current_value
                )
                self.current_value = "Error"
                self.result_label.config(text="Error")

    def _handle_operator(self, operator):
        """Handle an operator while building an expression."""

        operators = ("+", "-", "×", "÷")

        # Continue from the previous result.
        if self.just_calculated:
            self.expression = self.current_value
            self.current_value = ""
            self.just_calculated = False

        # Start a new expression.
        if not self.expression:
            if self.current_value in ("", "Error"):
                return

            self.expression = self.current_value
            self.current_value = ""

            self.expression += operator

        # A number is currently being entered.
        elif self.current_value:
            # Commit that number to the expression.
            self.expression += self.current_value
            self.current_value = ""

            # Add the new operator.
            self.expression += operator

        # No number is currently being entered.
        # Therefore an operator is already at the end.
        elif self.expression[-1:] in operators:
            # Replace the previous operator.
            self.expression = self.expression[:-1] + operator

        else:
            self.expression += operator

        # Keep this for existing percentage functionality.
        self.operator = operator

    # Update display.
        self.result_label.config(
            text=self.expression
    )