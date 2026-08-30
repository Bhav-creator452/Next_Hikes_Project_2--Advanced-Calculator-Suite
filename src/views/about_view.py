"""About view."""
import customtkinter as ctk

from src.config import APP_NAME, APP_VERSION, APP_TAGLINE
from src.components.dialogs import SectionHeader
from src.theme import theme_manager, FONTS

FEATURES = [
    "Standard & Scientific calculators with safe expression evaluation",
    "BMI calculator with WHO category ranges",
    "Unit converter across 7 categories",
    "Currency converter with live rates and offline fallback",
    "Unified, persistent calculation history",
    "Centralized theme and settings system",
]

TECH_STACK = ["Python 3", "CustomTkinter", "requests", "pytest"]


class AboutView(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        colors = theme_manager.colors
        super().__init__(master, fg_color=colors.bg, **kwargs)

        self.grid_columnconfigure(0, weight=1)
        container = ctk.CTkFrame(self, fg_color="transparent")
        container.grid(row=0, column=0, sticky="n", pady=32)
        container.grid_columnconfigure(0, weight=1, minsize=420)

        ctk.CTkLabel(container, text=APP_NAME, font=FONTS["section_header"],
                     text_color=colors.accent).grid(row=0, column=0, sticky="w", padx=8)
        ctk.CTkLabel(container, text=APP_TAGLINE, font=FONTS["body"],
                     text_color=colors.text_secondary).grid(row=1, column=0, sticky="w", padx=8, pady=(2, 4))
        ctk.CTkLabel(container, text=f"Version {APP_VERSION}", font=FONTS["small"],
                     text_color=colors.text_muted).grid(row=2, column=0, sticky="w", padx=8, pady=(0, 20))

        card = ctk.CTkFrame(container, fg_color=colors.bg_secondary, corner_radius=14)
        card.grid(row=3, column=0, sticky="ew", padx=8)
        card.grid_columnconfigure(0, weight=1)

        SectionHeader(card, "Features").grid(row=0, column=0, sticky="w", padx=16, pady=(16, 4))
        for i, f in enumerate(FEATURES, start=1):
            ctk.CTkLabel(card, text=f"\u2022 {f}", font=FONTS["label"], text_color=colors.text_secondary,
                         anchor="w", wraplength=440, justify="left").grid(row=i, column=0, sticky="w", padx=16, pady=2)

        row = len(FEATURES) + 1
        SectionHeader(card, "Tech Stack").grid(row=row, column=0, sticky="w", padx=16, pady=(16, 4))
        ctk.CTkLabel(card, text=", ".join(TECH_STACK), font=FONTS["label"], text_color=colors.text_secondary,
                     anchor="w", wraplength=440, justify="left").grid(row=row + 1, column=0, sticky="w", padx=16, pady=(0, 16))

        ctk.CTkLabel(container, text="Developer: Bhavdeep Kaur", font=FONTS["small"],
                     text_color=colors.text_muted).grid(row=4, column=0, sticky="w", padx=8, pady=(16, 0))
        ctk.CTkLabel(container, text="Project link: https://github.com/Bhav-creator452/Next_Hikes_Project_2--Advanced-Calculator-Suite",
                     font=FONTS["small"], text_color=colors.text_muted).grid(row=5, column=0, sticky="w", padx=8, pady=(2, 0))
