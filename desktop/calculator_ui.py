"""
Brutalist calculator UI.
Design language: raw exposure, hard edges, monospace type,
stark black/white palette with a single red accent.
"""

import tkinter as tk
from calculator_engine import CalculatorEngine

# ------------------------------------------------------------------
# Palette
# ------------------------------------------------------------------
BG          = "#0a0a0a"   # near-black canvas
DISPLAY_BG  = "#000000"
DISPLAY_FG  = "#ffffff"
OP_ACTIVE   = "#ff2200"   # red highlight for active operator

BTN_NUM_BG  = "#ffffff"
BTN_NUM_FG  = "#000000"
BTN_NUM_ACT = "#cccccc"

BTN_OP_BG   = "#1a1a1a"
BTN_OP_FG   = "#ffffff"
BTN_OP_ACT  = "#333333"

BTN_FN_BG   = "#2a2a2a"
BTN_FN_FG   = "#aaaaaa"
BTN_FN_ACT  = "#444444"

BTN_CLR_BG  = "#ff2200"
BTN_CLR_FG  = "#ffffff"
BTN_CLR_ACT = "#cc1a00"

BTN_EQ_BG   = "#ffffff"
BTN_EQ_FG   = "#000000"
BTN_EQ_ACT  = "#aaaaaa"

BORDER      = "#ffffff"
BORDER_DIM  = "#333333"

# ------------------------------------------------------------------
# Fonts
# ------------------------------------------------------------------
FONT_DISPLAY  = ("Courier", 34, "bold")
FONT_SUBINFO  = ("Courier", 10, "bold")
FONT_BTN      = ("Courier", 16, "bold")
FONT_BTN_SM   = ("Courier", 13, "bold")

# ------------------------------------------------------------------
# Button layout
# (label, grid_row, grid_col, colspan, style)
# ------------------------------------------------------------------
BUTTON_MAP = [
    ("AC",  0, 0, 1, "clear"),
    ("⌫",   0, 1, 1, "fn"),
    ("%",   0, 2, 1, "fn"),
    ("÷",   0, 3, 1, "op"),

    ("7",   1, 0, 1, "num"),
    ("8",   1, 1, 1, "num"),
    ("9",   1, 2, 1, "num"),
    ("×",   1, 3, 1, "op"),

    ("4",   2, 0, 1, "num"),
    ("5",   2, 1, 1, "num"),
    ("6",   2, 2, 1, "num"),
    ("-",   2, 3, 1, "op"),

    ("1",   3, 0, 1, "num"),
    ("2",   3, 1, 1, "num"),
    ("3",   3, 2, 1, "num"),
    ("+",   3, 3, 1, "op"),

    ("+/-", 4, 0, 1, "fn"),
    ("0",   4, 1, 1, "num"),
    (".",   4, 2, 1, "num"),
    ("=",   4, 3, 1, "equals"),
]

STYLE_COLORS = {
    "num":    (BTN_NUM_BG,  BTN_NUM_FG,  BTN_NUM_ACT),
    "op":     (BTN_OP_BG,   BTN_OP_FG,   BTN_OP_ACT),
    "fn":     (BTN_FN_BG,   BTN_FN_FG,   BTN_FN_ACT),
    "clear":  (BTN_CLR_BG,  BTN_CLR_FG,  BTN_CLR_ACT),
    "equals": (BTN_EQ_BG,   BTN_EQ_FG,   BTN_EQ_ACT),
}

OPERATORS = {"÷", "×", "-", "+"}

# ------------------------------------------------------------------
# Keyboard mapping
# ------------------------------------------------------------------
# Keysym names for special/operator keys — wrapped as <keysym> by _bind_keyboard.
# Plain digit/decimal keys are bound separately as bare characters.
KEY_MAP = {
    "Return":    "=",
    "KP_Enter":  "=",
    "Escape":    "AC",
    "BackSpace": "⌫",
    "percent":   "%",
    "plus":      "+",
    "minus":     "-",
    "asterisk":  "×",
    "slash":     "÷",
    "KP_Add":      "+",
    "KP_Subtract": "-",
    "KP_Multiply": "×",
    "KP_Divide":   "÷",
    "KP_Decimal":  ".",
}


