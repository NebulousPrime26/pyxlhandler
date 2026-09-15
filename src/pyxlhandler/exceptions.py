class SheetExistsError(Exception):
    """Raised when a sheet with the specified name already exists in the workbook."""


class SheetNotFoundError(Exception):
    """Raised when a sheet with the specified name does not exist in the workbook."""


class InvalidSheetError(Exception):
    """Raised when a sheet name is invalid for use in Excel."""

    @classmethod
    def from_name(cls, name: str):
        return cls(f"Invalid sheet name '{name}'")
