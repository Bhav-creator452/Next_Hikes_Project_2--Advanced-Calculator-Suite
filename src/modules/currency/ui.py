"""Currency Converter UI: live rates with offline fallback and clear labeling."""
import customtkinter as ctk

from src.modules.currency.currency import CurrencyService, CurrencyServiceError
from src.config import SUPPORTED_CURRENCIES, CURRENCY_SYMBOLS
from src.components.dialogs import SectionHeader, InputField, Dropdown
from src.components.buttons import SwapButton
from src.theme import theme_manager, FONTS
from src.utils.formatting import format_number, safe_float


class CurrencyConverterUI(ctk.CTkFrame):
    def __init__(self, master, on_result=None, **kwargs):
        colors = theme_manager.colors
        super().__init__(master, fg_color=colors.bg, **kwargs)
        self.on_result = on_result
        self.service = CurrencyService()

        self.grid_columnconfigure(0, weight=1)
        container = ctk.CTkFrame(self, fg_color="transparent")
        container.grid(row=0, column=0, sticky="n", pady=24)
        container.grid_columnconfigure(0, weight=1, minsize=420)

        SectionHeader(container, "Currency Converter").grid(row=0, column=0, sticky="w", padx=8, pady=(0, 16))

        card = ctk.CTkFrame(container, fg_color=colors.bg_secondary, corner_radius=14)
        card.grid(row=1, column=0, sticky="ew", padx=8)
        card.grid_columnconfigure(0, weight=1)
        card.grid_columnconfigure(2, weight=1)

        self.from_currency = Dropdown(card, values=SUPPORTED_CURRENCIES, command=lambda v: self._convert())
        self.from_currency.set("USD")
        self.from_currency.grid(row=0, column=0, sticky="ew", padx=16, pady=(16, 8))

        self.swap_btn = SwapButton(card, command=self._swap)
        self.swap_btn.grid(row=0, column=1, padx=4, pady=(16, 8))

        self.to_currency = Dropdown(card, values=SUPPORTED_CURRENCIES, command=lambda v: self._convert())
        self.to_currency.set("INR")
        self.to_currency.grid(row=0, column=2, sticky="ew", padx=16, pady=(16, 8))

        self.amount_entry = InputField(card, placeholder="Amount")
        self.amount_entry.grid(row=1, column=0, columnspan=3, sticky="ew", padx=16, pady=8)
        self.amount_entry.insert(0, "100")
        self.amount_entry.bind("<KeyRelease>", lambda e: self._convert())

        self.result_label = ctk.CTkLabel(card, text="", font=FONTS["display_result_small"],
                                          text_color=colors.text, anchor="w")
        self.result_label.grid(row=2, column=0, columnspan=3, sticky="ew", padx=16, pady=(8, 4))

        self.status_label = ctk.CTkLabel(card, text="", font=FONTS["small"],
                                          text_color=colors.text_muted, anchor="w")
        self.status_label.grid(row=3, column=0, columnspan=3, sticky="ew", padx=16, pady=(0, 8))

        refresh_btn = ctk.CTkButton(card, text="Refresh Rates", command=self._convert,
                                     fg_color=colors.button, hover_color=colors.button_hover,
                                     text_color=colors.text, corner_radius=10, height=34)
        refresh_btn.grid(row=4, column=0, columnspan=3, sticky="ew", padx=16, pady=(0, 16))

        # Populate initial rate/result without recording a history entry.
        self._suppress_history = True
        self._convert()
        self._suppress_history = False

    def _swap(self):
        f, t = self.from_currency.get(), self.to_currency.get()
        self.from_currency.set(t)
        self.to_currency.set(f)
        self._convert()

    def _convert(self):
        colors = theme_manager.colors
        amount = safe_float(self.amount_entry.get())
        from_c = self.from_currency.get()
        to_c = self.to_currency.get()

        try:
            converted, is_live, label = self.service.convert(amount, from_c, to_c)
        except CurrencyServiceError as e:
            self.result_label.configure(text="--", text_color=colors.error)
            self.status_label.configure(text=str(e), text_color=colors.error)
            return

        symbol = CURRENCY_SYMBOLS.get(to_c, "")
        self.result_label.configure(text=f"{symbol}{format_number(converted, '2')}", text_color=colors.text)

        if is_live:
            self.status_label.configure(text=f"\u2713 {label}", text_color=colors.success)
        else:
            self.status_label.configure(text=f"\u26a0 {label}", text_color=colors.operator)

        if self.on_result and not self._suppress_history and amount:
            expr = f"{format_number(amount)} {from_c} \u2192 {to_c}"
            self.on_result(expr, f"{symbol}{format_number(converted, '2')}")
