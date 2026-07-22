"""
Brutalist Desktop Calculator
Entry point — run this file to launch the app.
"""

import tkinter as tk
from calculator_ui import CalculatorUI


def main():
    root = tk.Tk()
    CalculatorUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
