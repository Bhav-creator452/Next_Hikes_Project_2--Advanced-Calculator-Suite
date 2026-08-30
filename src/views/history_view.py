"""
History view: a dedicated, scrollable space for viewing/reusing past
calculations. Deliberately NOT embedded inside the calculator modules,
per Rule 4 (history must not permanently consume calculator space).
"""
import customtkinter as ctk
from collections import defaultdict
from datetime import datetime, date

from src.components.dialogs import SectionHeader, HistoryItem
from src.theme import theme_manager, FONTS


class HistoryView(ctk.CTkFrame):
    def __init__(self, master, history_manager, on_reuse=None, **kwargs):
        colors = theme_manager.colors
        super().__init__(master, fg_color=colors.bg, **kwargs)
        self.history_manager = history_manager
        self.on_reuse = on_reuse

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        header = ctk.CTkFrame(self, fg_color="transparent")
        header.grid(row=0, column=0, sticky="ew", padx=24, pady=(20, 8))
        header.grid_columnconfigure(0, weight=1)

        SectionHeader(header, "History").grid(row=0, column=0, sticky="w")

        clear_btn = ctk.CTkButton(header, text="Clear History", command=self._clear_history,
                                   fg_color=colors.error_bg, hover_color=colors.error_bg,
                                   text_color=colors.error, corner_radius=8, height=32)
        clear_btn.grid(row=0, column=1, sticky="e")

        self.scroll = ctk.CTkScrollableFrame(self, fg_color="transparent")
        self.scroll.grid(row=1, column=0, sticky="nsew", padx=24, pady=(0, 20))
        self.scroll.grid_columnconfigure(0, weight=1)

        self.refresh()

    def refresh(self):
        for widget in self.scroll.winfo_children():
            widget.destroy()

        entries = self.history_manager.get_all()
        colors = theme_manager.colors

        if not entries:
            ctk.CTkLabel(self.scroll, text="No calculations yet.", font=FONTS["body"],
                         text_color=colors.text_muted).grid(row=0, column=0, pady=40)
            return

        groups = defaultdict(list)
        for e in entries:
            groups[self._day_label(e.get("timestamp"))].append(e)

        row = 0
        for label, items in groups.items():
            ctk.CTkLabel(self.scroll, text=label, font=FONTS["label"], text_color=colors.text_muted,
                         anchor="w").grid(row=row, column=0, sticky="ew", pady=(12, 4))
            row += 1
            for entry in items:
                item = HistoryItem(
                    self.scroll,
                    expression=entry.get("expression", ""),
                    result=entry.get("result", ""),
                    timestamp=self._time_label(entry.get("timestamp")),
                    on_click=lambda e=entry: self._reuse(e),
                    on_delete=lambda eid=entry.get("id"): self._delete(eid),
                )
                item.grid(row=row, column=0, sticky="ew", pady=3)
                row += 1

    def _reuse(self, entry):
        if self.on_reuse:
            self.on_reuse(entry)

    def _delete(self, entry_id):
        self.history_manager.delete_entry(entry_id)
        self.refresh()

    def _clear_history(self):
        self.history_manager.clear()
        self.refresh()

    @staticmethod
    def _day_label(ts: str) -> str:
        if not ts:
            return "Earlier"
        try:
            dt = datetime.fromisoformat(ts)
        except ValueError:
            return "Earlier"
        if dt.date() == date.today():
            return "Today"
        return dt.strftime("%B %d, %Y")

    @staticmethod
    def _time_label(ts: str) -> str:
        if not ts:
            return ""
        try:
            dt = datetime.fromisoformat(ts)
            return dt.strftime("%I:%M %p").lstrip("0")
        except ValueError:
            return ""
