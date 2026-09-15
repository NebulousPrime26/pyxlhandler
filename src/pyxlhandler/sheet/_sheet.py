from __future__ import annotations

from ..exceptions import InvalidSheetError
from ..typing import CellValue
from ..utils import invalid_sheet_name


class Sheet:
    def __init__(self, name: str):
        if type(name) is not str:
            raise TypeError(f"Sheet name must be a string, got {type(name).__name__} instead.")
        if invalid_sheet_name(name):
            raise InvalidSheetError.from_name(name)

        self._name: str = name

    def set_value(self, cell: str, value: list[CellValue] | CellValue) -> None:
        if type(cell) is not str:
            raise TypeError(f"Cell must be a string, got {type(cell).__name__} instead.")
        if type(value) is list and len(value) > 1 and ":" not in cell:
            raise ValueError("Cannot set multiple values to a single cell without a range.")

        raise NotImplementedError("Setting cell values is not implemented yet.")

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, value: str) -> None:
        if invalid_sheet_name(value):
            raise InvalidSheetError.from_name(value)

        self._name = value
