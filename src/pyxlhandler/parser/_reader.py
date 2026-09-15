from __future__ import annotations

import functools
import logging
from typing import TYPE_CHECKING

from ._utils import DEFUSED, open_excel

if DEFUSED:
    from defusedxml import ElementTree as ET
else:
    import xml.etree.ElementTree as ET

if TYPE_CHECKING:
    import zipfile
    from xml.etree.ElementTree import Element

_LOGGER = logging.getLogger(__name__)


class ExcelReader:
    def __init__(self, file_path: str):
        self._excel_file: zipfile.ZipFile = open_excel(file_path)

        self._sheet_xml: dict[str, Element] = {}
        self._workbook_xml: Element

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self._excel_file.close()

    @functools.cached_property
    def sheets(self):
        self._load_workbook()

        namespace = "http://schemas.openxmlformats.org/spreadsheetml/2006/main"
        ns = f"{{{namespace}}}"

        return [
            s.get("name")
            for s in self._workbook_xml.iterfind(f".//{ns}sheet")
            if s.get("name")
        ]

    def _load_workbook(self) -> None:
        """Load the workbook xml file from the Excel zip archive."""
        if hasattr(self, "_workbook_xml"):
            return

        with self._excel_file.open("xl/workbook.xml") as workbook_file:
            self._workbook_xml = ET.parse(workbook_file).getroot()

        _LOGGER.debug("Workbook XML loaded successfully.")

    def _load_sheet(self, sheet_name: str) -> None:
        if sheet_name not in self.sheets:
            raise ValueError(f"Sheet '{sheet_name}' does not exist in the workbook.")

        if sheet_name in self._sheet_xml:
            return

        with self._excel_file.open(f"xl/worksheets/{sheet_name}.xml") as sheet_file:
            self._sheet_xml[sheet_name] = ET.parse(sheet_file).getroot()

        _LOGGER.debug(f"{sheet_name} XML loaded successfully.")
