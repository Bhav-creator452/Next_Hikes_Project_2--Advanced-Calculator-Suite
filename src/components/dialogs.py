"""Lightweight reusable dialog / card components."""
import customtkinter as ctk

from src.theme import theme_manager, FONTS, CORNER_RADIUS


def show_confirm_dialog(master, title: str, message: str, on_confirm) -> None:
    """A minimal modal confirmation dialog (used for e.g. 'Clear History')."""
    colors = theme_manager.colors
    dialog = ctk.CTkToplevel(master)
    dialog.title(title)
    dialog.geometry("360x180")
    dialog.configure(fg_color=colors.bg_secondary)
    dialog.resizable(False, False)
    dialog.grab_set()

    ctk.CTkLabel(dialog, text=message, font=FONTS["body"], text_color=colors.text,
                 wraplength=320, justify="center").pack(expand=True, padx=20, pady=(24, 12))

    btn_frame = ctk.CTkFrame(dialog, fg_color="transparent")
    btn_frame.pack(pady=(0, 20))

    def _confirm():
        dialog.destroy()
        on_confirm()

    ctk.CTkButton(btn_frame, text="Cancel", command=dialog.destroy,
                   fg_color=colors.button, hover_color=colors.button_hover,
                   text_color=colors.text).pack(side="left", padx=8)
    ctk.CTkButton(btn_frame, text="Confirm", command=_confirm,
                   fg_color=colors.error, hover_color=colors.error,
                   text_color="#ffffff").pack(side="left", padx=8)


class SectionHeader(ctk.CTkLabel):
    def __init__(self, master, text: str, **kwargs):
        colors = theme_manager.colors
        super().__init__(master, text=text, font=FONTS["section_header"],
                          text_color=colors.text, anchor="w", **kwargs)


class InputField(ctk.CTkEntry):
    def __init__(self, master, placeholder: str = "", **kwargs):
        colors = theme_manager.colors
        super().__init__(
            master, placeholder_text=placeholder, fg_color=colors.bg_secondary,
            border_color=colors.border, text_color=colors.text,
            font=FONTS["body"], corner_radius=8, height=38, **kwargs,
        )


class ResultCard(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        colors = theme_manager.colors
        super().__init__(master, fg_color=colors.bg_elevated, corner_radius=CORNER_RADIUS, **kwargs)
        self.grid_columnconfigure(0, weight=1)

        self.value_label = ctk.CTkLabel(self, text="", font=FONTS["display_result_small"],
                                         text_color=colors.text)
        self.value_label.grid(row=0, column=0, sticky="w", padx=20, pady=(16, 0))

        self.caption_label = ctk.CTkLabel(self, text="", font=FONTS["label"],
                                           text_color=colors.text_secondary)
        self.caption_label.grid(row=1, column=0, sticky="w", padx=20, pady=(0, 16))

    def set(self, value: str, caption: str = "", is_error: bool = False) -> None:
        colors = theme_manager.colors
        self.value_label.configure(text=value, text_color=colors.error if is_error else colors.text)
        self.caption_label.configure(text=caption)


class Dropdown(ctk.CTkOptionMenu):
    def __init__(self, master, values, command=None, **kwargs):
        colors = theme_manager.colors
        super().__init__(
            master, values=values, command=command,
            fg_color=colors.bg_secondary, button_color=colors.button,
            button_hover_color=colors.button_hover, text_color=colors.text,
            font=FONTS["body"], dropdown_font=FONTS["body"], corner_radius=8,
            **kwargs,
        )


class HistoryItem(ctk.CTkFrame):
    def __init__(self, master, expression: str, result: str, timestamp: str,
                 on_click=None, on_delete=None, **kwargs):
        colors = theme_manager.colors
        super().__init__(master, fg_color=colors.bg_secondary, corner_radius=10, **kwargs)
        self.grid_columnconfigure(0, weight=1)

        text_frame = ctk.CTkFrame(self, fg_color="transparent")
        text_frame.grid(row=0, column=0, sticky="ew", padx=(14, 4), pady=10)

        ctk.CTkLabel(text_frame, text=expression, font=FONTS["label"],
                     text_color=colors.text_secondary, anchor="w").pack(fill="x")
        ctk.CTkLabel(text_frame, text=result, font=FONTS["body"],
                     text_color=colors.text, anchor="w").pack(fill="x")
        ctk.CTkLabel(text_frame, text=timestamp, font=FONTS["small"],
                     text_color=colors.text_muted, anchor="w").pack(fill="x")

        if on_click:
            for widget in (self, text_frame, *text_frame.winfo_children()):
                widget.bind("<Button-1>", lambda e: on_click())

        if on_delete:
            del_btn = ctk.CTkButton(self, text="\u00d7", width=28, height=28,
                                     fg_color="transparent", hover_color=colors.error_bg,
                                     text_color=colors.text_muted, command=on_delete)
            del_btn.grid(row=0, column=1, padx=(0, 10))
