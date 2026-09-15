from __future__ import annotations


class Cell:
    def __init__(self):
        self._value: float | int | str | None = None
        self._formula: str | None = None

    def clear(self):
        self._value = None
        self._formula = None

    @property
    def value(self) -> float | int | str | None:
        return self._value

    @value.setter
    def value(self, value: float | str | None):
        if value is not None and self._formula is not None:
            raise ValueError("Cannot set value when a formula is already set.")

        self._value = value

    @property
    def formula(self) -> str | None:
        return self._formula

    @formula.setter
    def formula(self, formula: str | None):
        self._formula = formula
