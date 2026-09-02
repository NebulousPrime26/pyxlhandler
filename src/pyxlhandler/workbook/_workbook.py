from __future__ import annotations

import os.path
from typing import overload


class Book:
    def __init__(self):
        self._sheets: dict[str, Sheet] = {}
        self._sheet_order: list[str] = []

        raise NotImplementedError()

    @classmethod
    def from_file(cls, filename: str) -> Book:
        raise NotImplementedError()

    def add_sheet(self, name: str, index: int = -1) -> Sheet:
        sheet = Sheet(name)
        self._sheets[name] = sheet

        if index == -1:
            self._sheet_order.append(name)
        else:
            self._sheet_order.insert(index, name)

        return sheet

    def remove_sheet(self, name: str) -> None:
        self._sheets.pop(name)

        if name in self._sheet_order:
            self._sheet_order.remove(name)

        raise NotImplementedError()

    def rename_sheet(self, old_name: str, new_name: str) -> None:
        if old_name not in self._sheets:
            raise ValueError(f"Sheet '{old_name}' does not exist.")
        if new_name in self._sheets:
            raise ValueError(f"Sheet '{new_name}' already exists.")

        sheet = self._sheets.pop(old_name)
        sheet.name = new_name

        self._sheets[new_name] = sheet
        self._sheet_order[self._sheet_order.index(old_name)] = new_name

        raise NotImplementedError()

    @overload
    def get_sheet(self, name: str) -> Sheet: ...
    @overload
    def get_sheet(self, *name: str) -> list[Sheet]: ...
    def get_sheet(self, *name: str):
        raise NotImplementedError()

    @overload
    def get_sheet_by_index(self, index: int) -> Sheet: ...
    @overload
    def get_sheet_by_index(self, *index: int) -> list[Sheet]: ...
    def get_sheet_by_index(self, *index: int):
        raise NotImplementedError()

    def get_sheet_names(self) -> list[str]:
        return self._sheet_order

    def save(self, filename: str, *, overwrite: bool = False) -> None:
        if not overwrite and os.path.exists(filename):
            raise FileExistsError(
                f"File '{filename}' already exists. Use overwrite=True to overwrite."
            )

        raise NotImplementedError()

    @property
    def sheets(self) -> dict[str, Sheet]:
        return self._sheets.copy()


class Sheet:
    def __init__(self, name: str):
        self._name = name
        raise NotImplementedError()

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, value: str) -> None:
        if type(value) is str:
            self._name = value

        raise TypeError("Sheet name must be a string.")
