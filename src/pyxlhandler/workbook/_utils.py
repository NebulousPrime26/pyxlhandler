from __future__ import annotations


def invalid_sheet_name(name: str) -> bool:
    """Check if the sheet name is invalid for use in Excel.

    Args:
        name (str): Sheet name to validate.

    Returns:
        bool: True if the sheet name is invalid, False otherwise.
    """
    if type(name) is not str:
        return True
    if not name:
        return True
    if len(name) > 31:
        return True
    return any(c in name for c in r"[]:*?/\\")
