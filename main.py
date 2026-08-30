"""
CalcSuite entry point.

Run with:
    python main.py
"""
import customtkinter as ctk

from src.app import CalcSuiteApp


def main():
    ctk.set_appearance_mode("Dark")
    app = CalcSuiteApp()
    app.mainloop()


if __name__ == "__main__":
    main()
