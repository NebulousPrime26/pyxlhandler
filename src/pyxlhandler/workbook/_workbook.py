from __future__ import annotations

import logging
import os.path
from collections.abc import Iterable
from typing import overload

from ..parser import ExcelReader
from ._properties import Properties

_LOGGER = logging.getLogger(__name__)


class Book:
    def __init__(self):
        self._sheets: dict[str, Sheet] = {}
        self._sheet_order: list[str] = []

        self._properties: Properties = Properties()

    @classmethod
    def from_file(cls, file_path: str) -> Book:
        with ExcelReader(file_path) as reader:
            book = cls()
            book._sheet_order = reader.sheets

        book._properties = Properties.from_file(file_path)

        return book

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

    @overload
    def get_sheet(self, name: str) -> Sheet: ...
    @overload
    def get_sheet(self, name: Iterable[str]) -> list[Sheet]: ...
    def get_sheet(self, name: str | Iterable[str]):
        raise NotImplementedError()

    @overload
    def get_sheet_by_index(self, index: int) -> Sheet: ...
    @overload
    def get_sheet_by_index(self, index: Iterable[int]) -> list[Sheet]: ...
    def get_sheet_by_index(self, index: int | Iterable[int]):
        raise NotImplementedError()

    def get_sheet_names(self) -> list[str]:
        return self._sheet_order

    def save(self, file_path: str, *, overwrite: bool = False) -> None:
        if not overwrite and os.path.exists(file_path):
            raise FileExistsError(
                f"File '{file_path}' already exists. Use overwrite=True to overwrite."
            )

        # TODO: Implement saving logic here

        self._properties = Properties.from_file(file_path)

        raise NotImplementedError()

    @property
    def properties(self) -> Properties:
        return self._properties


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
