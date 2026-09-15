from __future__ import annotations

import logging
import os.path
from collections.abc import Iterable
from typing import overload

from ..exceptions import InvalidSheetError, SheetExistsError, SheetNotFoundError
from ..parser import ExcelReader, ExcelWriter
from ..utils import invalid_sheet_name
from ._properties import Properties

_LOGGER = logging.getLogger(__name__)


class Book:
    def __init__(self):
        self._sheets: list[Sheet] = []
        self._properties: Properties = Properties()

    @classmethod
    def from_file(cls, file_path: str) -> Book:
        """Create a `Book` instance from a XLSX file.

        Args:
            file_path (str): Path to the XLSX file.

        Returns:
            Book: A `Book` instance representing the workbook.
        """
        with ExcelReader(file_path) as reader:
            book = cls()
            book._sheets = [Sheet(name) for name in reader.sheets]

        book._properties = Properties.from_file(file_path)

        return book

    def add_sheet(self, sheet: Sheet, index: int = -1, overwrite: bool = False) -> None:
        """Add a sheet to the book.

        Args:
            sheet (Sheet): The sheet to add.
            index (int, optional): The index at which to add the sheet. Defaults to -1.
            overwrite (bool, optional): Whether to overwrite the sheet if it already exists. Defaults to False.

        Raises:
            InvalidSheetError: If the sheet name is invalid.
            SheetExistsError: If the sheet name already exists and `overwrite=False`.
        """
        sheet_name: str = sheet.name

        if invalid_sheet_name(sheet_name):
            raise InvalidSheetError.from_name(sheet_name)
        if not overwrite and sheet_name in [s.name for s in self._sheets]:
            raise SheetExistsError(f"Sheet '{sheet_name}' already exists.")

        if index == -1:
            self._sheets.append(sheet)
        else:
            self._sheets.insert(index, sheet)

    def remove_sheet(self, name: str) -> None:
        """Remove sheet from book if it exists.

        Nothing happens in case the sheet didn't exist.

        Args:
            name (str): Sheet name to remove.
        """
        sheet: Sheet | None = next((s for s in self._sheets if s.name == name), None)

        if sheet is None:
            _LOGGER.warning(f"Sheet '{name}' does not exist. No action taken.")
            return

        self._sheets.remove(sheet)

    def rename_sheet(self, old_name: str, new_name: str) -> None:
        """Rename an existing` sheet.

        Args:
            old_name (str): The current name of the sheet to rename.
            new_name (str): The new name for the sheet.

        Raises:
            SheetNotFoundError: If the sheet with `old_name` does not exist.
            SheetExistsError: If the sheet with `new_name` already exists.
        """
        sheet: Sheet | None = next((s for s in self._sheets if s.name == old_name), None)

        if sheet is None:
            raise SheetNotFoundError(f"Sheet '{old_name}' does not exist.")
        if new_name in self._sheets:
            raise SheetExistsError(f"Sheet '{new_name}' already exists.")

        index: int = self._sheets.index(sheet)
        sheet.name = new_name
        self._sheets[index] = sheet

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
        return [s.name for s in self._sheets]

    def save(self, file_path: str, *, overwrite: bool = False) -> None:
        if not overwrite and os.path.exists(file_path):
            raise FileExistsError(f"File '{file_path}' already exists. Use overwrite=True to overwrite.")

        with ExcelWriter(file_path) as writer:
            writer.write(self.get_sheet_names())

        self._properties = Properties.from_file(file_path)

    @property
    def properties(self) -> Properties:
        return self._properties


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
