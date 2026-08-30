"""BMI Calculator UI: form-focused layout."""
import customtkinter as ctk

from src.modules.bmi.calculator import calculate_bmi, to_kg, to_cm
from src.utils.validation import validate_bmi_inputs
from src.components.dialogs import SectionHeader, InputField, ResultCard, Dropdown
from src.theme import theme_manager, FONTS

CATEGORY_COLOR_KEY = {
    "Underweight": "accent",
    "Normal": "success",
    "Overweight": "operator",
    "Obese": "error",
}


class BMICalculatorUI(ctk.CTkFrame):
    def __init__(self, master, on_result=None, **kwargs):
        colors = theme_manager.colors
        super().__init__(master, fg_color=colors.bg, **kwargs)
        self.on_result = on_result

        self.grid_columnconfigure(0, weight=1)
        container = ctk.CTkFrame(self, fg_color="transparent")
        container.grid(row=0, column=0, sticky="n", pady=24)
        container.grid_columnconfigure(0, weight=1, minsize=380)

        SectionHeader(container, "BMI Calculator").grid(row=0, column=0, sticky="w", padx=8, pady=(0, 16))

        form = ctk.CTkFrame(container, fg_color=colors.bg_secondary, corner_radius=14)
        form.grid(row=1, column=0, sticky="ew", padx=8)
        form.grid_columnconfigure(0, weight=1)
        form.grid_columnconfigure(1, weight=1)

        # Height row
        ctk.CTkLabel(form, text="Height", font=FONTS["label"], text_color=colors.text_secondary,
                     anchor="w").grid(row=0, column=0, sticky="w", padx=16, pady=(16, 4))
        self.height_unit = Dropdown(form, values=["cm", "ft-in"], command=self._on_unit_change, width=90)
        self.height_unit.grid(row=0, column=1, sticky="e", padx=16, pady=(16, 4))

        self.height_entry = InputField(form, placeholder="e.g. 170")
        self.height_entry.grid(row=1, column=0, columnspan=2, sticky="ew", padx=16, pady=(0, 12))

        # Weight row
        ctk.CTkLabel(form, text="Weight", font=FONTS["label"], text_color=colors.text_secondary,
                     anchor="w").grid(row=2, column=0, sticky="w", padx=16, pady=(0, 4))
        self.weight_unit = Dropdown(form, values=["kg", "lb"], width=90)
        self.weight_unit.grid(row=2, column=1, sticky="e", padx=16, pady=(0, 4))

        self.weight_entry = InputField(form, placeholder="e.g. 65")
        self.weight_entry.grid(row=3, column=0, columnspan=2, sticky="ew", padx=16, pady=(0, 12))

        self.error_label = ctk.CTkLabel(form, text="", font=FONTS["small"], text_color=colors.error,
                                         anchor="w")
        self.error_label.grid(row=4, column=0, columnspan=2, sticky="ew", padx=16)

        calc_btn = ctk.CTkButton(form, text="Calculate BMI", command=self._calculate,
                                  fg_color=colors.accent, hover_color=colors.accent_hover,
                                  text_color=colors.accent_text, corner_radius=10, height=40)
        calc_btn.grid(row=5, column=0, columnspan=2, sticky="ew", padx=16, pady=16)

        self.result_card = ResultCard(container)
        self.result_card.grid(row=2, column=0, sticky="ew", padx=8, pady=(16, 0))
        self.result_card.set("--", "Enter your height and weight to see your BMI.")

    def _on_unit_change(self, value):
        placeholder = "e.g. 5.7 (ft.in)" if value == "ft-in" else "e.g. 170"
        self.height_entry.configure(placeholder_text=placeholder)

    def _calculate(self):
        self.error_label.configure(text="")
        height_unit = self.height_unit.get()
        weight_unit = self.weight_unit.get()

        height_text = self.height_entry.get()
        weight_text = self.weight_entry.get()

        ok, height_val, weight_val, err = validate_bmi_inputs(
            height_text, weight_text, height_unit, weight_unit
        )
        if not ok:
            self.error_label.configure(text=err)
            return

        try:
            if height_unit == "ft-in":
                ft = int(height_val)
                inch = (height_val - ft) * 10  # 5.7 -> 5 ft 7 in convention
                height_cm = to_cm(0, "ft-in", height_ft=ft, height_in=inch)
            else:
                height_cm = to_cm(height_val, "cm")
            weight_kg = to_kg(weight_val, weight_unit)
            result = calculate_bmi(weight_kg, height_cm)
        except ValueError as e:
            self.error_label.configure(text=str(e))
            return

        colors = theme_manager.colors
        color_key = CATEGORY_COLOR_KEY.get(result.category, "accent")
        is_error_color = color_key == "error"
        caption = (
            f"{result.category} \u2022 Healthy range: "
            f"{result.healthy_range_kg[0]}\u2013{result.healthy_range_kg[1]} kg"
        )
        self.result_card.set(f"BMI: {result.bmi}", caption, is_error=is_error_color)

        if self.on_result:
            expr = f"BMI ({height_text}{height_unit}, {weight_text}{weight_unit})"
            self.on_result(expr, f"{result.bmi} \u2022 {result.category}")
