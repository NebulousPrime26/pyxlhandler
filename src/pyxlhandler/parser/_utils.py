from __future__ import annotations

import importlib.util
import os
import zipfile
from typing import Final

DEFUSED: Final[bool] = importlib.util.find_spec("defusedxml") is not None


def open_excel(file_path: str) -> zipfile.ZipFile:
    """Open an Excel file if it exists and is valid.

    Args:
        file_path (str): The path to the file to be checked.

    Raises:
        FileNotFoundError: If the file does not exist.
        PermissionError: If the file is not readable.
        ValueError: If the file is not a valid Excel file.

    Returns:
        ZipFile: The opened Excel file.
    """
    if not os.path.isfile(file_path):
        raise FileNotFoundError(f"The file '{file_path}' does not exist.")
    if not os.access(file_path, os.R_OK):
        raise PermissionError(f"The file '{file_path}' is not readable.")
    if not file_path.lower().endswith((".xls", ".xlsx")):
        raise ValueError(f"The file '{file_path}' is not a valid Excel file.")

    return zipfile.ZipFile(file_path, mode="r")
