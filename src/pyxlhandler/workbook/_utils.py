from __future__ import annotations


def is_sheet_name_valid(name: str) -> bool:
    """Validate if sheet can be used by Excel.

    Args:
        name (str): Sheet name to validate.

    Returns:
        bool: True if the sheet name is valid, False otherwise.
    """
    if type(name) is not str:
        return False
    if not name:
        return False
    if len(name) > 31:
        return False
    return not any(c in name for c in r"[]:*?/\\")