class CalculatorUI:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.engine = CalculatorEngine()
        self._op_buttons: dict[str, tk.Button] = {}

        self._configure_window()
        self._build_header()
        self._build_display()
        self._build_divider()
        self._build_buttons()
        self._bind_keyboard()

    # ------------------------------------------------------------------
    # Window
    # ------------------------------------------------------------------

    def _configure_window(self):
        self.root.title("CALCULATOR")
        self.root.configure(bg=BG)
        self.root.resizable(False, False)

        # Outer border frame — raw solid outline
        self.outer = tk.Frame(
            self.root, bg=BG,
            highlightbackground=BORDER,
            highlightthickness=3,
        )
        self.outer.pack(padx=10, pady=10)

    # ------------------------------------------------------------------
    # Header
    # ------------------------------------------------------------------

    def _build_header(self):
        hdr = tk.Frame(self.outer, bg=BG)
        hdr.pack(fill="x", padx=6, pady=(6, 0))

        tk.Label(
            hdr, text="// CALCULATOR", font=FONT_SUBINFO,
            bg=BG, fg=BORDER_DIM, anchor="w",
        ).pack(side="left")

        tk.Label(
            hdr, text="BRUTALIST v1.0", font=FONT_SUBINFO,
            bg=BG, fg=BORDER_DIM, anchor="e",
        ).pack(side="right")

    # ------------------------------------------------------------------
    # Display
    # ------------------------------------------------------------------

    def _build_display(self):
        disp_frame = tk.Frame(
            self.outer, bg=DISPLAY_BG,
            highlightbackground=BORDER_DIM,
            highlightthickness=1,
        )
        disp_frame.pack(fill="x", padx=6, pady=6)

        # Sub-info row: previous operand + active operator
        self.sub_var = tk.StringVar(value="")
        tk.Label(
            disp_frame, textvariable=self.sub_var,
            font=FONT_SUBINFO, bg=DISPLAY_BG, fg=BORDER_DIM,
            anchor="e", padx=8, pady=6,
        ).pack(fill="x")

        # Main number display
        self.display_var = tk.StringVar(value="0")
        self.display_lbl = tk.Label(
            disp_frame, textvariable=self.display_var,
            font=FONT_DISPLAY, bg=DISPLAY_BG, fg=DISPLAY_FG,
            anchor="e", padx=8, pady=8,
            width=13,
        )
        self.display_lbl.pack(fill="x")

    # ------------------------------------------------------------------
    # Divider
    # ------------------------------------------------------------------

    def _build_divider(self):
        tk.Frame(self.outer, bg=BORDER, height=3).pack(fill="x")

    # ------------------------------------------------------------------
    # Buttons
    # ------------------------------------------------------------------

    def _build_buttons(self):
        grid = tk.Frame(self.outer, bg=BG)
        grid.pack(padx=0, pady=0)

        for (label, row, col, colspan, style) in BUTTON_MAP:
            bg, fg, active_bg = STYLE_COLORS[style]
            font = FONT_BTN_SM if label in ("+/-", "⌫") else FONT_BTN

            btn = tk.Button(
                grid,
                text=label,
                font=font,
                bg=bg, fg=fg,
                activebackground=active_bg,
                activeforeground=fg,
                relief=tk.FLAT,
                bd=0,
                width=5 if colspan == 1 else 11,
                height=2,
                cursor="hand2",
                highlightbackground=BG,
                highlightthickness=2,
                command=lambda l=label: self._on_press(l),
            )
            btn.grid(
                row=row, column=col, columnspan=colspan,
                padx=2, pady=2, sticky="nsew",
            )

            if label in OPERATORS:
                self._op_buttons[label] = btn

    # ------------------------------------------------------------------
    # Keyboard
    # ------------------------------------------------------------------

    def _bind_keyboard(self):
        for key, action in KEY_MAP.items():
            self.root.bind(f"<{key}>", lambda e, a=action: self._on_press(a))
        # Also bind plain character keys
        for char in "0123456789.":
            self.root.bind(char, lambda e, c=char: self._on_press(c))

    # ------------------------------------------------------------------
    # Event handler
    # ------------------------------------------------------------------

    def _on_press(self, label: str):
        if label == "AC":
            self.engine.reset()
        elif label == "⌫":
            self.engine.backspace()
        elif label == "+/-":
            self.engine.toggle_sign()
        elif label == "%":
            self.engine.percentage()
        elif label == "=":
            self.engine.calculate()
        elif label in OPERATORS:
            self.engine.input_operator(label)
        elif label == ".":
            self.engine.input_decimal()
        else:
            self.engine.input_digit(label)

        self._refresh()

    # ------------------------------------------------------------------
    # Refresh UI state
    # ------------------------------------------------------------------

    def _refresh(self):
        # Main display
        self.display_var.set(self.engine.display)

        # Sub-info: show "previous op" line while operator is pending
        op = self.engine.active_operator
        if op:
            self.sub_var.set(f"{self.engine._previous}  {op}")
        else:
            self.sub_var.set("")

        # Highlight active operator button in red
        for sym, btn in self._op_buttons.items():
            if sym == op:
                btn.configure(bg=OP_ACTIVE, fg=BTN_CLR_FG)
            else:
                btn.configure(bg=BTN_OP_BG, fg=BTN_OP_FG)
