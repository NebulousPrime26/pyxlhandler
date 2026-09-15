from __future__ import annotations

from ..exceptions import InvalidSheetError
from ..utils import invalid_sheet_name


class Sheet:
    def __init__(self, name: str):
        if type(name) is not str:
            raise TypeError(f"Sheet name must be a string, got {type(name).__name__} instead.")
        if invalid_sheet_name(name):
            raise InvalidSheetError.from_name(name)

        self._name = name

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, value: str) -> None:
        if invalid_sheet_name(value):
            raise InvalidSheetError.from_name(value)

        self._name = value
