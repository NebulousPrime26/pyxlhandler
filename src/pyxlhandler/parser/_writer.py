import zipfile
from typing import Final, Self
from xml.sax.saxutils import escape


class ExcelWriter:
    _CT_WORKBOOK: Final[str] = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet.main+xml"
    _CT_WORKSHEET: Final[str] = "application/vnd.openxmlformats-officedocument.spreadsheetml.worksheet+xml"
    _CT_STYLES: Final[str] = "application/vnd.openxmlformats-officedocument.spreadsheetml.styles+xml"

    _RT_OFFICE_DOC: Final[str] = "http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument"
    _RT_WORKSHEET: Final[str] = "http://schemas.openxmlformats.org/officeDocument/2006/relationships/worksheet"
    _RT_STYLES: Final[str] = "http://schemas.openxmlformats.org/officeDocument/2006/relationships/styles"

    def __init__(self, file_path: str):
        self._zip_file = zipfile.ZipFile(file_path, mode="w")

    def __enter__(self) -> Self:
        return self

    def __exit__(self, exc_type, exc_value, traceback) -> None:
        self._zip_file.close()

    def write(self, sheet_names: list[str]) -> None:
        """
        Write an XLSX file with the given sheet names.

        Args:
            sheet_names: List of sheet names (e.g., ["Test", "Test2"])
        """
        if not sheet_names:
            raise ValueError("At least one sheet is required")

        self._zip_file.writestr("[Content_Types].xml", self._content_types(len(sheet_names)))
        self._zip_file.writestr("_rels/.rels", self._root_rels())
        self._zip_file.writestr("xl/workbook.xml", self._workbook_xml(sheet_names))
        self._zip_file.writestr("xl/_rels/workbook.xml.rels", self._workbook_rels(len(sheet_names)))
        self._zip_file.writestr("xl/styles.xml", self._styles_xml())

        for i in range(1, len(sheet_names) + 1):
            self._zip_file.writestr(f"xl/worksheets/sheet{i}.xml", self._worksheet_xml())

    def _content_types(self, sheet_count: int) -> str:
        parts: list[str] = [
            '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>',
            '<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">',
            '<Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>',
            '<Default Extension="xml" ContentType="application/xml"/>',
            f'<Override PartName="/xl/workbook.xml" ContentType="{self._CT_WORKBOOK}"/>',
            f'<Override PartName="/xl/styles.xml" ContentType="{self._CT_STYLES}"/>',
        ]

        for i in range(1, sheet_count + 1):
            parts.append(f'<Override PartName="/xl/worksheets/sheet{i}.xml" ContentType="{self._CT_WORKSHEET}"/>')
        parts.append("</Types>")

        return "".join(parts)

    def _root_rels(self) -> str:
        return (
            '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
            '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
            f'<Relationship Id="rId1" Type="{self._RT_OFFICE_DOC}" Target="xl/workbook.xml"/>'
            "</Relationships>"
        )

    def _workbook_xml(self, sheet_names: list[str]) -> str:
        parts: list[str] = [
            '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>',
            '<workbook xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main"',
            ' xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships">',
            "<sheets>",
        ]

        for i, name in enumerate(sheet_names, start=1):
            safe_name = escape(name, {'"': "&quot;"})
            parts.append(f'<sheet name="{safe_name}" sheetId="{i}" r:id="rId{i}"/>')

        parts.append("</sheets>")
        parts.append("</workbook>")

        return "".join(parts)

    def _workbook_rels(self, sheet_count: int) -> str:
        parts: list[str] = [
            '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>',
            '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">',
        ]

        for i in range(1, sheet_count + 1):
            parts.append(f'<Relationship Id="rId{i}" Type="{self._RT_WORKSHEET}" Target="worksheets/sheet{i}.xml"/>')

        parts.append(f'<Relationship Id="rId{sheet_count + 1}" Type="{self._RT_STYLES}" Target="styles.xml"/>')
        parts.append("</Relationships>")

        return "".join(parts)

    def _styles_xml(self) -> str:
        return (
            '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
            '<styleSheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main">'
            '<fonts count="1"><font><sz val="11"/><name val="Calibri"/></font></fonts>'
            '<fills count="1"><fill><patternFill patternType="none"/></fill></fills>'
            '<borders count="1"><border/></borders>'
            '<cellStyleXfs count="1"><xf numFmtId="0" fontId="0" fillId="0" borderId="0"/></cellStyleXfs>'
            '<cellXfs count="1"><xf numFmtId="0" fontId="0" fillId="0" borderId="0" xfId="0"/></cellXfs>'
            "</styleSheet>"
        )

    def _worksheet_xml(self) -> str:
        return (
            '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
            '<worksheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main">'
            "<sheetData/>"
            "</worksheet>"
        )
