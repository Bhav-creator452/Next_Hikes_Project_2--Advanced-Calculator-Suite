"""Two-level calculator display: small expression line + dominant result line."""
import customtkinter as ctk

from src.theme import theme_manager, FONTS


class Display(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        colors = theme_manager.colors
        super().__init__(master, fg_color="transparent", **kwargs)

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=1)

        self.expression_label = ctk.CTkLabel(
            self, text="", anchor="e", justify="right",
            font=FONTS["display_expression"], text_color=colors.text_secondary,
        )
        self.expression_label.grid(row=0, column=0, sticky="ew", padx=16, pady=(10, 0))

        self.result_label = ctk.CTkLabel(
            self, text="0", anchor="e", justify="right",
            font=FONTS["display_result"], text_color=colors.text,
        )
        self.result_label.grid(row=1, column=0, sticky="sew", padx=16, pady=(0, 12))

    def set_expression(self, text: str) -> None:
        self.expression_label.configure(text=text)

    def set_result(self, text: str, is_error: bool = False) -> None:
        colors = theme_manager.colors
        # Shrink font for long results so they never get clipped.
        font_key = "display_result" if len(text) <= 10 else "display_result_small"
        self.result_label.configure(
            text=text,
            font=FONTS[font_key],
            text_color=colors.error if is_error else colors.text,
        )
