"""
Calculator engine — pure computation logic, no UI dependencies.
"""


class CalculatorEngine:
    def __init__(self):
        self.reset()

    def reset(self):
        self._current = "0"
        self._previous = ""
        self._operator = None
        self._result_shown = False
        self._error = False

    # ------------------------------------------------------------------
    # Input handlers
    # ------------------------------------------------------------------

    def input_digit(self, digit: str):
        if self._error:
            self.reset()
        if self._result_shown:
            self._current = digit
            self._result_shown = False
        elif self._current == "0":
            self._current = digit
        else:
            if len(self._current.lstrip("-")) < 12:
                self._current += digit

    def input_decimal(self):
        if self._error:
            self.reset()
        if self._result_shown:
            self._current = "0."
            self._result_shown = False
        elif "." not in self._current:
            self._current += "."

    def input_operator(self, op: str):
        if self._error:
            return
        if self._operator and not self._result_shown:
            self.calculate()
            if self._error:
                return
        self._previous = self._current
        self._operator = op
        self._result_shown = True

    def backspace(self):
        if self._error or self._result_shown:
            self.reset()
            return
        if len(self._current) > 1:
            self._current = self._current[:-1]
            if self._current == "-":
                self._current = "0"
        else:
            self._current = "0"

    def toggle_sign(self):
        if self._error or self._current == "0":
            return
        if self._current.startswith("-"):
            self._current = self._current[1:]
        else:
            self._current = "-" + self._current

    def percentage(self):
        if self._error:
            return
        try:
            value = float(self._current) / 100
            self._current = self._format(value)
        except ValueError:
            pass

    def calculate(self):
        if not self._operator or not self._previous:
            return
        try:
            a = float(self._previous)
            b = float(self._current)
            op = self._operator

            if op == "+":
                result = a + b
            elif op == "-":
                result = a - b
            elif op == "×":
                result = a * b
            elif op == "÷":
                if b == 0:
                    self._current = "DIV/0 ERR"
                    self._operator = None
                    self._result_shown = True
                    self._error = True
                    return
                result = a / b
            else:
                return

            self._current = self._format(result)
            self._operator = None
            self._result_shown = True

        except (ValueError, OverflowError):
            self._current = "ERROR"
            self._operator = None
            self._result_shown = True
            self._error = True

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    @staticmethod
    def _format(value: float) -> str:
        if value != value:          # NaN
            return "ERROR"
        if abs(value) >= 1e12:
            return f"{value:.4e}"
        if value == int(value) and abs(value) < 1e12:
            return str(int(value))
        text = f"{value:.10f}".rstrip("0").rstrip(".")
        return text

    # ------------------------------------------------------------------
    # Public read-only state
    # ------------------------------------------------------------------

    @property
    def display(self) -> str:
        return self._current

    @property
    def active_operator(self):
        return self._operator
