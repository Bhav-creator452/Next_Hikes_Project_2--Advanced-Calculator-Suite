# src/app.py

import tkinter as tk

from src.constants import (
    WINDOW_TITLE,
    WINDOW_WIDTH,
    WINDOW_HEIGHT,
    BACKGROUND_COLOR
)

from src.ui import CalculatorUI


class CalculatorApp:

    def __init__(self):
        self.root = tk.Tk()

        self.root.title(WINDOW_TITLE)
        self.root.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")
        self.root.configure(bg=BACKGROUND_COLOR)

        # Allow the calculator window to be resized.
        self.root.resizable(True, True)

        # Set a sensible minimum size.
        self.root.minsize(700, 550)

        # Center the window initially.
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()

        x = (screen_width - WINDOW_WIDTH) // 2
        y = (screen_height - WINDOW_HEIGHT) // 2

        self.root.geometry(
            f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}+{x}+{y}"
    )

        self.ui = CalculatorUI(self.root)

    def run(self):

        self.root.mainloop()